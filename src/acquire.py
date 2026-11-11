"""Acquire primary infrastructure/typology APIs and secondary performance data.

Run from the project directory: python src/acquire.py. Existing snapshot files
are retained; remove a file explicitly to refresh it. Never silently mix dates.
"""
from pathlib import Path
import hashlib, json, tempfile, zipfile
from datetime import datetime, timezone
import requests
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data/raw'
RAW.mkdir(parents=True, exist_ok=True)
SOURCES = {
    'municipality_correspondences_2025_2026.csv': 'https://www.agvchapp.bfs.admin.ch/api/communes/correspondances?includeUnmodified=true&includeTerritoryExchange=false&startPeriod=06-04-2025&endPeriod=01-01-2026',
    'bfs_typologies_labels_2026.csv': 'https://www.agvchapp.bfs.admin.ch/api/communes/levels?date=01-01-2026&labelLanguages=de',
    'bakom_metadata.json': 'https://data.geo.admin.ch/api/stac/v1/collections/ch.bakom.standorte-mobilfunkanlagen/items/standorte-mobilfunkanlagen',
    'bakom_stations_2026-11-09.geojson': 'https://data.geo.admin.ch/ch.bakom.standorte-mobilfunkanlagen/standorte-mobilfunkanlagen/standorte-mobilfunkanlagen_2056.json',
    'boundaries_2026.gpkg.zip': 'https://data.geo.admin.ch/ch.swisstopo.swissboundaries3d/swissboundaries3d_2026-01/swissboundaries3d_2026-01_2056_5728.gpkg.zip',
}
OOKLA = 'https://ookla-open-data.s3.amazonaws.com/parquet/performance/type=mobile/year=2026/quarter=3/2026-07-01_performance_mobile_tiles.parquet'
POP = 'https://www.pxweb.bfs.admin.ch/api/v1/de/px-x-0102010000_100/px-x-0102010000_100.px'

def get_file(name, url):
    target = RAW / name
    if not target.exists():
        tmp = target.with_suffix(target.suffix + '.part')
        with requests.get(url, timeout=(20, 180), stream=True) as r:
            r.raise_for_status()
            with tmp.open('wb') as f:
                for chunk in r.iter_content(1024 * 1024): f.write(chunk)
        tmp.replace(target)
    return target

def population():
    path = RAW/'population_2025.json'
    if path.exists(): return
    meta = requests.get(POP, timeout=45); meta.raise_for_status()
    m = meta.json()
    (RAW/'population_metadata.json').write_text(json.dumps(m, ensure_ascii=False, indent=2))
    query = []
    for v in m['variables']:
        if v['code']=='Jahr': values=['2025']
        elif v['code'].startswith('Kanton'):
            values=[x for x,t in zip(v['values'],v['valueTexts']) if t.startswith('......')]
        elif v['code']=='Bevölkerungstyp': values=['1']
        else: values=['-99999']
        query.append({'code':v['code'],'selection':{'filter':'item','values':values}})
    body={'query':query,'response':{'format':'json-stat2'}}
    (RAW/'population_query.json').write_text(json.dumps(body,ensure_ascii=False,indent=2))
    r=requests.post(POP,json=body,timeout=60);r.raise_for_status()
    path.write_bytes(r.content)

def main():
    for name,url in SOURCES.items():
        print('Acquire/cache',name,flush=True);get_file(name,url)
    population()
    if not (RAW/'ookla_bbox_q3_2026.parquet').exists():
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'global.parquet'
            with requests.get(OOKLA,stream=True,timeout=(20,180)) as r:
                r.raise_for_status()
                with p.open('wb') as f:
                    for c in r.iter_content(1024*1024):f.write(c)
            table=pq.read_table(p,filters=[('tile_x','>=',5.9),('tile_x','<=',10.6),('tile_y','>=',45.7),('tile_y','<=',47.9)])
            pq.write_table(table,RAW/'ookla_bbox_q3_2026.parquet')
    manifest={'created_utc':datetime.now(timezone.utc).isoformat(),
              'client_date':'2026-11-11','performance_period':'2026-Q3',
              'snapshot_note':'Existing files are immutable cached snapshots. Acquisition date recorded in this run; source dates below differ.',
              'sources':SOURCES|{'population_2025.json':POP,'ookla_bbox_q3_2026.parquet':OOKLA},
              'source_dates':{'stations':'2026-11-09','boundaries':'2026-01-01','typology':'2020 definition, 2026-01-01 municipality status','population':'2025-12-31, geography 2025-04-06','performance':'2026-07-01 through 2026-09-30'},
              'files':[]}
    for p in sorted(RAW.iterdir()):
        if p.is_file() and p.name!='manifest.json':
            manifest['files'].append({'file':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    (RAW/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
    print('Source manifest saved',flush=True)

if __name__=='__main__':main()

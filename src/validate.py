"""Meaningful checks for joins, conserved population and measurement semantics."""
from pathlib import Path
import json,sqlite3,hashlib
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
def main():
    raw=ROOT/'data/raw';out=ROOT/'data/processed';res=ROOT/'results'
    m=pd.read_csv(out/'municipalities.csv');t=pd.read_parquet(out/'tiles_assigned.parquet');s=pd.read_csv(out/'stations_assigned.csv')
    checks={}
    assert m.bfs_id.is_unique and len(m)==2110;checks['municipality_keys']='PASS'
    assert t.quadkey.is_unique and s.record_key.is_unique;checks['fact_keys']='PASS'
    assert set(t.bfs_id)<=set(m.bfs_id) and set(s.bfs_id)<=set(m.bfs_id);checks['foreign_keys']='PASS'
    assert m.population.notna().all() and m.municipality_type.notna().all();checks['municipality_enrichment']='PASS'
    population=json.loads((raw/'population_2025.json').read_text())
    assert m.population.sum()==sum(population['value']);checks['population_conserved_through_mergers']='PASS'
    assert m.loc[~m.observed,'download_mbps'].isna().all();checks['unobserved_speed_not_zero']='PASS'
    assert np.isclose(m.tests.sum(),t.tests.sum());checks['test_count_conserved']='PASS'
    reconstructed=t.groupby('bfs_id').apply(lambda x:np.average(x.download_mbps,weights=x.tests),include_groups=False)
    actual=m.set_index('bfs_id').loc[reconstructed.index,'download_mbps']
    assert np.allclose(reconstructed,actual);checks['weighted_aggregation']='PASS'
    with sqlite3.connect(out/'mobile_divide.sqlite') as con:
        assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
        assert con.execute('SELECT COUNT(*) FROM municipalities').fetchone()[0]==len(m)
    checks['sqlite_integrity']='PASS'
    manifest=json.loads((raw/'manifest.json').read_text())
    for record in manifest['files']:
        assert hashlib.sha256((raw/record['file']).read_bytes()).hexdigest()==record['sha256']
    checks['raw_snapshot_hashes']='PASS'
    (res/'validation.json').write_text(json.dumps(checks,indent=2));print(json.dumps(checks,indent=2))
if __name__=='__main__':main()

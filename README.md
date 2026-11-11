# Swiss mobile divide — Group 01

**Arthik Muralitharan · Klodian Elshani · Kristian Perkovic**

ZHAW Data Analytics, HS 2026. Concept presentation: 17 November 2026,
11:00–12:45 teaching block, SW301. Individual group slot: approximately 10 minutes.

## Research question

How does observed mobile download performance differ between urban,
intermediate and rural Swiss municipalities, and how is it associated with
outdoor station density after accounting for population density, mountain
status and the share of station records reporting 5G?

This is a cross-sectional association study. It does not identify causal
effects, population-wide user experience, territorial radio coverage, or
differences between individual mobile network operators.

## Start here

- `project_group_01.ipynb`: executed, annotated end-to-end notebook.
- `docs/START_HIER.md`: German handover, deadlines and remaining human actions.
- `docs/METHODS_AND_RESULTS.md`: reproducible interpretation, assumptions and limitations.
- `docs/POINTS_AND_EVIDENCE.md`: criterion-by-criterion evidence and honest status.
- `docs/AI_USAGE.md`: actual AI assistance, failures and corrections.
- `results/`: actual tables, figures, model diagnostics and integration audit.
- `data/raw/manifest.json`: URLs, source dates and SHA-256 snapshot checksums.

## Public repository

https://github.com/elshaklo/swiss-mobile-divide-group01 — verified public on 11 November 2026. Full raw snapshots are included in the Moodle materials ZIP, not GitHub.

## Reproduce from included data

Python 3.14 was used for the supplied run. The exact tested environment is in
`requirements.txt`. On another supported Python version, installing compatible
versions may be necessary; do not silently replace results.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/pipeline.py
python src/validate.py
```

To collect data yourself via official APIs and rebuild from source:

```bash
python src/acquire.py
python src/pipeline.py
```

`acquire.py` retains cached snapshots. The BAKOM download URL is live, so a
future fresh download has a newer data date. Inspect its STAC metadata and
update filenames/manifest before interpreting it as the November 2026 snapshot.
The Ookla bbox extract includes surrounding countries; the pipeline applies
Swiss municipality polygons before aggregating. The global file is temporary
and is not required to reproduce the included results.

## PostgreSQL bonus — executed, not only configured

SQLite is included to satisfy the explicit minimum requirement. A separate
PostgreSQL run executes joins and aggregations from Python and checks numerical
agreement with SQLite. The supplied data dump contains the actual three tables.

For a reproducible container setup, with Docker already installed:

```bash
export POSTGRES_PASSWORD='choose-a-local-password'
docker compose up -d
export PG_DSN="postgresql+psycopg://student:${POSTGRES_PASSWORD}@127.0.0.1:55432/mobile_divide"
python src/postgres.py
```

Alternative: point `PG_DSN` to your own PostgreSQL instance. No credentials or
personal connection strings are included. Only the dedicated
`mobile_divide_group01` schema is written. Stop the local container with
`docker compose stop` when finished.

## Data and licence

Primary explanatory data: direct BAKOM station/STAC and BFS typology/population
API requests, with request code, date and cached raw responses. Secondary
outcome source: Speedtest by Ookla Global Fixed and Mobile Network Performance
Maps, mobile layer, 2026 Q3, accessed 11 November 2026. It contains aggregated,
self-selected tests rather than random-sample measurements. `tests` weights
tile means; summed `devices` are not unique devices across a municipality.

Sources: [BAKOM](https://data.geo.admin.ch/api/stac/v1/collections/ch.bakom.standorte-mobilfunkanlagen/items/standorte-mobilfunkanlagen),
[BFS typology API](https://www.agvchapp.bfs.admin.ch/api/communes/levels?date=01-01-2026&labelLanguages=de),
[BFS population](https://www.pxweb.bfs.admin.ch/pxweb/de/px-x-0102010000_100/-/px-x-0102010000_100.px/),
[swisstopo](https://www.swisstopo.admin.ch/en/landscape-model-swissboundaries3d),
[Ookla source and licence](https://github.com/teamookla/ookla-open-data).

Ookla data and derived performance outputs: CC BY-NC-SA 4.0. Retain attribution,
non-commercial use and share-alike terms. Swiss source data retain their
respective provider terms and attribution. See `DATA_SOURCES.md`. Do not
present these data as independently measured radio coverage by the group.

## Submission and remaining actions

The topic is formally approved at the concept presentation. Confirm with the
lecturer that API-collected explanatory station data plus secondary Ookla
outcomes satisfy the primary-source requirement. No approval is claimed yet.
Public repository: https://github.com/elshaklo/swiss-mobile-divide-group01. The three-person 15-minute MP4 still needs to be recorded by the group. Moodle submission must be
verified separately; presence of local files does not establish submission.

AI assistance is disclosed in the notebook, presentation and AI usage log.

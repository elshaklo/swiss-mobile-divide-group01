# Sources and usage terms

| Provider | Access | Content / structure | Version / date |
|---|---|---|---|
| BAKOM | STAC JSON + official GeoJSON asset (EPSG:2056) | station identifier, coordinates, technology, environment type | 2026-11-09 |
| BFS municipality application | documented REST API, CSV | BFS municipality key, 2020 urban/intermediate/rural typology, mountain indicator | municipality status 2026-01-01 |
| BFS correspondences | documented REST API, CSV | former and current BFS codes, mergers/transfers | 2025-04-06 → 2026-01-01 |
| BFS STATPOP | PxWeb API, POST query saved | permanent residents, 2025, all municipalities | 2025-12-31; geography 2025-04-06 |
| swisstopo | STAC-linked official GeoPackage | municipality polygons, official area in hectares | 2026-01-01 |
| Ookla | public S3 Parquet, bbox extraction | mobile tile means, tests, devices, centroids/WKT | 2026 Q3 |

Exact URLs and SHA-256 hashes are in `data/raw/manifest.json`. The source query for population is saved in `population_query.json`. The global Ookla dataset contains 3,477,926 tiles; only the bbox extract is bundled. No Kaggle source is used. Official API retrieval is performed by the supplied acquisition code with AI assistance and cached responses, not represented as unaided manual collection.

## Official references

- BFS API documentation: https://www.agvchapp.bfs.admin.ch/documents/rest_api_de.pdf
- BFS spatial typology explanation: https://statistik.admin.ch/de/themen/raeumliche-analysen/raeumliche-gliederungen
- BAKOM source metadata: https://data.geo.admin.ch/api/stac/v1/collections/ch.bakom.standorte-mobilfunkanlagen/items/standorte-mobilfunkanlagen
- Swisstopo product documentation: https://www.swisstopo.admin.ch/dam/de/sd-web/8MrSSW4PQcUM/2025-01%20sBOUND%20ProdInfo-DE.pdf
- Ookla source description and licence: https://github.com/teamookla/ookla-open-data
- Clustered covariance documentation: https://www.statsmodels.org/stable/generated/statsmodels.regression.linear_model.OLSResults.get_robustcov_results.html
- Grouped validation: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupKFold.html

## Attribution and licences

Speedtest by Ookla Global Fixed and Mobile Network Performance Maps, mobile layer 2026 Q3, accessed 11 November 2026. Based on Group 01's AI-assisted analysis. Source data and derived performance outputs under **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International**: https://creativecommons.org/licenses/by-nc-sa/4.0/. Changes: geographic filtering, spatial aggregation, modelling and visualisation. No Ookla endorsement is implied.

BAKOM, BFS and swisstopo are credited for their respective official data; their original terms continue to apply. This licence notice does not relicense third-party material. No institutional logo is used. Public-code publication should exclude raw/processed files by default and retain this source notice with derived figures.

# Assessment evidence — max. 22 points, no guaranteed grade

Source: Moodle evaluation text supplied by Klodian in this chat on 11 November 2026. The lecturer makes the final decision. Material below is an evidence map, not a self-awarded score.

## Minimum requirements (9 points)

| Criterion | Concrete evidence | Status |
|---|---|---|
| Data collection by web API | `src/acquire.py`, saved BFS query/response, STAC response and URL/hash manifest | Executed; formal acceptance of design pending |
| >=2 sources and documented integration | BAKOM, BFS, swisstopo, Ookla; `results/integration_audit.csv`; official municipality correspondences | Executed |
| SQLite with SQL from Python | `mobile_divide.sqlite`, notebook §3, `group_summary.sql`, saved SQL result | Executed |
| Rich graphical/non-graphical EDA | Descriptives, missingness, coverage table, boxplot, scatter, maps, correlation matrix | Executed |
| Regression/classification beyond plain prediction | Rural/Intermediate/Urban comparison plus adjusted log-OLS and predictive comparison | Executed |
| Suitable model evaluation | Held-out R², RMSE, MAE; mean baseline; 5-fold canton-grouped evaluation | Executed |
| Correct interpretation | Methods/results discussion, coefficient intervals, weak prediction and selection bias disclosed | Prepared; group must explain it |
| AI usage documentation | `AI_USAGE.md`, notebook §12, AI slides and recording script | Actual tool/failure log prepared; add members' experience |
| Materials available on Moodle | Prepared ZIP with data, notebook, code; presentation PDF; MP4 must be recorded | Upload and video outstanding |

## Additional criteria (max. 6 points)

| Criterion | Concrete evidence | Status |
|---|---|---|
| Creative implementation | Coverage-aware comparison, official merger harmonization, boundary sensitivity, canton-held-out validation | Implemented; creativity judged by lecturer |
| PostgreSQL (not SQLite) | Actual PostgreSQL 17 tables, primary/foreign keys, SQL joins/aggregations from Python, dump and parity check | Executed |
| Geographic integration/visualization | EPSG:2056 point-in-polygon, Swiss choropleths, boundary sensitivity | Executed |
| Test with p-value | Welch ANOVA, corrected pairwise tests, Spearman and caveats | Executed |
| Additional k-means | k=2…6 selection, silhouette, scaling, profiles and stability | Executed |
| Public GitHub code and URL in presentation | Repository-ready code, README, ignore rules; actual URL must be added after publication | Outstanding until published |

## Video (max. 7 points)

Three members × five minutes = **15 minutes**. Final deck and script address outline, clear topic, substance, spoken explanation, slide quality, actual AI reflection and time keeping. A script or AI-generated voiceover does not prove freely spoken group understanding. Record the actual group explaining the work; do not just scroll through code. Appendix evidence is for review, not part of the 15-minute talk.

## Concept presentation (separate 20% of module grade)

Eight equally weighted criteria: structure, background/problem, objective/question, data, methods, expected results, language, scientific slide quality. The concept deck follows all eight, with full names and clear hypothesis wording. Topic approval occurs at this presentation. Live delivery and final grading are not automated.

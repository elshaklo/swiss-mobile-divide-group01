# Methods and results — Group 01

Status: actual executed analysis, 11 November 2026. Prepared with OpenAI Codex; formal topic approval and group review remain outstanding.

## Research question and unit of analysis

How does observed mobile download performance differ across urban, intermediate and rural Swiss municipalities, and how is it associated with outdoor station density after adjustment? The observational unit is one municipality. We compare municipalities, not individual residents or operators. All results are cross-sectional associations.

## Sources and time alignment

BAKOM station records: 9 November 2026; collected from official STAC/data endpoints. BFS typology: 2020 definition with municipality status on 1 January 2026. BFS permanent population: 31 December 2025 using geography 6 April 2025. Municipality geometries: swisstopo 1 January 2026. Outcome: Ookla mobile 2026 Q3, July–September. Retrieval: 11 November 2026.

These periods do not coincide. November infrastructure cannot establish what infrastructure was operating during Q3. No operator identifier or 5G connection indicator is available in the public Ookla outcome data. We therefore cannot attribute performance to an operator or infer a causal 5G effect. Official API-collected explanatory data are combined with secondary speed observations; confirm this design with the lecturer at formal approval.

## Integration and losses

- 2,136 boundary features become 2,110 Swiss municipalities after excluding lakes and foreign units and dissolving by BFS id.
- 2,115 population units become 2,110 through official BFS correspondences. Seven source codes change; population is conserved. This includes mergers and the Moutier code/canton change.
- All 2,110 municipalities receive a typology and population value. No guessed name matching.
- 22,731 station records, no exact station/coordinate duplicates; 22,681 spatially assigned and 50 outside municipality polygons. Unmatched records remain in the audit.
- The Ookla bounding-box extract has 30,162 tiles; 14,066 centroids fall in Swiss municipality polygons; 16,096 foreign/lake/outside tiles are excluded. These are spatial exclusions, not silently discarded missing speeds.
- 51,815 tests across 1,847 municipalities; 263 municipalities have no observed mobile tiles. Missing performance remains NULL, never 0 Mbps.

See `results/integration_audit.csv`, raw JSON/CSV and the SQL database for reproducible evidence.

## Definitions

Outdoor infrastructure density = number of BAKOM operator-station records classified `Outdoor > 6 Werp` / official municipality area in km². A station record is not necessarily a unique physical mast and is not an individual antenna element. Co-located operators are retained. The 5G share counts records reporting 5G divided by outdoor records, not actual 5G traffic or coverage. Municipalities with no outdoor records have an undefined share; a separate indicator is used where variable.

Municipality download = sum(tile mean download × tests) / sum(tests); units converted from kbps to Mbps. Upload and latency are similarly aggregated. Test counts reproduce the source counts. Summed devices across tiles must not be called unique municipality devices.

The main model uses >=30 tests and >=3 tiles, positive population and known type: 405 municipalities (241 Urban, 107 Intermediate, 57 Rural). This pragmatic fixed rule is not a claim that tests are independent or representative. Only 5.6% of all Rural municipalities qualify, versus 47.3% of Urban and 18.4% of Intermediate. Measurement selection is a major limitation.

## Main descriptive results

Median municipality download: Urban **188.4 Mbps**, Intermediate **159.7 Mbps**, Rural **149.2 Mbps**. Urban minus Rural median: **39.2 Mbps**. A 1,000-resample canton-cluster bootstrap gives a 95% interval **−6.9 to 60.0 Mbps**. The interval includes zero; this is not decisive evidence of a general population-wide rural disadvantage.

The bootstrap resamples cantons with replacement and recomputes the difference of municipality medians; it does not fix self-selection. Report the sample and interval with the point estimate.

## Tests and association

Welch ANOVA on log speed: F=4.426, p=0.01386. Median-centred Levene p=0.00806 supports avoiding the equal-variance assumption. Kruskal–Wallis p=0.00652 is a sensitivity check. Pairwise Welch tests use Holm correction: Urban–Intermediate p=0.03062; Urban–Rural p=0.12895; Intermediate–Rural p=0.99783. The global test does not mean every pair differs.

Spearman station-density/download association: rho=0.3113, p=1.50e−10, n=405. These conventional p-values are exploratory because neighbouring municipalities may be dependent; do not describe them as definitive spatial inference.

## Regression and interpretation

OLS response is log(download Mbps). Predictors: municipality type (Urban reference), log(1+population density), mountain-region indicator, log(1+outdoor station density), and 5G record share. We use canton-clustered covariance and a t distribution, with 26 canton clusters; small-cluster and residual spatial-dependence uncertainty remains. Canton fixed effects are a sensitivity model.

Adjusted Rural coefficient: **-0.0626**, 95% CI **[-0.2855, 0.1603]**, p=**0.5682**. Converting the coefficient gives about **−6.1%**, with an interval about **−24.8% to +17.4%** conditional on the model. The group effect is uncertain; a non-significant result is not proof of equality.

Station-density coefficient on log(1+density): **0.2628**, p=**0.00253**. Since the predictor is log(1+x), do not call this a constant elasticity of raw density. For a change from 0.5 to 1 outdoor station record/km², the fitted multiplicative association is exp(beta × [ln(2)−ln(1.5)])−1, about **7.9%**, holding model covariates fixed. This is not a causal intervention estimate.

In-sample log-response R² rises from 0.0672 (control-only) to 0.1020 (with infrastructure); the difference is not a causal share of the urban/rural gap. The Breusch–Pagan p≈0.00061 flags heteroskedasticity; clustered inference is used. Mountain status is not measured altitude. Multicollinearity and unmeasured provider/device/tariff composition limit coefficient interpretation.

## Held-out model evaluation

A distinct predictive linear model uses speed in Mbps to report interpretable error. Mean baseline, linear regression and a fixed-parameter random forest are compared using the same predictors. Preprocessing is fitted inside training folds. No tuning on test observations.

| Validation | Model | R² | RMSE Mbps | MAE Mbps |
|---|---|---:|---:|---:|
| Random 80/20 holdout | Mean baseline | -0.004 | 69.0 | 57.5 |
| 5-fold canton-grouped OOF | Mean baseline | -0.025 | 76.7 | 59.4 |
| Random 80/20 holdout | Linear regression | 0.097 | 65.4 | 53.8 |
| 5-fold canton-grouped OOF | Linear regression | 0.023 | 74.9 | 57.0 |
| Random 80/20 holdout | Random forest | 0.042 | 67.4 | 54.7 |
| 5-fold canton-grouped OOF | Random forest | -0.025 | 76.7 | 58.6 |

The random holdout contains 81 municipalities. Canton-grouped five-fold evaluation predicts all 405 municipalities in held-out cantons. The forest does not outperform the linear model. R² near zero in grouped validation means limited transferable predictive information. Do not market the model as a reliable national speed predictor. Explanatory log-OLS R² and predictive Mbps R² use different scales.

## Sensitivity

Results are provided for all 1,847 observed municipalities, a lower threshold (967), equal tile weighting, wholly interior tiles (403 of the main municipalities), and all station types. The adjusted rural coefficient even changes sign with unweighted tile averaging; do not hide this sensitivity. Station-density association remains positive across these checks, subject to the same confounding caveats.

A stricter 100-test threshold leaves 78 Urban, 2 Intermediate and 1 Rural municipalities. It is retained as a coverage diagnostic only; a group regression is not fitted for an unusably small comparison group.

## Clustering

K-means on standardized log(1+x) download, upload, latency, station density and population density; compare k=2…6 by silhouette. k=2 selected. Seed stability is recorded. Profile 1 median: download 206.5 Mbps, upload 41.0 Mbps, latency 20.9 ms, density 1.58 station records/km². Profile 2 median: 123.9 Mbps, 25.6 Mbps, 26.0 ms, density 0.27. These are descriptive profiles, not independently validated natural categories. Since speed is a clustering feature, clusters cannot prove a speed gap.

## Conclusion

Among adequately measured municipalities, urban median mobile download is higher. Measurement selection, a bootstrap interval crossing zero, uncertain adjusted rural differences and weak transfer to unseen cantons prevent a blanket national claim. Outdoor station density has a positive conditional association with measured speed, but the available cross-section cannot establish cause. The strongest contribution is a transparent, coverage-aware spatial comparison with auditable data integration.

## Next research steps

Obtain time-aligned historical infrastructure, several performance quarters, richer provider/device composition, and representative measurements in rural municipalities. Add true elevation/terrain and surrounding-station buffers only when measured correctly. A station outside a municipality may serve users inside it; administrative density is an imperfect infrastructure proxy. No values are invented for these missing controls.

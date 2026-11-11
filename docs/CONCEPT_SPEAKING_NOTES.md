# Konzeptvortrag — zehn Minuten, Gruppe 01

Die Aufteilung ist ein Vorschlag. Verwendet die englischen Absätze zum Üben und sprecht anschliessend mit Stichworten. Die Zeitangaben sind Zielzeiten, keine gemessene Aufnahme. Appendix-Folie 11 wird nicht vorgetragen. Bei Rückfragen das Ergebnisprojekt nicht als bereits genehmigt darstellen.

| Person | Folien | Zielzeit |
|---|---|---|
| Arthik | 1–3 | 0:00–3:00 |
| Klodian | 4–7 | 3:00–7:00 |
| Kristian | 8–10 | 7:00–10:00 |

## Slide 1 — Arthik — 0:00–0:35

Good morning. We are Arthik Muralitharan, Klodian Elshani and Kristian Perkovic, group one. Our project looks at the mobile divide in Switzerland. We want to compare measured mobile performance in urban, intermediate and rural municipalities and relate it to mobile infrastructure. We will introduce the question, explain our data and methods, and finish with expected results and limitations.

## Slide 2 — Arthik — 0:35–1:40

The motivation is a practical distinction: having a mobile signal does not necessarily mean having a fast connection. Our project therefore measures observed performance rather than simply counting locations with a signal. We also want to avoid assuming in advance that every rural municipality has a disadvantage.

Our research question is: How does observed mobile download performance differ between urban, intermediate and rural Swiss municipalities, and how is it associated with station density after adjustment? This goes beyond predicting one speed value. We are interested in a comparison between groups and in whether infrastructure adds information after other municipality characteristics are considered. The word association is deliberate: a cross-sectional analysis cannot establish that adding an antenna causes a particular speed increase.

## Slide 3 — Arthik — 1:40–3:00

We combine four providers. From BAKOM, we collect official station information through the government data service: coordinates, technology and whether a record is an outdoor or indoor installation. From BFS APIs, we obtain the official urban, intermediate and rural typology, permanent population and municipality correspondences. Swisstopo provides municipality boundaries and area. Ookla provides secondary mobile performance observations: tile-level download, upload, latency and the number of tests.

The periods are shown explicitly. Performance covers the third quarter of 2026, whereas the infrastructure snapshot is from November. The dates are not identical, so we will not interpret the model as a historical causal effect. The API access and raw schemas have already been checked for feasibility. At formal topic approval, we would like to confirm that our directly collected explanatory API data combined with secondary Ookla performance data satisfy the collection requirement. Klodian will now explain how these sources fit together.

## Slide 4 — Klodian — 3:00–3:55

There are three different record types. A BAKOM record identifies an operator station at a location. It does not necessarily identify a unique physical mast, and it does not count every antenna element. An Ookla record represents a geographical tile containing aggregated mobile tests. A municipality record has an official BFS number and a polygon.

Our final analytical table has one row per municipality. We calculate test-weighted download performance and the density of outdoor station records per square kilometre. We also calculate the fraction of those records reporting 5G. This is a technology indicator for infrastructure, not the percentage of speedtests actually using 5G.

## Slide 5 — Klodian — 3:55–4:55

The integration has four steps. First, acquire the sources and retain raw responses and file hashes. Second, harmonize municipality identifiers. Municipalities merge and codes can change, so simple name matching is unreliable. The official BFS correspondence service lets us map older population units to the current boundaries and conserve the total population.

Third, assign station points and tile centroids to municipality polygons in the Swiss coordinate reference system. Fourth, aggregate tile means using their test counts and calculate infrastructure density. We log unmatched records and every change in record counts. We will not replace an unmeasured speed with zero. Border tiles also need a sensitivity check because one tile can overlap more than one municipality.

## Slide 6 — Klodian — 4:55–6:00

The exploration will include maps, speed distributions, missingness and measurement coverage by municipality type. For group differences, we use Welch ANOVA on log speed because it allows unequal variances. We also examine Spearman correlation between density and speed. Both analyses will include p-values and explicit assumptions.

The explanatory regression uses log download as the response. Predictors include municipality type, station density, the 5G infrastructure share, population density and the mountain-region indicator. We will use canton-clustered uncertainty to account for some regional dependence. Mountain status is a regional classification; we will not call it measured elevation. The aim is to estimate conditional associations and uncertainty, not to prove that infrastructure alone explains a digital divide.

## Slide 7 — Klodian — 6:00–7:00

Model fit on the same observations used for training can be misleading. We therefore compare a mean baseline, linear regression and a random forest on held-out observations. The reported measures will be R-squared, RMSE and MAE. Preprocessing is learned only from the training data.

We also test geographic transfer by holding out entire cantons in five folds. This is a stronger test than randomly mixing neighbouring municipalities between training and evaluation. As an additional descriptive method, we use k-means on standardized network-related features. We compare different cluster counts using silhouette scores and check stability. Because speed is included as a clustering feature, the clusters will not be treated as independent evidence of a speed gap. Kristian will explain what we expect to learn and how we handle the limits.

## Slide 8 — Kristian — 7:00–8:00

Our hypothesis is that urban municipalities may have higher measured downloads and denser infrastructure. After adjustment, the difference could become smaller, remain present or be too uncertain to establish. These are possible outcomes, not conclusions built into the project.

The deliverables are a transparent group comparison, effect estimates with uncertainty, maps, a model evaluation and exploratory network profiles. A small or uncertain effect is still useful if it is explained correctly. We do not plan to choose methods simply because they produce a significant result. Instead, we want a result that can be traced back to the data and reproduced from the notebook.

## Slide 9 — Kristian — 8:00–9:00

The largest risk is measurement selection. People choose when and where to run speedtests, and rural municipalities may have fewer observations. We therefore show both measurement coverage and the sample used for modelling. We cannot assume that the observed tests represent every resident or all locations in the municipality.

The infrastructure proxy also has limitations: a station outside a municipal boundary may serve users inside it, and terrain, devices, tariffs and providers matter. The November infrastructure snapshot differs from the performance quarter. We will document these limitations rather than describing station density as radio coverage. For reproducibility, we retain raw data, audit the joins, use SQLite and an additional PostgreSQL implementation, and document our AI assistance and corrections.

## Slide 10 — Kristian — 9:00–10:00

After the concept presentation, our next steps are to incorporate lecturer feedback, review the analysis as a group and refine the robustness checks. We prepare the executed notebook, data, presentation and evidence appendix for the January deadline. Our three-person final video must last fifteen minutes, five minutes per member.

We have already checked technical feasibility. Formal topic approval is still the purpose of this presentation. The specific approval question is whether directly collected infrastructure and BFS API data, combined with secondary Ookla performance data, are accepted for the data-collection requirement. We will also clarify the inconsistent Moodle deadline field. Thank you. We are happy to discuss the design and its limitations.

## Stichwortkarten auf Deutsch

- Arthik: Signal ≠ Geschwindigkeit; Frage mit Vergleich; vier Quellen und unterschiedliche Zeitstände.
- Klodian: drei Datenebenen; BFS-Schlüssel/Fusionen; räumliche Zuordnung; Gewichtung; Regression und echte Testdaten.
- Kristian: Hypothesen offenlassen; Messlücken; keine Kausalität; Reproduzierbarkeit; Freigabe und nächste Schritte.

Mit Stoppuhr proben. Wenn ihr schneller als zehn Minuten seid, erklärt anhand der Datenstruktur ein konkretes Beispiel und macht sinnvolle Pausen; keine zusätzlichen ungesicherten Behauptungen ergänzen.

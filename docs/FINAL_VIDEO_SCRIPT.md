# Ergebnisvideo — Ziel: 15 Minuten, drei Mitglieder

**Noch kein aufgenommenes Video.** Die tatsächliche Laufzeit muss beim Proben und nach der Aufnahme geprüft werden. Die Zielblöcke sind je fünf Minuten; sprecht frei anhand von Stichwortkarten. Folien 15–22 sind Belege für die Bewertung und werden im Hauptvortrag nicht durchgegangen. Folien 1–14 zeigen das Ergebnis.

Aufteilungsvorschlag: Arthik 1–5, Klodian 6–9, Kristian 10–14. Die Namen kennzeichnen vorgeschlagene Sprecher, nicht nachträglich behauptete Arbeitsbeiträge. Die KI-Reflexion muss nach eurer eigenen Prüfung um echte persönliche Erfahrungen ergänzt werden.

## Arthik — 0:00–5:00

### Slide 1 — 0:00–0:40

Good morning. We are Arthik Muralitharan, Klodian Elshani and Kristian Perkovic. Our project examines the mobile divide in Switzerland. We compare measured mobile download performance between urban, intermediate and rural municipalities and relate it to infrastructure. Our main contribution is a transparent comparison that also shows where the measurements and the model are insufficient. We will cover the data, the integration, the findings and their limitations, and explain how we used AI.

### Slide 2 — 0:40–1:35

Having a signal and having a fast connection are different things. We focus on observed performance, not on a map claiming that every location is covered. Our research question asks how measured download differs across municipality types and how it is associated with station density after adjustment.

This is more than a standard prediction problem: the group comparison is the central question. The unit is one municipality, not one resident or one mobile provider. Our design is observational and cross-sectional. That means we can describe relationships, but we cannot conclude that installing an additional station causes a specific improvement. Devices, tariffs, providers and terrain could influence the relationship and are not fully observed here.

### Slide 3 — 1:35–2:40

We combine four providers and collect official explanatory data through APIs. BAKOM provides station records and their location, technology and environment type. BFS provides municipality typology, population and official correspondences for changed municipalities. Swisstopo provides polygons and municipality area. The outcome comes from secondary Ookla mobile performance tiles for the third quarter of 2026.

A station record is not necessarily a distinct physical mast; different operators may be located together. The 5G share tells us which infrastructure records report 5G, not which speedtests used 5G. We also state the dates clearly. November infrastructure does not perfectly match performance observed from July to September. These sources are useful together, but their combination does not identify a causal historical infrastructure effect.

### Slide 4 — 2:40–3:50

The integration is recorded step by step. The boundary dataset contains municipalities as well as lakes and foreign units. After filtering and dissolving by BFS identifier, we have 2,110 Swiss municipalities. The population data initially have 2,115 units on an older geography. We use official BFS correspondences to handle mergers and changed codes, including Moutier. Seven source codes change, and the total population is conserved.

We assign station coordinates and tile centroids to polygons in the Swiss coordinate reference system. From 22,731 station records, 22,681 are assigned and 50 remain outside municipality polygons. From a bounding box containing 30,162 performance tiles, 14,066 are assigned to Swiss municipalities. The other tiles include surrounding countries and lake or outside centroids. These exclusions are documented rather than hidden. We do not snap foreign observations to the nearest Swiss municipality.

### Slide 5 — 3:50–5:00

There are 51,815 tests across 1,847 municipalities. The remaining 263 have no observed tiles, so their speed is missing, not zero. For the main comparison, we use a pragmatic minimum of thirty tests across three tiles. This gives 405 municipalities: 241 urban, 107 intermediate and 57 rural.

The chart shows why sample selection matters. Almost half of urban municipalities qualify, but only 5.6 percent of rural municipalities do. This is a comparison among sufficiently measured municipalities, not a representative survey of Swiss residents. Passing the threshold does not make individual tests independent. We keep the full master table and compare alternative inclusion rules. This measurement imbalance is a central result, and Klodian will now explain the performance comparison within that selected sample.

## Klodian — 5:00–10:00

### Slide 6 — 5:00–6:20

First, we calculate a municipality speed by weighting each tile mean by its number of tests. We then compare the median of those municipality speeds, giving each municipality equal weight. This distinction matters: the result is not a national average user experience dominated by cities with many tests.

In the main sample, median download is 188.4 megabits per second for urban municipalities, 159.7 for intermediate and 149.2 for rural municipalities. The urban-minus-rural difference is 39.2 megabits per second. However, the point estimate is only part of the result. A canton-cluster bootstrap gives a 95 percent interval from minus 6.9 to 60.0. We resample cantons rather than treating all municipalities as fully independent.

The interval includes zero. Therefore we do not claim that these data establish a general nationwide rural disadvantage. Nor does an interval including zero prove equality. It means our estimate is uncertain under this design, and measurement selection remains a separate limitation.

### Slide 7 — 6:20–7:35

We use Welch ANOVA on log speed because the group variances differ. The global p-value is about 0.0139, which suggests some group difference under the test assumptions. It does not say that every pair differs. In the corrected pairwise tests, urban versus rural has a p-value of about 0.129. The urban–intermediate comparison is stronger.

For station density and download, Spearman correlation is about 0.311. This is a positive, moderate monotonic association. Its conventional p-value is small, but neighbouring municipalities can be dependent, so we label this exploratory evidence. A small p-value is not the size of an effect, and it does not remove confounding. We therefore complement these tests with clustered regression uncertainty and sensitivity analyses instead of presenting one significant number as the answer.

### Slide 8 — 7:35–8:50

The explanatory model uses log download and includes municipality type, station density, population density, mountain status and the 5G infrastructure share. The rural coefficient is approximately minus 0.063 relative to urban municipalities. Converted to a percentage, this is about minus 6.1 percent conditional on the model, but the uncertainty interval ranges from roughly minus 24.8 to plus 17.4 percent. The adjusted rural difference is therefore uncertain.

The station-density coefficient is positive, with a p-value of about 0.0025 using canton-clustered, t-based uncertainty. We do not interpret it as a causal effect. The predictor is log of one plus density, so it is also not a constant elasticity of raw density. As an illustration, moving from half a station record to one record per square kilometre is associated with around eight percent higher fitted speed, holding the model variables fixed. This is an association within our data, not a forecast of what a new antenna would achieve.

### Slide 9 — 8:50–10:00

For prediction, we use separate models with speed measured directly in megabits per second. We compare a mean baseline, linear regression and a random forest. The same observations are held out for comparison, and preprocessing is fitted only on training data. This avoids leaking information from evaluation observations into the model.

On a random twenty-percent holdout, linear regression has an R-squared around 0.097. When we hold out complete cantons in five folds, it falls to about 0.023, with an RMSE around 75 megabits per second. That is weak predictive transfer. The random forest does not improve it. More complexity is not automatically better. We report this openly because model evaluation is part of the question, not an opportunity to select the most flattering training score. Kristian will explain what the robustness checks and network profiles add.

## Kristian — 10:00–15:00

### Slide 10 — 10:00–11:15

Our sensitivity checks show that the adjusted group contrast depends on measurement choices. The rural coefficient is negative using all observed municipalities and under the lower threshold, but it becomes slightly positive when tiles are averaged equally rather than weighted by tests. We do not hide that change of sign or describe the group effect as robust.

A stricter threshold is also not automatically more reliable. With at least one hundred tests, only two intermediate and one rural municipality remain, compared with seventy-eight urban municipalities. That is not a useful comparison, so we retain it as a coverage diagnostic and do not fit a group regression. Other checks exclude every tile that overlaps a municipal border, include all station types, or add canton fixed effects. The density association remains positive across the reported checks, but it still has the same observational limitations.

### Slide 11 — 11:15–12:15

As an additional analysis, we use k-means to describe network profiles. The features are download, upload, latency, station density and population density. We transform skewed nonnegative variables and standardize them so one measurement unit does not dominate the distances. We compare two to six clusters using silhouette scores and check stability across different seeds.

Two profiles are selected. One has median download around 206.5 megabits per second and denser infrastructure; the other has around 123.9 with lower density and higher latency. These profiles are descriptive. Cluster numbers are arbitrary and should not be called good and bad municipalities. Because speed is itself one of the inputs, the clusters do not independently prove a speed gap.

### Slide 12 — 12:15–13:20

Our conclusion has three parts. First, among the adequately measured municipalities, urban median download is higher. Second, the adjusted rural difference remains uncertain and the predictive models transfer weakly to unseen cantons. Third, outdoor station density has a positive conditional association with observed speed, but the cross-section cannot establish a causal effect.

The main limitations are measurement self-selection, sparse rural observations, different source dates and missing information on devices, providers and tariffs. Administrative station density is an imperfect proxy because a station can serve users across a municipal boundary. We would improve the study with historical infrastructure matching the performance quarter, several quarters of observations and more representative rural measurements. We do not claim that an uncertain rural coefficient means no connectivity problem exists. The data do not support that conclusion either.

### Slide 13 — 13:20–14:20

We used OpenAI Codex for official-source research, API retrieval, integration code, models, interpretation and presentation drafts. The benefits were faster implementation and help organising the evidence. The usage is documented in the notebook and in an AI log.

There were also concrete failures. Initial package and certificate problems required a corrected environment. A naive municipality join missed mergers and code changes; the official BFS correspondence service fixed it, with population conservation checked. A constant regression predictor was removed where it had no variation. An unusable strict-threshold comparison was not retained as a convincing result. These examples show that AI output still needs checking. Each of us must understand and justify our own explanation. After our group review, we will add our genuine personal experiences and any other tools actually used, rather than inventing a reflection.

### Slide 14 — 14:20–15:00

The project includes an executed notebook, raw source snapshots with hashes, a complete integration audit, SQLite and a separately executed PostgreSQL implementation. Primary and foreign keys are enforced in PostgreSQL, and the SQL results match SQLite numerically. The appendix contains code snippets, an actual executed-notebook screenshot and output evidence for the assessment criteria.

The final submission combines the materials archive, the result presentation and this fifteen-minute group explanation. The public code repository is linked on this slide. The Moodle upload must still be verified separately; a local file is not proof of submission. Thank you for listening.

## Vor der Aufnahme

1. Bei jedem Übergang die Stoppuhr prüfen. Mit der tatsächlichen Sprechgeschwindigkeit auf exakt 15 Minuten proben; die Zielzeiten allein garantieren keine Laufzeit.
2. Die englischen Absätze in eigene Stichworte übersetzen. Zahlen wie „0.023 R²“ oder „5.6% ländlich“ erklären können.
3. Die KI-Reflexion nach echter Gruppenprüfung auf Vergangenheitsform anpassen und persönliche Beispiele ergänzen.
4. Falls das öffentliche Repository inzwischen erstellt ist, seine echte URL auf Folie 14 ergänzen und den letzten Absatz aktualisieren.
5. MP4 öffnen, Ton prüfen, Gesamtlänge und Dateigrösse kontrollieren. Dateiname: `video_recording_group_01.mp4`.

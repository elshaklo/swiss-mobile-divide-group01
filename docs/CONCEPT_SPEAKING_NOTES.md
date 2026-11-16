# Konzeptvortrag — einfacheres Englisch, Gruppe 01

Diese Version verwendet kürzere Sätze und einfachere Wörter. Die fachlichen Inhalte und die Folienaufteilung bleiben erhalten. „Municipality“ bedeutet Gemeinde; „station density“ bedeutet Anzahl Anlageneinträge pro Quadratkilometer.

Die Aufteilung ist ein Vorschlag. Übt den Text und sprecht danach möglichst frei mit Stichworten. Die Zeiten sind Zielzeiten, keine gemessene Vortragsdauer. Mit Stoppuhr proben; nicht künstlich langsam sprechen. Folie 11 ist der Quellenanhang und wird nicht vorgetragen.

| Person | Folien | Zielzeit |
|---|---|---|
| Arthik | 1–3 | 0:00–3:00 |
| Klodian | 4–7 | 3:00–7:00 |
| Kristian | 8–10 | 7:00–10:00 |

## Slide 1 — Arthik — 0:00–0:35

Good morning. We are Arthik Muralitharan, Klodian Elshani and Kristian Perkovic. We are group one.

Our project is about mobile internet in Switzerland. We want to find out if mobile internet is slower in rural areas than in cities. We also want to see how this is linked to the number of mobile stations.

First, we will explain our question. Then we will present the data and methods. Finally, we will discuss what we expect and what the limits are.

## Slide 2 — Arthik — 0:35–1:40

A phone can have a signal, but the internet can still be slow. This is why we look at measured download speed, not only at places with a mobile signal.

We compare three types of municipalities. A municipality is a local area, such as a town or village. The three types are urban, intermediate and rural. Intermediate areas have both urban and rural features.

Our main question is: How does mobile download speed differ between these three groups? And how is this linked to station density when we also consider other factors?

Station density means the number of station records per square kilometre. Other factors include population density and mountain areas.

We want to find links in the data. We cannot prove that adding one station causes a certain increase in speed.

## Slide 3 — Arthik — 1:40–3:00

We use data from four sources.

First, BAKOM gives us information about mobile stations. This includes their location, technology and whether they are indoors or outdoors.

Second, BFS gives us the official municipality types and population numbers. It also helps us deal with changes, for example when two municipalities merge. We collect these data through APIs. An API lets our Python code request data directly from a service.

Third, swisstopo gives us municipality borders and their area.

Fourth, Ookla gives us existing speedtest data. These include download speed, upload speed, delay and the number of tests in each small map tile. We did not carry out these speedtests ourselves.

The speed data cover July to September 2026. The station data are from November. These dates are different, and we will explain this limit.

We have already checked that we can access and combine the data. We would like the lecturer to confirm that this mix of API data and existing speedtest data meets the project rules.

Klodian will now explain how we combine the data.

## Slide 4 — Klodian — 3:00–3:55

Our sources have three different types of records.

BAKOM has one record for a mobile operator's station at a location. Several operators can use the same mast. So a station record is not always a separate physical mast.

Ookla has one record for each small map tile. This record contains average values from the tests in that tile.

Each municipality has an official BFS number and a border on the map.

We combine these sources into one table with one row per municipality. We calculate download speed and the number of outdoor station records per square kilometre.

We also calculate the share of station records that list 5G. This does not tell us how many speedtests actually used 5G.

## Slide 5 — Klodian — 3:55–4:55

We combine the data in four steps.

First, we collect the data and save the original files. We also save checksums, which help us check if a file has changed.

Second, we match the official municipality numbers. We use BFS information to handle mergers and changed numbers. We check that no population is lost during this step.

Third, we use the map to find which municipality contains each station and each tile's centre point.

Fourth, we calculate the values for each municipality. A tile with more tests gets more weight when we calculate average speed.

We record any data that we cannot match. If a municipality has no speed data, we leave the value missing. We do not call it zero speed.

We also check tiles near borders, because one tile can cover parts of two municipalities.

## Slide 6 — Klodian — 4:55–6:00

First, we explore the data. We use maps, charts and tables. We look at speed differences and check where data are missing.

To compare the three groups, we use Welch ANOVA. This test can handle groups with different amounts of variation. We use the logarithm of speed to make very high values less dominant.

We also use Spearman correlation to check whether higher station density tends to go together with higher speed. We report p-values and explain the limits of these tests.

Our main model is a linear regression with log speed. It includes municipality type, station density, the 5G share, population density and mountain status.

We allow for similarities between municipalities in the same canton when we calculate uncertainty. Mountain status tells us whether a municipality is in a mountain region. It is not a measured height.

The model helps us study links between these factors. It does not prove cause and effect.

## Slide 7 — Klodian — 6:00–7:00

A model can fit the data it has already seen but work poorly on new data. This is why we keep some data separate for testing.

We compare three models: a simple average, linear regression and a random forest. We use R-squared, RMSE and MAE to judge their performance. RMSE and MAE describe prediction errors. We fit the data preparation steps only on the training data.

We also test the models on cantons that they have not seen during training. We do this in five rounds.

As an extra method, we use k-means. It puts municipalities with similar network features into groups. We put the features on a common scale and compare two to six groups. We use a score called the silhouette score to help choose the number of groups.

Speed is one of the inputs. So these groups are not separate proof of a speed difference.

Kristian will now explain our expected results and the main limits.

## Slide 8 — Kristian — 7:00–8:00

We expect that urban municipalities may have higher download speeds and more stations per square kilometre.

But this is a hypothesis, not a result that we assume is true. After we consider the other factors, the difference may become smaller. It may also be too uncertain for a clear answer.

Our project will provide maps, a comparison of the three groups and an evaluation of the models. We will show both the estimated differences and their uncertainty.

A small or uncertain difference is still a useful result. We will not choose a method just because it gives a significant result.

We want other people to understand our steps and be able to run the analysis again using our notebook.

## Slide 9 — Kristian — 8:00–9:00

The biggest limit is how the speedtests are collected. People decide when and where to run a test. The tests are not a random sample of all residents.

Rural municipalities may have fewer tests. We therefore show which municipalities have data and which we use in the model. We cannot assume that the results describe every person or every place.

Station density also has limits. A station outside a municipality can serve people inside it. Terrain, phones, mobile plans and operators can also affect speed.

The dates of the station and speed data are different too.

To make our work easy to check, we save the original data and document the joins. We use SQLite and also PostgreSQL. We explain how we used AI, what it helped with and what we had to correct.

## Slide 10 — Kristian — 9:00–10:00

After this presentation, we will use the lecturer's feedback to improve the project. We will review the analysis together and check how the results change when we make different choices.

For the final submission, we prepare the notebook, data, slides and an appendix with evidence for the project criteria.

Our final group video must be fifteen minutes long: five minutes per person.

We have checked that the technical steps work. Today, we would like to get approval for the topic and data sources. In particular, we want to confirm that our API data and the existing Ookla speedtest data meet the collection requirement.

We will also clarify the conflicting deadline shown on Moodle.

Thank you for listening. We are happy to answer your questions.

## Stichwortkarten auf Deutsch

- Arthik: Signal ist nicht gleich Geschwindigkeit; drei Gemeindetypen; Forschungsfrage; vier Quellen; unterschiedliche Zeitstände.
- Klodian: drei Datenebenen; BFS-Nummern und Fusionen; Zuordnung auf der Karte; Gewichtung; Regression; neue Testdaten; k-means.
- Kristian: Erwartung ist keine feststehende Antwort; wenige Messungen auf dem Land; keine Kausalität; nachvollziehbare Arbeit; Freigabe und nächste Schritte.

## Wichtige Wörter zum Üben

| Englisch | Bedeutung |
|---|---|
| municipality | Gemeinde |
| urban / intermediate / rural | städtisch / intermediär / ländlich |
| station density | Anzahl Anlageneinträge pro Quadratkilometer |
| download speed | Downloadgeschwindigkeit |
| map tile | kleine Kartenkachel |
| missing data | fehlende Daten |
| uncertainty | Unsicherheit |
| training data / test data | Daten zum Lernen / separate Daten zum Prüfen |
| cause and effect | Ursache und Wirkung |

Die Fachbegriffe auf den Folien müssen nicht alle auswendig erklärt werden. Versteht aber, warum ihr die jeweilige Methode verwendet. Sprecht die Zahlen und Begriffe vor dem Vortrag einmal laut durch.

# Mögliche Rückfragen — verstehen statt auswendig lernen

**Was ist bei euch die primäre Datenerhebung?**  
Direkte Abfragen der offiziellen BAKOM-/BFS-Dienste, mit gespeichertem Code, Anfragen und Rohantworten. Ookla ist ausdrücklich eine sekundäre Quelle für Geschwindigkeit. Diese Kombination bei der Themenfreigabe bestätigen lassen. Nicht behaupten, selbst Funkmessungen durchgeführt zu haben.

**Warum Gemeinden und nicht einzelne Speedtests?**  
Die offizielle Typologie und die vergleichbaren Verwaltungsattribute liegen auf Gemeindeebene vor. Ookla veröffentlicht aggregierte Kacheln, keine Einzelmessungen. Aus Gemeindeergebnissen kann man keine Aussagen über jede einzelne Person ableiten.

**Warum ist der Mittelwert gewichtet?**  
Eine Kachel mit zehn Tests soll beim Rekonstruieren des durchschnittlichen gemessenen Downloads zehnmal so stark zählen wie eine Kachel mit einem Test. Der Vergleich der Gemeindemediane gewichtet danach jede Gemeinde gleich. Andere Gewichtungen werden als Sensitivität gezeigt.

**Sind 51’815 Tests ebenso viele unabhängige Beobachtungen?**  
Nein. Die Regression hat 405 Gemeinde-Beobachtungen im Hauptmodell. Tests können wiederholt von denselben Geräten und räumlich abhängig sein. Summierte devices sind keine eindeutige Anzahl Geräte im ganzen Gemeindegebiet.

**Warum nur 405 von 2’110 Gemeinden?**  
Die Regel mindestens 30 Tests und drei Kacheln soll extrem dünne Messungen begrenzen. Sie ist eine pragmatische Regel, kein Nachweis von Repräsentativität. Gerade ländliche Gemeinden fallen häufig weg. Deshalb zeigen wir die Auswahl und andere Schwellen.

**Was bedeutet p=0.129 für Stadt/Land?**  
Unter den Annahmen des korrigierten Tests liefert die Stichprobe keine klare Evidenz für diesen Paarunterschied auf dem üblichen 5%-Niveau. Das beweist weder Gleichheit noch die Abwesenheit eines Problems. Effekt und Unsicherheit mitberichten.

**Warum globale ANOVA signifikant, Stadt/Land aber nicht?**  
Der globale Test fragt, ob irgendwo zwischen den drei Gruppen Unterschiede bestehen. Er behauptet nicht, dass jedes Paar unterschiedlich ist. Paarweise Tests werden ausserdem für Mehrfachvergleiche korrigiert.

**Warum Welch statt klassischer ANOVA?**  
Die Gruppen haben unterschiedliche Varianzen; Levene p≈0.008. Welch setzt keine gleichen Gruppenvarianzen voraus. Räumliche Unabhängigkeit ist weiterhin fraglich; p-Werte sind explorativ.

**Bedeutet höhere Antennendichte bessere Versorgung?**  
Wir sehen eine positive Assoziation mit gemessener Geschwindigkeit. Die Zahl der Betreiber-Anlagen pro km² misst weder die vollständige Funkabdeckung noch Leistung, Auslastung oder Versorgung durch Anlagen jenseits der Grenze.

**Was bedeutet der 5G-Anteil?**  
Anteil der Outdoor-Anlageneinträge, die 5G als Technologie nennen. Nicht Anteil der Fläche, Menschen oder Tests mit 5G. Keine Aussage über den individuellen Mobilfunkvertrag.

**Warum kein Höhenmeter-Wert wie ursprünglich vorgeschlagen?**  
Eine belastbare mittlere Höhe wurde nicht erhoben. Stattdessen nutzen wir den offiziell verfügbaren Berggebietsindikator, mit korrekter Bezeichnung. Eine Zentroidhöhe wäre ebenfalls keine mittlere Gemeinde-Höhe.

**Warum ist die Vorhersage so schwach?**  
Tarife, Geräte, Provider und Last sind nicht beobachtet; Messungen sind selbstgewählt und spärlich. Infrastruktur- und Gemeindeattribute erklären nur einen kleinen Teil der Unterschiede. R²≈0.023 in nicht gesehenen Kantonen ist offen als schwach ausgewiesen.

**Warum nicht einfach das beste Random-Forest-Ergebnis zeigen?**  
Auf denselben Testdaten ist der Wald hier nicht besser. Trainingsfit als Testleistung darzustellen wäre falsch. Die einfache Baseline ist nötig, um überhaupt einen Nutzen beurteilen zu können.

**Warum SQLite und PostgreSQL?**  
SQLite ist in den Mindestanforderungen explizit genannt; PostgreSQL separat als Zusatzkriterium. Beide sind ausgeführt und gespeichert. Die PostgreSQL-Abfragen sind keine blosse Konfiguration; ihre Resultate werden numerisch mit SQLite verglichen.

**Was ist an eurem Projekt kreativ?**  
Die konkrete Schweizer Vergleichsfrage, offizielle Geografie-Harmonisierung, sichtbare Messlücken, Grenzkachel-Sensitivität und Evaluation in zurückgehaltenen Kantonen. Ob das den Kreativitätspunkt verdient, entscheidet die Lehrperson.

**Sind die zwei Cluster ein Beweis für einen digitalen Graben?**  
Nein. Geschwindigkeit fliesst in das Clustering ein; das Ergebnis wäre als unabhängiger Beweis zirkulär. Es beschreibt kombinierte Netzwerkprofile.

**Was hat KI falsch gemacht?**  
Konkrete Beispiele im KI-Log: naive Gemeindeverknüpfung, konstanter Prädiktor, untaugliche Gruppe bei strenger Schwelle sowie technische Wiederholungsprobleme. Korrekturen sind dokumentiert. Eigene Erfahrungen erst nach tatsächlicher Prüfung ergänzen.

**Was würdet ihr verbessern?**  
Zeitgleiche historische Anlagen, mehrere Quartale, bessere ländliche Messungen, echte Gelände-/Höhendaten sowie Provider-/Gerätezusammensetzung. Nicht einfach mehr Algorithmen hinzufügen.

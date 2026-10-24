# Ausbau der Geräteunterstützung

Ich veröffentliche den aktuellen Ausbau einschließlich P03 und P05 bis P14
sowie P16 mit v0.8.2-beta.6. P15 ist abgewählt. Diese umfangreiche Beta enthält
neue Geräteklassen und größere Umbauten; ich empfehle ein Backup und eine
bewusste Prüfung nach dem Update. v0.8.1 bleibt Stable/Latest.
Die folgende Übersicht trennt den enthaltenen Code von noch offenen Geräteprüfungen. Ein Gateway behält sein vorhandenes
HA-Gerät; Kennungen, Namen und Verläufe bestehender Entitäten bleiben erhalten.

| Arbeitspaket | Stand dieses Checkpoints | Noch offen |
|---|---|---|
| 1. Bestandsaufnahme | 361 Modellzeilen einzeln zugeordnet, einschließlich zweier allgemeiner Befehlsmodelle; Herkunft, Datenverträge und Lücken dokumentiert | Vollständige Prüfung der strukturierten Datenformate und anderer Adapter am Gerät |
| 2. Katalog und Erkennung | Gemeinsame Definition der Enthärterressourcen, profilabhängige Abfragen, dynamische Kreise und bestehende Grenzen | Weitere Geräteprofile nach gesicherter Zuordnung |
| 3. WE800i-Anzeigen | Aktuelle Sensoren und Binärsensoren implementiert, synthetische Tests | Vergleich mit MyBuderus am echten WE800i, weitere Einheiten und Erholung nach Neustart bestätigen |
| 4. WE800i-Bedienung | Vier Bedienfunktionen vorbereitet und standardmäßig deaktiviert | Reale Schreibbestätigung vor Freigabe; Abbruchfunktion ungeklärt |
| 5. Weitere Heizungsfunktionen | Bestehende Unterstützung abgeglichen; sechs Heiz-/Kühlanzeigen je angebotener Raumzone und Warmwasser-Gerätetyp ergänzt | Weitere fehlende Felder und zusätzliche Schreibfunktionen einzeln prüfen; Gerätebestätigung |
| 6. Zusammengesetzte Entitäten | Midea/RWH-Warmwasser, Midea Climate Series, sieben Air-Familien und drei Dry-Familien in Beta.6 enthalten und synthetisch geprüft | Physische Bestätigung; weitere Familien und abgegrenzte Zusatzfunktionen |
| 7. Weitere Programme | RRC-Programmauswahl und Bearbeitung vorhandener Wochenschaltpunkte, ICOM-Urlaubszeiten und WDDW2-Urlaubsmodus enthalten | Neue Programme und Schaltpunkte, zusätzliche Geräte- und Browserbestätigung |
| 8. Weitere Geräte und Wartung | Geräteadapter und administrative Ressourcen im Index getrennt gekennzeichnet | Adapterprüfung und gesonderte Bedienabläufe; keine Freigabe allein aufgrund von Schreibrechten |
| 9. Diagnose und Übersicht | Schema 27 enthält Gerätefamilien, Aktualitäts-, Laufzeit-, Sammlungs- und Energieprüfung ohne Messwerte; frühere Sicherheits-, Profil- und Registrierungsangaben bleiben erhalten | Erweiterung je weiterem Gerätepaket |
| 10. Tests und Freigabe | Gezielte Regressionstests und gemeinsame Qualitätsprüfung | Geräteprüfungen; die Veröffentlichung setzt erfolgreiche GitHub-Prüfungen voraus |

Zusätzlich sind P01 (WDDW2-Typen), P02 (Ressourcennamen und Sprache) und P04
(Enthärterphasen und Prüfanleitung) enthalten. P13 ergänzt acht reine
[Wallbox-Anzeigen](pointt-wallboxes.md). P14 behält ein Anlagengerät je
PointT-Gateway bei; P16 korrigiert und dokumentiert Werteumrechnungen.
Die Bestätigung am WE800i benötigt weiterhin die Rückmeldung des Melders
von Issue #60.

Der [Ressourcenindex](app-resource-inventory.md) ist ein Arbeitsnachweis und
noch keine vollständige Freigabeliste. Ein Pfadfund beweist weder die
Verfügbarkeit am Gerät noch die Eignung als Bedienelement. Die
[WE800i-Beschreibung](water-softener.md) hält diese Unterschiede fest.

Das Paket für Verbrauchshistorie und Regenerationsprotokoll (P15) ist
abgewählt. Aktuelle Verbrauchssensoren aus `/recordings` und ein rückwirkender
Import historischer Messreihen sind nicht enthalten.
Der Wunsch nach Weichwasserverbrauch in Issue #60 ist deshalb gesondert zu
klären und wird durch den aktuellen Durchflusssensor nicht als erledigt gewertet.

Für die weitere Arbeit bleiben die Pakete getrennt prüfbar. Insbesondere
dürfen Änderungen an administrativen Funktionen, Energieauswertung und
Schreibabläufen nicht mit einer pauschalen Behauptung vollständiger
Geräteunterstützung freigegeben werden.

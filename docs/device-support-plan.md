# Ausbau der Geräteunterstützung

Der bisherige Ausbau ist in v0.8.2-beta.5 veröffentlicht. P03 ergänzt lokal
die Datenverträge und Laufzeitkorrekturen; diese Änderungen sind noch nicht veröffentlicht.
Die folgende Übersicht trennt den enthaltenen Code von noch offenen Geräteprüfungen. Ein Gateway behält sein vorhandenes
HA-Gerät; Kennungen, Namen und Verläufe bestehender Entitäten bleiben erhalten.

| Arbeitspaket | Stand dieses Checkpoints | Noch offen |
|---|---|---|
| 1. Bestandsaufnahme | 361 Modellzeilen einzeln zugeordnet, einschließlich zweier allgemeiner Befehlsmodelle; Herkunft, Datenverträge und Lücken dokumentiert | Vollständige Prüfung der strukturierten Datenformate und anderer Adapter am Gerät |
| 2. Katalog und Erkennung | Gemeinsame Definition der Enthärterressourcen, profilabhängige Abfragen, dynamische Kreise und bestehende Grenzen | Weitere Geräteprofile nach gesicherter Zuordnung |
| 3. WE800i-Anzeigen | Aktuelle Sensoren und Binärsensoren implementiert, synthetische Tests | Vergleich mit MyBuderus am echten WE800i, weitere Einheiten und Erholung nach Neustart bestätigen |
| 4. WE800i-Bedienung | Vier Bedienfunktionen vorbereitet und standardmäßig deaktiviert | Reale Schreibbestätigung vor Freigabe; Abbruchfunktion ungeklärt |
| 5. Weitere Heizungsfunktionen | Bestehende Unterstützung abgeglichen; sechs Heiz-/Kühlanzeigen je angebotener Raumzone und Warmwasser-Gerätetyp ergänzt | Weitere fehlende Felder und zusätzliche Schreibfunktionen einzeln prüfen; Gerätebestätigung |
| 6. Zusammengesetzte Entitäten | Noch nicht implementiert | Thermostat, Klimagerät, Warmwasser- und Lüfterentität mit geprüfter Zuordnung der Teilfunktionen |
| 7. Weitere Programme | Pfadfunde im Index eingeordnet | Eigene Parser, Konflikterkennung, Dialoge, Browserprüfung und Gerätebestätigung |
| 8. Weitere Geräte und Wartung | Geräteadapter und administrative Ressourcen im Index getrennt gekennzeichnet | Adapterprüfung und gesonderte Bedienabläufe; keine Freigabe allein aufgrund von Schreibrechten |
| 9. Diagnose und Übersicht | Schema 18 ergänzt Laufzeit- und Sammlungsprüfung ohne Messwerte; frühere Sicherheits-, Profil- und Registrierungsangaben bleiben erhalten | Erweiterung je weiterem Gerätepaket |
| 10. Tests und Freigabe | Gezielte Regressionstests und gemeinsame Qualitätsprüfung | Geräteprüfungen; die Veröffentlichung setzt erfolgreiche GitHub-Prüfungen voraus |

Zusätzlich sind P01 (WDDW2-Typen), P02 (Ressourcennamen und Sprache) und P04
(Enthärterphasen und Prüfanleitung) enthalten. Der nächste Umsetzungsschritt
ist nach dem lokal abgeschlossenen [P03](resource-contracts.md) nun P05 mit der ConnectKey-Zonenbedienung. Die Bestätigung am WE800i benötigt
weiterhin die Rückmeldung des Melders von Issue #60.

Der [Ressourcenindex](app-resource-inventory.md) ist ein Arbeitsnachweis und
noch keine vollständige Freigabeliste. Ein Pfadfund beweist weder die
Verfügbarkeit am Gerät noch die Eignung als Bedienelement. Die
[WE800i-Beschreibung](water-softener.md) hält diese Unterschiede fest.

Aktuelle Verbrauchssensoren aus `/recordings` bleiben ein optionales eigenes
Paket. Ein rückwirkender Import historischer Messreihen ist nicht vorgesehen.
Der Wunsch nach Weichwasserverbrauch in Issue #60 ist deshalb gesondert zu
klären und wird durch den aktuellen Durchflusssensor nicht als erledigt gewertet.

Für die weitere Arbeit bleiben die Pakete getrennt prüfbar. Insbesondere
dürfen Änderungen an administrativen Funktionen, Energieauswertung und
Schreibabläufen nicht mit einer pauschalen Behauptung vollständiger
Geräteunterstützung freigegeben werden.

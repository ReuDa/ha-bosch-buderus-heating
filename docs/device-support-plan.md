# Ausbau der Geräteunterstützung

Ich setze den Ausbau auf v0.8.2-beta.4 auf. Der Anhang zum Auftrag vom
22.10.2026 bleibt der vereinbarte Umfang. Ein Gateway behält sein vorhandenes
HA-Gerät; Kennungen, Namen und Verläufe bestehender Entitäten bleiben erhalten.

| Arbeitspaket | Stand dieses Checkpoints | Noch offen |
|---|---|---|
| 1. Bestandsaufnahme | Index der pfadtragenden MyBuderus-Ressourcenmodelle, einschließlich zusammengesetzter Heizkreis- und Warmwasserpfade | Vollständige Prüfung aller Datenformate, übriger dynamischer Konstruktionen und anderer Adapter |
| 2. Katalog und Erkennung | Gemeinsame Definition der Enthärterressourcen, profilabhängige Abfragen, dynamische Kreise und bestehende Grenzen | Weitere Geräteprofile nach gesicherter Zuordnung |
| 3. WE800i-Anzeigen | Aktuelle Sensoren und Binärsensoren implementiert, synthetische Tests | Vergleich mit MyBuderus am echten WE800i, weitere Einheiten und Erholung nach Neustart bestätigen |
| 4. WE800i-Bedienung | Separates nachfolgendes Paket, in diesem Stand keine neuen Schreibfunktionen | Reale Schreibbestätigung vor Freigabe; Abbruchfunktion ungeklärt |
| 5. Weitere Heizungsfunktionen | Bestehende Unterstützung im Ressourcenindex abgeglichen | Fehlende Verdichter-, Kältekreis-, Warmwasser-, Solar-, Lüftungs-, Zonen-, Pool- und PV-Felder einzeln prüfen und ergänzen |
| 6. Zusammengesetzte Entitäten | Noch nicht implementiert | Thermostat, Klimagerät, Warmwasser- und Lüfterentität mit geprüfter Zuordnung der Teilfunktionen |
| 7. Weitere Programme | Pfadfunde im Index eingeordnet | Eigene Parser, Konflikterkennung, Dialoge, Browserprüfung und Gerätebestätigung |
| 8. Weitere Geräte und Wartung | Geräteadapter und administrative Ressourcen im Index getrennt gekennzeichnet | Adapterprüfung und gesonderte Bedienabläufe; keine Freigabe allein aufgrund von Schreibrechten |
| 9. Diagnose und Übersicht | Schema 16 mit Profil, Abfragen, Enthärterprüfung und Registrierungsstatus; deutsche und englische Gerätebeschreibung | Erweiterung je weiterem Gerätepaket |
| 10. Tests und Freigabe | Gezielte Regressionstests und gemeinsame Qualitätsprüfung | Geräteprüfungen und GitHub-Prüfungen des späteren PR-Standes |

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

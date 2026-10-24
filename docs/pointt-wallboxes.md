# PointT wallboxes

## English

I added a read-only adapter in v0.8.2-beta.6 for gateways reported as
`commodule` or `commodule2`. It uses the existing PointT account and HTTPS
transport, with a separate parser for wallbox objects. It does not use the
additional-device MQTT connection. A device must be returned by the account
and selected in the integration. Retail names alone do not establish support.

The implemented scope is charge point `cp0`. I have not established discovery
of additional charge points or a complete list of compatible retail models.
The selected gateway retains its device identifier; the eight new sensors use
stable IDs. Existing heating entities and user settings are preserved.

| Reading | Interpretation |
| --- | --- |
| Charging state | Eleven known reported states, kept distinct. A vehicle pause does not prove a full battery. Unknown codes stay unknown. |
| Charging power | Last component of `telemetry.meter`, already in kW. |
| Reported charged energy | First component of `telemetry.meter`, converted from Wh to kWh once. No accumulation or long-term statistics state class. |
| Active charging time | Reported `activeChargingTime` in minutes, without local extrapolation. |
| Reported current limit | `telemetry.limit` in A, read-only. This is a limit, not measured current. |
| Charging start | Reported `chargingStart`, accepted only with an explicit UTC offset. |
| Wallbox role | `conf.wallboxMode`: standalone, leader or follower. This is not the charging strategy. |
| Hardware current limit | `info.hwCurrentLimit` in A, read-only diagnostic sensor. |

Missing, malformed, negative and non-finite numbers do not become zero. The
energy counter may drop between reports without being added to a synthetic
total. Its exact session/reset scope still needs device confirmation, so it
is not offered as a lifetime energy meter for the Energy dashboard.

I read three object endpoints under `rest/v1/cp0`: `telemetry`, `conf` and
`info`. Telemetry follows the 60-second standard or 120-second cloud-friendly
interval. Configuration is read every 5 or 10 minutes; information every 15
or 30 minutes. Setup makes at most three logical reads per wallbox. The shared
transport retains its bounded read retries, token refresh and account-wide
rate-limit brake. Diagnostics create no extra requests.

A local 403, 404, 406 or malformed object withdraws only that section. It is
retried at its regular interval. Authentication, connection, service and
rate-limit failures stop the wallbox cycle and withdraw its readings.
Authentication requests reauthentication. A temporarily unavailable wallbox
does not prevent a mixed heating account from loading. Readings expire after
twice their section interval; this measures response freshness, not a
guarantee that an upstream service has uncached device data. Polls are
serialized, and recovery updates the same entities without a restart.

Schema 26 diagnostics expose section intervals, freshness and valid/invalid
field counts. They omit readings, dates, gateway and device identifiers,
account data, labels, serial numbers and unknown text. Product and software
information are used only in the ordinary HA device information.

### Remaining work

I have no wallbox in my account. The implementation has synthetic protocol,
HTTP and Home Assistant tests; it has not been compared with a physical
wallbox. Model compatibility, displayed values, cloud response freshness and
energy resets require that comparison.

Start, pause, current changes, lock/authentication settings, RFID, charging
strategies and forced overrides remain unavailable. Although command routes
are identified, their full admission rules differ with firmware, external
energy management, wallbox role and active limiters. Start may involve both
authentication and an override. I have not turned these routes into generic
buttons or a writable current number. Before adding a command, its complete
preconditions, effect and read-back confirmation must be established. A
hardware test alone does not replace that contract work. Charge logs and
historical energy import are also outside this implementation.

## Deutsch

Ich habe in v0.8.2-beta.6 eine Anbindung mit acht Anzeigen für
die gemeldeten Gatewaytypen `commodule` und `commodule2` ergänzt. Sie nutzt den
vorhandenen PointT-Zugang mit einem eigenen Parser für Wallbox-Antworten.
Das Gerät muss im Konto gemeldet und in der Integration ausgewählt sein.
Ein Verkaufsname allein reicht für die Zuordnung nicht aus. Der zusätzliche
MQTT-Zugang wird hierfür nicht verwendet.

Der Umfang ist auf `cp0` begrenzt. Weitere Ladepunkte und eine vollständige
Liste kompatibler Verkaufsmodelle sind noch nicht belegt. Die Gerätekennung
bleibt erhalten. Die neuen Anzeigen haben stabile IDs; bestehende
Heizungsentitäten und Benutzereinstellungen bleiben bestehen.

| Anzeige | Bedeutung |
| --- | --- |
| Ladezustand | Elf bekannte Zustände bleiben getrennt. Eine Pause durch das Fahrzeug bedeutet nicht automatisch einen vollen Akku. Unbekannte Codes bleiben unbekannt. |
| Ladeleistung | Letzter Bestandteil von `telemetry.meter`, bereits in kW. |
| Gemeldete geladene Energie | Erster Bestandteil von `telemetry.meter`, einmal von Wh nach kWh umgerechnet. Keine Aufsummierung und keine Statistikklasse für Langzeitwerte. |
| Aktive Ladezeit | Gemeldete Minuten aus `activeChargingTime`, ohne eigene Hochrechnung. |
| Gemeldete Stromgrenze | `telemetry.limit` in A. Eine Grenze, kein gemessener Strom und kein Regler. |
| Ladebeginn | `chargingStart`, nur mit eindeutigem UTC-Versatz angenommen. |
| Rolle im Wallbox-Verbund | `conf.wallboxMode`: eigenständig, führend oder folgend. Keine Ladestrategie. |
| Hardware-Stromgrenze | `info.hwCurrentLimit` in A als Diagnoseanzeige. |

Fehlende, ungültige, negative oder nicht endliche Zahlen werden nicht als
null dargestellt. Ein sinkender Energiewert wird nicht zu einem eigenen
Gesamtzähler addiert. Wann genau der Wert zurückgesetzt wird, muss noch am
Gerät geprüft werden. Deshalb ist er kein Gesamtverbrauchszähler für das
Energie-Dashboard.

Die drei Objektabfragen unter `rest/v1/cp0` betreffen `telemetry`, `conf` und
`info`. Telemetrie wird je nach Abfrageprofil alle 60 oder 120 Sekunden
gelesen, Konfiguration alle 5 oder 10 Minuten und Geräteinformation alle 15
oder 30 Minuten. Beim Start gibt es höchstens drei logische Abfragen pro
Wallbox. Begrenzte HTTP-Lesewiederholungen, Token-Erneuerung und die gemeinsame
Kontosperre bei Anfragelimits bleiben erhalten. Die Diagnose fragt nichts
zusätzlich ab.

403, 404, 406 und fehlerhafte Objekte betreffen nur ihren Abschnitt. Beim
nächsten regulären Termin wird dieser erneut geprüft. Anmelde-, Verbindungs-,
Dienst- und Anfragelimitfehler beenden den Wallbox-Durchlauf und machen seine
Anzeigen unverfügbar. Anmeldefehler lösen eine erneute Anmeldung aus. Eine
vorübergehend nicht erreichbare Wallbox verhindert nicht das Laden eines
gemischten Kontos mit Heizung. Nach zweimal dem jeweiligen Abfrageintervall
gelten Antworten als veraltet. Das beschreibt den Empfang der Antwort und
beweist nicht, dass der vorgeschaltete Dienst ungepufferte Gerätedaten liefert.
Abfragen laufen nacheinander. Die Anzeigen erholen sich mit denselben IDs.

Diagnose-Schema 26 enthält Intervalle, Aktualität und Zähler gültiger oder
ungültiger Felder. Messwerte, Datumsangaben, Kennungen, Kontodaten, Namen,
Seriennummern und unbekannte Texte bleiben ausgeschlossen. Produkt und
Software erscheinen ausschließlich in der gewöhnlichen HA-Geräteinformation.

### Noch offen

In meinem Konto ist keine Wallbox eingerichtet. Protokoll, HTTP-Zugang und
HA-Einbindung werden mit synthetischen Antworten geprüft. Ein Geräteabgleich
hat nicht stattgefunden. Modellkompatibilität, Anzeigen, Aktualität der
Cloud-Antworten und Rücksetzungen der Energie benötigen Praxisbestätigung.

Start, Pause, Stromänderungen, Sperren, Authentifizierung, RFID,
Ladestrategien und erzwungene Übersteuerungen sind noch nicht verfügbar.
Die Befehlsrouten sind identifiziert; die vollständigen Freigaberegeln hängen
unter anderem von Firmware, Energiemanagement, Verbundrolle und aktiver
Begrenzung ab. Ein Start kann zusätzlich authentifizieren und Grenzen
übersteuern. Daraus habe ich keine allgemeinen Tasten oder Stromregler
abgeleitet. Vor der Umsetzung müssen Vorbedingungen, Wirkung und
Rücklesebestätigung vollständig geklärt sein. Ein einzelner Gerätetest ersetzt
diese Vertragsprüfung nicht. Ladeprotokolle und historische Energieimporte
sind ebenfalls noch nicht enthalten.

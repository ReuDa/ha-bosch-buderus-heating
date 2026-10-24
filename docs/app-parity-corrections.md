# Corrections after the app comparison

I corrected the six confirmed functional findings in the local, unreleased
integration. I also updated the setup wording and aligned the numeric salt
warning with the app rule. This work adds no new device family and does not
change existing entity IDs or the selected device layout.

| Area | Result |
|---|---|
| Sensor receive format | Decode the items envelope, choose the newest timestamped item and merge non-null fields. Reject ambiguous or malformed samples. |
| Partial state reports | Merge update responses and replace full get snapshots. Desired-only acknowledgements cannot confirm writes or refresh reported fields. |
| Freshness | Track the observation time of each field. Updating one field does not keep unrelated fields fresh. Partial messages from a new connection do not reuse the old connection's fields. |
| Configuration | Reachable PointT gateways remain selectable during an optional cloud discovery outage. Existing cloud selections are preserved; they cannot be silently transferred to another account. |
| Multipart energy | Require the supported emonValue schema before exposing converted values. Missing or incompatible type metadata makes the reading unknown. |
| Cancelled RRC writes | Invalidate the affected selection or week after cancellation. A later regular read can restore the confirmed state without repeating the PUT. |
| Water-heater temperatures | Accept only tiny floating-point conversion noise around valid integer device targets. Range and step validation still apply. |
| Salt warning | Interpret valid inputs as Float, compare their integer parts and use 20% only when the threshold resource is absent. Known failed, stale or malformed sources remain unknown. |
| Setup text | German and English now explain that controls depend on the model and reported capabilities. |

The eight BACON fixture files now contain the actual sensor envelope. Their
values remain synthetic. The tests exercise this format through normal ingest
and the existing local MQTT/WebSocket transport harness. Additional regressions
cover out-of-order samples, partial reports, missing fields, field aging,
connection changes, configuration outages, cancellation and Fahrenheit service
calls.

The original P16 test figures remain a historical result in its audit inventory.
Final local validation: 3,036 automated cases passed, including separately
counted parameter variants, with 96.83% combined statement and branch coverage.
Ruff, format validation, strict Mypy (80 files), reproducible packaging and
import from an isolated ZIP installation passed. The separate rule comparison
matched all 707 filter cases and all 13 selected salt cases. German and English
have the same 585 translation keys and matching placeholders. No physical
device test or new release was performed.

## Deutsche Einordnung

Ich habe die sechs bestätigten Funktionsfehler korrigiert und die zugehörigen
Gegenbeispiele in die regulären Tests übernommen. Teilmeldungen ergänzen jetzt
die zuletzt bestätigten Felder. Jedes Feld behält dabei sein eigenes Alter.
Eine reine Annahme des gewünschten Zustands bestätigt weiterhin keinen
Schreibzugriff.

Die Salzwarnung entspricht bei gültigen Werten der belegten App-Regel:
20,9 Prozent Salz bei einer Schwelle von 20 Prozent lösen bereits eine Warnung
aus. Fehlt die Schwellenressource, gelten 20 Prozent. Eine bekannte, aber
ausgefallene oder veraltete Quelle wird dadurch nicht ersetzt. Die eigentlichen
Messwerte behalten ihre Nachkommastellen.

Der Abgleich ersetzt keine Geräteprüfung. Liveverhalten, Wiederverbindung und
Schreibwirkung der neuen Gerätefamilien sind weiterhin an passenden Geräten
zu bestätigen. Auch die Bedeutung der App-Aktivmeldung für laufende
Messwertübermittlung bleibt offen. P15 bleibt abgewählt und P14 behält ein
Anlagengerät pro PointT-Gateway. Ich habe weder eine neue Version veröffentlicht
noch reale Schreibbefehle an Geräte gesendet.

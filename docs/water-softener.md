# Water softeners / Wasserenthärter

## Deutsch

Ich ergänze mit diesem Entwicklungsstand die Unterstützung für den Buderus
Logawater Soft WE800i aus [Issue #60](https://github.com/SoftwareSchmied/ha-bosch-buderus-heating/issues/60).
Grundlage sind v0.8.2-beta.4, der dort bereitgestellte Diagnoseexport und die
Ressourcenmodelle von MyBuderus 5.0.0. Die Diagnose bestätigt die erfolgreiche
Anmeldung und das erkannte Modell `watersoftener`, enthält aber noch keine
Enthärter-Messwerte. Die unten beschriebenen Funktionen sind deshalb noch
nicht an einem echten WE800i bestätigt.

### Erkennung und Anzeigen

Ein ausdrücklich erkanntes Enthärtermodell erhält die in der App belegten
Abfragen unter `/swCircuits/sw1`. Die Hardwarekennung WX100 allein reicht
dafür nicht aus. Weitere Kreise kommen ausschließlich aus gemeldeten
Referenzen. Deren Pfade haben Vorrang vor ergänzenden Abfragen. Die bekannten
Blattressourcen werden auch bei einem unlesbaren übergeordneten Verzeichnis
geprüft. Die Grenzen von 30 Pfaden je Batch, 512 Pfaden und acht Ebenen gelten
weiterhin, ebenso die gemeinsame Abfrage und die Cloud-Sperrzeiten.

Alle Entitäten bleiben unter dem vorhandenen Gateway-Gerät. Es entsteht kein
zusätzliches Gerät pro Enthärterkreis. Bestehende Heizungsentitäten und ihre
Kennungen werden nicht umbenannt.

| Pfad unter `/swCircuits/{sw}/` | Anzeige | Einheit und Bedeutung |
|---|---|---|
| `sensor/saltLevel` | Salzfüllstand | Prozent, nur 0 bis 100 |
| `sensor/saltLevelAlarm` | Salz-Warnschwelle | Prozent, nur 0 bis 100 |
| beide Salzressourcen | Salzvorrat niedrig | Füllstand kleiner oder gleich der gemeldeten Schwelle |
| `sensor/availableWater` | Verfügbares Weichwasser | Liter oder gemeldete Kubikmeter; Vorrat, kein Verbrauchszähler |
| `sensor/waterFlow` | Wasserdurchfluss | Liter pro Minute |
| `regeneration/enabled` | Regeneration aktiv | Nur `on` und `off` werden zu einem Binärzustand |
| `regeneration/phase` | Regenerationsphase | Sieben bekannte Phasen, deutsch und englisch übersetzt |
| `regeneration/totalProgressStatus` | Regenerationsfortschritt | Prozent, nur 0 bis 100 |
| `regeneration/totalRemainingTime` | Verbleibende Regenerationszeit | Gemeldete Zeiteinheit; ohne Einheit Sekunden gemäß App-Umrechnung |
| `regeneration/timeUntilNext` | Zeit bis zur nächsten Regeneration | Gemeldete Zeiteinheit; ohne Einheit Tage gemäß App-Modell `nextInDays` |
| `regeneration/singleRegAppoint` | Geplante Regeneration | Gemeldete Zeiteinheit; ohne Einheit Tage gemäß App-Modell `scheduleDays` |
| `holidayMode/enabled` | Urlaubsmodus | Eigener Zustand des Enthärters |

Fehlt bei Salzfüllstand, Schwelle, Fortschritt, Wasservorrat oder Durchfluss
die Einheit, verwende ich die jeweilige oben genannte App-Zuordnung. Eine
widersprüchliche ausdrücklich gemeldete Einheit wird abgewiesen.
Fehlende, ungültige und nicht endliche Werte ergeben keinen erfundenen
Nullwert. Eine ausgefallene Quelle wird nicht durch eine andere ersetzt.

Die Salzwarnung benötigt einen gültigen Füllstand und eine gültige aktuelle
Schwelle desselben Kreises. Den App-Ersatzwert von 20 Prozent übernehme ich
ohne Gerätebestätigung nicht. W006 bleibt ohne zusätzliche Bedeutungszuordnung.
Der separat in der App gefundene Code E7 ist kein Beleg für die Bedeutung von
W006 und ersetzt nicht die numerische Salzwarnung.

### Vorbereitete Bedienfunktionen

Die folgenden Bedienelemente sind standardmäßig deaktiviert. Für die
Freigabe steht noch die Bestätigung an einem echten Gerät aus. Sie erscheinen
nur bei passenden aktuellen Schreibrechten, Optionen und Grenzen.

| Bedienelement | Verhalten |
|---|---|
| Salz-Warnschwelle | Zahlenfeld mit den angebotenen Grenzen innerhalb von 0 bis 100 Prozent |
| Urlaubsmodus | Schalter für die angebotenen Codes `on` und `off` |
| Regeneration planen | Zahlenfeld in Tagen; Grenzen stammen vom Gerät |
| Regeneration starten | Eigene Taste für den belegten Befehl `on` |

Eine Schrittweite von 1 dient der Bedienung. Sie wird nicht zu einer
erfundenen Protokollgrenze. Gültige Zwischenwerte innerhalb der gemeldeten
Grenzen werden nicht aufgrund dieses Bedienhinweises abgewiesen.
Alle Schreibzugriffe verwenden die vorhandene gemeinsame Prüfung,
Serialisierung und Rücklesebestätigung. Ein Timeout führt zu keinem zweiten
Startbefehl. Eine Abbruchtaste für die Regeneration ist nicht freigegeben,
weil ein angebotener Code `off` allein keinen bestätigten Abbruchablauf belegt.

### Diagnose und noch nötige Bestätigung

Diagnose-Schema 16 nennt das erkannte Geräteprofil und die zusätzlichen
Abfragen. Pro Enthärterressource zeigt es Schemafehler, Einheit und die
Gültigkeit des Wertes, aber keinen Messwert oder unbekannten Zustandstext.
Zusätzlich unterscheide ich registrierte, deaktivierte, nicht geladene,
unbekannte und nicht verfügbare Entitäten. Namen und Entitäts-IDs werden nicht
exportiert. Unbekannte dynamische Kreiskennungen werden redigiert. Der Export verursacht
keine zusätzlichen Cloud-Anfragen.

Für die Gerätebestätigung werden ein frischer Diagnoseexport aus diesem
Entwicklungsstand sowie ein Vergleich der verfügbaren Anzeigen mit MyBuderus
benötigt. Schreibtests sollen anschließend einzeln erfolgen, mit dokumentierter
Einstellung, Ergebnis in MyBuderus und gegebenenfalls wiederhergestelltem
Ausgangswert. Eine manuell gestartete Regeneration ist ein realer Geräteablauf.

Der in Issue #60 gewünschte Weichwasserverbrauch ist damit noch nicht
vollständig abgedeckt: Die App bezieht Verbrauchswerte aus `/recordings`.
Ich berechne keinen vermeintlichen Gesamtverbrauch aus einzelnen
Durchflussmessungen. Das gesonderte optionale Verbrauchspaket und historische
Messreihen sind nicht Teil dieser Umsetzung. Issue #60 bleibt bis zur
Rückmeldung und Klärung dieses Umfangs offen.

## English

I am adding an initial WE800i implementation based on v0.8.2-beta.4, the
diagnostics in issue #60 and MyBuderus 5.0.0 resource models. The supplied
diagnostics confirm gateway discovery, but do not contain softener readings.
APK findings and synthetic tests are not physical-device verification.

Explicit softener models receive the documented `/swCircuits/sw1` probes.
Additional circuit IDs must be advertised. References retain priority; an
unreadable parent does not suppress known leaf probes. Shared polling,
backoff, the 30/512/8 discovery limits and one HA device per gateway remain.

Current capabilities cover salt level and threshold, derived low salt,
available soft-water volume, flow, regeneration state/phase/progress/time,
scheduled regeneration and holiday state. Unknown values remain unknown.
Available water is a volume-storage measurement, not cumulative consumption.
Unitless next/scheduled regeneration values use the app's explicit days
semantics. Unitless remaining regeneration time uses seconds, matching the app conversion to minutes.
The 20% alarm fallback is not assumed. W006 is not mapped to E7 or low salt.

Prepared controls cover the salt threshold, holiday switch, regeneration
delay in days and a separate regeneration start button. They are disabled by
default pending device verification. Current rights, options and bounds are
required; UI steps do not invent API restrictions. Writes use the shared
transaction and read-back. A timed-out command is not resent. Cancellation
is not offered without a verified command contract.

Diagnostics schema 16 records profiles, local entity registration and capability validation without
measurements, unknown texts, credentials or private dynamic IDs. It adds no
cloud calls. Actual display comparison, interruption/recovery checks and
individual write confirmation in MyBuderus remain outstanding. Consumption
from `/recordings` remains a separate optional package; issue #60 is not
considered closed by this initial implementation.

## Evidence references

- MyBuderus base APK SHA-256:
  `a274242b55d467997b67322492ddee80f17b0a25f2762fa874ca03330550c1ec`.
- `watersoftenerprovider.data.remote.resources`: `WaterSoftenerSensorResource`,
  `WaterSoftenerRegenerationResource`, `WaterSoftenerHolidayResource`.
- `WaterSoftenerModelMapperImpl`: model families, numeric low-salt comparison,
  separate E7 handling and conversion to the public regeneration models.
- `NextRegeneration`: `nextInDays` and `scheduleDays` distinguish day offsets
  from clock times. `RegenerationPhase` defines seven named phases.
- `HppDemoDevice` confirms app-side scalar shapes and selected units. Demo
  values and limits are not used as appliance defaults or copied into Git.
- [App resource implementation inventory](app-resource-inventory.md).

- The operation screen divides remaining regeneration time by 60 before passing
  it to TimerUtils, which constructs a duration in minutes. This establishes
  seconds as the app-side default for an omitted unit.

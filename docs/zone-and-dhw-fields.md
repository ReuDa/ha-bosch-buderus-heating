# Zusätzliche Raumzonen- und Warmwasseranzeigen

Ich habe die MyBuderus-Ressourcenmodelle mit dem vorhandenen Katalog
abgeglichen. Für Raumzonen fehlten die ausgeschriebenen Pfadbestandteile
`heating` und `cooling`. Die bisherigen `heat`, `cool` und `heatCool`
bleiben unterstützt und behalten ihre bestehenden Kennungen.

| Neue Pfade | Darstellung |
|---|---|
| `/zones/{zone}/heating/manualRoomSetpoint` | Manueller Heizsollwert |
| `/zones/{zone}/heating/temporaryRoomSetpoint` | Vorübergehender Heizsollwert |
| `/zones/{zone}/heating/operationMode` | Heizbetriebsart |
| `/zones/{zone}/cooling/manualRoomSetpoint` | Manueller Kühlsollwert |
| `/zones/{zone}/cooling/temporaryRoomSetpoint` | Vorübergehender Kühlsollwert |
| `/zones/{zone}/cooling/operationMode` | Kühlbetriebsart |
| `/dhwCircuits/{dhw}/dhwType` | Warmwasser-Gerätetyp, standardmäßig deaktiviert |

Die Temperaturfelder benötigen `floatValue` mit Einheit `C`, die
Betriebsarten und der Gerätetyp benötigen `stringValue`. Fehlende Werte,
Fehlermarker, ungültige Formen und nachträglich unpassende Einheiten liefern
keinen Messwert. Veraltete Quellen werden nicht als aktuelle Anzeige verwendet.
Heizen und Kühlen erhalten unterscheidbare deutsche und englische Namen.

Die zusätzlichen Suchpfade entstehen nur für bereits gemeldete Komponenten:
höchstens sechs weitere Pfade je Raumzone und einer je Warmwasserkreis.
Sie verwenden das bestehende Discovery-Budget und die gemeinsamen Abfragen.
Der statische Gerätetyp wird nach der Erkennung nicht regelmäßig abgefragt.
Es entstehen weder zusätzliche Gateway-Geräte noch neue Schreibfunktionen.

Nachweis: MyBuderus 5.0.0, `ConnectKeyZonesResource.Heating/Cooling`
und `ConnectKeyDhwCircuitResource.DhwType`, einschließlich der lokalen
Zuordnung zu Zahlen- beziehungsweise Textwerten. Die automatisierten Tests
verwenden synthetische Antworten. Eine Bestätigung an diesen Raumzonen
oder Warmwasser-Gerätetypen steht noch aus.

Der erweiterte Ressourcenindex enthält auch die dynamischen RRC-Programm-
und Zonenpfade. Das belegt deren Pfadaufbau, noch keinen passenden Adapter
oder fertigen Parser. Verzeichnisse und administrative Funktionen werden
gesondert eingeordnet.

## English

I added the explicit `heating` and `cooling` zone resource variants and
the DHW device-type reading identified in MyBuderus 5.0.0. Existing shorter
variants and entity identities remain unchanged. Temperature readings require
numeric Celsius resources; modes and the device type require scalar strings.
Every update validates the current schema and value, and stale readings
become unavailable. Heating and cooling use distinct localized names.

Only reported components receive optional probes: six additional paths per
zone and one per DHW circuit, within the existing shared budgets and polling.
The device type is disabled by default and does not cause regular polling.
No write functions or extra gateway devices are added. Synthetic tests cover
schema changes, missing/invalid values, recovery and gateway isolation.
Physical-device verification remains outstanding.

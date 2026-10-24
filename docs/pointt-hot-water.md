# PointT hot water

## English

I added one native Home Assistant water-heater entity per discovered PointT
hot-water circuit. It combines the measured water temperature, the active
setpoint reported by the appliance and the operating mode. It stays on the
existing appliance device and can be used on the device page or a dashboard.

The readings come from that circuit's `actualTemp` and `currentSetpoint`.
Missing or invalid readings remain unknown. I do not substitute the extra
hot-water target, an Eco/Comfort start temperature or another circuit's reading.
Reported Celsius, Fahrenheit and Kelvin values are converted to Home
Assistant's display unit.

The active setpoint is an **indication, not a temperature control**. The
existing supported commands do not directly set `currentSetpoint`.
The individually adjustable `temperatureLevels` are start thresholds; they
remain under **Operate appliance** and in the existing number entities.
A `water_heater.set_temperature` call cannot change those thresholds, start an
extra charge or switch an operating mode. No artificial control limits or step
size are advertised.

Home Assistant's standard more-info dialog shows the current temperature and
mode without a target-temperature control. The read-only target is available
as the entity's `temperature` attribute. A standard tile can show all three
values; replace the example entity ID with the one from your installation:

```yaml
type: tile
entity: water_heater.your_hot_water_circuit
state_content:
  - state
  - current_temperature
  - temperature
```

Tapping the tile opens the native operating-mode dialog.

### Operating modes

Only understood codes actually offered by the circuit are selectable. The
labels follow the existing PointT selectors and the user's profile language.

| PointT code | English | German |
| --- | --- | --- |
| `Off` | Off | Aus |
| `low` | Eco | Eco |
| `high` | Comfort | Komfort |
| `ownprogram` | Auto | Auto |
| `eco` | Eco+ | Eco+ |
| `HCprogram` | Follow heating schedule | Heizungszeitprogramm folgen |

A read-only operating mode can still be displayed. A missing or unknown
current mode makes the combined entity unavailable. Additional offered codes
remain accessible through the existing select entity under its own contract.
I do not infer heating activity, charging, disinfection or holiday status from
the selected operating mode or from a temperature difference.

### Requests, continuity and validation

Creating and displaying the entity uses cached discovery/polling results.
It adds no discovery paths, polling intervals or regular cloud requests.
Before a mode write, I reread and compare its value and metadata. I use the
existing serialized write transaction with mandatory read-back. A usual change
uses one preflight GET, one PUT and one confirming GET. Existing bounded
read-back retries and account pauses still apply; an uncertain result does
not resend the PUT.

Confirming a mode write does not confirm its resulting setpoint. The combined
entity therefore hides an older setpoint until a regular reading arrives.
Failed or unconfirmed mode writes leave the mode unavailable until recovery
through regular polling.

New entities can appear during polling when their required data becomes usable.
Their identity includes the exact gateway and circuit. Existing sensors,
number controls, select IDs, custom names, disabled states and device
assignments remain intact. The original mode select moves to Configuration,
where it remains available for individual use and existing automations.

Tests cover exact circuit routing, mode subsets, unknown codes, stale/invalid
readings, display units, failed writes, recovery and real Home Assistant
service/registry behavior. These are software tests with synthetic devices;
this change has not been installed or write-tested on a physical appliance.
I also tested the native dialog and the tile above in Home Assistant's browser
frontend in German and English, including a mobile viewport, mode changes,
updated readings and closing with Escape.

## Deutsch

Ich habe für jeden entdeckten PointT-Warmwasserkreis eine gemeinsame
Warmwasserentität ergänzt. Sie zeigt die gemessene Temperatur, den von der
Anlage gemeldeten aktuellen Sollwert und die Betriebsart. Sie bleibt beim
bisherigen Anlagengerät und lässt sich auf der Geräteseite oder in einem
Dashboard verwenden.

Die Temperaturen stammen aus `actualTemp` und `currentSetpoint` desselben
Warmwasserkreises. Fehlende oder ungültige Werte bleiben unbekannt.
Extra-Warmwasser-Sollwert, Starttemperaturen und Werte anderer Kreise dienen
nicht als Ersatz. Die Anzeige berücksichtigt die eingestellte Temperatureinheit.

Der aktuelle Sollwert ist eine **Anzeige ohne direkten Temperaturregler**.
Über die bisher unterstützten Befehle lässt sich `currentSetpoint` nicht direkt
einstellen. Die getrennten Starttemperaturen für Eco, Eco+ und Komfort bleiben
unter **Anlage bedienen** und in den vorhandenen Zahlenentitäten einstellbar.
Ein Temperaturbefehl an die neue Entität verändert weder diese Schwellen noch
die Betriebsart und startet auch keine Extra-Warmwasserbereitung.

Der Standarddialog von Home Assistant zeigt Isttemperatur und Betriebsart.
Der nur lesbare Sollwert steht im Attribut `temperature` zur Verfügung.
Das oben gezeigte Beispiel für eine normale Dashboard-Kachel zeigt alle drei
Angaben gemeinsam. Dafür muss lediglich die Beispiel-Entitäts-ID ersetzt werden.

Die Tabelle oben zeigt die Betriebsarten und ihre deutschen Beschriftungen.
Auswählbar sind nur bekannte Optionen, die der jeweilige Kreis tatsächlich
anbietet und schreiben lässt. Eine nur lesbare Betriebsart bleibt sichtbar.
Eine fehlende oder unbekannte aktuelle Betriebsart macht die gemeinsame
Entität nicht verfügbar. Weitere angebotene Codes bleiben über das bisherige
Auswahlfeld erreichbar. Aus der gewählten Betriebsart wird keine aktive
Aufheizung, Desinfektion oder Abwesenheit abgeleitet.

Die neue Anzeige nutzt vorhandene Daten und erzeugt keine zusätzlichen
regelmäßigen Cloud-Abfragen. Vor einem Betriebsartenwechsel prüfe ich den
aktuellen Wert und die Metadaten erneut. Ein üblicher Wechsel benötigt einen
Prüfabruf, einen Schreibzugriff und einen bestätigenden Abruf. Die bisherigen
begrenzten Rückleseversuche und Abfragepausen bleiben erhalten.

Nach einem bestätigten Betriebsartenwechsel bleibt ein älterer Sollwert in
dieser Entität vorübergehend ausgeblendet, bis ein regulärer Abruf den aktuellen
Wert liefert. Ein fehlgeschlagener oder unbestätigter Schreibzugriff wird nicht
als Erfolg angezeigt. Die Wiederherstellung erfolgt beim regulären Polling.

Neue Entitäten können beim Polling hinzukommen. Bestehende IDs, eigene Namen,
deaktivierte Entitäten und Gerätezuordnungen bleiben erhalten. Das ursprüngliche
Betriebsartenfeld steht unter Konfiguration weiterhin zur Verfügung.

Automatisierte Tests prüfen Datenzuordnung, Einheiten, Übersetzungen,
Schreibfehler, Wiederherstellung und die Home-Assistant-Dienste. Eine Installation
und reale Schreibtests dieses neuen Stands an der Anlage stehen noch aus.
Zusätzlich habe ich den nativen Dialog und die oben gezeigte Kachel im
Home-Assistant-Frontend auf Deutsch und Englisch geprüft, einschließlich
Mobilansicht, Betriebsartenwechsel, aktualisierter Werte und Schließen mit Escape.

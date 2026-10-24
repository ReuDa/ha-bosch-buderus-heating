# Heating controls

## English

I added **Settings > Devices & services > Bosch/Buderus Heating > Configure >
Operate appliance**. When an entry contains several PointT gateways, I ask
which appliance to operate first. The dialog groups the discovered controls
into heating circuit, hot water and system tabs. Additional temperature
levels and technical settings are under **More settings**.

Editing a field changes a draft. **Apply** validates all submitted values
before writing, then confirms each changed setting by reading it back.
**Discard** restores the values displayed when the form opened.
**Reload values** discards the draft and uses the latest regular polling
results. Opening, editing and reloading the dialog do not query the cloud.
German and English labels follow the user's profile language.

Before each write, I also reread the relevant resource and reject a draft
if its value or metadata has changed. Writes are serialized with polling and
other integration writes. This check cannot make cloud writes atomic:
another controller can still act between a read and a write. Multiple
settings are separate transactions. On failure, confirmed earlier changes
remain applied and the last attempted change may have an uncertain outcome.
The dialog explains this and retains the remaining draft.

On the device page, I use shorter control names, relevant icons and number
inputs instead of sliders. Home Assistant controls the page layout.
Existing entity IDs, unique IDs, custom names, disabled states, history and
device assignments remain intact. A new installation may generate shorter
default entity IDs from the new names. No registry migration is needed.
Controls on the device page still write individually when edited.
The original heating-circuit mode and manual-target controls are under
Configuration; the climate is the combined everyday control.

### Heating-circuit climates

I add one climate entity per eligible, discovered PointT heating circuit.
Its identity uses the gateway and the exact circuit key, including HC2 and
later circuits. It remains on the existing appliance device. Climate entities
can appear during regular polling when the necessary metadata becomes available.
The original number and select entities remain usable by existing automations.

The supported PointT codes map as follows:

| PointT | Home Assistant | Temperature |
| --- | --- | --- |
| `manual` | Heat | Reads and writes `manualRoomSetpoint` |
| `auto` | Auto | Reads `currentRoomSetpoint`; temperature changes disabled |
| `off` | Off | No temperature command |

Only advertised, understood codes appear. An unknown current mode makes
the climate unavailable; the original select retains additional advertised
codes. A temperature call never changes a mode. Combined mode/temperature
calls are rejected before any write; select the mode separately first.
Bounds and units come from that circuit. I convert temperatures and steps
between the reported unit and Home Assistant's configured unit.

I show room temperature only from that circuit's valid `roomtemperature`
resource. I do not substitute a flow temperature, infer active heating from
a temperature difference or claim that a winter-mode flag proves heat output.
No heating-action state is invented.

Cooling is outside this climate implementation. A reported cooling-only
circuit, active cooling or stale/unknown heating context makes the climate
unavailable. Existing individual controls remain available under their own
contracts. The mode, target and known heating context are checked again on
the appliance before a climate write. Scheduling, temporary overrides and
cooling setpoints are not changed by this climate.

Automated tests and a local browser harness cover the implementation.
Installation in the user's Home Assistant and real appliance writes remain
separate validation steps.

## Deutsch

Ich habe **Einstellungen > Geräte & Dienste > Bosch/Buderus Heating >
Konfigurieren > Anlage bedienen** ergänzt. Bei mehreren PointT-Gateways
erscheint zuerst eine Anlagenauswahl. Reiter trennen die erkannten Heizkreise,
Warmwasser und die Anlage. Weitere Temperaturstufen und technische
Einstellungen stehen unter **Weitere Einstellungen**.

Eingaben bleiben zunächst ein Entwurf. **Übernehmen** prüft alle Eingaben,
schreibt die geänderten Einstellungen und bestätigt jede durch Rücklesen.
**Verwerfen** stellt die beim Öffnen angezeigten Werte wieder her.
**Werte neu laden** verwirft den Entwurf und verwendet die Ergebnisse der
regulären Abfragen. Öffnen, Bearbeiten und Neuladen lösen keine Cloud-Abfrage
aus. Die Texte folgen der Profilsprache.

Vor jeder Änderung lese ich die betreffende Ressource erneut. Geänderte
Werte oder Metadaten führen zum Abbruch. Schreiben und Polling der Integration
laufen dabei nacheinander. Andere Steuerungen können trotzdem zwischen
Rücklesen und Schreiben eingreifen. Mehrere Einstellungen werden einzeln
geschrieben. Bei einem Fehler bleiben bereits bestätigte Änderungen wirksam;
die zuletzt versuchte Änderung kann bereits übernommen worden sein.
Der Dialog erklärt das und erhält die verbleibenden Eingaben.

Die Geräteseite erhält kürzere Namen, passende Symbole und Zahlenfelder.
Die Anordnung bestimmt Home Assistant. Bestehende Entitäts-IDs, eindeutige
Kennungen, eigene Namen, Deaktivierungen, Historien und Gerätezuordnungen
bleiben erhalten. Bei einer neuen Installation können aus den kürzeren Namen
auch kürzere Standard-Entitäts-IDs entstehen. Eine Registry-Migration ist
nicht erforderlich. Änderungen auf der Geräteseite werden weiterhin einzeln
geschrieben.
Die bisherigen Einzelregler für Heizkreis-Betriebsart und manuellen Sollwert
stehen unter Konfiguration. Die Klimaentität übernimmt die gemeinsame
Alltagsbedienung.

### Klimaentitäten der Heizkreise

Jeder geeignete, tatsächlich erkannte Heizkreis erhält eine Klimaentität
am bisherigen Anlagengerät. Die Kennung enthält Gateway und Kreisschlüssel.
Auch HC2 und später während des Pollings erkannte Fähigkeiten werden
berücksichtigt. Bestehende Einzelentitäten bleiben für Automationen nutzbar.

| PointT | Home Assistant | Temperatur |
| --- | --- | --- |
| `manual` | Heizen | Manuellen Sollwert lesen und ändern |
| `auto` | Automatisch | Aktuellen Sollwert anzeigen, keine Temperaturänderung |
| `off` | Aus | Kein Temperaturbefehl |

Nur angebotene, verstandene Codes werden zugeordnet. Bei unbekannter
aktueller Betriebsart ist die Klimaentität nicht verfügbar. Die ursprüngliche
Auswahl bietet weiterhin zusätzliche gemeldete Codes an.
Temperaturbefehle wechseln niemals die Betriebsart. Kombinierte Befehle für
Betriebsart und Temperatur werden vor dem Schreiben abgewiesen.
Grenzen und Einheiten stammen aus dem jeweiligen Heizkreis.

Die Raumtemperatur stammt ausschließlich aus einem gültigen
`roomtemperature`-Messwert dieses Kreises. Vorlauftemperaturen werden nicht
ersatzweise verwendet. Ein aktives Heizen wird nicht aus Temperaturen oder
der Sommer-/Winterumschaltung abgeleitet.

Kühlen gehört nicht zum Umfang dieser Klimaentität. Bei gemeldetem
Kühlbetrieb, einem reinen Kühlkreis oder veralteten beziehungsweise unbekannten
Angaben zum Heiz-/Kühlbetrieb wird sie nicht verfügbar. Die Einzelentitäten
bleiben nach ihren eigenen Regeln nutzbar. Vor einem Klimabefehl werden
Betriebsart, Sollwert und bekannte Angaben zum Heiz-/Kühlbetrieb erneut
gelesen. Zeitprogramme, temporäre Sollwerte und Kühlsollwerte bleiben erhalten.

Automatisierte Tests und eine lokale Browserprüfung prüfen die Umsetzung.
Die Installation in Home Assistant und reale Schreibtests an der Anlage
stehen als eigene Prüfschritte aus.

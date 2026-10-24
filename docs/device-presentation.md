# Home Assistant device presentation

The shared-device decision below remains in effect. The later
[heating controls](heating-controls.md) add climate entities to that same device
and shorten control labels; the original entity identities remain intact.

Die folgende Entscheidung für ein gemeinsames Anlagengerät gilt weiterhin.
Die später ergänzte [Heizungsbedienung](heating-controls.md) fügt Klimaentitäten
am selben Gerät hinzu und verkürzt die Beschriftungen der Bedienelemente.
Die bestehenden Entitätskennungen bleiben erhalten.

## English

I reviewed the option of splitting heating circuits, hot water and heat
sources into additional Home Assistant devices. I chose to keep one shared
device per PointT heating gateway. This is a presentation decision, not a
discovery defect or a claim that a heating circuit is a separate appliance.

Related entities remain recognizable by their default name prefixes, such as
Heating circuit 1, Hot water 1 and Heat generator 1. The integration uses
reported circuit identities and configured circuit names where available.
Custom entity names in Home Assistant continue to take precedence. Several
gateways remain separate even if their local circuit numbers are identical.

This decision does not add, remove or move entities. Existing entity IDs,
unique IDs, history, disabled states, user names, areas, labels and device
references stay as they are. There is no new registry migration or layout
option. The existing compatibility migrations for older previews remain.

An entity can still be assigned to its own Home Assistant area when a circuit
needs a different area from the shared device. Such an explicit entity area
overrides the device area; the integration does not set those overrides.
Dashboard cards can group entities without changing their device assignment.

Shared system readings, notifications, holiday calendars and derived values
stay associated with the gateway as before. Account-wide request statistics
remain independent of a particular device. A central heat-source reading is
not automatically attributed to one generator merely because only one
generator currently appears in discovery.

Independent appliances connected through the additional cloud adapter, and
separate PointT wallboxes, keep their own device identities. The decision
does not merge those appliances into the heating gateway.

### If a split is considered later

Additional devices would primarily offer separate device pages and device
area assignments. They would not discover additional resources or add new
measurements. Logical circuits must be labelled as logical parts, with stable
identities based on the gateway and reported circuit key.

A future implementation needs an explicit, reversible assignment migration.
Preserving entity IDs alone is insufficient: actions targeting a device can
select a different entity set after a split, and inherited areas or labels
may change. The parent link between devices does not automatically transfer
the parent's area, labels or automation targets. A migration must explain
these effects, preserve user changes and handle temporary device absence.

No split or migration has been implemented as part of this decision.

## Deutsch

Ich habe geprüft, ob Heizkreise, Warmwasser und Wärmeerzeuger als zusätzliche
Home-Assistant-Geräte übersichtlicher wären. Ich behalte ein gemeinsames
Gerät je PointT-Heizungs-Gateway bei. Das ist eine Darstellungsentscheidung
und kein Discovery-Fehler. Ein Heizkreis wird dadurch nicht als eigenständiges
physisches Heizgerät eingeordnet.

Zusammengehörige Entitäten bleiben über ihre Standardnamen erkennbar, etwa
Heizkreis 1, Warmwasser 1 und Wärmeerzeuger 1. Die Integration verwendet die
gemeldeten Kreiskennungen und vorhandene konfigurierte Kreisnamen.
Eigene Entitätsnamen in Home Assistant haben weiterhin Vorrang. Mehrere
Gateways bleiben getrennt, auch wenn ihre lokalen Kreisnummern gleich sind.

Diese Entscheidung fügt keine Entitäten hinzu, entfernt keine und ordnet
keine einem anderen Gerät zu. Entitäts-IDs, eindeutige Kennungen, Historie,
Deaktivierungen, eigene Namen, Bereiche, Labels und Geräteverweise bleiben
erhalten. Es gibt keine neue Migration und keine zusätzliche Ansichtsoption.
Vorhandene Kompatibilitätsmigrationen für ältere Vorabstände bleiben bestehen.

Eine Entität kann in Home Assistant weiterhin einen eigenen Bereich erhalten,
wenn ihr Heizkreis zu einem anderen Bereich als das gemeinsame Gerät gehört.
Dieser ausdrücklich gesetzte Entitätsbereich hat Vorrang vor dem Gerätebereich.
Die Integration setzt solche Zuordnungen nicht selbst. Auch Dashboard-Karten
können Entitäten gruppieren, ohne ihre Gerätezuordnung zu verändern.

Übergreifende Anlagenwerte, Meldungen, Urlaubskalender und abgeleitete Werte
bleiben wie bisher dem Gateway zugeordnet. Kontoweite Anfragestatistiken
gehören weiterhin zu keinem einzelnen Gerät. Ein allgemeiner
Wärmeerzeugerwert wird nicht allein deshalb einem bestimmten Erzeuger
zugerechnet, weil gerade nur ein Erzeuger entdeckt wurde.

Eigenständige Geräte des zusätzlichen Cloud-Zugangs und separate
PointT-Wallboxen behalten ihre eigenen Gerätekennungen. Die Entscheidung
führt diese Geräte nicht mit dem Heizungs-Gateway zusammen.

### Falls eine Aufteilung später gewünscht wird

Zusätzliche Geräte würden vor allem eigene Geräteseiten und getrennte
Bereichszuordnungen auf Geräteebene ermöglichen. Sie würden keine weiteren
Ressourcen finden und keine neuen Messwerte hinzufügen. Logische Kreise
müssten als solche bezeichnet werden. Ihre stabilen Kennungen müssten aus
Gateway und gemeldetem Kreisschlüssel entstehen.

Eine spätere Umsetzung benötigt eine ausdrückliche, umkehrbare Migration
der Zuordnungen. Entitäts-IDs allein zu erhalten reicht nicht aus:
Gerätebezogene Aktionen können nach einer Aufteilung andere Entitäten
ansprechen. Geerbte Bereiche und Labels können sich ebenfalls verändern.
Die Verknüpfung mit einem übergeordneten Gerät überträgt dessen Bereich,
Labels oder Automationsziele nicht automatisch. Eine Migration muss diese
Auswirkungen erklären, Benutzereinstellungen bewahren und vorübergehend
fehlende Geräte berücksichtigen.

Mit dieser Entscheidung ist keine Aufteilung oder Migration umgesetzt worden.

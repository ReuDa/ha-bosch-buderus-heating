# Additional cloud devices: connection foundation

I added a separate Bacon connection for devices listed by the account's
claiming service. The implementation in v0.8.2-beta.6 supplies device
selection, MQTT status and a diagnostic connection entity. Midea/RWH controls and readings are now described in the separate
[water-heater package](bacon-water-heaters.md). Beta.6 also covers
[Midea Climate Series](bacon-air-conditioners.md) and
[seven Air purifier families](bacon-air-purifiers.md) and
[three Dry dehumidifier families](bacon-dehumidifiers.md), with individual scope
and outstanding physical-device checks. Other family packages remain open.
Water heaters, air conditioners, air purifiers and dehumidifiers are not yet
advertised as fully supported.

## Setup and separation

Discovery uses the existing SingleKey ID authorization only when its granted
scope includes Bacon. During operation, both connections share the same token
manager, including serialized refresh and token persistence.

Setup offers gateways and additional devices separately. A Bacon-only account
can be configured. Only returned, explicitly selected identifiers are used.
Entity identities combine a separate namespace with a hash of account subject
and device identifier. PointT identities and settings remain unchanged.
New devices require Reconfigure and explicit selection.

Each selected device receives **Device connection**. An explicit live offline
message shows disconnected. Missing current observations, removed membership
or a connection loss make this entity unavailable.

## Transport contract

| Operation | Contract |
| --- | --- |
| Account devices | HTTPS GET https://claiming.euc1.bacon.bosch-tt-cw.com/v1/users/self/devices, returning a list of identifiers |
| Authentication | Bearer access token for HTTPS and the WebSocket upgrade |
| Broker | broker.euc1.bacon.bosch-tt-cw.com:443, TLS certificate validation, WebSocket /mqtt, MQTT 5 |
| MQTT credentials | Token subject as username, access token as password |
| Client identifier | 64 hexadecimal characters from SHA-256 over a random UUID's bytes |
| Subscription | users/{subject}/#, QoS 1 |
| Device information | users/{subject}/devices/{device}/topics/info |
| Opaque metadata and sensor messages | Same device prefix with topics/meta and topics/sensor |
| Read state | Empty payload to shadows/state/get; response on shadows/state/get/accepted |
| Request change | {"state":{"desired":{...}}} to shadows/state/update |
| Confirmation | Newer accepted shadow containing the requested values in state.reported |
| Rejection | State get/update rejected topics, or MQTT/HTTP failure |

The client identifier format was checked with the real service. An arbitrary
text identifier was rejected with reason 135. The documented format connected
with the same account. No embedded application secrets are needed.

Token rotation renews the connection. Each connection uses a fresh MQTT client
without an outgoing command queue from an earlier session. Authentication
errors request renewed sign-in. Connection failures back off. Quota errors wait
at least 60 seconds; a longer numeric Retry-After is honored. Configuration
retry dialogs enforce their wait too.

Membership and state resynchronize every five minutes. Token checks and
availability updates run every minute. These are integration policies, not
vendor limit claims. Bounds are 128 devices, 128 KiB per message, 16 JSON nesting
levels and an incoming queue of 256 messages.

## State and write rules for family adapters

The P08 foundation stores metadata and sensor objects without assigning units
or controls; P09 interprets the admitted water-heater families and P10 adds
[identified Midea Climate Series devices](bacon-air-conditioners.md). The family adapter must establish their meanings and validate
requested fields against current metadata.

The information timestamp is used only for ordering. Its epoch unit is not
established by P08. Connection status requires a non-retained information
update and expires after 15 minutes without a newer one. Retained information,
duplicate timestamps, sensor caches and cloud shadow reads do not establish
physical connectivity. This conservative rule needs real-device validation.

Sensor envelopes contain an optional deviceType and an items array. Each
item has its own integer timestamp. The newest unambiguous item extends
non-null fields in the current sample. Empty, retained and old messages do
not refresh readings. Each field retains its own observation time.

Shadows require integer version and timestamp fields and an object state.
A full get response replaces the reported snapshot; update responses merge
non-null reported fields. Desired-only acknowledgements preserve reported
values and do not refresh them or confirm writes. Each changed requested
field needs a newer reported observation. Duplicate updates cannot extend
its freshness. A full get can refresh unchanged fields and resolve uncertainty.
Conflicting observations of the same field at the same version are rejected.
Old and retained responses cannot confirm commands. New connections cannot
combine partial reports with cached fields from the previous connection.

Each internal write acquires a device lock, reads state and checks current
connectivity. Pending desired changes block another write. A mandatory family
validator checks permitted options and limits. An already reported requested
value causes no further command.

A PUBACK or accepted desired value is insufficient. A newer reported state
must match the request on the same connection. Rejection, removal, offline
status, cancellation or timeout leaves the outcome unconfirmed. No blind
retransmission follows. A regular read can clear uncertainty. Family adapters
must check state generation and the uncertainty flag before displaying
confirmed values.

No server compare-and-swap or client transaction token has been established.
The check confirms convergence to the requested state, not exclusive ownership
of the change. An external controller can still intervene. No generic Home
Assistant write service is exposed.

## Diagnostics and validation

Schema 21 adds aggregate connection, availability, received-state and metadata
counts, error categories and unconfirmed-command counts. It exports no token,
subject, identifier, model, sensor contents, network information or device name.
Diagnostics cause no cloud requests.

On 24 October 2026 I checked the actual account device-list request
(HTTP 200, empty list), MQTT authentication, subscription and clean disconnect.
I published no MQTT messages. The account has no Bacon device, so real-device
messages and physical writes remain untested.

Automated tests exercise real HTTP requests, the real aiomqtt MQTT 5 codec
against a local WebSocket broker, mixed and Bacon-only setup, token sharing,
identity preservation, redaction, ordering, timeouts and write confirmation.
All device examples in those tests are synthetic.

## Deutsch

Ich habe eine getrennte Bacon-Verbindung für weitere Cloud-Geräte ergänzt.
Die Umsetzung in v0.8.2-beta.6 bietet Geräteauswahl, Verbindung
und **Geräteverbindung** als Diagnoseentität. Midea/RWH-Anzeigen und Bedienung
sind inzwischen im [Warmwasserpaket](bacon-water-heaters.md) ergänzt.
Weitere Familien bleiben offen. Warmwassergeräte, Klimageräte, Luftreiniger
und Luftentfeuchter sind dadurch noch nicht vollständig unterstützt.

Ich verwende die vorhandene SingleKey-ID-Anmeldung mit passender Berechtigung
und dieselbe gesicherte Token-Erneuerung. Gateways und weitere Geräte bleiben
getrennt. Auch ein Konto ausschließlich mit weiteren Geräten ist möglich.
Nur gemeldete und ausdrücklich ausgewählte Kennungen werden übernommen.
Bestehende PointT-Entitäten behalten ihre Identität. Weitere Geräte können
über Neukonfigurieren ausgewählt werden.

Die Verbindung nutzt MQTT 5 über einen TLS-gesicherten WebSocket. Die
Verbindungskennung besteht aus 64 hexadezimalen Zeichen, gebildet aus
SHA-256 über zufällige UUID-Bytes. Nach einem Abbruch wird ein neuer Client
angelegt. Alte ausgehende Befehle werden nicht übernommen. Bei Anmeldefehlern
wird eine neue Anmeldung angefordert. Anfragelimits und Wartezeiten gelten
auch bei Fehlern. Geräteliste und Zustand werden alle fünf Minuten abgeglichen.
Die Grenzen von 128 Geräten, 128 KiB pro Nachricht, 16 JSON-Ebenen und
256 eingehenden Nachrichten sind eigene Schutzgrenzen.

Für die Geräteverbindung benötige ich eine nicht gespeicherte
Informationsmeldung. Eine ausdrückliche Offline-Meldung zeigt getrennt.
Nach 15 Minuten ohne neue Meldung, bei Geräteentfernung oder einem
Verbindungsabbruch wird die Anzeige nicht verfügbar. Die Einheit des
Informationszeitstempels ist noch nicht belegt. Ich verwende ihn deshalb
nur für die Reihenfolge. Gespeicherte Meldungen beweisen keinen aktuellen
Gerätezustand. Diese vorsichtige Regel benötigt noch eine Geräteprüfung.

Die interne Schreibgrundlage prüft Zustand, offene Änderungen und eine
verpflichtende Prüfung durch den jeweiligen Geräteadapter. Erst ein neuerer
gemeldeter Zustand mit den gewünschten Werten bestätigt das Ergebnis.
Eine reine Empfangsbestätigung genügt nicht. Bei unklarem Ausgang erfolgt
kein zweiter Befehl. Ohne belegte serverseitige Konfliktsperre können
gleichzeitige Änderungen durch andere Bedienungen nicht vollständig
ausgeschlossen werden. Es gibt keinen allgemeinen Schreibdienst.
Die Adapter müssen Verbindungsstand und unbestätigte Ergebnisse beachten.

Diagnose-Schema 21 ergänzt ausschließlich Zähler und Fehlerkategorien.
Zugangsdaten, Gerätekennungen, Namen, Netzwerkdaten und Anlagenwerte bleiben
ausgeschlossen. Die Diagnose erzeugt keine zusätzlichen Anfragen.

Am 24.10.2026 habe ich die Geräteliste mit HTTP 200 und anschließend Anmeldung,
Abonnement und Trennung am echten Broker geprüft. Die Geräteliste war leer.
Ich habe dabei keine MQTT-Nachricht veröffentlicht. Reale Gerätemeldungen und
Schreibtests stehen aus. Die automatisierten Geräteprüfungen verwenden
ausdrücklich synthetische Daten.

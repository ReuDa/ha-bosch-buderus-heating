# Project specification status

This document tracks the incremental implementation of the externally stored
project specification. The source specification itself is intentionally not
part of this repository. The status reflects implemented and verified code,
not merely planned architecture.

Status updated on **2026-10-25**. The published releases and the newer,
locally tested development work are listed separately below.

## Current beta: 0.8.2-beta.6

**This beta contains substantial changes and needs careful field testing.**
I added device families and native Home Assistant entity types and reworked
connections, discovery, freshness and conversions. I recommend a full backup
before updating. Version **0.8.1 remains Stable/Latest**.

The Beta.6 release passed 3,036 automated cases with 96.83% combined
statement and branch coverage. Ruff, formatting, strict Mypy, reproducible
packaging and an isolated ZIP import passed. Diagnostics use schema 27.
These software results do not establish physical-device behavior.

## Unreleased development since Beta.6

The following work is implemented in PRs #85 to #87 but is not part of a
published release:

- [Heating controls](heating-controls.md): a tabbed **Operate appliance** dialog,
  Apply/Discard, permanently visible additional settings, and Escape including
  after form updates. The device page uses input fields and PointT climates.
- [PointT hot water](pointt-hot-water.md): a combined measured-temperature,
  active-target and operating-mode entity on the existing appliance device.
  The active target is read-only; the separate start temperatures retain their
  own controls.
- [Connection recovery](connection-recovery.md): shared token refresh survives
  cancelled callers and reloads, rejected refresh tokens are not repeatedly
  sent, and OAuth request limits use the existing account pause.

The code checkpoint passed **3,190 automated cases with 96.78% combined
statement and branch coverage**, the JavaScript checks and both complete
Home Assistant browser tests. All GitHub checks passed. The test count includes
parameterized cases; these figures are separate from the Beta.6 release above.

I installed the development build on my Buderus system with Home Assistant
2026.10.3. On 2026-10-24, I confirmed 19.0 to 18.5 to 19.0 °C through the controls
dialog and native climate, and hot water Auto to Off to Auto through the native
water-heater entity. I checked both directions in MyBuderus and restored all
changed settings. All 135 previous entities retained their IDs and user settings;
one new PointT hot-water entity was added. Regular polling restored its displayed
active target after the mode change.

This confirms those operations on my installation. It does not confirm other
devices, every operating mode, physical outage recovery or long-term stability.
Issue #49 and the WE800i field checks in issue #60 retain their separate scope.

## Scope of Beta.6

- I added native [water heaters](bacon-water-heaters.md) for Midea/RWH,
  [climate entities](bacon-air-conditioners.md) for the Midea Climate Series,
  [fans](bacon-air-purifiers.md) for seven Air purifier families and
  [dehumidifiers](bacon-dehumidifiers.md) for Dry 4000i/6000i/8000i.
- I added eight [read-only wallbox sensors](pointt-wallboxes.md), a separate
  connection for additional cloud appliances, zone controls and existing
  RRC weekly-program editing. ICOM holidays and WDDW2 holiday mode use their
  separate device contracts.
- I completed P16 with 132 conversion rules and 250 numeric candidates
  classified. The [conversion audit](conversion-audit.md) retains its original
  test checkpoint; the [follow-up corrections](app-parity-corrections.md)
  document the final review fixes and validation.
- I retained one device per existing PointT heating gateway. Separate cloud
  appliances and wallboxes keep their own identities. See
  [device presentation](device-presentation.md).
- I cancelled P15. Consumption history and regeneration logs are not included.

Physical checks of the new families, reconnection and real write effects are
outstanding. Wallbox controls, additional device actions and new RRC schedule
points are outside the implemented scope. WE800i controls remain disabled by
default pending confirmation in issue #60. See the
[device-support plan](device-support-plan.md) for remaining work.

## Accepted deviations

- Energy data is read every 5 minutes instead of every 10 minutes.
- Static values are read during discovery only and not again after 24 hours.

Both deviations are accepted for this project.

## Status by area

| Area | Status | Main remaining work |
|---|---|---|
| Repository, package structure, and CI | implemented | Preview ZIP is reproducible and was imported in isolation; HACS and hassfest also run in the release workflow before publication |
| Default HACS catalog listing | completed | Accepted on 2026-10-20 through [hacs/default#10040](https://github.com/hacs/default/pull/10040); installation is available directly through HACS search |
| OAuth/PKCE and token rotation | implemented, with unreleased lifecycle corrections | Real Bosch, reauthentication and endurance tests; see [connection recovery](connection-recovery.md) |
| Dynamic discovery | implemented | Reconfiguration and capability-based firmware schema checks are available; observe additional real installations |
| Polling and partial failures | mostly implemented | Standard and cloud-friendly profiles are available; gateway jitter remains open |
| Negative capabilities | implemented | Active pauses are reported in aggregate diagnostics |
| State and availability model | implemented | Redacted diagnostics are available |
| Read-only entities | implemented on one K40 | Maturity levels and default activation are implemented; additional installation profiles remain open |
| Faults and notifications | implemented on one K40 | Active fault 6249 is verified; warning, maintenance, critical, historical, and optional component-resource variants need additional real installations |
| Energy | mostly implemented | Direct counters, calculated environmental energy, and reset detection are implemented; long-term testing remains open |
| Diagnostics and support export | implemented | Understandable HTTP and capability success counters are available; observe additional real support cases |
| Reconfiguration and repairs | implemented | Gateway selection, brand changes, rediscovery, polling profiles, rate-limit repair, and firmware-schema repair are available |
| Write service and controls | mostly implemented | Safe user controls are released dynamically and were tested selectively on the reference installation; additional installation profiles remain open |
| Everyday controls dialog and PointT combined entities | implemented, unreleased; selected operations confirmed on my Buderus system | Additional modes, circuits and installations; see [heating controls](heating-controls.md) and [PointT hot water](pointt-hot-water.md) |
| Developer CLI | mostly implemented | Anonymized inventory export from Home Assistant diagnostics is available; automated contract-fixture generation can follow if needed |
| Preview gate 0.1.0 | implemented and released | Continue field validation |
| Release gate 1.0 | open | Multiple profiles, Bosch, endurance testing, and additional real write tests |

## Next priorities

1. Complete the review and release process for PRs #85, #86 and #87 in dependency
   order. Validate the combined package before assigning and publishing a new beta.
2. Additional real Bosch and Buderus installation profiles and anonymized
   inventories.
3. An endurance run after deployment, including token rotation, cloud outages,
   and rate limits.

# Project specification status

This document tracks the incremental implementation of the externally stored
project specification. The source specification itself is intentionally not
part of this repository. The status reflects implemented and verified code,
not merely planned architecture.

## Current beta: 0.8.2-beta.6

**This beta contains substantial changes and needs careful field testing.**
I added device families and native Home Assistant entity types and reworked
connections, discovery, freshness and conversions. I recommend a full backup
before updating. Version **0.8.1 remains Stable/Latest**.

The implementation passes 3,036 automated cases with 96.83% combined
statement and branch coverage. Ruff, formatting, strict Mypy, reproducible
packaging and an isolated ZIP import passed. Diagnostics use schema 27.
These software results do not establish physical-device behavior.

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
| OAuth/PKCE and token rotation | mostly implemented | Real Bosch and real reauthentication tests |
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
| Developer CLI | mostly implemented | Anonymized inventory export from Home Assistant diagnostics is available; automated contract-fixture generation can follow if needed |
| Preview gate 0.1.0 | implemented and released | Continue field validation |
| Release gate 1.0 | open | Multiple profiles, Bosch, endurance testing, and additional real write tests |

## Next priorities

1. Additional real Bosch and Buderus installation profiles and anonymized
   inventories.
2. An endurance run after deployment, including token rotation, cloud outages,
   and rate limits.

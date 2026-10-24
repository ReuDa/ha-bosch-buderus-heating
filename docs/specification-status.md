# Project specification status

This document tracks the incremental implementation of the externally stored
project specification. The source specification itself is intentionally not
part of this repository. The status reflects implemented and verified code,
not merely planned architecture.

## Current beta: 0.8.2-beta.5

I included initial WE800i discovery, readings and controls disabled by default,
additional zone and DHW readings, WDDW2 type corrections, German resource names
and diagnostics schema 17. The combined implementation passes 1,767 automated
cases with 96.70% statement and branch coverage. Physical verification of the
new device functions remains open; issue #60 and consumption history remain
outstanding. See the [device-support plan](device-support-plan.md).
Version 0.8.1 remains Stable/Latest.

## Local progress after Beta.5

I added native dehumidifiers for the identified Dry 4000i, 6000i and 8000i
families, individual humidity targets and modes, separate operating states
and diagnostics schema 25. Synthetic HA and MQTT tests cover the contracts.
Physical-device confirmation, timers and additional action controls remain
open. This is local and unreleased. See [dehumidifiers](bacon-dehumidifiers.md).

I added native fans for seven identified Air purifier families, discrete
stages, offered settings, separately classified readings and diagnostics
schema 24. Synthetic HA and MQTT tests cover the contracts. Physical-device
confirmation, timers and filter reset remain open. This is local and
unreleased. See [air purifiers](bacon-air-purifiers.md).

I added native Midea Climate Series entities with offered climate controls,
reported-state confirmation and diagnostics schema 23. This is local and
unreleased; physical-device validation and advanced functions remain open.
See [air conditioners](bacon-air-conditioners.md).

I added Midea/RWH water heaters on top of the local connection foundation.
The admitted scope includes temperatures, offered operating modes, confirmed
target/mode changes and optional status indicators. It remains unreleased;
physical-device tests and additional actions are open. See
[water heaters](bacon-water-heaters.md) for the exact scope.

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

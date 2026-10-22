"""Synthetic protocol fixtures for issue 60; no physical-device claims."""

from dataclasses import replace
from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.bosch_buderus_heating.binary_sensor import (
    BoschBuderusBinarySensor,
    build_binary_sensor_descriptions,
)
from custom_components.bosch_buderus_heating.const import DOMAIN
from custom_components.bosch_buderus_heating.coordinator import (
    BoschBuderusDataUpdateCoordinator,
    Freshness,
    ResourceSnapshot,
)
from custom_components.bosch_buderus_heating.diagnostics import _gateway_diagnostics
from custom_components.bosch_buderus_heating.discovery import (
    DiscoveryDiagnostics,
    async_discover_resources,
)
from custom_components.bosch_buderus_heating.pointt import (
    BatchItemResult,
    Gateway,
    RateLimited,
    Resource,
    ResourceMetadata,
    ResourceReference,
)
from custom_components.bosch_buderus_heating.pointt.redaction import (
    diagnostic_resource_path,
    resource_path_template,
)
from custom_components.bosch_buderus_heating.resource_catalog import (
    poll_group,
    supports_entity,
)
from custom_components.bosch_buderus_heating.sensor import (
    BoschBuderusSensor,
    build_sensor_descriptions,
)
from custom_components.bosch_buderus_heating.water_softener import (
    SOFTENER_CAPABILITIES,
    is_water_softener,
    low_salt,
    softener_schema_issue,
    softener_value,
)


def reading(suffix, value=None, unit=None, circuit="sw1"):
    kind = (
        "stringValue"
        if suffix
        in {"regeneration/enabled", "regeneration/phase", "holidayMode/enabled"}
        else "floatValue"
    )
    return Resource(
        f"/swCircuits/{circuit}/{suffix}",
        value=value,
        has_value=True,
        metadata=ResourceMetadata(resource_type=kind, unit=unit),
    )


def client_for(resources):
    client = AsyncMock()
    client.get_resources_bulk.side_effect = lambda gateway, paths: tuple(
        BatchItemResult(gateway, path, 200, resource=resources[path])
        if path in resources
        else BatchItemResult(gateway, path, 404)
        for path in paths
    )
    return client


def coordinator_for(hass, resources, gateway="softener"):
    entry = MockConfigEntry(domain=DOMAIN)
    entry.add_to_hass(hass)
    coordinator = BoschBuderusDataUpdateCoordinator(
        hass, client_for(resources), Gateway(gateway, model="watersoftener"), entry
    )
    coordinator.resources = resources
    coordinator.data = {
        path: ResourceSnapshot(resource, True, datetime.now(UTC))
        for path, resource in resources.items()
    }
    coordinator.last_update_success = True
    coordinator.update_interval = None
    return coordinator


@pytest.mark.parametrize(
    "model,expected",
    [
        ("watersoftener", True),
        ("WE800i", True),
        ("Logawater WE800i", True),
        ("8000iS", True),
        ("WE500", True),
        ("K40", False),
        ("WX100_V1", False),
        ("NOTWE800i", False),
        (None, False),
    ],
)
def test_profile_requires_explicit_device_evidence(model, expected):
    assert is_water_softener(Gateway("x", model=model), {}) == expected


@pytest.mark.parametrize("status", [403, 404, 406])
async def test_unreadable_parent_does_not_hide_softener_leaves(status):
    salt = reading("sensor/saltLevel", 68, "%")
    client = client_for({salt.path: salt})
    normal = client.get_resources_bulk.side_effect
    client.get_resources_bulk.side_effect = lambda gateway, paths: tuple(
        replace(result, status=status) if result.resource is None else result
        for result in normal(gateway, paths)
    )
    report = DiscoveryDiagnostics()
    found = await async_discover_resources(
        client,
        "softener",
        gateway=Gateway("softener", model="watersoftener"),
        diagnostics=report,
    )
    assert found == {salt.path: salt}
    paths = [
        path
        for call in client.get_resources_bulk.await_args_list
        for path in call.args[1]
    ]
    assert len(paths) == len(set(paths))
    assert not any(
        path.startswith(("/heatingCircuits", "/heatSources", "/dhwCircuits"))
        for path in paths
    )
    assert report.device_profile == "water_softener"
    assert report.completed
    assert all(
        len(call.args[1]) <= 30 for call in client.get_resources_bulk.await_args_list
    )


async def test_unidentified_gateway_can_advertise_an_additional_softener():
    path = "/swCircuits/sw2"
    system = Resource("/system", references=(ResourceReference(path),))
    salt = reading("sensor/saltLevel", 75, "%", "sw2")
    client = client_for({system.path: system, salt.path: salt})
    result = await async_discover_resources(client, "generic", roots=("/system",))
    assert salt.path in result
    requested = {
        p for call in client.get_resources_bulk.await_args_list for p in call.args[1]
    }
    assert not any(p.startswith("/swCircuits/sw1/") for p in requested)


async def test_late_appliance_profile_and_reference_priority():
    appliance = Resource("/system/appliance/model", value="WE800i", has_value=True)
    system = Resource(
        "/system",
        references=(
            ResourceReference(appliance.path),
            ResourceReference("/system/brand"),
        ),
    )
    salt = reading("sensor/saltLevel", 80)
    client = client_for({x.path: x for x in (system, appliance, salt)})
    report = DiscoveryDiagnostics()
    result = await async_discover_resources(
        client, "late", roots=("/system",), diagnostics=report
    )
    assert salt.path in result
    batches = [call.args[1] for call in client.get_resources_bulk.await_args_list]
    assert next(
        i for i, batch in enumerate(batches) if "/system/brand" in batch
    ) < next(i for i, batch in enumerate(batches) if salt.path in batch)
    assert report.device_profile == "water_softener"


@pytest.mark.parametrize(
    "depth,limit,reason", [(8, 5, "resource_limit"), (1, 512, "depth_limit")]
)
async def test_softener_respects_global_discovery_bounds(depth, limit, reason):
    client = client_for({})
    report = DiscoveryDiagnostics()
    await async_discover_resources(
        client,
        "s",
        gateway=Gateway("s", model="WE800i"),
        maximum_depth=depth,
        maximum_resources=limit,
        diagnostics=report,
    )
    assert report.stop_reason == reason
    assert (
        sum(len(call.args[1]) for call in client.get_resources_bulk.await_args_list)
        <= limit
    )


async def test_profile_does_not_swallow_rate_limit():
    client = AsyncMock()
    client.get_resources_bulk.side_effect = lambda gateway, paths: tuple(
        BatchItemResult(gateway, p, 429) for p in paths
    )
    with pytest.raises(RateLimited):
        await async_discover_resources(
            client, "s", gateway=Gateway("s", model="WE800i")
        )
    client.get_resources_bulk.assert_awaited_once()


@pytest.mark.parametrize(
    "value", [None, True, "20", -1, 101, float("nan"), float("inf"), {}, []]
)
def test_bad_salt_is_never_zero_or_low(value):
    salt = reading("sensor/saltLevel", value)
    threshold = reading("sensor/saltLevelAlarm", 20)
    assert softener_value(salt) is None
    assert low_salt(salt, threshold) is None


@pytest.mark.parametrize(
    "value,expected", [(0, True), (19.9, True), (20, True), (20.1, False), (100, False)]
)
def test_low_salt_uses_actual_threshold(value, expected):
    salt = reading("sensor/saltLevel", value)
    assert low_salt(salt, reading("sensor/saltLevelAlarm", 20)) is expected
    assert low_salt(salt, None) is None
    assert low_salt(salt, reading("sensor/saltLevelAlarm", 20, circuit="sw2")) is None


@pytest.mark.parametrize(
    "value,expected",
    [("on", True), ("off", False), (None, None), (True, None), ("new mode", None)],
)
def test_binary_requires_known_string_state(value, expected):
    assert softener_value(reading("regeneration/enabled", value)) is expected


@pytest.mark.parametrize(
    "suffix,unit,expected",
    [
        ("sensor/saltLevel", "kWh", "unconfirmed_unit"),
        ("regeneration/totalRemainingTime", None, "unconfirmed_unit"),
        ("regeneration/totalRemainingTime", "min", None),
        ("sensor/availableWater", "l", None),
        ("sensor/waterFlow", "l/min", None),
    ],
)
def test_metadata_controls_unit_support(suffix, unit, expected):
    resource = reading(suffix, 5, unit)
    assert softener_schema_issue(resource) == expected
    assert supports_entity(resource) is (expected is None)
    assert poll_group(resource).value != "static"


def test_all_current_capabilities_have_unique_entities_and_correct_units(hass):
    resources = {}
    for capability in SOFTENER_CAPABILITIES:
        value = (
            "normal"
            if capability.kind == "phase"
            else "on"
            if capability.kind == "binary"
            else 50
        )
        unit = capability.units[0] if capability.units else None
        resource = reading(capability.suffix, value, unit)
        resources[resource.path] = resource
    coordinator = coordinator_for(hass, resources)
    sensors = [
        BoschBuderusSensor(coordinator, desc)
        for desc in build_sensor_descriptions(resources)
    ]
    binaries = [
        BoschBuderusBinarySensor(coordinator, desc)
        for desc in build_binary_sensor_descriptions(resources)
    ]
    assert len(sensors) == 9
    assert len(binaries) == 3
    assert len({x.unique_id for x in [*sensors, *binaries]}) == 12
    assert all(
        x.device_info["identifiers"] == {(DOMAIN, "softener")}
        for x in [*sensors, *binaries]
    )
    volume = next(
        x
        for x in sensors
        if x.entity_description.resource_path.endswith("availableWater")
    )
    assert volume.device_class is SensorDeviceClass.VOLUME_STORAGE
    assert volume.state_class is SensorStateClass.MEASUREMENT
    phase = next(
        x for x in sensors if x.entity_description.resource_path.endswith("/phase")
    )
    assert phase.native_value == "normal"
    assert phase.options == [
        "normal",
        "refill",
        "brine_preparation",
        "brine_draw",
        "backwash",
        "rinse",
        "end",
    ]


def test_gateway_isolation_unavailability_and_identity_recovery(hass):
    salt = reading("sensor/saltLevel", 80)
    alarm = reading("sensor/saltLevelAlarm", 20)
    resources = {x.path: x for x in (salt, alarm)}
    first, second = (coordinator_for(hass, resources, gw) for gw in ("first", "second"))
    description = next(
        d
        for d in build_binary_sensor_descriptions(resources)
        if d.value_key == "low_salt"
    )
    one, two = (BoschBuderusBinarySensor(c, description) for c in (first, second))
    identity = one.unique_id
    first.data[salt.path] = ResourceSnapshot(
        reading("sensor/saltLevel", 10), True, datetime.now(UTC)
    )
    assert one.is_on is True and two.is_on is False
    first.data[salt.path] = replace(first.data[salt.path], available=False)
    assert not one.available and one.is_on is None
    first.data[salt.path] = replace(first.data[salt.path], available=True)
    assert one.available and one.is_on is True and one.unique_id == identity
    first.data[alarm.path] = replace(first.data[alarm.path], available=False)
    assert not one.available and one.is_on is None


def test_unknown_phase_and_numeric_sentinels_are_unknown(hass):
    salt = reading("sensor/saltLevel", 30)
    bad = replace(salt, metadata=replace(salt.metadata, numeric_error_values=(30,)))
    assert softener_value(bad) is None
    phase = reading("regeneration/phase", "private unexpected state")
    coordinator = coordinator_for(hass, {phase.path: phase})
    description = build_sensor_descriptions(coordinator.resources)[0]
    entity = BoschBuderusSensor(coordinator, description)
    assert entity.native_value is None
    assert "private unexpected state" not in entity.options


def test_diagnostics_omit_state_and_dynamic_ids(hass):
    salt = reading("sensor/saltLevel", 67.4321, circuit="private-device")
    coordinator = coordinator_for(hass, {salt.path: salt})
    report = _gateway_diagnostics(1, coordinator)
    assert report["device_profile"] == "water_softener"
    assert "67.4321" not in str(report)
    assert "private-device" not in str(report)
    assert diagnostic_resource_path(salt.path) == "/swCircuits/{sw}/sensor/saltLevel"
    assert resource_path_template(salt.path) == "/swCircuits/{sw}/sensor/saltLevel"
    assert (
        diagnostic_resource_path("/swCircuits/sw2/sensor/saltLevel")
        == "/swCircuits/sw2/sensor/saltLevel"
    )


@pytest.mark.parametrize("stale_path", ["sensor/saltLevel", "sensor/saltLevelAlarm"])
def test_stale_salt_sources_do_not_claim_a_current_warning(hass, stale_path):
    salt, alarm = reading("sensor/saltLevel", 10), reading("sensor/saltLevelAlarm", 20)
    resources = {x.path: x for x in (salt, alarm)}
    coordinator = coordinator_for(hass, resources)
    descriptions = build_binary_sensor_descriptions(resources)
    low = BoschBuderusBinarySensor(
        coordinator, next(x for x in descriptions if x.value_key == "low_salt")
    )
    path = f"/swCircuits/sw1/{stale_path}"
    coordinator.data[path] = replace(coordinator.data[path], freshness=Freshness.STALE)
    assert not low.available and low.is_on is None
    sensor = BoschBuderusSensor(
        coordinator,
        next(
            x for x in build_sensor_descriptions(resources) if x.resource_path == path
        ),
    )
    assert not sensor.available and sensor.native_value is None


async def test_list_reference_is_not_treated_as_a_circuit():
    root = Resource("/swCircuits", references=(ResourceReference("/swCircuits/list"),))
    listing = Resource(
        "/swCircuits/list", references=(ResourceReference("/swCircuits/sw2"),)
    )
    client = client_for({x.path: x for x in (root, listing)})
    await async_discover_resources(client, "generic", roots=("/swCircuits",))
    requested = {
        p for call in client.get_resources_bulk.await_args_list for p in call.args[1]
    }
    assert not any(p.startswith("/swCircuits/list/") for p in requested)
    assert "/swCircuits/sw2/sensor/saltLevel" in requested


def test_registration_diagnostics_distinguish_disabled_and_unavailable(hass):
    from homeassistant.helpers import entity_registry as er

    salt = reading("sensor/saltLevel", 67.4321)
    flow = reading("sensor/waterFlow", 2)
    coordinator = coordinator_for(hass, {x.path: x for x in (salt, flow)})
    registry = er.async_get(hass)
    registered = registry.async_get_or_create(
        "sensor",
        DOMAIN,
        "softener:swCircuits:sw1:sensor:saltLevel",
        config_entry=coordinator._config_entry,
    )
    hass.states.async_set(registered.entity_id, "unavailable")
    report = _gateway_diagnostics(1, coordinator)["softener_entities"]
    assert report[0]["entities"] == [
        {"platform": "sensor", "disabled": False, "state": "unavailable"}
    ]
    assert report[1]["registered"] is False
    registry.async_update_entity(
        registered.entity_id, disabled_by=er.RegistryEntryDisabler.USER
    )
    hass.states.async_remove(registered.entity_id)
    report = _gateway_diagnostics(1, coordinator)["softener_entities"]
    assert report[0]["entities"] == [
        {"platform": "sensor", "disabled": True, "state": "not_loaded"}
    ]
    assert registered.entity_id not in str(report)

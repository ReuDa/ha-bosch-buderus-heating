"""Dry-family contracts, incomplete observations and confirmed isolated writes."""

import asyncio
import copy
import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from homeassistant.components.humidifier.const import HumidifierAction as Action
from homeassistant.exceptions import HomeAssistantError, ServiceValidationError

from custom_components.bosch_buderus_heating.bacon import dry
from custom_components.bosch_buderus_heating.bacon.dry_entities import (
    BaconDryChildLock,
    BaconDrySensor,
    BaconDryStatus,
    track_entities,
)
from custom_components.bosch_buderus_heating.bacon.models import Device
from custom_components.bosch_buderus_heating.humidifier import (
    BaconDehumidifier,
    async_setup_entry,
)
from tests.test_bacon_dhw import responding
from tests.test_bacon_session import emit, environment

FIXTURES = Path(__file__).parent / "fixtures/contracts/bacon-dry"


def configured(name="dry_8000i", serial="serial-A", account=None):
    account = account or environment()
    data = json.loads((FIXTURES / (name + ".json")).read_text())
    for suffix, key in (
        ("topics/info", "info"),
        ("topics/meta", "metadata"),
        ("topics/sensor", "sensor"),
        ("shadows/state/get/accepted", "shadow"),
    ):
        emit(account, suffix, data[key], serial)
    return account, BaconDehumidifier(account, serial), data


def update(account, data, **patch):
    data["shadow"]["version"] += 1
    data["shadow"]["state"]["reported"].update(patch)
    emit(account, "shadows/state/get/accepted", data["shadow"])


@pytest.mark.parametrize(
    "name,prefix", [(n, p) for n, ps in dry.FAMILIES.items() for p in ps]
)
def test_only_proven_prefixes(name, prefix):
    assert dry.family(Device("test", model=prefix + " model")) == name


@pytest.mark.parametrize(
    "model", [None, "", "Dry", "Dry 4000", "dry_4000i", "Air 4000i", "xDry 8000i"]
)
def test_unproven_models(model):
    assert dry.family(Device("test", model=model)) is None


@pytest.mark.parametrize("profile", ["dry_4000i", "dry_8000i"])
def test_profile_capabilities_and_private_diagnostics(profile):
    account, unit, data = configured(profile)
    basic = profile == "dry_4000i"
    assert unit.available and unit.is_on is True
    assert unit.device_class == "dehumidifier" and unit.mode == "auto"
    assert unit.available_modes == (["auto", "night"] if basic else list(dry.MODES))
    assert unit.current_humidity == 60 and unit.target_humidity == (55 if basic else 50)
    assert (unit.min_humidity, unit.max_humidity, unit.target_humidity_step) == (
        (40, 65, 5) if basic else (30, 80, 10)
    )
    assert unit.action == Action.DRYING
    assert BaconDrySensor(account, "serial-A", "temperature").native_value == 22.5
    assert BaconDryChildLock(account, "serial-A", "child_lock").available is not basic
    assert BaconDryStatus(account, "serial-A", "condensate_pump").available is not basic
    assert account.diagnostics()["dehumidifiers"][profile] == {
        "identified": 1,
        "metadata_current": 1,
        "sensor_current": 1,
    }
    for private in (
        "serial-A",
        data["info"]["appliance"]["type"],
        "relHumidity",
        "customTitle",
        "22.5",
    ):
        assert private not in json.dumps(account.diagnostics())


@pytest.mark.parametrize(
    "field,value,unit,expected",
    [
        ("relHumidity", 50, "%", 50),
        ("relHumidity", 0, "%", 0),
        ("relHumidity", 100, "%", 100),
        ("relHumidity", 50.5, "%", None),
        ("relHumidity", 50.0, "%", None),
        ("relHumidity", 101, "%", None),
        ("relHumidity", -1, "%", None),
        ("relHumidity", 50, None, None),
        ("relHumidity", 50, "fraction", None),
        ("roomTemperature", 72.5, "degF", 22.5),
        ("roomTemperature", 22.5, "Celsius", 22.5),
        ("roomTemperature", 71, "degC", None),
        ("roomTemperature", 20, "K", None),
        ("unknown", 20, "%", None),
    ],
)
def test_explicit_measurements_units_and_types(field, value, unit, expected):
    _, unit_entity, _ = configured()
    device = unit_entity.device
    device.sensor[field] = value
    device.metadata["topics"]["sensor"][field] = {"unit": unit}
    assert dry.measurement(device, field) == expected


@pytest.mark.parametrize(
    "value", [None, True, "50", {}, float("nan"), float("inf"), 10**1000]
)
def test_invalid_measurements_are_unknown(value):
    _, unit, _ = configured()
    for field in ("relHumidity", "roomTemperature"):
        unit.device.sensor[field] = value
        assert dry.measurement(unit.device, field) is None


@pytest.mark.parametrize(
    "patch",
    [
        {"min": 61},
        {"max": 59},
        {"min": "0"},
        {"max": True},
        {"max": float("nan")},
        {"min": -1001},
    ],
)
def test_invalid_or_exceeded_sensor_bounds(patch):
    _, unit, _ = configured()
    unit.device.metadata["topics"]["sensor"]["relHumidity"].update(patch)
    assert unit.current_humidity is None


@pytest.mark.parametrize(
    "power,sensor,error,mode,expected,action",
    [
        (False, {}, False, "auto", "off", Action.OFF),
        (True, {"idleState": True}, False, "auto", "idle", Action.IDLE),
        (
            True,
            {"idleState": False, "relHumidity": 30},
            False,
            "auto",
            "running",
            Action.DRYING,
        ),
        (
            True,
            {"idleState": True, "relHumidity": 90},
            False,
            "auto",
            "idle",
            Action.IDLE,
        ),
        (
            True,
            {"waterTankFull": True, "idleState": True},
            False,
            "auto",
            "water_tank_full",
            None,
        ),
        (
            True,
            {"defrostingActive": True, "idleState": True},
            False,
            "auto",
            "defrosting",
            None,
        ),
        (
            True,
            {"waterTankFull": True, "defrostingActive": True},
            True,
            "auto",
            "device_error",
            None,
        ),
        (False, {"waterTankFull": True}, False, "auto", "water_tank_full", Action.OFF),
        (True, {"idleState": None}, False, "auto", None, None),
        (True, {"waterTankFull": None}, False, "auto", None, None),
        (True, {"defrostingActive": 0}, False, "auto", None, None),
        (True, {}, None, "auto", None, None),
        (True, {}, False, "unknown", None, None),
        (None, {}, False, "auto", None, None),
        (True, {}, False, "laundry", "running", Action.DRYING),
    ],
)
def test_operating_state_uses_reports_not_humidity_comparison(
    power, sensor, error, mode, expected, action
):
    account, unit, data = configured()
    unit.device.sensor.update(sensor)
    unit.device.error_present = error
    update(account, data, powerEnabled=power, opMode=mode)
    status = BaconDrySensor(account, "serial-A", "operating_status")
    assert status.native_value == expected and status.available == (
        expected is not None
    )
    assert unit.action == action


@pytest.mark.parametrize(
    "info,expected",
    [
        ({}, None),
        ({"error": None}, False),
        ({"error": {}}, True),
        ({"error": {"causeCode": "private unknown", "errorClass": "99999"}}, True),
        ({"error": []}, None),
        ({"error": False}, None),
        ({"error": "unknown"}, None),
    ],
)
def test_error_info_presence_is_not_a_guessed_error_class(info, expected):
    account, unit, data = configured()
    emit(
        account,
        "topics/info",
        {
            "timestamp": 3,
            "online": True,
            "appliance": data["info"]["appliance"],
            **info,
        },
    )
    sensor = BaconDryStatus(account, "serial-A", "device_error")
    assert sensor.is_on is expected and sensor.available == (expected is not None)
    assert unit.device.error_present is expected
    for value in ("private unknown", "99999", "causeCode", "errorClass"):
        assert value not in repr(unit.device) and value not in json.dumps(
            account.diagnostics()
        )


def test_error_ordering_retained_data_and_reconnect_cannot_clear_live_error():
    account, unit, data = configured()
    error = BaconDryStatus(account, "serial-A", "device_error")
    emit(account, "topics/info", {**data["info"], "timestamp": 4, "error": {}})
    for stamp in (3, 4):
        emit(
            account, "topics/info", {**data["info"], "timestamp": stamp, "error": None}
        )
    assert error.is_on is True
    emit(
        account,
        "topics/info",
        {**data["info"], "timestamp": 5, "error": None},
        retained=True,
    )
    assert error.is_on is None and unit.action is None
    emit(account, "topics/info", {**data["info"], "timestamp": 6, "error": None})
    assert error.is_on is False and unit.action == Action.DRYING
    unit.device.info_received_at -= 901
    assert not error.available and not unit.available
    account._disconnected()
    account.connected = True
    account.generation += 1
    emit(account, "topics/info", {**data["info"], "timestamp": 7}, retained=True)
    assert not error.available
    emit(account, "topics/info", {**data["info"], "timestamp": 8})
    assert error.is_on is False and unit.action is None


@pytest.mark.parametrize(
    "patch",
    [
        {"min": None},
        {"min": True},
        {"max": 101},
        {"max": 30},
        {"step": 0},
        {"step": 1.5},
        {"step": 60},
        {"unit": "g"},
    ],
)
async def test_bad_target_metadata_disables_writes(patch):
    account, unit, _ = configured()
    unit.device.metadata["shadows"]["state"]["humiditySetpoint"].update(patch)
    assert unit.target_humidity is None and unit.min_humidity == unit.max_humidity == 0
    assert unit.target_humidity_step is None
    with pytest.raises(ServiceValidationError):
        await unit.async_set_humidity(50)
    account._mqtt.publish.assert_not_called()


def test_target_grid_explicit_percent_contract_and_missing_data():
    _, unit, _ = configured()
    meta = unit.device.metadata["shadows"]["state"]
    meta["humiditySetpoint"] = {"min": 30, "max": 79, "step": 10}
    assert unit.max_humidity == 70 and unit.target_humidity == 50
    meta["humiditySetpoint"].pop("step")
    assert unit.target_humidity_step == 1 and unit.max_humidity == 79
    meta.pop("humiditySetpoint")
    assert unit.target_humidity is None
    unit.device.state = None
    assert unit.is_on is None and unit.mode is None and unit.action is None


@pytest.mark.parametrize(
    "value", [True, None, "50", 55, 50.0, 29, 81, float("nan"), float("inf"), 10**1000]
)
async def test_target_without_rounding_or_publish(value):
    account, unit, _ = configured()
    with pytest.raises(ServiceValidationError):
        await unit.async_set_humidity(value)
    account._mqtt.publish.assert_not_called()


async def test_confirmed_commands_preserve_other_fields_and_device():
    account, unit, data = configured()
    _, other, _ = configured("dry_4000i", "serial-B", account)
    old = copy.deepcopy(unit.device.state.reported)
    writes = responding(account, data)
    await unit.async_turn_off()
    await unit.async_turn_on()
    await unit.async_set_mode("night")
    await unit.async_set_humidity(60)
    lock = BaconDryChildLock(account, "serial-A", "child_lock")
    await lock.async_turn_on()
    assert lock.is_on is True
    await lock.async_turn_off()
    assert lock.is_on is False
    await unit.async_set_mode("laundry")
    assert writes == [
        {"powerEnabled": False},
        {"powerEnabled": True},
        {"opMode": "night"},
        {"humiditySetpoint": 60},
        {"childLockEnabled": True},
        {"childLockEnabled": False},
        {"opMode": "laundry"},
    ]
    assert unit.mode == "laundry" and unit.target_humidity == 60
    for key in (
        "displayEnabled",
        "laundryModeTimestamp",
        "onTimestamp",
        "offTimestamp",
        "customTitle",
    ):
        assert unit.device.state.reported[key] == old[key]
    assert other.is_on is True and other.target_humidity == 55 and other.mode == "auto"
    with pytest.raises(ServiceValidationError):
        await unit.async_set_humidity(50)
    assert len(writes) == 7


@pytest.mark.parametrize(
    "patch",
    [
        {},
        {"powerEnabled": 1},
        {"opMode": "unknown"},
        {"displayEnabled": False},
        {"laundryModeTimestamp": 0},
        {"onTimestamp": 0},
        {"condensatePumpRunning": True},
        {"fanSpeed": 1},
        {"customTitle": "x"},
        {"powerEnabled": False, "opMode": "auto"},
    ],
)
async def test_no_generic_command_escape(patch):
    account, unit, _ = configured()
    with pytest.raises(ServiceValidationError):
        await unit.write(patch)
    account._mqtt.publish.assert_not_called()


@pytest.mark.parametrize(
    "change",
    [
        "read_only",
        "options",
        "bounds",
        "model",
        "offline",
        "metadata",
        "laundry",
        "pending",
    ],
)
async def test_fresh_state_revalidates_capability_and_concurrent_changes(change):
    account, unit, data = configured()

    def mutate():
        meta = data["metadata"]["shadows"]["state"]
        if change == "read_only":
            meta["humiditySetpoint"]["ro"] = True
        elif change == "options":
            meta["opMode"]["enum"] = ["auto"]
        elif change == "bounds":
            meta["humiditySetpoint"]["max"] = 50
        elif change == "model":
            unit.device.model = "Dry 6000i"
        elif change == "offline":
            unit.device.online = False
        elif change == "metadata":
            data["metadata"] = {}
        elif change == "laundry":
            data["shadow"]["state"]["reported"]["opMode"] = "laundry"
        elif change == "pending":
            data["shadow"]["state"]["desired"] = {"humiditySetpoint": 40}
        emit(account, "topics/meta", data["metadata"])

    writes = responding(account, data, after_read=mutate)
    with pytest.raises(HomeAssistantError):
        if change == "options":
            await unit.async_set_mode("night")
        else:
            await unit.async_set_humidity(60)
    assert writes == []


@pytest.mark.parametrize(
    "outcome", ["desired", "retained", "timeout", "disconnect", "reject"]
)
async def test_unconfirmed_commands_are_unavailable_without_replay(outcome):
    account, unit, data = configured()
    writes = responding(account, data, outcome=outcome)
    with pytest.raises(HomeAssistantError):
        await unit.async_set_humidity(60)
    assert writes == [{"humiditySetpoint": 60}] and not unit.available
    assert (
        unit.target_humidity is None
        and unit.action is None
        and unit.available_modes == []
    )
    if outcome != "disconnect":
        data["shadow"]["version"] += 2
        emit(account, "shadows/state/get/accepted", data["shadow"])
        assert unit.available and unit.target_humidity == 50
    assert writes == [{"humiditySetpoint": 60}]


def test_independent_streams_snapshot_and_recovery():
    account, unit, data = configured()
    sensor = BaconDrySensor(account, "serial-A", "humidity")
    identity = sensor.unique_id
    unit.device.sensor_received_at -= 901
    for key in unit.device.sensor_fields_received_at:
        unit.device.sensor_fields_received_at[key] -= 901
    for timestamp, retained in [(1, False), (2, False), (3, True)]:
        emit(
            account,
            "topics/sensor",
            {"items": [{"timestamp": timestamp, "relHumidity": 40}]},
            retained=retained,
        )
    assert not sensor.available and unit.current_humidity is None and unit.available
    assert unit.action is None
    emit(account, "topics/sensor", {"items": [{"timestamp": 3, "relHumidity": 40}]})
    assert sensor.native_value == 40 and unit.action is None
    assert BaconDryStatus(account, "serial-A", "idle").is_on is None
    unit.device.state_received_at -= 901
    for key in unit.device.state_fields_received_at:
        unit.device.state_fields_received_at[key] -= 901
    assert not unit.available and sensor.available
    assert unit.min_humidity == unit.max_humidity == 0
    account._disconnected()
    assert not sensor.available
    account.connected = True
    account.generation += 1
    emit(account, "topics/info", {**data["info"], "timestamp": 3})
    emit(account, "topics/meta", data["metadata"], retained=True)
    emit(account, "shadows/state/get/accepted", data["shadow"])
    assert unit.available and unit.action is None
    emit(
        account,
        "topics/sensor",
        {"items": [{**data["sensor"]["items"][0], "timestamp": 4}]},
    )
    assert unit.action == Action.DRYING and sensor.unique_id == identity
    emit(
        account,
        "topics/info",
        {"timestamp": 4, "online": True, "appliance": {"type": "unknown"}},
    )
    assert not unit.available and not sensor.available


async def test_late_discovery_keeps_entity_identity_and_unload_listeners(hass):
    account = environment()
    added, cleanup = [], []
    entry = SimpleNamespace(
        runtime_data=SimpleNamespace(bacon=account), async_on_unload=cleanup.append
    )
    await async_setup_entry(hass, entry, added.extend)
    for platform in ("sensor", "switch", "binary_sensor"):
        track_entities(entry, account, added.extend, platform)
    assert not added
    _, _, data = configured("dry_4000i", account=account)
    assert len(added) == 8  # humidifier, three sensors, three flags and device error
    remembered = {e.unique_id for e in added}
    emit(account, "topics/meta", {})
    assert not any(
        e.available for e in added if e.key not in ("device_error", "dehumidifier")
    )
    emit(account, "topics/meta", data["metadata"])
    assert all(e.available for e in added)
    _, _, extended = configured()
    data["metadata"] = extended["metadata"]
    emit(account, "topics/meta", data["metadata"])
    emit(
        account,
        "topics/sensor",
        {"items": [{**extended["sensor"]["items"][0], "timestamp": 3}]},
    )
    assert len(added) == 10 and remembered <= {e.unique_id for e in added}
    assert all(e.available for e in added)
    for remove in cleanup:
        remove()
    configured("dry_8000i", "serial-B", account)
    assert len(added) == 10
    await async_setup_entry(
        hass, SimpleNamespace(runtime_data=SimpleNamespace(bacon=None)), Mock()
    )


@pytest.mark.parametrize("cancel", [False, True])
async def test_delayed_confirmation_and_cancellation(cancel):
    account, unit, data = configured()
    account._timeout = 2
    sent = asyncio.Event()
    writes = []

    async def publish(topic, payload, **kwargs):
        if topic.endswith("/get"):
            emit(account, "shadows/state/get/accepted", data["shadow"])
            return
        writes.append(json.loads(payload)["state"]["desired"])
        desired = copy.deepcopy(data["shadow"])
        desired["version"] += 1
        desired["state"]["desired"] = writes[-1]
        emit(account, "shadows/state/update/accepted", desired)
        sent.set()

    account._mqtt.publish.side_effect = publish
    task = asyncio.create_task(unit.async_set_humidity(60))
    try:
        await sent.wait()
        await asyncio.sleep(0)
        assert not task.done() and unit.target_humidity == 50
        if cancel:
            task.cancel()
            with pytest.raises(asyncio.CancelledError):
                await task
            assert not unit.available
        response = copy.deepcopy(data["shadow"])
        response["version"] += 2
        response["state"]["reported"]["humiditySetpoint"] = 60
        emit(account, "shadows/state/update/accepted", response)
        if not cancel:
            await task
            assert unit.target_humidity == 60
        assert writes == [{"humiditySetpoint": 60}]
    finally:
        if not task.done():
            task.cancel()
            await asyncio.gather(task, return_exceptions=True)


async def test_readonly_missing_rights_and_unknown_modes_never_publish():
    account, unit, data = configured("dry_4000i")
    lock = BaconDryChildLock(account, "serial-A", "child_lock")
    assert lock.is_on is None
    with pytest.raises(ServiceValidationError):
        await lock.async_turn_on()
    with pytest.raises(ServiceValidationError):
        await unit.async_set_mode("laundry")
    unit.device.metadata["shadows"]["state"]["opMode"].pop("ro")
    assert unit.supported_features == 0 and unit.available_modes == []
    update(account, data, opMode="unknown", powerEnabled=False)
    with pytest.raises(ServiceValidationError):
        await unit.async_turn_on()
    unit.device.model = None
    with pytest.raises(ServiceValidationError):
        await unit.async_turn_off()
    account._mqtt.publish.assert_not_called()

"""MQTT 5 account lifecycle and reported-state confirmation for Bacon."""

from __future__ import annotations

import asyncio
import contextlib
import hashlib
import json
import ssl
from collections.abc import Callable
from time import monotonic
from typing import Any
from uuid import uuid4

import aiomqtt

from . import dhw, rac
from .client import BaconClient
from .models import (
    BROKER,
    MAX_BYTES,
    USER_AGENT,
    BaconError,
    Device,
    Shadow,
    object_payload,
    shadow,
    token_subject,
    topic,
)

STALE_AFTER = 900
RESYNC_INTERVAL = 300
MAINTENANCE_INTERVAL = 60
WriteValidator = Callable[[Device, dict[str, Any]], bool]


class BaconAccount:
    """One selected account, with no command replay across connections."""

    def __init__(
        self,
        client: BaconClient,
        selected: tuple[str, ...],
        *,
        notify: Callable[[], None] = lambda: None,
        mqtt_factory: Callable[..., Any] = aiomqtt.Client,
        command_timeout: float = 20,
    ) -> None:
        self.client, self.selected, self.notify = client, selected, notify
        self.devices = {serial: Device(serial) for serial in selected}
        self.connected = False
        self.error: str | None = None
        self.generation = 0
        self.reconnects = 0
        self.invalid_messages = 0
        self._factory, self._timeout = mqtt_factory, command_timeout
        self._mqtt: Any = None
        self._task: asyncio.Task[None] | None = None
        self._locks = {serial: asyncio.Lock() for serial in selected}
        self._readers: dict[str, asyncio.Future[Shadow]] = {}
        self._changed = asyncio.Event()
        self._rejected: set[str] = set()
        self._listeners: set[Callable[[], None]] = set()
        self._claimed: set[str] = set()

    def add_listener(self, listener: Callable[[], None]) -> Callable[[], None]:
        self._listeners.add(listener)
        return lambda: self._listeners.discard(listener)

    def _notify(self) -> None:
        self._changed.set()
        self.notify()
        for listener in tuple(self._listeners):
            listener()

    def attach_task(self, task: asyncio.Task[None]) -> None:
        self._task = task

    async def close(self) -> None:
        if self._task:
            self._task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._task
        self._disconnected()

    def _disconnected(self) -> None:
        self.connected = False
        self._mqtt = None
        for device in self.devices.values():
            device.generation = 0
            device.state_generation = 0
            device.sensor_generation = device.metadata_generation = 0
        for future in tuple(self._readers.values()):
            if not future.done():
                future.set_exception(BaconError("connection"))
        self._notify()

    async def run(self) -> None:
        delay = 5.0
        try:
            while True:
                try:
                    await self.run_connection()
                    delay = 5
                except BaconError as err:
                    self.error = err.category
                    delay = max(delay, err.retry_after)
                    if err.category in {"authentication", "account_changed"}:
                        return
                except aiomqtt.MqttError as err:
                    self.error = _mqtt_error(err)
                    if self.error == "authentication":
                        return
                    if self.error == "rate_limited":
                        delay = max(60, delay)
                finally:
                    self._disconnected()
                self.reconnects += 1
                await asyncio.sleep(delay)
                delay = min(300, delay * 2)
        finally:
            self._disconnected()

    async def run_connection(self) -> None:
        offered = await self.client.get_devices()
        self._set_membership(offered)
        for serial in self.selected:
            if serial not in offered:
                self.devices[serial].online = None
        if not set(offered).intersection(self.selected):
            raise BaconError("devices_unavailable", RESYNC_INTERVAL)
        token = await self.client.access_token()
        subject = token_subject(token)
        if subject != self.client.subject:
            raise BaconError("account_changed")
        tls = await asyncio.to_thread(ssl.create_default_context)
        # A fresh client has no queued messages from an earlier connection.
        async with self._factory(
            BROKER,
            443,
            identifier=hashlib.sha256(uuid4().bytes).hexdigest(),
            username=subject,
            password=token,
            protocol=aiomqtt.ProtocolVersion.V5,
            transport="websockets",
            websocket_path="/mqtt",
            websocket_headers={
                "Authorization": f"Bearer {token}",
                "User-Agent": USER_AGENT,
            },
            tls_context=tls,
            clean_start=True,
            keepalive=60,
            timeout=20,
            max_queued_incoming_messages=256,
            max_queued_outgoing_messages=1,
            max_inflight_messages=1,
            max_concurrent_outgoing_calls=1,
        ) as mqtt:
            self._mqtt = mqtt
            await mqtt.subscribe(f"users/{subject}/#", qos=1)
            self.generation += 1
            self.connected, self.error = True, None
            self._notify()
            receiver = asyncio.create_task(self._receive(mqtt, subject))
            last_sync = 0.0
            try:
                while True:
                    now = monotonic()
                    if not last_sync or now - last_sync >= RESYNC_INTERVAL:
                        if last_sync:
                            self._set_membership(await self.client.get_devices())
                        for serial in sorted(self._claimed):
                            await mqtt.publish(
                                topic(subject, serial, "shadows/state/get"),
                                b"",
                                qos=1,
                                retain=False,
                            )
                        last_sync = now
                    done, _ = await asyncio.wait(
                        {receiver}, timeout=MAINTENANCE_INTERVAL
                    )
                    if done:
                        await receiver
                        raise BaconError("connection")
                    current = await self.client.access_token()
                    if current != token:
                        # Renew the authenticated WebSocket before using the new token.
                        return
                    self._notify()
            finally:
                receiver.cancel()
                with contextlib.suppress(
                    asyncio.CancelledError, BaconError, aiomqtt.MqttError
                ):
                    await receiver

    def _set_membership(self, offered: tuple[str, ...]) -> None:
        self._claimed = set(offered).intersection(self.selected)
        for serial, device in self.devices.items():
            if serial not in self._claimed:
                device.generation = device.state_generation = 0
                device.sensor_generation = device.metadata_generation = 0
                device.online = None
        self._notify()

    async def _receive(self, mqtt: Any, subject: str) -> None:
        async for message in mqtt.messages:
            try:
                self.ingest(
                    str(message.topic),
                    bytes(message.payload),
                    subject,
                    retained=message.retain,
                )
            except BaconError as err:
                if err.category == "rate_limited":
                    raise
                self.invalid_messages += 1
        raise BaconError("connection")

    def ingest(
        self, name: str, payload: bytes, subject: str, *, retained: bool = False
    ) -> None:
        prefix = f"users/{subject}/devices/"
        if not name.startswith(prefix):
            return
        serial, _, suffix = name[len(prefix) :].partition("/")
        if serial not in self._claimed:
            return
        device = self.devices[serial]
        if suffix in {"shadows/state/get/rejected", "shadows/state/update/rejected"}:
            if retained:
                return
            data = object_payload(payload)
            if data.get("code") == 429:
                raise BaconError("rate_limited")
            self._rejected.add(serial)
            reader = self._readers.get(serial)
            if reader is not None and not reader.done():
                reader.set_exception(BaconError("request_rejected"))
            self._notify()
            return
        if suffix not in {
            "topics/info",
            "topics/meta",
            "topics/sensor",
            "shadows/state/get/accepted",
            "shadows/state/update/accepted",
        }:
            return
        data = object_payload(payload)
        if suffix == "topics/info":
            stamp, online = data.get("timestamp"), data.get("online")
            if type(stamp) is not int or stamp < 0 or type(online) is not bool:
                raise BaconError("invalid_information")
            if stamp <= device.info_timestamp:
                return
            device.info_timestamp = stamp
            # The information timestamp's unit is not established. Use it only
            # for ordering; a retained message cannot prove a live connection.
            device.online = online
            if not retained:
                device.info_received_at = monotonic()
                device.generation = self.generation
            appliance = data.get("appliance")
            model = appliance.get("type") if isinstance(appliance, dict) else None
            new_model = model if isinstance(model, str) and len(model) <= 80 else None
            if device.model is not None and new_model != device.model:
                # Never combine a replacement model with its predecessor's data.
                device.state = None
                device.sensor = {}
                device.metadata = {}
                device.sensor_timestamp = -1
                device.state_generation = 0
                device.sensor_generation = device.metadata_generation = 0
            device.model = new_model
        elif suffix == "topics/meta":
            device.metadata = data
            # Retained capability metadata is valid for this subscription.
            # It does not establish device connectivity or fresh measurements.
            device.metadata_generation = self.generation
        elif suffix == "topics/sensor":
            if retained:
                return
            stamp = data.get("timestamp")
            if type(stamp) is not int or stamp < 0:
                raise BaconError("invalid_sensor")
            if stamp <= device.sensor_timestamp:
                return
            device.sensor = data
            device.sensor_timestamp = stamp
            device.sensor_received_at = monotonic()
            device.sensor_generation = self.generation
        else:
            if retained:
                return
            current = shadow(data)
            if device.state and current.version < device.state.version:
                return
            if (
                device.state
                and current.version == device.state.version
                and (
                    current.reported != device.state.reported
                    or current.desired != device.state.desired
                )
            ):
                raise BaconError("conflicting_version")
            device.state = current
            device.state_generation = self.generation
            device.state_received_at = monotonic()
            reader = self._readers.get(serial)
            if suffix == "shadows/state/get/accepted":
                device.uncertain = False
                if reader and not reader.done():
                    reader.set_result(current)
        device.received_at = monotonic()
        self._notify()

    def available(self, serial: str) -> bool:
        device = self.devices[serial]
        return (
            self.connected
            and serial in self._claimed
            and device.generation == self.generation
            and monotonic() - device.info_received_at <= STALE_AFTER
            and device.online is not None
        )

    async def read_state(self, serial: str) -> Shadow:
        if not self.connected or self._mqtt is None or serial not in self._claimed:
            raise BaconError("connection")
        if serial in self._readers:
            raise BaconError("busy")
        assert self.client.subject is not None
        future: asyncio.Future[Shadow] = asyncio.get_running_loop().create_future()
        self._readers[serial] = future
        try:
            await self._mqtt.publish(
                topic(self.client.subject, serial, "shadows/state/get"),
                b"",
                qos=1,
                retain=False,
            )
            async with asyncio.timeout(self._timeout):
                return await future
        except (TimeoutError, aiomqtt.MqttError) as err:
            raise BaconError("state_unconfirmed") from err
        finally:
            self._readers.pop(serial, None)
            if not future.done():
                future.cancel()
            elif not future.cancelled():
                future.exception()

    async def write_state(
        self,
        serial: str,
        desired: dict[str, Any],
        validator: WriteValidator,
    ) -> Shadow:
        """Internal family adapter API; no generic HA write service is exposed."""
        if serial not in self.devices:
            raise BaconError("invalid_identifier")
        async with self._locks[serial]:
            device = self.devices[serial]
            try:
                # Freeze the caller's values before awaiting a response.
                desired = object_payload(json.dumps(desired, allow_nan=False))
            except (TypeError, ValueError, RecursionError) as err:
                raise BaconError("invalid_payload") from err
            baseline = await self.read_state(serial)
            if not self.available(serial) or device.online is not True or not desired:
                raise BaconError("device_unavailable")
            if not _contains(baseline.reported, baseline.desired):
                raise BaconError("busy")
            # Family-specific options, limits and metadata must be checked here.
            if not validator(device, desired):
                raise BaconError("unsupported_command")
            encoded = json.dumps({"state": {"desired": desired}}, allow_nan=False)
            object_payload(encoded)
            if len(encoded.encode()) > MAX_BYTES:
                raise BaconError("invalid_payload")
            if _contains(baseline.reported, desired):
                return baseline
            self._rejected.discard(serial)
            assert self.client.subject is not None
            mqtt = self._mqtt
            generation = self.generation
            if mqtt is None:
                raise BaconError("connection")
            try:
                async with asyncio.timeout(self._timeout):
                    # A lost PUBACK is ambiguous. Never publish the command twice.
                    with contextlib.suppress(aiomqtt.MqttError):
                        await mqtt.publish(
                            topic(self.client.subject, serial, "shadows/state/update"),
                            encoded,
                            qos=1,
                            retain=False,
                        )
                    while True:
                        self._changed.clear()
                        if (
                            serial in self._rejected
                            or not self.available(serial)
                            or device.online is not True
                            or self.generation != generation
                        ):
                            raise BaconError("command_unconfirmed")
                        current = device.state
                        if (
                            current is not None
                            and device.state_generation == generation
                            and current.version > baseline.version
                            and current.timestamp >= baseline.timestamp
                            and _contains(current.reported, desired)
                        ):
                            return current
                        await self._changed.wait()
            except asyncio.CancelledError:
                device.uncertain = True
                self._notify()
                raise
            except (TimeoutError, BaconError) as err:
                device.uncertain = True
                self._notify()
                raise BaconError("command_unconfirmed") from err

    def diagnostics(self) -> dict[str, object]:
        return {
            "connected": self.connected,
            "selected_devices": len(self.selected),
            "online_devices": sum(
                self.available(s) and d.online is True for s, d in self.devices.items()
            ),
            "error": self.error,
            "reconnects": self.reconnects,
            "invalid_messages": self.invalid_messages,
            "states_received": sum(d.state is not None for d in self.devices.values()),
            "metadata_received": sum(bool(d.metadata) for d in self.devices.values()),
            "unconfirmed_commands": sum(d.uncertain for d in self.devices.values()),
            "air_conditioners": {
                "midea_climate": {
                    "identified": sum(rac.supported(d) for d in self.devices.values()),
                    "metadata_current": sum(
                        rac.supported(d)
                        and d.metadata_generation == self.generation
                        and self.available(s)
                        and d.online is True
                        for s, d in self.devices.items()
                    ),
                    "sensor_current": sum(
                        rac.supported(d)
                        and d.sensor_generation == self.generation
                        and monotonic() - d.sensor_received_at <= STALE_AFTER
                        and self.available(s)
                        and d.online is True
                        for s, d in self.devices.items()
                    ),
                },
            },
            "water_heaters": {
                name: {
                    "identified": sum(
                        dhw.family(d) == name for d in self.devices.values()
                    ),
                    "metadata_current": sum(
                        dhw.family(d) == name
                        and d.metadata_generation == self.generation
                        and self.available(s)
                        and d.online is True
                        for s, d in self.devices.items()
                    ),
                    "sensor_current": sum(
                        dhw.family(d) == name
                        and d.sensor_generation == self.generation
                        and monotonic() - d.sensor_received_at <= STALE_AFTER
                        and self.available(s)
                        and d.online is True
                        for s, d in self.devices.items()
                    ),
                }
                for name in dhw.FAMILIES
            },
        }


def _contains(actual: dict[str, Any], desired: dict[str, Any]) -> bool:
    return all(
        key in actual
        and (
            isinstance(actual[key], dict) and _contains(actual[key], value)
            if isinstance(value, dict)
            else type(actual[key]) is type(value) and actual[key] == value
        )
        for key, value in desired.items()
    )


def _mqtt_error(err: aiomqtt.MqttError) -> str:
    if isinstance(err, aiomqtt.MqttCodeError):
        code = getattr(err.rc, "value", err.rc)
        if code in (134, 135):
            return "authentication"
        if code in (151, 152, 159):
            return "rate_limited"
    return "connection"

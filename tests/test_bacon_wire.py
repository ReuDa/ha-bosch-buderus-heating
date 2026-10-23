"""Exercise the actual aiomqtt MQTT 5 WebSocket codec against a local broker."""

import asyncio
import json
import ssl
from pathlib import Path
from unittest.mock import Mock
from urllib.parse import urlsplit

import aiomqtt
import pytest
from aiohttp import web

from custom_components.bosch_buderus_heating.bacon.models import topic
from custom_components.bosch_buderus_heating.water_heater import BaconWaterHeater
from tests.test_bacon_contracts import token
from tests.test_bacon_session import environment, state
from tests.test_pointt_transport_and_client import serve

pytestmark = pytest.mark.usefixtures("socket_enabled")


def length(number):
    result = bytearray()
    while True:
        value = number % 128
        number //= 128
        result.append(value | (128 if number else 0))
        if not number:
            return bytes(result)


def packet(header, body):
    return bytes([header]) + length(len(body)) + body


def string(value):
    value = value.encode()
    return len(value).to_bytes(2, "big") + value


def publish(name, body):
    return packet(0x30, string(name) + b"\0" + json.dumps(body).encode())


@pytest.mark.parametrize("family_name", [None, "midea", "rwh"])
async def test_real_websocket_mqtt5_auth_subscription_and_readback(family_name):
    received = []
    writes = []
    ready = asyncio.Event()
    connected = asyncio.Event()
    fixture = (
        json.loads(
            (
                Path(__file__).parent
                / "fixtures/contracts/bacon-dhw"
                / (family_name + ".json")
            ).read_text()
        )
        if family_name
        else None
    )
    shadow_state = fixture["shadow"] if fixture else state()

    async def broker(request):
        assert request.headers["Authorization"] == "Bearer " + token()
        ws = web.WebSocketResponse(protocols=("mqtt",))
        await ws.prepare(request)
        pending = bytearray()
        async for frame in ws:
            if frame.type != web.WSMsgType.BINARY:
                continue
            pending.extend(frame.data)
            while len(pending) > 1:
                count, shift, pos = 0, 0, 1
                while True:
                    value = pending[pos]
                    count += (value & 127) << shift
                    pos += 1
                    if value < 128:
                        break
                    shift += 7
                if len(pending) < pos + count:
                    break
                header = pending[0]
                body = bytes(pending[pos : pos + count])
                del pending[: pos + count]
                kind = header >> 4
                if kind == 1:
                    assert body.startswith(b"\0\4MQTT\5")
                    assert body[7] & 0xC2 == 0xC2  # username, password, clean start
                    assert string("account-A") in body
                    assert string(token()) in body
                    await ws.send_bytes(packet(0x20, b"\0\0\0"))
                    connected.set()
                elif kind == 8:
                    assert body[2:] == b"\0" + string("users/account-A/#") + b"\1"
                    await ws.send_bytes(packet(0x90, body[:2] + b"\0\1"))
                    await ws.send_bytes(
                        publish(
                            topic("account-A", "serial-A", "topics/info"),
                            fixture["info"]
                            if fixture
                            else {"online": True, "timestamp": 1},
                        )
                    )
                    if fixture:
                        for suffix, key in (
                            ("topics/meta", "metadata"),
                            ("topics/sensor", "sensor"),
                        ):
                            await ws.send_bytes(
                                publish(
                                    topic("account-A", "serial-A", suffix), fixture[key]
                                )
                            )
                elif kind == 3:
                    size = int.from_bytes(body[:2], "big")
                    name = body[2 : 2 + size].decode()
                    pid = body[2 + size : 4 + size]
                    assert body[4 + size] == 0  # no MQTT properties
                    received.append(name)
                    await ws.send_bytes(packet(0x40, pid))
                    if name.endswith("/shadows/state/get"):
                        assert body[5 + size :] == b""
                    else:
                        assert fixture and name == topic(
                            "account-A", "serial-A", "shadows/state/update"
                        )
                        desired = json.loads(body[5 + size :])["state"]["desired"]
                        writes.append(desired)
                        shadow_state["state"]["reported"].update(desired)
                        shadow_state["version"] += 1
                    await ws.send_bytes(publish(name + "/accepted", shadow_state))
                    ready.set()
                elif kind == 12:
                    await ws.send_bytes(packet(0xD0, b""))
                elif kind == 14:
                    return ws
        return ws

    account = environment()
    account._timeout = 2
    account.devices["serial-A"].info_timestamp = -1
    account.client.get_devices.return_value = ("serial-A",)
    async with serve([("GET", "/mqtt", broker)]) as url:
        target = urlsplit(url)

        def local_factory(host, port, **kwargs):
            assert host == "broker.euc1.bacon.bosch-tt-cw.com"
            assert port == 443
            assert len(kwargs["identifier"]) == 64
            assert all(c in "0123456789abcdef" for c in kwargs["identifier"])
            assert kwargs.pop("tls_context").verify_mode == ssl.CERT_REQUIRED
            return aiomqtt.Client(target.hostname, target.port, **kwargs)

        account._factory = Mock(side_effect=local_factory)
        task = asyncio.create_task(account.run())
        account.attach_task(task)
        try:
            async with asyncio.timeout(5):
                await connected.wait()
                await ready.wait()
                # A response already sent by the broker may still be in aiomqtt's queue.
                for _ in range(100):
                    if account.devices["serial-A"].state is not None:
                        break
                    await asyncio.sleep(0.001)
            assert account.devices["serial-A"].state.version == 1
            assert account.available("serial-A")
            assert received == [topic("account-A", "serial-A", "shadows/state/get")]
            assert account._factory.call_count == 1
            if fixture:
                heater = BaconWaterHeater(account, "serial-A")
                assert heater.current_temperature == 48
                mode = "hybrid" if family_name == "midea" else "dual"
                await heater.async_set_operation_mode(mode)
                await heater.async_set_temperature(temperature=55)
                assert writes == [
                    {"powerEnabled": True, "opMode": mode},
                    {"tempSetpoint": 55},
                ]
                assert heater.current_operation == mode
                assert heater.target_temperature == 55
        finally:
            await account.close()
    assert not account.connected

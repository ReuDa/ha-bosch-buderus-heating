"""Selection helpers keeping account and backend identities separate."""

from __future__ import annotations

from typing import Any

from homeassistant.helpers.selector import (
    SelectOptionDict,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from ..ha_schema import validation as vol
from ..pointt import AuthTokens
from ..pointt.token_manager import StaticTokenProvider
from .client import BaconClient
from .models import (
    CONF_BACON_ACCOUNT,
    CONF_BACON_IDS,
    BaconError,
    account_key,
    device_list,
)


async def discover(
    client_session: Any, tokens: AuthTokens
) -> tuple[tuple[str, ...], str]:
    if "bacon" not in tokens.scope:
        return (), ""
    client = BaconClient(client_session, StaticTokenProvider(tokens.access_token))
    devices = await client.get_devices()
    assert client.subject is not None
    return devices, account_key(client.subject)


def extend_schema(
    schema: vol.Schema,
    devices: tuple[str, ...],
    *,
    selected: list[str] | None = None,
    has_gateways: bool = True,
) -> vol.Schema:
    if not devices:
        return schema
    fields = {
        key: value
        for key, value in schema.schema.items()
        if has_gateways or str(key) != "gateway_ids"
    }
    fields[vol.Optional(CONF_BACON_IDS, default=selected or [])] = SelectSelector(
        SelectSelectorConfig(
            options=[SelectOptionDict(value=s, label=f"…{s[-6:]}") for s in devices],
            multiple=True,
            mode=SelectSelectorMode.LIST,
        )
    )
    return vol.Schema(fields)


def selected_devices(data: dict[str, Any], known: tuple[str, ...]) -> list[str]:
    try:
        selected = device_list(data.get(CONF_BACON_IDS, []))
    except BaconError as err:
        raise ValueError("Invalid device selection") from err
    if not set(selected).issubset(known):
        raise ValueError("Device selection changed")
    return list(selected)


def config_data(devices: list[str], account: str) -> dict[str, Any]:
    return {CONF_BACON_IDS: devices, CONF_BACON_ACCOUNT: account}

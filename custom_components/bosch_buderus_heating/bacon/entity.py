"""Connectivity only; appliance controls belong to the later family packages."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.const import EntityCategory
from homeassistant.helpers.device_registry import DeviceInfo

from ..const import DOMAIN
from .models import device_key
from .session import BaconAccount

if TYPE_CHECKING:
    from homeassistant.components.binary_sensor.const import BinarySensorDeviceClass
else:
    from homeassistant.components.binary_sensor import BinarySensorDeviceClass


class BaconConnectivity(BinarySensorEntity):
    _attr_has_entity_name = True
    _attr_should_poll = False
    _attr_translation_key = "bacon_connectivity"
    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, account: BaconAccount, serial: str) -> None:
        self.account, self.serial = account, serial
        assert account.client.subject is not None
        self._identity = device_key(account.client.subject, serial)
        self._attr_unique_id = self._identity + ":connectivity"

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        self.async_on_remove(self.account.add_listener(self.async_write_ha_state))

    @property
    def available(self) -> bool:
        return self.account.available(self.serial)

    @property
    def is_on(self) -> bool | None:
        return self.account.devices[self.serial].online if self.available else None

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self._identity)},
            name=f"Bosch/Buderus (…{self.serial[-6:]})",
            manufacturer="Bosch Thermotechnik",
        )

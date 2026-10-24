"""Dynamic read-only binary sensors for discovered PointT resources."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from . import BoschBuderusConfigEntry
from .bacon.dhw_status import track_status
from .bacon.dry_entities import track_entities as track_dry_entities
from .bacon.entity import BaconConnectivity
from .coordinator import BoschBuderusDataUpdateCoordinator, Freshness, ResourceSnapshot
from .device import device_info_for_resource, grouped_entity_name
from .dhw_safety import assess_dhw_safety, is_dhw_safety_path
from .faults import (
    MAX_FAULT_ATTRIBUTES,
    fault_severity_label,
    fault_summary,
    no_active_faults_label,
)
from .holiday_writes import holiday_resources_from_snapshots
from .holidays import (
    HolidayState,
    is_holiday_resource_path,
    parse_holiday_state,
)
from .pointt import Resource
from .resource_catalog import (
    CapabilityMaturity,
    capability_maturity,
    entity_enabled_by_default,
    resource_name,
    supports_entity,
)
from .sensor import (
    _is_boolean_resource,
    _nested_scalar_keys,
    _nested_value,
    _semantic_key,
    _values_scalar_keys,
)
from .start_counters import is_start_counter_path
from .water_softener import low_salt, softener_capability, softener_value

if TYPE_CHECKING:
    from homeassistant.components.binary_sensor.const import BinarySensorDeviceClass
else:
    # Older HA defines this class in the platform module. Newer HA retains
    # that runtime export, but types it at its defining location in const.
    from homeassistant.components.binary_sensor import BinarySensorDeviceClass


@dataclass(frozen=True, kw_only=True)
class BoschBuderusBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Describe one boolean extracted from a PointT resource."""

    resource_path: str
    value_key: str | None = None


async def async_setup_entry(
    hass: HomeAssistant,
    entry: BoschBuderusConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Create entities from every safe boolean found during discovery."""
    entities: list[BinarySensorEntity] = []
    if (account := entry.runtime_data.bacon) is not None:
        track_dry_entities(entry, account, async_add_entities, "binary_sensor")
        entities.extend(
            BaconConnectivity(account, serial) for serial in account.selected
        )
    for coordinator in entry.runtime_data.coordinators:
        entities.append(BoschBuderusSystemFaultBinarySensor(coordinator))
        if any(is_holiday_resource_path(path) for path in coordinator.resources):
            entities.append(BoschBuderusHolidayActiveBinarySensor(coordinator))
    async_add_entities(entities)
    if account is not None:
        track_status(entry, account, async_add_entities)
    for coordinator in entry.runtime_data.coordinators:
        _track_binary_sensors(entry, coordinator, async_add_entities)


def _track_binary_sensors(
    entry: BoschBuderusConfigEntry,
    coordinator: BoschBuderusDataUpdateCoordinator,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add recovered capabilities once, using the shared polling listener."""
    seen: set[str] = set()

    @callback
    def discover() -> None:
        resources = dict(coordinator.resources)
        resources.update(
            {
                path: snapshot.resource
                for path, snapshot in (coordinator.data or {}).items()
                if snapshot.available
            }
        )
        additions = []
        for description in build_binary_sensor_descriptions(resources):
            if description.key not in seen:
                seen.add(description.key)
                additions.append(BoschBuderusBinarySensor(coordinator, description))
        if additions:
            async_add_entities(additions)

    discover()
    entry.async_on_unload(coordinator.async_add_listener(discover))


class BoschBuderusHolidayActiveBinarySensor(
    CoordinatorEntity[BoschBuderusDataUpdateCoordinator], BinarySensorEntity
):
    """Report the PointT holiday state independently from away mode."""

    _attr_has_entity_name = True
    _attr_translation_key = "holiday_active"
    _attr_icon = "mdi:palm-tree"

    def __init__(self, coordinator: BoschBuderusDataUpdateCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.gateway.gateway_id}:holiday_active"

    @property
    def available(self) -> bool:
        return super().available and any(
            is_holiday_resource_path(path) for path in self._available_resources
        )

    @property
    def is_on(self) -> bool | None:
        return self._state.active

    @property
    def extra_state_attributes(self) -> dict[str, object]:
        state = self._state
        now = datetime.now(UTC)
        return {
            "period_count": len(state.periods),
            "active_period_count": sum(
                period.start <= now < period.end for period in state.periods
            ),
            "invalid_period_count": state.invalid_period_count,
        }

    @property
    def device_info(self) -> DeviceInfo:
        return device_info_for_resource(self.coordinator, "/gateway")

    @property
    def _available_resources(self) -> dict[str, Resource]:
        return holiday_resources_from_snapshots(self.coordinator.data or {})

    @property
    def _state(self) -> HolidayState:
        return parse_holiday_state(
            self._available_resources,
            fallback_timezone=dt_util.get_default_time_zone(),
            timezones=self.coordinator.holiday_timezones,
        )


class BoschBuderusSystemFaultBinarySensor(
    CoordinatorEntity[BoschBuderusDataUpdateCoordinator], BinarySensorEntity
):
    """Report whether an actionable or unknown system fault is active."""

    _attr_has_entity_name = True
    _attr_translation_key = "system_fault"
    _attr_device_class = BinarySensorDeviceClass.PROBLEM
    _attr_icon = "mdi:alert-circle"

    def __init__(self, coordinator: BoschBuderusDataUpdateCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.gateway.gateway_id}:system_fault"

    @property
    def available(self) -> bool:
        return super().available and self.coordinator.faults.has_known_state

    @property
    def is_on(self) -> bool:
        return bool(self.coordinator.faults.active_faults)

    @property
    def extra_state_attributes(self) -> dict[str, object]:
        tracker = self.coordinator.faults
        codes = sorted(
            {item.code for item in tracker.active_faults if item.code is not None}
        )
        attributes: dict[str, object] = {
            "active_fault_count": len(tracker.active_faults),
            "active_notification_count": len(tracker.active),
            "highest_severity": (
                tracker.highest_severity.value if tracker.highest_severity else None
            ),
            "codes": codes[:MAX_FAULT_ATTRIBUTES],
            "codes_truncated": len(codes) > MAX_FAULT_ATTRIBUTES,
        }
        if tracker.active_faults:
            attributes["summary"] = fault_summary(
                tracker.active_faults[0], self.coordinator.hass.config.language
            )
            attributes["highest_severity_label"] = fault_severity_label(
                tracker.active_faults[0].severity,
                self.coordinator.hass.config.language,
            )
        else:
            attributes["summary"] = no_active_faults_label(
                self.coordinator.hass.config.language
            )
        return attributes

    @property
    def device_info(self) -> DeviceInfo:
        return device_info_for_resource(self.coordinator, "/gateway")


def build_binary_sensor_descriptions(
    resources: Mapping[str, Resource],
) -> tuple[BoschBuderusBinarySensorEntityDescription, ...]:
    """Build stable descriptions for all discovered safe boolean states."""
    descriptions: list[BoschBuderusBinarySensorEntityDescription] = []
    for resource in resources.values():
        if is_start_counter_path(resource.path) or not supports_entity(resource):
            continue
        if (
            softener := softener_capability(resource.path)
        ) is not None and softener.suffix == "sensor/saltLevel":
            descriptions.append(_description(resource, "low_salt"))
        keys = _nested_scalar_keys(resource.value, include_booleans=True)
        if not keys and resource.values:
            keys = _values_scalar_keys(resource, include_booleans=True)
        if keys:
            descriptions.extend(_description(resource, key) for key in keys)
        elif _is_boolean_resource(resource):
            descriptions.append(_description(resource, None))
    return tuple(descriptions)


def _description(
    resource: Resource, value_key: str | None
) -> BoschBuderusBinarySensorEntityDescription:
    return BoschBuderusBinarySensorEntityDescription(
        key=_semantic_key(resource.path, value_key),
        name=resource_name(resource.path, value_key),
        resource_path=resource.path,
        value_key=value_key,
        entity_category=(
            EntityCategory.DIAGNOSTIC
            if capability_maturity(resource.path) is CapabilityMaturity.UNDERSTOOD
            and softener_capability(resource.path) is None
            else None
        ),
        device_class=BinarySensorDeviceClass.PROBLEM
        if value_key == "low_salt"
        else None,
        entity_registry_enabled_default=entity_enabled_by_default(resource.path),
    )


class BoschBuderusBinarySensor(
    CoordinatorEntity[BoschBuderusDataUpdateCoordinator],
    BinarySensorEntity,
):
    """Represent one boolean value from a discovered PointT resource."""

    _attr_has_entity_name = True
    entity_description: BoschBuderusBinarySensorEntityDescription

    def __init__(
        self,
        coordinator: BoschBuderusDataUpdateCoordinator,
        description: BoschBuderusBinarySensorEntityDescription,
    ) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        display_name = resource_name(
            description.resource_path,
            description.value_key,
            language=coordinator.hass.config.language,
        )
        self._attr_name = grouped_entity_name(
            coordinator, description.resource_path, display_name
        )
        self._attr_unique_id = f"{coordinator.gateway.gateway_id}:{description.key}"

    @property
    def available(self) -> bool:
        snapshot = self._snapshot
        if not (super().available and snapshot is not None and snapshot.available):
            return False
        if (
            softener_capability(snapshot.resource.path) is not None
            or is_dhw_safety_path(snapshot.resource.path)
        ) and snapshot.freshness is not Freshness.FRESH:
            return False
        if self.entity_description.value_key == "low_salt":
            threshold = self._threshold_snapshot
            return threshold is None or (
                threshold.available and threshold.freshness is Freshness.FRESH
            )
        return True

    @property
    def is_on(self) -> bool | None:
        snapshot = self._snapshot
        if snapshot is None:
            return None
        resource = snapshot.resource
        if is_dhw_safety_path(resource.path):
            if not snapshot.available or snapshot.freshness is not Freshness.FRESH:
                return None
            return assess_dhw_safety(resource).value
        if softener_capability(resource.path) is not None:
            if not snapshot.available or snapshot.freshness is not Freshness.FRESH:
                return None
            if self.entity_description.value_key == "low_salt":
                threshold = self._threshold_snapshot
                if threshold is not None and (
                    not threshold.available
                    or threshold.freshness is not Freshness.FRESH
                ):
                    return None
                return low_salt(
                    resource,
                    threshold.resource
                    if threshold is not None
                    and threshold.available
                    and threshold.freshness is Freshness.FRESH
                    else None,
                )
            result = softener_value(resource)
            return result if isinstance(result, bool) else None
        value = (
            _nested_value(resource, self.entity_description.value_key)
            if self.entity_description.value_key is not None
            else resource.value
        )
        return value if isinstance(value, bool) else None

    @property
    def device_info(self) -> DeviceInfo:
        return device_info_for_resource(
            self.coordinator, self.entity_description.resource_path
        )

    @property
    def _snapshot(self) -> ResourceSnapshot | None:
        return (self.coordinator.data or {}).get(self.entity_description.resource_path)

    @property
    def _threshold_snapshot(self) -> ResourceSnapshot | None:
        path = (
            self.entity_description.resource_path.removesuffix("saltLevel")
            + "saltLevelAlarm"
        )
        return (self.coordinator.data or {}).get(path)

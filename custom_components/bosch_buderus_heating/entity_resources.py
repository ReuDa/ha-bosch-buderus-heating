"""Validated cached measurements for combined PointT entities."""

from __future__ import annotations

import math

from homeassistant.const import UnitOfTemperature
from homeassistant.util.unit_conversion import TemperatureConverter

from .coordinator import BoschBuderusDataUpdateCoordinator, Freshness
from .pointt import Resource
from .unit_contracts import TEMPERATURE_UNITS


def fresh_resource(
    coordinator: BoschBuderusDataUpdateCoordinator, path: str
) -> Resource | None:
    snapshot = (coordinator.data or {}).get(path)
    if (
        not coordinator.last_update_success
        or snapshot is None
        or not snapshot.available
        or snapshot.freshness is not Freshness.FRESH
    ):
        return None
    resource = snapshot.resource
    metadata = resource.metadata
    if (
        resource.path != path
        or not resource.has_value
        or resource.has_values
        or not metadata.availability_flags_valid
        or metadata.available is False
        or metadata.used is False
    ):
        return None
    return resource


def temperature(resource: Resource | None) -> float | None:
    if resource is None:
        return None
    value, meta = resource.value, resource.metadata
    unit = TEMPERATURE_UNITS.get(meta.unit or "")
    if (
        meta.resource_type != "floatValue"
        or unit is None
        or not meta.numeric_error_states_valid
        or isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(value)
        or value in meta.numeric_error_values
        or (meta.minimum is not None and value < meta.minimum)
        or (meta.maximum is not None and value > meta.maximum)
    ):
        return None
    return TemperatureConverter.convert(value, unit, UnitOfTemperature.CELSIUS)

"""Confirmed ICOM transactions; every changed leaf is sent at most once."""

from __future__ import annotations

from collections.abc import Mapping
from datetime import date

from .holiday_writes import (
    HolidayChangedError,
    HolidayWriteNotConfirmed,
    validate_holiday_values,
)
from .holidays import HolidayWriteValues, icom_write_configuration, icom_write_values
from .legacy_holidays import (
    ICOM_EMPTY_PERIODS,
    ICOM_FIELDS,
    icom_dates,
    icom_empty,
    is_icom_slot,
)
from .pointt import PointTClient, Resource, WriteValidationError
from .pointt.models import JsonValue


class IcomHolidayWriteService:
    """Keep the last authoritative read and invalidate any uncertain resources."""

    def __init__(self, client: PointTClient) -> None:
        self.client = client
        self.confirmed: dict[str, Resource] = {}
        self.invalidated: set[str] = set()

    async def async_write(
        self,
        gateway_id: str,
        resources: Mapping[str, Resource],
        operation: str,
        source_path: str,
        values: HolidayWriteValues | None,
        expected: HolidayWriteValues | None,
    ) -> Resource:
        """Recheck each step, commit dates last and stop on any conflict or failure."""
        self.confirmed = {}
        self.invalidated = set()
        if not is_icom_slot(source_path) or operation not in (
            "create",
            "update",
            "delete",
        ):
            raise WriteValidationError("Invalid legacy holiday request")
        paths = tuple(
            f"{source_path}/{field}"
            for field in (*ICOM_FIELDS, "delete")
            if f"{source_path}/{field}" in resources
        )
        if not paths:
            raise WriteValidationError("The legacy holiday was not discovered")
        current = await self._read(gateway_id, paths)
        configuration = icom_write_configuration(current, source_path)
        baseline = icom_write_values(current, source_path)
        if configuration is None or baseline is None:
            raise WriteValidationError("Legacy holiday capabilities are incomplete")
        if expected is not None and baseline != expected:
            raise HolidayChangedError("The legacy holiday changed")
        start_path = f"{source_path}/startStop"
        if operation == "create":
            if not icom_empty(current.get(start_path)):
                raise HolidayChangedError("The legacy holiday slot is no longer free")
        elif icom_dates(current.get(start_path)) is None:
            raise HolidayChangedError("The legacy holiday no longer exists")
        if operation == "delete":
            if not configuration.can_delete or expected is None:
                raise WriteValidationError(
                    "Deleting this legacy holiday is unavailable"
                )
            self.invalidated.update(paths)
            self.confirmed.clear()
            await self.client.put_resource_value(
                gateway_id, f"{source_path}/delete", "TRUE"
            )
            actual = await self._read(gateway_id, paths)
            if not icom_empty(actual.get(start_path)):
                raise HolidayWriteNotConfirmed(actual.get(start_path))
            return actual[start_path]
        if values is None or values.source_path != source_path:
            raise WriteValidationError("Legacy holiday source changed")
        validate_holiday_values(values, configuration)
        self._validate_dates(values)
        if (
            values.fix_temperature != baseline.fix_temperature
            and values.heating_mode not in ("FIX_TEMP", "FIX_TEMPERATURE")
        ):
            raise WriteValidationError(
                "Fixed temperature requires the fixed-temperature holiday mode"
            )
        if (
            values.name is not None
            or values.ventilation_mode is not None
            or values.thermal_disinfection is not None
        ):
            raise WriteValidationError("Legacy holidays do not support these fields")
        if (
            values.fix_temperature != baseline.fix_temperature
            and configuration.fix_temperature_min is None
        ):
            raise WriteValidationError("Legacy temperature is not writable")
        desired: dict[str, JsonValue] = {
            "dhwMode": values.dhw_mode,
            "hcMode": values.heating_mode,
            "fixTemperature": values.fix_temperature,
            "assignedTo": list(values.assigned_to),
            "startStop": f"{values.start_date}/{values.end_date}",
        }
        for field, value in desired.items():
            path = f"{source_path}/{field}"
            if path not in current:
                continue
            previous = current[path]
            previous_value = (
                list(previous.values) if field == "assignedTo" else previous.value
            )
            if value == previous_value:
                continue
            if not previous.metadata.writable:
                raise WriteValidationError("Legacy holiday field is not writable")
            # A complete read immediately before every mutation detects app changes
            # between steps. PointT provides no atomic compare-and-set operation.
            checked = await self._read(gateway_id, paths)
            if checked != current:
                raise HolidayChangedError("The legacy holiday changed between steps")
            self.invalidated.update(paths)
            self.confirmed.clear()
            if field == "assignedTo":
                await self.client.put_icom_holiday_assignments(
                    gateway_id, int(source_path.rsplit("hm", 1)[-1]), values.assigned_to
                )
            else:
                await self.client.put_resource_value(gateway_id, path, value)
            actual = await self._read(gateway_id, paths)
            read_value = (
                list(actual[path].values)
                if field == "assignedTo"
                else actual[path].value
            )
            if read_value != value or any(
                actual[other] != current[other] for other in paths if other != path
            ):
                raise HolidayWriteNotConfirmed(actual.get(start_path))
            current = actual
        # A full final comparison also covers no-op submissions and slot identity.
        actual_values = icom_write_values(current, source_path)
        if actual_values != values:
            raise HolidayWriteNotConfirmed(current.get(start_path))
        return current[start_path]

    async def _read(
        self, gateway_id: str, paths: tuple[str, ...]
    ) -> dict[str, Resource]:
        result: dict[str, Resource] = {}
        self.invalidated.update(paths)
        for path in paths:
            self.confirmed.pop(path, None)
        for path in paths:
            resource = await self.client.get_resource(gateway_id, path)
            if resource.path != path:
                raise WriteValidationError("Legacy holiday response has the wrong path")
            result[path] = resource
            self.confirmed[path] = resource
            self.invalidated.discard(path)
        return result

    @staticmethod
    def _validate_dates(values: HolidayWriteValues) -> None:
        try:
            start, end = (
                date.fromisoformat(values.start_date),
                date.fromisoformat(values.end_date),
            )
        except (TypeError, ValueError) as err:
            raise WriteValidationError("Invalid legacy holiday dates") from err
        if (
            start.isoformat() != values.start_date
            or end.isoformat() != values.end_date
            or not 2000 <= start.year <= end.year <= 2100
            or end < start
            or f"{values.start_date}/{values.end_date}" in ICOM_EMPTY_PERIODS
        ):
            raise WriteValidationError("Invalid legacy holiday date range")

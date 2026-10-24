"""Names, icons and categories shared by the device page and controls dialog."""

from __future__ import annotations

import re

from homeassistant.const import EntityCategory

from .coordinator import BoschBuderusDataUpdateCoordinator
from .device import grouped_entity_name

# Keep the meaning of each setting, especially DHW start temperatures.
_LABELS = {
    "operationMode": ("Betriebsart", "Operating mode"),
    "manualRoomSetpoint": ("Manueller Sollwert", "Manual setpoint"),
    "maxFlowTemp": ("Vorlaufgrenze", "Flow temperature limit"),
    "temperatureLevels/comfort2": ("Heiztemperatur", "Heating temperature"),
    "chargeDuration": ("Dauer Extra-Warmwasser", "Extra hot water duration"),
    "singleChargeSetpoint": ("Extra-Warmwasser Sollwert", "Extra hot water target"),
    "charge": ("Extra-Warmwasser", "Extra hot water"),
    "reduceTempOnAlarm": ("Absenkung bei Störung", "Reduce on alarm"),
    "silentMode/enabled": ("Leiser Betrieb", "Silent mode"),
    "awayMode/enabled": ("Abwesenheit", "Away mode"),
    "seasonOptimizer/mode": ("Saisonbetrieb", "Season mode"),
    "additionalHeater/operationMode": ("Zuheizer", "Auxiliary heater"),
}


def _heating_presentation(path: str) -> bool:
    return path.startswith(("/heatingCircuits/", "/dhwCircuits/")) or path in {
        "/system/awayMode/enabled",
        "/system/silentMode/enabled",
        "/system/seasonOptimizer/mode",
        "/heatSources/additionalHeater/operationMode",
    }


def control_label(path: str, fallback: str, language: str) -> str:
    """Short localized function name without discarding its meaning."""
    if not _heating_presentation(path):
        return fallback
    german = language.casefold().startswith("de")
    if "/temperatureLevels/" in path:
        level = path.rsplit("/", 1)[-1]
        if path.startswith("/dhwCircuits/"):
            level_labels = {
                "eco": ("Eco+ Starttemperatur", "Eco+ start temperature"),
                "low": ("Eco Starttemperatur", "Eco start temperature"),
                "high": ("Komfort Starttemperatur", "Comfort start temperature"),
            }
            if level in level_labels:
                return level_labels[level][not german]
        elif level == "eco":
            return "Absenktemperatur" if german else "Setback temperature"
    for suffix, labels in reversed(tuple(_LABELS.items())):
        if path.endswith("/" + suffix):
            return labels[not german]
    return fallback


def control_name(
    coordinator: BoschBuderusDataUpdateCoordinator, path: str, fallback: str
) -> str:
    """Shorten generic groups, preserving configured room and device names."""
    if not _heating_presentation(path):
        return grouped_entity_name(coordinator, path, fallback)
    name = control_label(path, fallback, coordinator.hass.config.language)
    grouped = grouped_entity_name(coordinator, path, name)
    group = grouped.removesuffix(" \N{EN DASH} " + name)
    group = re.sub(
        r"^(?:Heizkreis|Heating circuit) (\d+)$",
        r"HK \1" if coordinator.hass.config.language.startswith("de") else r"HC \1",
        group,
    )
    group = re.sub(
        r"^(?:Warmwasser|Hot water) (\d+)$",
        r"WW \1" if coordinator.hass.config.language.startswith("de") else r"DHW \1",
        group,
    )
    return f"{group}: {name}"


def control_icon(path: str, *, numeric: bool = False) -> str | None:
    if not _heating_presentation(path):
        return None
    if path.endswith("/chargeDuration"):
        return "mdi:timer-outline"
    if numeric:
        return "mdi:thermometer"
    if path.startswith("/dhwCircuits/"):
        return "mdi:water-boiler"
    if "/awayMode/" in path:
        return "mdi:home-export-outline"
    if "/silentMode/" in path:
        return "mdi:volume-low"
    if "/seasonOptimizer/" in path:
        return "mdi:sun-snowflake"
    return "mdi:radiator"


def control_category(path: str, *, numeric: bool = False) -> EntityCategory | None:
    if not _heating_presentation(path):
        return EntityCategory.CONFIG if numeric else None
    # Keep the original controls available for automations while the climate
    # provides the combined everyday heating control on the device page.
    if path.startswith("/heatingCircuits/") and path.endswith(
        ("/manualRoomSetpoint", "/operationMode")
    ):
        return EntityCategory.CONFIG
    if numeric and not path.endswith("/manualRoomSetpoint"):
        return EntityCategory.CONFIG
    if path in {
        "/heatSources/additionalHeater/operationMode",
        "/system/seasonOptimizer/mode",
    } or path.endswith("/reduceTempOnAlarm"):
        return EntityCategory.CONFIG
    return None

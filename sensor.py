"""Checkly sensor platform."""
from __future__ import annotations

from typing import TypedDict

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

# from . import UptimeRobotDataUpdateCoordinator
from . import ChecklyCoordinator
from .const import DOMAIN, LOGGER
from .entity import ChecklyEntity


class StatusValue(TypedDict):
    """Sensor details."""

    value: str
    icon: str


SENSORS_INFO = {
    0: StatusValue(value="pause", icon="mdi:television-pause"),
    1: StatusValue(value="not_checked_yet", icon="mdi:television"),
    2: StatusValue(value="up", icon="mdi:television-shimmer"),
    8: StatusValue(value="seems_down", icon="mdi:television-off"),
    9: StatusValue(value="down", icon="mdi:television-off"),
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Checkly sensors."""
    coordinator: ChecklyCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        ChecklySensor(
            coordinator,
            SensorEntityDescription(
                key=str(check.id),
                name=check.name,
                entity_category=EntityCategory.DIAGNOSTIC,
                device_class="checkly__check_status",
            ),
            check=check,
        )
        for check in coordinator.data
    )


class ChecklySensor(ChecklyEntity, SensorEntity):
    """Representation of a Checkly sensor."""

    @property
    def native_value(self) -> str:
        """Return the status of the check."""
        LOGGER.warn(self.check)
        return SENSORS_INFO[self.check.status]["value"]

    @property
    def icon(self) -> str:
        """Return the status of the check."""
        LOGGER.warn(self.check)
        return SENSORS_INFO[self.check.status]["icon"]

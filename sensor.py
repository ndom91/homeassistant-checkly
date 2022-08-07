"""Checkly sensor platform."""
from __future__ import annotations

from typing import TypedDict

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import ChecklyCoordinator
from .const import DOMAIN, LOGGER
from .entity import ChecklyEntity


class StatusValue(TypedDict):
    """Sensor details."""

    value: str
    icon: str


SENSORS_INFO = {
    # failing
    0: StatusValue(value="failing", icon="mdi:alarm-light-off"),
    # degraded
    1: StatusValue(value="degraded", icon="mdi:alarm-light-off-outline"),
    # passing
    2: StatusValue(value="passing", icon="mdi:alarm-light"),
    # unknown
    3: StatusValue(value="unknown", icon="mdi:cloud-question"),
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
                key=str(check['id']),
                name=check['name'],
                device_class="checkly__check_status",
            ),
            check=check,
        )
        for check in coordinator.data
    )


class ChecklySensor(ChecklyEntity, SensorEntity):
    """Representation of a Checkly sensor."""

    @property
    def name(self) -> str:
        """Return the name of the check."""
        return self.check["name"]

    @property
    def native_value(self) -> str:
        """Return the status of the check."""
        return SENSORS_INFO[self.check["current_status"]]["value"]

    @property
    def icon(self) -> str:
        """Return the icon of the state of the check."""
        return SENSORS_INFO[self.check["current_status"]]["icon"]

"""Diagnostics support for Checkly."""
from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from . import ChecklyCoordinator
from .const import DOMAIN, CONF_ACCOUNT_ID


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator: ChecklyCoordinator = hass.data[DOMAIN][entry.entry_id]

    return {
        "account": entry.data[CONF_ACCOUNT_ID],
        "checks": [
            {
                "id": check['id'],
                "type": str(check['checkType']),
                "frequency": check['frequency'],
                "activated": check['activated'],
            }
            for check in coordinator.data
        ],
    }

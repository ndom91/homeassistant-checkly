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
    # account: dict[str, Any] | str | None = None
    # try:
    #     response = await coordinator.api.get_account_details()
    # except Exception as err:
    #     account = str(err)
    # else:
    #     if (details := response.data) is not None:
    #         account = {
    #             "up_checks": details.up_checks,
    #             "down_checks": details.down_checks,
    #             "paused_checks": details.paused_checks,
    #         }

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

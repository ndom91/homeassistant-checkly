"""The Checkly integration."""
from __future__ import annotations

from datetime import timedelta

from typing import Any
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_API_KEY
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, LOGGER, PLATFORMS, CONF_ACCOUNT_ID
from .entity import ChecklyEntity
from .checkly import ChecklyApi


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Config entry example."""
    hass.data.setdefault(DOMAIN, {})
    dev_reg = dr.async_get(hass)

    accountId: str = entry.data[CONF_ACCOUNT_ID]
    key: str = entry.data[CONF_API_KEY]

    if not key.startswith("cu"):
        raise ConfigEntryAuthFailed(
            "Wrong API key type detected, use the 'User' API key"
        )

    api = ChecklyApi(key, accountId)

    hass.data[DOMAIN][entry.entry_id] = coordinator = ChecklyCoordinator(
        hass,
        api,
        config_entry_id=entry.entry_id,
        dev_reg=dev_reg
    )
    await coordinator.async_refresh()
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


class ChecklyCoordinator(DataUpdateCoordinator):
    """Checkly coordinator."""

    data: list[Any]
    config_entry: ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        api,
        config_entry_id: str,
        dev_reg: dr.DeviceRegistry
    ) -> None:
        """Initialize coordinator."""
        super().__init__(
            hass,
            LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=90),
        )
        self._config_entry_id = config_entry_id
        self._device_registry = dev_reg
        self.api = api
        self.hass = hass

    @property
    def icon(self):
        return 'https://www.checklyhq.com/images/racoon_favicon.png'

    async def _async_update_data(self):
        """Fetch data from API endpoint."""
        try:
            # LOGGER.warn('RUNNING ASYNC FETCH JOB...')
            checks = await self.hass.async_add_executor_job(self.api.get_checks)
            check_statuses = await self.hass.async_add_executor_job(self.api.get_check_statuses)

            for check in checks:
                for check_status in check_statuses:
                    if ("checkId" in check_status.keys()) and check["id"] == check_status["checkId"]:
                        check["current_status"] = 0 if check_status["hasFailures"] else 1 if check_status["isDegraded"] else 2
                        break
                    else:
                        check["current_status"] = 3

        except Exception as err:
            LOGGER.error(f'Data Update Error - {err}')
            raise UpdateFailed(f"Error communicating with API: {err}")

        current_checks = {
            list(device.identifiers)[0][1]
            for device in dr.async_entries_for_config_entry(
                self._device_registry, self._config_entry_id
            )
        }
        new_checks = {str(check['id']) for check in checks}
        if stale_checks := current_checks - new_checks:
            for check_id in stale_checks:
                if device := self._device_registry.async_get_device(
                    {(DOMAIN, check_id)}
                ):
                    self._device_registry.async_remove_device(device.id)

        if self.data:
            self.hass.async_create_task(
                self.hass.config_entries.async_reload(self._config_entry_id)
            )
            return None

        return checks

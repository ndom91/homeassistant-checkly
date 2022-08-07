"""The Checkly integration."""
from __future__ import annotations

# from pyuptimerobot import (
#     UptimeRobot,
#     UptimeRobotAuthenticationException,
#     UptimeRobotException,
#     UptimeRobotMonitor,
# )

# import logging
from datetime import timedelta
import async_timeout


from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_API_KEY
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import API_ATTR_OK, COORDINATOR_UPDATE_INTERVAL, DOMAIN, LOGGER, PLATFORMS, API_URL, CONF_ACCOUNT_ID
from .entity import ChecklyEntity
from .checkly import ChecklyApi


# async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
#     """Set up Checkly from a config entry."""
#     hass.data.setdefault(DOMAIN, {})
#     key: str = entry.data[CONF_API_KEY]
#     if !key.startswith("cu"):
#         raise ConfigEntryAuthFailed(
#             "Wrong API key type detected, use the 'User' API key"
#         )
#     checkly_api = API_URL
#     dev_reg = dr.async_get(hass)
#
#     hass.data[DOMAIN][entry.entry_id] = coordinator = UptimeRobotDataUpdateCoordinator(
#         hass,
#         config_entry_id=entry.entry_id,
#         dev_reg=dev_reg,
#         api=uptime_robot_api,
#     )
#
#     await coordinator.async_config_entry_first_refresh()
#
#     await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
#
#     return True
#
#
# async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
#     """Unload a config entry."""
#     unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
#     if unload_ok:
#         hass.data[DOMAIN].pop(entry.entry_id)
#
#     return unload_ok
#
#
# class UptimeRobotDataUpdateCoordinator(DataUpdateCoordinator):
#     """Data update coordinator for Checkly."""
#
#     data: list[UptimeRobotMonitor]
#     config_entry: ConfigEntry
#
#     def __init__(
#         self,
#         hass: HomeAssistant,
#         config_entry_id: str,
#         dev_reg: dr.DeviceRegistry,
#         api: UptimeRobot,
#     ) -> None:
#         """Initialize coordinator."""
#         super().__init__(
#             hass,
#             LOGGER,
#             name=DOMAIN,
#             update_interval=COORDINATOR_UPDATE_INTERVAL,
#         )
#         self._config_entry_id = config_entry_id
#         self._device_registry = dev_reg
#         self.api = api
#
#     async def _async_update_data(self) -> list[UptimeRobotMonitor] | None:
#         """Update data."""
#         try:
#             response = await self.api.async_get_monitors()
#         except UptimeRobotAuthenticationException as exception:
#             raise ConfigEntryAuthFailed(exception) from exception
#         except UptimeRobotException as exception:
#             raise UpdateFailed(exception) from exception
#         else:
#             if response.status != API_ATTR_OK:
#                 raise UpdateFailed(response.error.message)
#
#         monitors: list[UptimeRobotMonitor] = response.data
#
#         current_monitors = {
#             list(device.identifiers)[0][1]
#             for device in dr.async_entries_for_config_entry(
#                 self._device_registry, self._config_entry_id
#             )
#         }
#         new_monitors = {str(monitor.id) for monitor in monitors}
#         if stale_monitors := current_monitors - new_monitors:
#             for monitor_id in stale_monitors:
#                 if device := self._device_registry.async_get_device(
#                     {(DOMAIN, monitor_id)}
#                 ):
#                     self._device_registry.async_remove_device(device.id)
#
#         # If there are new monitors, we should reload the config entry so we can
#         # create new devices and entities.
#         if self.data and new_monitors - {str(monitor.id) for monitor in self.data}:
#             self.hass.async_create_task(
#                 self.hass.config_entries.async_reload(self._config_entry_id)
#             )
#             return None
#
#         return monitors


# _LOGGER = logging.getLogger(__name__)


# async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Config entry example."""
    hass.data.setdefault(DOMAIN, {})

    LOGGER.warn(f'entry.data: {entry.data}')

    accountId: str = entry.data[CONF_ACCOUNT_ID]
    key: str = entry.data[CONF_API_KEY]

    LOGGER.warn(f'accountId: {accountId}, apiKey: {key}')

    if not key.startswith("cu"):
        raise ConfigEntryAuthFailed(
            "Wrong API key type detected, use the 'User' API key"
        )

    api = ChecklyApi(key, accountId)

    # hass.data[DOMAIN][entry.entry_id] = coordinator = ChecklyCoordinator(
    #     hass,
    #     api=api,
    # )

    coordinator = ChecklyCoordinator(hass, api)
    # assuming API object stored here by __init__.py
    # api = hass.data[DOMAIN][entry.entry_id]

    # Fetch initial data so we have data when entities subscribe
    #
    # If the refresh fails, async_config_entry_first_refresh will
    # raise ConfigEntryNotReady and setup will try again later
    #
    # If you do not want to retry setup on failure, use
    # coordinator.async_refresh() instead
    #
    # await coordinator.async_config_entry_first_refresh()
    await coordinator.async_refresh()

    # async_add_entities(
    #     ChecklyEntity(coordinator, idx, ent) for idx, ent in enumerate(coordinator.data)
    # )


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


class ChecklyCoordinator(DataUpdateCoordinator):
    """Checkly coordinator."""

    def __init__(self, hass, api):
        """Initialize coordinator."""
        super().__init__(
            hass,
            LOGGER,
            # Name of the data. For logging purposes.
            name=DOMAIN,
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=timedelta(seconds=90),
        )
        self.api = api
        self.hass = hass

    @property
    def icon(self):
        return 'https://www.checklyhq.com/images/racoon_favicon.png'

    async def _async_update_data(self):
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
        try:
            # Note: asyncio.TimeoutError and aiohttp.ClientError are already
            # handled by the data update coordinator.
            LOGGER.warn(f'hassssss {self.hass}')
            async with async_timeout.timeout(10):
                return await self.api.get_checks()
        except Exception as err:
            # Raising ConfigEntryAuthFailed will cancel future updates
            # and start a config flow with SOURCE_REAUTH (async_step_reauth)
            LOGGER.error(f'ERR1 {err}')
            raise ConfigEntryAuthFailed from err
        except Exception as err:
            LOGGER.error(f'ERR2 {err}')
            raise UpdateFailed(f"Error communicating with API: {err}")

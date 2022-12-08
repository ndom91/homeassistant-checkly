""" NOTE: UNUSED - Switch could be used for enabling/disabling Checkly check"""

"""Checkly switch platform."""




from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from . import UptimeRobotDataUpdateCoordinator
from .const import API_ATTR_OK, DOMAIN, LOGGER
from .entity import UptimeRobotEntity
async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the Checkly switches."""
    coordinator: UptimeRobotDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        UptimeRobotSwitch(
            coordinator,
            SwitchEntityDescription(
                key=str(monitor.id),
                name=f"{monitor.friendly_name} Active",
                device_class=SwitchDeviceClass.SWITCH,
            ),
            monitor=monitor,
        )
        for monitor in coordinator.data
    )


class UptimeRobotSwitch(UptimeRobotEntity, SwitchEntity):
    """Representation of a Checkly switch."""

    _attr_icon = "mdi:cog"

    @property
    def is_on(self) -> bool:
        """Return True if the entity is on."""
        return bool(self.monitor.status != 0)

    async def _async_edit_monitor(self, **kwargs: Any) -> None:
        """Edit monitor status."""
        try:
            response = await self.api.async_edit_monitor(**kwargs)
        except UptimeRobotAuthenticationException:
            LOGGER.debug("API authentication error, calling reauth")
            self.coordinator.config_entry.async_start_reauth(self.hass)
            return
        except UptimeRobotException as exception:
            LOGGER.error("API exception: %s", exception)
            return

        if response.status != API_ATTR_OK:
            LOGGER.error("API exception: %s",
                         response.error.message, exc_info=True)
            return

        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn on switch."""
        await self._async_edit_monitor(id=self.monitor.id, status=0)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn off switch."""
        await self._async_edit_monitor(id=self.monitor.id, status=1)

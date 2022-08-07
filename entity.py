"""Base Checkly entity."""
from __future__ import annotations

# from pyuptimerobot import UptimeRobotMonitor

# from homeassistant.helpers.device_registry import DeviceEntryType
# from homeassistant.helpers.entity import DeviceInfo, EntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo

# from . import UptimeRobotDataUpdateCoordinator
from .const import DOMAIN
from .types import ChecklyCheck


# class UptimeRobotEntity(CoordinatorEntity[UptimeRobotDataUpdateCoordinator]):
#     """Base Checkly entity."""
#
#     _attr_attribution = ATTRIBUTION
#
#     def __init__(
#         self,
#         coordinator: UptimeRobotDataUpdateCoordinator,
#         description: EntityDescription,
#         monitor: UptimeRobotMonitor,
#     ) -> None:
#         """Initialize Checkly entities."""
#         super().__init__(coordinator)
#         self.entity_description = description
#         self._monitor = monitor
#         self._attr_device_info = DeviceInfo(
#             identifiers={(DOMAIN, str(self.monitor.id))},
#             name=self.monitor.friendly_name,
#             manufacturer="Checkly Team",
#             entry_type=DeviceEntryType.SERVICE,
#             model=self.monitor.type.name,
#             configuration_url=f"https://app.checklyhq.com/checks/{self.monitor.id}",
#         )
#         self._attr_extra_state_attributes = {
#             ATTR_TARGET: self.monitor.url,
#         }
#         self._attr_unique_id = str(self.monitor.id)
#         self.api = coordinator.api
#
#     @property
#     def _monitors(self) -> list[UptimeRobotMonitor]:
#         """Return all monitors."""
#         return self.coordinator.data or []
#
#     @property
#     def monitor(self) -> UptimeRobotMonitor:
#         """Return the monitor for this entity."""
#         return next(
#             (
#                 monitor
#                 for monitor in self._monitors
#                 if str(monitor.id) == self.entity_description.key
#             ),
#             self._monitor,
#         )
#
#     @property
#     def monitor_available(self) -> bool:
#         """Returtn if the monitor is available."""
#         return bool(self.monitor.status == 2)


class ChecklyEntity(CoordinatorEntity):
    """An entity using CoordinatorEntity.

    The CoordinatorEntity class provides:
      should_poll
      async_update
      async_added_to_hass
      available
    """

    def __init__(self, coordinator, idx, check):
        print(idx)
        print(check)
        """Initialize Checkly entities."""
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator)
        self.idx = idx
        # self.entity_description = description
        self._check = check
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, str(self.check.id))},
            name=self.check.name,
            manufacturer="Checkly",
            # entry_type=DeviceEntryType.SERVICE,
            # model=self.monitor.type.name,
            configuration_url=f"https://app.checklyhq.com/checks/{self.check.id}",
        )
        # self._attr_extra_state_attributes = {
        #     ATTR_TARGET: f"https://app.checklyhq.com/checks/{self.check.id}",
        # }
        self._attr_unique_id = str(self.check.id)
        self.api_url = coordinator.api_url

    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_is_on = self.coordinator.data[self.idx]["state"]
        self.async_write_ha_state()

    # async def async_turn_on(self, **kwargs):
    #     """Turn the light on.
    #
    #     Example method how to request data updates.
    #     """
    #     # Do the turning on.
    #     # ...
    #
    #     # Update the data
    #     await self.coordinator.async_request_refresh()

    @property
    def _checks(self) -> list[ChecklyCheck]:
        """Return all checks."""
        return self.coordinator.data or []

    @property
    def check(self) -> ChecklyCheck:
        """Return the checks for this entity."""
        return next(
            (
                check
                for check in self._checks
                if str(check.id) == self.entity_description.id
            ),
            self._check,
        )

    @property
    def check_available(self) -> bool:
        """Return if the check is available."""
        return bool(self.check.status == 2)

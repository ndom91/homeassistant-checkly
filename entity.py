"""Base Checkly entity."""
from __future__ import annotations

from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN, LOGGER
from .types import ChecklyCheck


class ChecklyEntity(CoordinatorEntity):
    """An entity using CoordinatorEntity."""
    def __init__(self, coordinator, idx, check):
        """Initialize Checkly entities."""
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator)
        self.idx = idx
        self.check_id = check["id"]
        self._check = check
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, str(self.check['id']))},
            name=self.check["name"],
            manufacturer="Checkly",
            model=self.check["checkType"],
            configuration_url=f"https://app.checklyhq.com/checks/{self.check['id']}",
        )
        self._attr_unique_id = str(self.check['id'])

    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        LOGGER.warn(f'_handle_coordinator_update {self.idx}')
        # self._attr_is_on = self.coordinator.data[self.idx]["state"]

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
                if str(check['id']) == self.check_id
            ),
            self._check,
        )

    @property
    def check_available(self) -> bool:
        """Return if the check is available."""
        return bool(self.check.status == 2)

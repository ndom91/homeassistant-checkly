"""Constants for the Checkly integration."""
from __future__ import annotations

from datetime import timedelta
from logging import Logger, getLogger
from typing import Final

from homeassistant.const import Platform

LOGGER: Logger = getLogger(__package__)

CONF_ACCOUNT_ID: Final = "account_id"

# The free plan is limited to 10 requests/minute
COORDINATOR_UPDATE_INTERVAL: timedelta = timedelta(seconds=10)

DOMAIN: Final = "checkly"

# PLATFORMS: Final = [Platform.BINARY_SENSOR, Platform.SENSOR, Platform.SWITCH]
PLATFORMS: Final = [Platform.SENSOR]

ATTRIBUTION: Final = "Data provided by Checkly"

ATTR_TARGET: Final = "target"

API_ATTR_OK: Final = "ok"

API_BASE_URL: Final = "https://api.checklyhq.com/v1"

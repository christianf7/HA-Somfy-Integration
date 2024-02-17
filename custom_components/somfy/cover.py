import logging
from typing import Any
from homeassistant.core import callback
from homeassistant.core import HomeAssistant
from homeassistant.components.light import LightEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import BasicHub
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass,
    config_entry,
    async_add_entities,
) -> None:
    bridge: BasicHub = hass.data[DOMAIN][config_entry.entry_id]

    b = []

    for blind in bridge.blinds:
        b.append(Blind(blind.key, blind.label, bridge, hass))

    async_add_entities(b)


class Blind(CoordinatorEntity, LightEntity):
    _attr_has_entity_name = True

    def __init__(self, id, label, hub, hass: HomeAssistant) -> None:
        self._attr_unique_id = label.lower().replace(" ", "_")
        self._attr_name = label
        self.id = id
        self._is_closed = False
        self.hub = hub
        self.hass = hass
        _LOGGER.debug(f"[SOMFY] {self._attr_unique_id} was registred.")

    @property
    def name(self) -> str:
        return self._attr_name

    async def async_open_cover(self, **kwargs):
        self._is_closed = False
        self.hass.async_add_executor_job(
            self.hub.set_status, self.id, "open"
        )
        # await self.coordinator.async_request_refresh()

    async def async_close_cover(self, **kwargs):
        self._is_closed = True
        self.hass.async_add_executor_job(
            self.hub.set_status, self.id, "close"
        )
        # await self.coordinator.async_request_refresh()

    async def async_stop_cover(self, **kwargs):
        self._is_closed = True
        self.hass.async_add_executor_job(
            self.hub.set_status, self.id, "stop"
        )

"""Publish simple item state changes via MQTT."""

import asyncio
import logging

from homeassistant.components import mqtt
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.typing import ConfigType

from .const import (
    DOMAIN,
    STARTUP_DELAY,
)
from .mqttunit import MQTTUnit
from .schema import CONFIG_SCHEMA  # noqa: F401

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    # sourcery skip: assign-if-exp, boolean-if-exp-identity, reintroduce-else
    """Set up the MQTT state feed."""
    # Make sure MQTT is available and the entry is loaded
    await asyncio.sleep(STARTUP_DELAY)
    if not await mqtt.async_wait_for_mqtt_client(hass):
        _LOGGER.error("MQTT integration is not available")
        return False

    conf: ConfigType = config[DOMAIN]
    hass.data[DOMAIN] = []
    for mqtt_config in conf:
        unit = MQTTUnit(mqtt_config)
        unit.setup_unit(hass)
        hass.data[DOMAIN].append(unit)

    _register_services(hass)

    return True


def _register_services(hass):
    async def _async_publish_discovery_state(call: ServiceCall):
        async with asyncio.TaskGroup() as group:
            for unit in hass.data[DOMAIN]:
                group.create_task(unit.publisher.async_publish_discovery_state(call))

    hass.services.async_register(
        DOMAIN, "publish_discovery_state", _async_publish_discovery_state
    )

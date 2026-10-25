"""light methods for MQTT Discovery Statestream."""

import json
import logging

from homeassistant.components.light import (
    ATTR_TRANSITION,
    ColorMode,
    LightEntityCapabilityAttribute,
    LightEntityFeature,
    LightEntityStateAttribute,
)
from homeassistant.components.mqtt.const import (
    CONF_COMMAND_TOPIC,
    CONF_JSON_ATTRS_TOPIC,
    CONF_SCHEMA,
)
from homeassistant.const import (
    ATTR_ENTITY_ID,
    ATTR_STATE,
    CONF_BRIGHTNESS,
    CONF_COLOR_TEMP,
    CONF_EFFECT,
    SERVICE_TURN_OFF,
    SERVICE_TURN_ON,
    STATE_ON,
    Platform,
)
from homeassistant.helpers.entity import get_supported_features

from ..const import (
    ATTR_B,
    ATTR_COLOR,
    ATTR_G,
    ATTR_H,
    ATTR_JSON,
    ATTR_R,
    ATTR_S,
    ATTR_X,
    ATTR_Y,
    COMMAND_SET_LIGHT,
    STATE_CAPITAL_OFF,
    STATE_CAPITAL_ON,
)
from ..helpers.base_entity import DiscoveryEntity
from ..utils import EntityInfo, add_config_command

_LOGGER = logging.getLogger(__name__)


class DiscoveryItem(DiscoveryEntity):
    """Light class."""

    PLATFORM = Platform.LIGHT

    def build_config(self, config, entity_info: EntityInfo):
        """Build the config for a light."""
        del config[CONF_JSON_ATTRS_TOPIC]
        add_config_command(config, entity_info, CONF_COMMAND_TOPIC, COMMAND_SET_LIGHT)
        config[CONF_SCHEMA] = ATTR_JSON

        supported_features = get_supported_features(self._hass, entity_info.entity_id)
        if supported_features & LightEntityFeature.EFFECT:
            config[CONF_EFFECT] = True
            config[LightEntityCapabilityAttribute.EFFECT_LIST] = entity_info.attributes[
                LightEntityCapabilityAttribute.EFFECT_LIST
            ]
        if (
            LightEntityCapabilityAttribute.SUPPORTED_COLOR_MODES
            in entity_info.attributes
        ):
            supported_color_modes = entity_info.attributes[
                LightEntityCapabilityAttribute.SUPPORTED_COLOR_MODES
            ]
            config[LightEntityCapabilityAttribute.SUPPORTED_COLOR_MODES] = (
                supported_color_modes
            )
            config[CONF_BRIGHTNESS] = True
            if ColorMode.COLOR_TEMP in supported_color_modes:
                # MQTT color_temp values are published and consumed as Kelvin.
                config[LightEntityStateAttribute.COLOR_TEMP_KELVIN] = True
        else:
            config[LightEntityStateAttribute.COLOR_MODE] = False
            _LOGGER.warning(
                "Light '%s' has no '%s' attribute which is mandatory. Please report to owner",
                entity_info.entity_id,
                LightEntityCapabilityAttribute.SUPPORTED_COLOR_MODES,
            )

    async def async_publish_state(self, new_state, mybase):
        """Build the state for a light."""
        payload = {
            ATTR_STATE: STATE_CAPITAL_ON
            if new_state.state == STATE_ON
            else STATE_CAPITAL_OFF,
        }
        self._add_attribute(payload, new_state, LightEntityStateAttribute.BRIGHTNESS)
        self._add_attribute(
            payload, new_state, LightEntityCapabilityAttribute.MAX_COLOR_TEMP_KELVIN
        )
        self._add_attribute(
            payload, new_state, LightEntityCapabilityAttribute.MIN_COLOR_TEMP_KELVIN
        )
        self._add_attribute(payload, new_state, LightEntityStateAttribute.EFFECT)

        # Home Assistant's MQTT JSON light schema requires color_temp whenever
        # color_mode is color_temp. Source lights may briefly expose the mode
        # before their temperature value is available, so omit the mode for
        # that transient state instead of publishing an invalid payload.
        color_mode = new_state.attributes.get(LightEntityStateAttribute.COLOR_MODE)
        color_temp_kelvin = new_state.attributes.get(
            LightEntityStateAttribute.COLOR_TEMP_KELVIN
        )
        if color_mode == ColorMode.COLOR_TEMP:
            if color_temp_kelvin is not None:
                payload[LightEntityStateAttribute.COLOR_MODE] = color_mode
                payload[CONF_COLOR_TEMP] = color_temp_kelvin
        elif color_mode is not None:
            payload[LightEntityStateAttribute.COLOR_MODE] = color_mode

        if color := self._add_colors(new_state):
            payload[ATTR_COLOR] = color

        await self._async_mqtt_publish(ATTR_STATE, payload, mybase, encoded=True)

    def _add_attribute(self, payload, new_state, attribute, alt_attribute=None):
        save_attribute = alt_attribute or attribute
        if new_state.attributes.get(attribute):
            payload[save_attribute] = new_state.attributes[attribute]

    def _add_colors(self, new_state):
        color = {}
        if new_state.attributes.get(LightEntityStateAttribute.HS_COLOR):
            color[ATTR_H] = new_state.attributes[LightEntityStateAttribute.HS_COLOR][0]
            color[ATTR_S] = new_state.attributes[LightEntityStateAttribute.HS_COLOR][1]
        if new_state.attributes.get(LightEntityStateAttribute.XY_COLOR):
            color[ATTR_X] = new_state.attributes[LightEntityStateAttribute.XY_COLOR][0]
            color[ATTR_Y] = new_state.attributes[LightEntityStateAttribute.XY_COLOR][1]
        if new_state.attributes.get(LightEntityStateAttribute.RGB_COLOR):
            color[ATTR_R] = new_state.attributes[LightEntityStateAttribute.RGB_COLOR][0]
            color[ATTR_G] = new_state.attributes[LightEntityStateAttribute.RGB_COLOR][1]
            color[ATTR_B] = new_state.attributes[LightEntityStateAttribute.RGB_COLOR][2]

        return color

    async def _async_handle_message(self, msg):
        """Handle a message for a light."""
        valid, domain, entity, _command = self.validate_message(  # pylint: disable=unused-variable
            msg,
        )
        if not valid:
            return

        payload_json = json.loads(msg.payload)

        service_payload = {
            ATTR_ENTITY_ID: f"{domain}.{entity}",
        }
        if ATTR_TRANSITION in payload_json:
            service_payload[ATTR_TRANSITION] = payload_json[ATTR_TRANSITION]

        if payload_json[ATTR_STATE] == STATE_CAPITAL_ON:
            if LightEntityStateAttribute.BRIGHTNESS in payload_json:
                service_payload[LightEntityStateAttribute.BRIGHTNESS] = payload_json[
                    LightEntityStateAttribute.BRIGHTNESS
                ]
            if CONF_COLOR_TEMP in payload_json:
                service_payload[LightEntityStateAttribute.COLOR_TEMP_KELVIN] = (
                    payload_json[CONF_COLOR_TEMP]
                )
            if ATTR_COLOR in payload_json:
                if ATTR_H in payload_json[ATTR_COLOR]:
                    service_payload[LightEntityStateAttribute.HS_COLOR] = [
                        payload_json[ATTR_COLOR][ATTR_H],
                        payload_json[ATTR_COLOR][ATTR_S],
                    ]
                if ATTR_X in payload_json[ATTR_COLOR]:
                    service_payload[LightEntityStateAttribute.XY_COLOR] = [
                        payload_json[ATTR_COLOR][ATTR_X],
                        payload_json[ATTR_COLOR][ATTR_Y],
                    ]
                if ATTR_R in payload_json[ATTR_COLOR]:
                    service_payload[LightEntityStateAttribute.RGB_COLOR] = [
                        payload_json[ATTR_COLOR][ATTR_R],
                        payload_json[ATTR_COLOR][ATTR_G],
                        payload_json[ATTR_COLOR][ATTR_B],
                    ]
            if LightEntityStateAttribute.EFFECT in payload_json:
                service_payload[LightEntityStateAttribute.EFFECT] = payload_json[
                    LightEntityStateAttribute.EFFECT
                ]
            await self._hass.services.async_call(
                domain, SERVICE_TURN_ON, service_payload
            )
        elif payload_json[ATTR_STATE] == STATE_CAPITAL_OFF:
            await self._hass.services.async_call(
                domain, SERVICE_TURN_OFF, service_payload
            )
        else:
            _LOGGER.error(
                'Invalid state for "%s" - payload: %s for %s',
                COMMAND_SET_LIGHT,
                {msg.payload},
                {entity},
            )

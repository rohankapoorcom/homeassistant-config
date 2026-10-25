"""Publishing for MQTT Discovery Stream."""

import importlib
import json
import logging

from homeassistant.components import mqtt
from homeassistant.components.mqtt.const import (
    CONF_AVAILABILITY,
    CONF_AVAILABILITY_MODE,
    CONF_CONNECTIONS,
    CONF_DEFAULT_ENTITY_ID,
    CONF_ENTITY_PICTURE,
    CONF_IDENTIFIERS,
    CONF_JSON_ATTRS_TOPIC,
    CONF_MANUFACTURER,
    CONF_ORIGIN,
    CONF_PAYLOAD_AVAILABLE,
    CONF_PAYLOAD_NOT_AVAILABLE,
    CONF_STATE_TOPIC,
    CONF_SW_VERSION,
    CONF_TOPIC,
)
from homeassistant.const import (
    ATTR_DEVICE_CLASS,
    ATTR_ENTITY_PICTURE,
    ATTR_FRIENDLY_NAME,
    ATTR_ICON,
    ATTR_STATE,
    ATTR_UNIT_OF_MEASUREMENT,
    CONF_DEVICE,
    CONF_DEVICE_CLASS,
    CONF_ENTITY_CATEGORY,
    CONF_INCLUDE,
    CONF_MODEL,
    CONF_NAME,
    CONF_UNIQUE_ID,
    CONF_UNIT_OF_MEASUREMENT,
    Platform,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr, entity_registry as er
from homeassistant.helpers.json import JSONEncoder

from .const import (
    ATTR_ATTRIBUTES,
    ATTR_CONFIG,
    CONF_BASE_TOPIC,
    CONF_COMMAND_TOPIC,
    CONF_DISCOVERY_TOPIC,
    CONF_LOCAL_STATUS,
    CONF_OFFLINE_STATUS,
    CONF_ONLINE_STATUS,
    CONF_PUBLISH_RETAIN,
    CONF_TILDA,
    CONF_UNIQUE_ENTITY_PREFIX,
    CONF_UNIQUE_PREFIX,
    DOMAIN,
    SUPPORTED_ENTITY_TYPE_COMMANDS,
)
from .utils import (
    EntityInfo,
    build_topic,
    set_topic,
    simple_attribute_add,
    simple_entry_attribute,
    translate_all_to_abbreviations,
)

_LOGGER = logging.getLogger(__name__)


class Discovery:
    """Manage discovery publication for MQTT Discovery Statestream."""

    def __init__(self, hass: HomeAssistant, conf) -> None:
        """Initiate discovery."""
        self._hass = hass
        self._conf = conf
        self.discovery_classes = {}
        self.discovered_entities = []
        self._subscribed = []
        self._publish_retain: bool = conf.get(CONF_PUBLISH_RETAIN)
        self._command_topic = set_topic(conf, CONF_COMMAND_TOPIC)
        (
            self._local_status,
            self._local_status_topic,
            self._local_online_status,
            self._local_offline_status,
        ) = self._set_local_status()

        self._has_includes = bool(conf.get(CONF_INCLUDE))
        self._dev_reg = dr.async_get(hass)
        self._ent_reg = er.async_get(hass)
        self._discovery_topic = set_topic(conf, CONF_DISCOVERY_TOPIC)
        self.subscribe_possible = False
        self._error_domain = []
        self._unique_prefix = self._conf.get(CONF_UNIQUE_PREFIX)
        self._availability_mode = self._conf.get(CONF_AVAILABILITY_MODE)

    async def async_discovery_publish(self, entity_id, attributes, mybase):
        """Publish Discovery information for entitiy."""
        mycommand = f"{self._command_topic}{entity_id.replace('.', '/')}"
        ent_parts = entity_id.split(".")
        ent_domain = ent_parts[0]

        if ent_domain not in SUPPORTED_ENTITY_TYPE_COMMANDS:
            if ent_domain not in self._error_domain:
                _LOGGER.error("Entity type not supported - %s", entity_id)
                self._error_domain.append(ent_domain)
            return False

        if (
            ent_domain in [Platform.BINARY_SENSOR, Platform.SENSOR]
            and not self._has_includes
            and ATTR_DEVICE_CLASS not in attributes
        ):
            return False

        entity_info = EntityInfo(mycommand, attributes, mybase, entity_id)

        if ent_domain not in self.discovery_classes:
            await self._hass.async_add_executor_job(
                self._build_discovery_class, ent_domain
            )
        entityclass = self.discovery_classes[ent_domain]
        config = self._build_base(entity_info, entityclass)

        if ent_domain not in self._subscribed and self.subscribe_possible:
            await entityclass.async_subscribe_commands()
            self._subscribed.append(ent_domain)

        result = entityclass.build_config(config, entity_info)
        if result is False:
            return False

        if device := self._build_device(entity_id):
            config[CONF_DEVICE] = device

        config[CONF_ORIGIN] = {
            CONF_NAME: DOMAIN,
        }

        self.discovered_entities.append(entity_id)

        entity_id = entityclass.translate_entity_type(entity_id, attributes)

        config = translate_all_to_abbreviations(config)

        encoded = json.dumps(config, cls=JSONEncoder)
        entity_disc_topic = (
            f"{self._discovery_topic}{entity_id.replace('.', '/')}/{ATTR_CONFIG}"
        )
        await mqtt.async_publish(
            self._hass, entity_disc_topic, encoded, 1, self._publish_retain
        )

        return True

    def _build_base(self, entity_info: EntityInfo, entityclass):
        ent_parts = entity_info.entity_id.split(".")
        availability = [{CONF_TOPIC: f"~/{CONF_AVAILABILITY}"}]
        if self._local_status:
            availability.append(
                {
                    CONF_TOPIC: self._local_status_topic,
                    CONF_PAYLOAD_AVAILABLE: self._local_online_status,
                    CONF_PAYLOAD_NOT_AVAILABLE: self._local_offline_status,
                }
            )

        uid = entityclass.translate_entity_type(
            entity_info.entity_id, entity_info.attributes
        )
        config = {
            CONF_TILDA: entity_info.mybase.removesuffix("/"),
            CONF_UNIQUE_ID: f"{self._unique_prefix}_{uid}",
            CONF_DEFAULT_ENTITY_ID: self._build_default_entity_id(
                entity_info.entity_id
            ),
            CONF_STATE_TOPIC: build_topic(ATTR_STATE),
            CONF_JSON_ATTRS_TOPIC: build_topic(ATTR_ATTRIBUTES),
            CONF_AVAILABILITY: availability,
            CONF_AVAILABILITY_MODE: self._availability_mode,
        }
        name = None
        if ATTR_FRIENDLY_NAME in entity_info.attributes:
            name = entity_info.attributes[ATTR_FRIENDLY_NAME]
        else:
            name = ent_parts[1].replace("_", " ").title()
        if entry := self._ent_reg.async_get(entity_info.entity_id):
            if entry.device_id and name:
                device = self._dev_reg.async_get(entry.device_id)
                if device and name.startswith(device.name):
                    name = name[len(device.name) + 1 :].strip()
                    if name == "":
                        name = None
            simple_entry_attribute(config, entry.entity_category, CONF_ENTITY_CATEGORY)
            simple_entry_attribute(
                config, entry.original_device_class, CONF_DEVICE_CLASS
            )
            simple_entry_attribute(config, entry.device_class, CONF_DEVICE_CLASS)
        config[CONF_NAME] = name

        simple_attribute_add(
            config,
            entity_info.attributes,
            ATTR_UNIT_OF_MEASUREMENT,
            CONF_UNIT_OF_MEASUREMENT,
        )
        simple_attribute_add(config, entity_info.attributes, ATTR_ICON, ATTR_ICON)
        simple_attribute_add(
            config, entity_info.attributes, ATTR_ENTITY_PICTURE, CONF_ENTITY_PICTURE
        )

        return config

    def _build_default_entity_id(self, entity_id):
        """Add the source namespace to a default entity ID when configured."""

        if ent_prefix := self._conf.get(CONF_UNIQUE_ENTITY_PREFIX):
            domain, output_id = entity_id.split(".", 1)
            return f"{domain}.{ent_prefix}_{output_id}"

        return entity_id

    def _build_device(self, entity_id):  # sourcery skip: extract-method
        config_device = {}
        entry = self._ent_reg.async_get(entity_id)
        if entry and entry.device_id:
            if device := self._dev_reg.async_get(entry.device_id):
                simple_entry_attribute(
                    config_device, device.manufacturer, CONF_MANUFACTURER
                )
                simple_entry_attribute(config_device, device.model, CONF_MODEL)
                if device.name_by_user:
                    simple_entry_attribute(
                        config_device, device.name_by_user, CONF_NAME
                    )
                else:
                    simple_entry_attribute(config_device, device.name, CONF_NAME)
                simple_entry_attribute(
                    config_device, device.sw_version, CONF_SW_VERSION
                )
                simple_entry_attribute(
                    config_device, device.connections, CONF_CONNECTIONS
                )
                if device.identifiers:
                    config_device[CONF_IDENTIFIERS] = [
                        deviceid[1] for deviceid in device.identifiers
                    ]

        return config_device

    def _set_local_status(self):
        local_status = self._conf.get(CONF_LOCAL_STATUS)
        local_status_topic = None
        local_online_status = None
        local_offline_status = None
        if local_status:
            local_status_topic = local_status.get(CONF_TOPIC) or self._conf.get(
                CONF_BASE_TOPIC
            )
            local_online_status = local_status.get(CONF_ONLINE_STATUS)
            local_offline_status = local_status.get(CONF_OFFLINE_STATUS)
            if not local_status_topic.endswith("/status"):
                local_status_topic = f"{local_status_topic}/status"

        return (
            local_status,
            local_status_topic,
            local_online_status,
            local_offline_status,
        )

    def _build_discovery_class(self, entity_type):
        """Build the discovery class."""
        modulename = __name__.removesuffix(".discovery")
        module = importlib.import_module(f".classes.{entity_type}", package=modulename)

        publish_state = module.DiscoveryItem.PUBLISH_STATE

        module_class = module.DiscoveryItem(
            self._hass,
            self._conf.get(CONF_BASE_TOPIC),
            self._command_topic,
            self._publish_retain,
            self.discovered_entities,
            module.DiscoveryItem.PLATFORM,
            publish_state,
        )
        self.discovery_classes[entity_type] = module_class

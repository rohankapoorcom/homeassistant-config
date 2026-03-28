"""Utilities for MQTT Discovery Stream."""

import logging
from dataclasses import dataclass, field

from .const import (
    CONF_BASE_TOPIC,
    OUTPUT_ENTITIES,
)

_LOGGER = logging.getLogger(__name__)


def set_topic(conf, topic):
    """Create the topic string."""
    response_topic = conf.get(topic) or conf.get(CONF_BASE_TOPIC)
    if not response_topic.endswith("/"):
        response_topic = f"{response_topic}/"
    return response_topic


def translate_entity_type(entity_id):
    """Translate the entity type to the output type."""
    ent_parts = entity_id.split(".")
    if ent_parts[0] in OUTPUT_ENTITIES:
        output_entity = OUTPUT_ENTITIES[ent_parts[0]]
    else:
        output_entity = ent_parts[0]
    return f"{output_entity}.{ent_parts[1]}"


def simple_attribute_add(config, attributes, attribute_name, conf_name=None):
    """Simple check for attribute existence and inclusion."""
    if attribute_name in attributes:
        config[conf_name or attribute_name] = attributes[attribute_name]


def simple_entry_attribute(config_device, attribute, conf_name):
    """Simple check for attribute existence and inclusion."""
    if attribute:
        config_device[conf_name] = attribute


@dataclass
class EntityInfo:
    """Information for an entity."""

    mycommand: str = field(init=True, repr=True)
    attributes: str = field(init=True, repr=True)
    mybase: str = field(init=True, repr=True)
    entity_id: str = field(init=True, repr=True)


def add_config_command(config, entity_info: EntityInfo, confname, confvalue):
    """Add relevant commands to discovery config."""
    config[confname] = f"{entity_info.mycommand}/{confvalue}"


def build_topic(attrname):
    """Build a standard topic."""
    return f"~/{attrname}"

"""Utilities for MQTT Discovery Stream."""

from dataclasses import dataclass, field
from typing import Any

from homeassistant.components.mqtt.abbreviations import (
    ABBREVIATIONS,
    DEVICE_ABBREVIATIONS,
    ORIGIN_ABBREVIATIONS,
)
from homeassistant.components.mqtt.const import CONF_AVAILABILITY, CONF_ORIGIN
from homeassistant.const import CONF_DEVICE

from .const import CONF_BASE_TOPIC

ABBREVIATIONS_KEYS = list(ABBREVIATIONS.keys())
ABBREVIATIONS_VALUES = list(ABBREVIATIONS.values())
ORIGIN_ABBREVIATIONS_KEYS = list(ORIGIN_ABBREVIATIONS.keys())
ORIGIN_ABBREVIATIONS_VALUES = list(ORIGIN_ABBREVIATIONS.values())
DEVICE_ABBREVIATIONS_KEYS = list(DEVICE_ABBREVIATIONS.keys())
DEVICE_ABBREVIATIONS_VALUES = list(DEVICE_ABBREVIATIONS.values())


def set_topic(conf, topic):
    """Create the topic string."""
    response_topic = conf.get(topic) or conf.get(CONF_BASE_TOPIC)
    if not response_topic.endswith("/"):
        response_topic = f"{response_topic}/"
    return response_topic


def simple_attribute_add(config, attributes, attribute_name, conf_name=None):
    """Do simple check for attribute existence and inclusion."""
    if attribute_name in attributes:
        config[conf_name or attribute_name] = attributes[attribute_name]


def simple_entry_attribute(config_device, attribute, conf_name):
    """Do simple check for attribute existence and inclusion."""
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


def translate_all_to_abbreviations(
    payload: dict[str, Any] | str,
) -> None:
    """Use abbreviations in an MQTT discovery payload."""
    if CONF_ORIGIN in payload:
        payload[CONF_ORIGIN] = _translate_to_abbreviations(
            payload[CONF_ORIGIN], ORIGIN_ABBREVIATIONS_KEYS, ORIGIN_ABBREVIATIONS_VALUES
        )
    if CONF_DEVICE in payload:
        payload[CONF_DEVICE] = _translate_to_abbreviations(
            payload[CONF_DEVICE], DEVICE_ABBREVIATIONS_KEYS, DEVICE_ABBREVIATIONS_VALUES
        )
    if CONF_AVAILABILITY in payload:
        topics = []
        for topic in payload[CONF_AVAILABILITY]:
            topic = _translate_to_abbreviations(
                topic, ABBREVIATIONS_KEYS, ABBREVIATIONS_VALUES
            )
            topics.append(topic)
        payload[CONF_AVAILABILITY] = topics

    return _translate_to_abbreviations(
        payload, ABBREVIATIONS_KEYS, ABBREVIATIONS_VALUES
    )


def _translate_to_abbreviations(
    payload: dict[str, Any] | str, abbreviations_keys, abbreviations_values
) -> None:
    """Translate specific set of abbreviations."""
    if not isinstance(payload, dict):
        return None
    return_payload = {}
    for key in payload:
        keyvalue = key
        if key in abbreviations_values:
            keyvalue = abbreviations_keys[abbreviations_values.index(key)]
        return_payload[keyvalue] = payload[key]

    return return_payload

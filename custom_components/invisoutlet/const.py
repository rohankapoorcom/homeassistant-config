"""Constants for the InvisOutlet integration."""

from __future__ import annotations

from homeassistant.const import Platform

DOMAIN = "invisoutlet"

PLATFORMS = [
    Platform.BINARY_SENSOR,
    Platform.BUTTON,
    Platform.LIGHT,
    Platform.NUMBER,
    Platform.SELECT,
    Platform.SENSOR,
    Platform.SWITCH,
    Platform.UPDATE,
]

# The single InvisOutlet hub entry owns every outlet. Its data holds
# CONF_OUTLETS: a {serial: {host, ...}} map; setup creates one coordinator +
# device per outlet, all grouped under one "InvisOutlet" subentry.
CONF_ENTRY_TYPE = "entry_type"
ENTRY_TYPE_HUB = "hub"
SUBENTRY_AURA_EFFECT = "aura_effect"
# Hub grouping subentry holding all outlet devices. Created programmatically (no
# flow registered), so outlets group under one "InvisOutlet" row with no button.
SUBENTRY_OUTLET = "outlet"
CONF_OUTLETS = "outlets"
# Per-outlet keys under CONF_OUTLETS[serial]: the device name and area chosen in
# the add flow, applied when the device is first registered.
CONF_AREA = "area"
# Per-outlet map under CONF_OUTLETS[serial]: {light selector: effect_id} — the
# Aura effect selected on each physical color light. Stored in the entry (not
# RestoreEntity) so it survives the frequent reloads from adding/editing effects.
CONF_COLOR_EFFECTS = "color_effects"
# Key under the shared Aura Effects subentry's data: {effect_id: {name}}.
CONF_EFFECTS = "effects"

# Aura effect-mode select option machine values for the two static variants
# (plain HSV color vs. white color-temperature). Labels live in strings.json.
EFFECT_STATIC_COLOR = "static_color"
EFFECT_STATIC_TEMPERATURE = "static_temperature"

# The hardware maker; the product/model is "InvisOutlet".
MANUFACTURER = "Intecular"

# The "device" field of an outlet's mDNS TXT record. An attached faceplate rides
# along in the same record as sub_device, but advertises a service of its own
# while updating over its own Wi-Fi, reporting its own serial as "sn".
MODEL_OUTLET = "InvisOutlet"

# How the attached faceplate's firmware is delivered, stored per-outlet under
# CONF_OUTLETS[serial]. The value is the device method (callback 21 arg 1):
# 0 = over the faceplate's own Wi-Fi (default), 1 = via the InvisOutlet.
CONF_SUB_DEVICE_UPDATE_METHOD = "sub_device_update_method"
DEFAULT_SUB_DEVICE_UPDATE_METHOD = 0

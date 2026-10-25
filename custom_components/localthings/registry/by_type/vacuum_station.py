"""Stick-vacuum clean/auto-empty station device registry (issues #131 / #219).

Station dustbag/dustbin/UV-sanitize state plus, when present (VS9700),
wand battery/charging via `/status/stick/vs/0`. No suction/room-map control.
"""

from ..capabilities import common, ignored, vacuum_station
from ..capability import Capability
from ._base import DeviceRegistry, _build

REGISTRY = DeviceRegistry(
    name="vacuum_station",
    capabilities=_build(
        [
            *ignored.IGNORED,
            *common.UNIVERSAL,
            *common.POWER,
            vacuum_station.DUSTBAG,
            vacuum_station.DUSTBAG_USAGE,
            vacuum_station.DUSTBIN_SETTING,
            vacuum_station.CLEANSTATION_STATUS,
            vacuum_station.STICK_BODY,
            vacuum_station.LIGHTING,
            vacuum_station.DND,
            # AI cleaning mode: this VS9700 reports 'not supporting'
            # (issue #478), so there are no real supported values to model
            # a select/switch from yet. Ignored here rather than guessed;
            # revisit when a dump from a unit that supports it surfaces the
            # actual mode vocabulary.
            Capability(href="/mode/ai/vs/0"),
            # Phone-notification plumbing the station mirrors from the app
            # (incoming call / message contexts, and the stick-operation
            # notification toggle) -- not home-automation state.
            Capability(href="/notification/context/vs/0"),
            Capability(href="/notification/context/stick/operation/vs/0"),
        ]
    ),
)

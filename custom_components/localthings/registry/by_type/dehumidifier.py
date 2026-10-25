"""Dehumidifier device registry (Samsung TP1X_DA_AC_DHM-class, issue #88).

Shares the DA_AC_ board family with airconditioner.py (power, air filter,
auto-clean, mute-once all use the identical resource shapes), so those three
Capability objects are reused directly rather than duplicated. The
TP1X_DA_AC_DHM_01001_0000 revision (issues #271/#231) also reports
air_purifier.py's screen-on/off resource on the identical href/shape, so
that's reused too rather than re-defined.
"""

from ..capabilities import air_purifier, airconditioner, common, dehumidifier, ignored
from ._base import DeviceRegistry, _build

REGISTRY = DeviceRegistry(
    name="dehumidifier",
    capabilities=_build(
        [
            *ignored.IGNORED,
            *common.UNIVERSAL,
            *common.POWER,
            dehumidifier.MODE,
            dehumidifier.HUMIDITY,
            dehumidifier.WATERTANK_LIGHTING,
            airconditioner.AUTO_CLEAN,
            airconditioner.AIR_FILTER,
            airconditioner.MUTE_ONCE,
            air_purifier.DISPLAY,
            *dehumidifier.COVERAGE,
        ]
    ),
)

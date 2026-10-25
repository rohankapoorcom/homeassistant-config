"""Capabilities specific to the AirDresser family (Samsung DA_DF-class,
issues #162/#157).

This board family carried no /information/vs/0 token any existing family
routed on, so it gets its own device type (the 'DF' board token) -- but most
of the resources it exposes are already handled by the shared laundry
machinery:

  /washer/vs/0    -> AIR_DRESSER_SETTINGS (wrinkle_prevent only -- a
                      dedicated capability rather than reusing
                      dryer.DRYER_SETTINGS wholesale: this board never
                      populates dryLevel/dryTime/dryerType at all, and
                      those are permanently-empty-not-just-absent
                      dryer-only fields on an AirDresser, not merely unset
                      ones, so binding them here would ship three sensors
                      that can never read anything on this device type)
  /course/vs/0    -> AIR_DRESSER_COURSE (cycle select), table id from
                      /st/airdressercourse/vs/0 (issue #157's
                      DA_DF_TP2_20_COMMON reports "Table_00"; issue #162's
                      DA_DF_A51_20_COMMON has no table resource at all and
                      falls back to the name-only 'cycle' key, same as an
                      unrecognized table on washer/dryer). Options come
                      from laundry.cycle_options -- #157's board populates
                      /wm/editcourse/vs/0's editCourseList directly; #162's
                      has no editcourse resource at all and falls through
                      to cycle_options' supportedOptions decode instead.
                      Course names aren't identified yet for either table
                      (no code->name mapping was reported), so they render
                      as their raw codes until named in translations, same
                      as dryer.py's unidentified codes.
  /diagnosis/vs/0 -> reuses dishwasher.DIAGNOSIS
  /airdresseroption/sanitize/vs/0 -> AIR_DRESSER_SANITIZE (issue #157 only;
                      #162's board doesn't report this resource at all)
"""

from ..capability import Capability
from ..entities import SwitchDesc
from .laundry import cycle_select


def _wrinkle_write(p, rep, href=None):
    if p not in ("On", "Off"):
        return None
    return ["washer", "vs", "0"], {"x.com.samsung.da.wrinklePrevent": p}


def _sanitize_write(p, rep, href=None):
    if p not in ("On", "Off"):
        return None
    return ["airdresseroption", "sanitize", "vs", "0"], {"x.com.samsung.da.sanitize": p}


AIR_DRESSER_SETTINGS = Capability(
    href="/washer/vs/0",
    poll_tier="warm",
    entities=(
        SwitchDesc(
            key="wrinkle_prevent",
            field="x.com.samsung.da.wrinklePrevent",
            icon="mdi:iron",
            value_fn=lambda v: v == "On",
            write_fn=_wrinkle_write,
        ),
    ),
)

AIR_DRESSER_COURSE = Capability(
    href="/course/vs/0",
    entities=(
        cycle_select(
            translation_key="air_dresser_cycle",
            icon="mdi:tshirt-crew",
            table_href="/st/airdressercourse/vs/0",
        ),
    ),
)

AIR_DRESSER_SANITIZE = Capability(
    href="/airdresseroption/sanitize/vs/0",
    poll_tier="warm",
    entities=(
        SwitchDesc(
            key="sanitize",
            field="x.com.samsung.da.sanitize",
            icon="mdi:weather-sunny",
            value_fn=lambda v: v == "On",
            write_fn=_sanitize_write,
        ),
    ),
)

"""Per-effect behavior for the Aura effect templates.

Each mode owns everything mode-specific — its pixel layout (names, which pixels
are active, which are forced on, and whether each is HS / temperature /
brightness-only), whether the speed and random controls apply, and how the
template's state is pushed to a physical color light. The layout can depend on
the per-effect "random" toggle. The virtual entities and the Color Light
resolver consult this registry instead of branching on the mode inline, so
adding or changing an effect touches one place.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable, Sequence
from dataclasses import dataclass
from enum import Enum
from typing import Any

from invisoutlet import ColorEffect

from .const import EFFECT_STATIC_COLOR, EFFECT_STATIC_TEMPERATURE

# How many virtual pixels an effect device exposes.
PIXEL_COUNT = 9


class PixelKind(str, Enum):
    """What a pixel controls."""

    HS = "hs"
    TEMPERATURE = "temperature"
    BRIGHTNESS = "brightness"


@dataclass(frozen=True)
class PixelSpec:
    """One active pixel's role in a mode (its layout entry)."""

    name: str
    kind: PixelKind = PixelKind.HS
    forced_on: bool = False


@dataclass(frozen=True)
class PixelState:
    """One active pixel's resolved template state (brightness is 0-100)."""

    on: bool
    hue: int
    saturation: int
    brightness: int
    temperature: int


@dataclass(frozen=True)
class ApplyContext:
    """What an effect mode needs to push itself to a physical color light."""

    coordinator: Any
    light: int
    pixels: Sequence[PixelState]
    speed: float
    random: bool


ApplyFn = Callable[[ApplyContext], Awaitable[None]]
LayoutFn = Callable[[bool], tuple[PixelSpec, ...]]


@dataclass(frozen=True)
class EffectMode:
    """One effect mode and everything specific to it."""

    value: str
    apply: ApplyFn
    # Active pixels (and their roles) given the current "random" toggle; the
    # rest are grayed out.
    layout: LayoutFn
    # The device's mode int this effect drives (1 static HSV, 2 static temp,
    # 3-7 = ColorEffect). Used to tell whether the device is running us.
    device_mode: int
    has_speed: bool = True
    has_random: bool = False

    def pixels(self, random: bool) -> tuple[PixelSpec, ...]:
        """The active pixel specs for the current random state."""
        return self.layout(random)

    def spec(self, index: int, random: bool) -> PixelSpec | None:
        """The spec for pixel ``index``, or None if it isn't active."""
        specs = self.layout(random)
        return specs[index] if index < len(specs) else None


def _fixed(*specs: PixelSpec) -> LayoutFn:
    """A layout that ignores the random toggle."""
    return lambda _random: specs


# --- payloads -------------------------------------------------------------


async def _apply_static_color(ctx: ApplyContext) -> None:
    """Static (Color): a single HSV color across the whole array."""
    pixel = ctx.pixels[0]
    await ctx.coordinator.async_set_color_hsv(
        ctx.light,
        hue=pixel.hue,
        saturation=pixel.saturation,
        brightness=pixel.brightness,
        on=pixel.on,
    )


async def _apply_static_temperature(ctx: ApplyContext) -> None:
    """Static (Temperature): a per-LED white color-temperature."""
    await ctx.coordinator.async_set_temperature_pixels(
        ctx.light,
        temperatures=[p.temperature for p in ctx.pixels],
        brightness=[p.brightness for p in ctx.pixels],
        states=[p.on for p in ctx.pixels],
    )


def _randomizable_apply(effect: ColorEffect) -> ApplyFn:
    """Animated effect over only the lit pixels, with speed/randomize/level."""

    async def _apply(ctx: ApplyContext) -> None:
        lit = [p for p in ctx.pixels if p.on]
        await ctx.coordinator.async_set_effect_pixels(
            ctx.light,
            colors=[(p.hue, p.saturation) for p in lit],
            brightness=[p.brightness for p in lit],
            effect=effect,
            speed=int(ctx.speed),
            randomize=ctx.random,
            level=ctx.pixels[0].brightness,
        )

    return _apply


# --- layouts --------------------------------------------------------------

_TEMP_PIXELS = tuple(
    PixelSpec(f"Pixel {i + 1}", PixelKind.TEMPERATURE) for i in range(PIXEL_COUNT)
)


def _randomizable_layout(required: int = 1) -> LayoutFn:
    """Random: a single brightness pixel (device picks colors); otherwise nine
    color pixels with the first ``required`` forced on.
    """

    def layout(random: bool) -> tuple[PixelSpec, ...]:
        if random:
            return (PixelSpec("Brightness", PixelKind.BRIGHTNESS, forced_on=True),)
        return tuple(
            PixelSpec(f"Color {i + 1}", forced_on=i < required)
            for i in range(PIXEL_COUNT)
        )

    return layout


def _starry_night_layout(random: bool) -> tuple[PixelSpec, ...]:
    """Random: a single brightness pixel; otherwise a Background + Stars pair."""
    if random:
        return (PixelSpec("Brightness", PixelKind.BRIGHTNESS, forced_on=True),)
    return (
        PixelSpec("Background", forced_on=True),
        PixelSpec("Stars", forced_on=True),
    )


EFFECT_MODES: dict[str, EffectMode] = {
    EFFECT_STATIC_COLOR: EffectMode(
        value=EFFECT_STATIC_COLOR,
        apply=_apply_static_color,
        layout=_fixed(PixelSpec("Color", forced_on=True)),
        device_mode=1,
        has_speed=False,
    ),
    EFFECT_STATIC_TEMPERATURE: EffectMode(
        value=EFFECT_STATIC_TEMPERATURE,
        apply=_apply_static_temperature,
        layout=_fixed(*_TEMP_PIXELS),
        device_mode=2,
        has_speed=False,
    ),
    "breathing": EffectMode(
        "breathing",
        apply=_randomizable_apply(ColorEffect.BREATHING),
        layout=_randomizable_layout(1),
        device_mode=int(ColorEffect.BREATHING),
        has_random=True,
    ),
    "strobing": EffectMode(
        "strobing",
        apply=_randomizable_apply(ColorEffect.STROBING),
        layout=_randomizable_layout(1),
        device_mode=int(ColorEffect.STROBING),
        has_random=True,
    ),
    "color_cycle": EffectMode(
        "color_cycle",
        apply=_randomizable_apply(ColorEffect.COLOR_CYCLE),
        layout=_randomizable_layout(2),
        device_mode=int(ColorEffect.COLOR_CYCLE),
        has_random=True,
    ),
    "rainbow": EffectMode(
        "rainbow",
        apply=_randomizable_apply(ColorEffect.RAINBOW),
        layout=_randomizable_layout(1),
        device_mode=int(ColorEffect.RAINBOW),
        has_random=True,
    ),
    "starry_night": EffectMode(
        "starry_night",
        apply=_randomizable_apply(ColorEffect.STARRY_NIGHT),
        layout=_starry_night_layout,
        device_mode=int(ColorEffect.STARRY_NIGHT),
        has_random=True,
    ),
}

DEFAULT_MODE = EFFECT_MODES[EFFECT_STATIC_COLOR]


def get_effect_mode(value: str) -> EffectMode:
    """Return the mode definition for ``value`` (falling back to Static Color)."""
    return EFFECT_MODES.get(value, DEFAULT_MODE)


# Device mode int -> a human effect-type label (e.g. 6 -> "Rainbow"), for naming
# an externally-set effect we can't map to a specific template.
_MODE_LABELS = {
    mode.device_mode: mode.value.replace("_", " ").title()
    for mode in EFFECT_MODES.values()
}


def mode_label(device_mode: int) -> str | None:
    """A human effect-type name for a device mode int, or None if unknown."""
    return _MODE_LABELS.get(device_mode)

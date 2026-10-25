"""Reuse the companion app's native Matter commissioning to onboard outlets.

An InvisOutlet is a Matter-over-Wi-Fi device that only speaks Matter long
enough to receive Wi-Fi credentials; afterwards it is driven entirely over its
own websocket API. The HA companion app can run the phone's native Matter
commissioning flow (which provisions Wi-Fi) when the frontend fires a
``matter/commission`` external-bus message. The app then calls back to HA over
the websocket API with the setup code.

The ``matter/commission`` websocket command is owned by the core Matter
integration. When Matter is installed it commissions the device into HA's
fabric; when it is not, the command does not exist and the app reports a
spurious failure. Using the generic interceptor in :mod:`.ws_intercept` we wrap
that command so we can:

* decode the setup code, resolve the device's IP from its ``_matterc._udp``
  advertisement (matched by discriminator), and confirm it also announces
  ``_invis._tcp`` — i.e. it is one of ours;
* handle ours ourselves (the phone already provisioned Wi-Fi; we just need the
  IP to start our own onboarding), acknowledging the app so no error is shown;
* delegate anything that is not ours to the real Matter handler, unchanged.
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import asdict, dataclass
from typing import Any

import voluptuous as vol
from homeassistant.components import websocket_api
from homeassistant.components import zeroconf as ha_zeroconf
from homeassistant.core import HomeAssistant, callback
from zeroconf import IPVersion, ServiceStateChange, Zeroconf
from zeroconf.asyncio import AsyncServiceBrowser, AsyncServiceInfo

from .const import DOMAIN
from .ws_intercept import async_delegate, async_intercept_command

_LOGGER = logging.getLogger(__name__)

MATTER_DOMAIN = "matter"
COMMISSION_COMMAND = "matter/commission"

MATTER_COMMISSIONABLE_TYPE = "_matterc._udp.local."
INVIS_SERVICE_TYPE = "_invis._tcp.local."

# Fired when an outlet is provisioned via the app's Matter flow; carries the
# decoded setup code, the resolved IP, and whether it is one of ours.
EVENT_COMMISSIONED = f"{DOMAIN}_commissioned"

# Fired when the companion app reports the native flow finished; carries the
# phone-set device name. Relayed from the frontend via FINISHED_COMMAND below,
# because matter/commission/finish only reaches the app webview, not the server.
EVENT_COMMISSION_FINISHED = f"{DOMAIN}_commission_finished"
FINISHED_COMMAND = f"{DOMAIN}/commission_finished"

BASE38_CHARSET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-."


@dataclass
class SetupPayload:
    """Decoded fields of a Matter QR setup code."""

    version: int
    vendor_id: int
    product_id: int
    commissioning_flow: int
    discovery_capabilities: int
    discriminator: int
    passcode: int


def _base38_decode(payload: str) -> bytes:
    """Decode Matter's base38 encoding (5 chars -> 3 bytes, little-endian)."""
    out = bytearray()
    for i in range(0, len(payload), 5):
        chunk = payload[i : i + 5]
        value = 0
        for char in reversed(chunk):
            value = value * 38 + BASE38_CHARSET.index(char)
        out += value.to_bytes({5: 3, 4: 2, 2: 1}[len(chunk)], "little")
    return bytes(out)


def parse_setup_code(code: str) -> SetupPayload:
    """Decode a Matter QR setup code (``MT:...``) into its fields."""
    if not code.startswith("MT:"):
        raise ValueError(f"not a Matter QR setup code: {code!r}")
    data = _base38_decode(code[3:])
    if len(data) < 11:
        raise ValueError("setup payload too short")
    value = int.from_bytes(data[:11], "little")
    return SetupPayload(
        version=value & 0x7,
        vendor_id=(value >> 3) & 0xFFFF,
        product_id=(value >> 19) & 0xFFFF,
        commissioning_flow=(value >> 35) & 0x3,
        discovery_capabilities=(value >> 37) & 0xFF,
        discriminator=(value >> 45) & 0xFFF,
        passcode=(value >> 57) & 0x7FFFFFF,
    )


async def _async_browse_match(
    hass: HomeAssistant,
    service_type: str,
    predicate,
    timeout: float,
) -> AsyncServiceInfo | None:
    """Browse a zeroconf service type until an advertisement matches predicate."""
    aiozc = await ha_zeroconf.async_get_async_instance(hass)
    result: asyncio.Future[AsyncServiceInfo] = (
        asyncio.get_running_loop().create_future()
    )

    async def _query(name: str) -> None:
        info = AsyncServiceInfo(service_type, name)
        if (
            await info.async_request(aiozc.zeroconf, 3000)
            and predicate(info)
            and not result.done()
        ):
            result.set_result(info)

    def _on_change(
        zeroconf: Zeroconf,
        service_type: str,
        name: str,
        state_change: ServiceStateChange,
    ) -> None:
        if state_change is not ServiceStateChange.Removed:
            hass.async_create_task(_query(name))

    browser = AsyncServiceBrowser(aiozc.zeroconf, service_type, handlers=[_on_change])
    try:
        return await asyncio.wait_for(asyncio.shield(result), timeout)
    except TimeoutError:
        return None
    finally:
        await browser.async_cancel()


async def async_find_commissionable_ip(
    hass: HomeAssistant, discriminator: int, timeout: float = 15.0
) -> str | None:
    """Find the IP of the device advertising ``_matterc._udp`` with this discriminator."""
    expected = str(discriminator).encode()
    info = await _async_browse_match(
        hass,
        MATTER_COMMISSIONABLE_TYPE,
        lambda info: info.properties.get(b"D") == expected,
        timeout,
    )
    if info is None:
        return None
    addresses = info.parsed_addresses(IPVersion.V4Only) or info.parsed_addresses()
    return addresses[0] if addresses else None


async def async_invis_serial_at_ip(
    hass: HomeAssistant, ip: str, timeout: float = 5.0
) -> str | None:
    """Return the InvisOutlet serial (mDNS ``sn``) advertised at ``ip``, if any.

    Doubles as the "is it one of ours" check — only InvisOutlets announce
    ``_invis._tcp`` — and hands back the serial the zeroconf flow keys on, so it
    can be claimed before the outlet is fully added.
    """
    info = await _async_browse_match(
        hass,
        INVIS_SERVICE_TYPE,
        lambda info: ip in info.parsed_addresses(),
        timeout,
    )
    if info is None:
        return None
    sn = info.properties.get(b"sn")
    return sn.decode() if sn else None


async def async_identify_commission(
    hass: HomeAssistant, code: str
) -> dict[str, Any]:
    """Decode a setup code and work out whether it belongs to one of our outlets.

    Returns a detail dict with the decoded payload, resolved ``ip``, and
    ``is_invisoutlet`` flag. Never raises: a bad code is reported via ``error``.
    """
    detail: dict[str, Any] = {
        "code": code,
        "ip": None,
        "serial": None,
        "is_invisoutlet": False,
    }
    try:
        payload = parse_setup_code(code)
    except ValueError as err:
        detail["error"] = str(err)
        return detail

    detail.update(asdict(payload))
    ip = await async_find_commissionable_ip(hass, payload.discriminator)
    detail["ip"] = ip
    if ip is not None:
        serial = await async_invis_serial_at_ip(hass, ip)
        detail["serial"] = serial
        detail["is_invisoutlet"] = serial is not None
    return detail


@websocket_api.require_admin
@websocket_api.websocket_command(
    {
        vol.Required("type"): COMMISSION_COMMAND,
        vol.Required("code"): str,
        vol.Optional("network_only"): bool,
    }
)
@websocket_api.async_response
async def _ws_commission(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Wrap ``matter/commission``: claim ours, delegate the rest to Matter."""
    detail = await async_identify_commission(hass, msg["code"])

    if not detail["is_invisoutlet"]:
        _LOGGER.debug(
            "matter/commission not ours (%s); delegating",
            detail.get("error") or f"ip={detail['ip']}",
        )
        async_delegate(hass, COMMISSION_COMMAND, connection, msg)
        return

    _LOGGER.info(
        "Onboarding InvisOutlet at %s via app Matter commissioning", detail["ip"]
    )
    hass.bus.async_fire(EVENT_COMMISSIONED, detail)
    connection.send_result(msg["id"])


@websocket_api.require_admin
@websocket_api.websocket_command(
    {
        vol.Required("type"): FINISHED_COMMAND,
        vol.Required("success"): bool,
        vol.Required("name"): vol.Any(str, None),
    }
)
@callback
def _ws_commission_finished(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Relay the app's matter/commission/finish (name) from commission_bridge.js."""
    hass.bus.async_fire(
        EVENT_COMMISSION_FINISHED,
        {"success": msg["success"], "name": msg["name"]},
    )
    connection.send_result(msg["id"])


@callback
def async_setup_interceptor(hass: HomeAssistant) -> None:
    """Start intercepting matter/commission for the life of HA."""
    async_intercept_command(
        hass, COMMISSION_COMMAND, _ws_commission, reassert_domain=MATTER_DOMAIN
    )
    websocket_api.async_register_command(hass, _ws_commission_finished)

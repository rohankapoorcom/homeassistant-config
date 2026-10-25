"""Make decoded CBOR safe to hand to a JSON serializer, and read it back.

The sibling of `redact.py`: that one makes device data safe to *share*,
this one makes it safe to *represent*. Every path that carries a device's
own data out of this integration -- the `read_resource`/`write_resource`
service responses, diagnostics downloads, the discovery snapshot store --
ends at a JSON encoder, and CBOR can decode to values JSON has no form
for. A byte string is the one that shows up in practice: the appliance's
usage history at `/file/transfer/vs/0` (issue #301) is 2-3 KB of binary,
and without this it cannot leave the device at all.

This is the second time an export path has silently lost a payload for
being the wrong shape. The first was a Collection's list body reading as
an empty `2.05 {}` (issue #335), fixed by carrying `body` alongside `rep`.
That fix was correct and stays; this module is the general form of the
lesson, so the third case is representable before anyone hits it.

Unrepresentable values become a self-describing marker dict rather than
being dropped or stringified, and `from_json_safe` turns the markers back
into the values they stand for. That round trip is the point: a
contributor can paste a blob straight out of a service response into a
test fixture's `probes` map and the parser under test sees real `bytes`.
"""

from __future__ import annotations

import base64
import datetime
import hashlib
from decimal import Decimal
from typing import Any

TYPE_KEY = "__localthings_type__"

# Inlined base64 stops here; `len` and `sha256` stay honest about the whole
# value. Generous for the few-KB histories this exists for, small enough
# that a board offering a firmware image can't turn a diagnostics download
# into a multi-megabyte file.
MAX_INLINE_BYTES = 64 * 1024


def _bytes_marker(raw: bytes, max_inline: int) -> dict[str, Any]:
    head = raw[:max_inline]
    marker: dict[str, Any] = {
        TYPE_KEY: "bytes",
        "len": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "base64": base64.b64encode(head).decode("ascii"),
    }
    if len(head) != len(raw):
        marker["truncated"] = True
    return marker


def json_safe(value: Any, *, max_inline_bytes: int = MAX_INLINE_BYTES) -> Any:
    """Return `value` with everything a JSON encoder would reject replaced
    by a marker dict, recursively.

    Cycles are possible in principle (CBOR value sharing, tags 28/29) and
    would otherwise recurse forever, so already-visited containers become a
    marker too.
    """
    return _walk(value, max_inline_bytes, set())


def _walk(value: Any, max_inline: int, seen: set[int]) -> Any:
    if value is None or isinstance(value, (str, bool, int)):
        return value

    if isinstance(value, float):
        # orjson renders these as `null`, which reads as "the device sent
        # nothing" rather than "the device sent something JSON can't hold".
        if value != value or value in (float("inf"), float("-inf")):
            return {TYPE_KEY: "float", "value": repr(value)}
        return value

    if isinstance(value, (bytes, bytearray, memoryview)):
        return _bytes_marker(bytes(value), max_inline)

    if isinstance(value, (dict, list, tuple, set, frozenset)):
        if id(value) in seen:
            return {TYPE_KEY: "cycle"}
        seen = seen | {id(value)}

    if isinstance(value, dict):
        # CBOR map keys need not be strings; JSON object keys must be. A
        # coerced key is marked so it can't be mistaken for one the device
        # actually sent as text.
        out = {}
        for key, item in value.items():
            safe_key = key if isinstance(key, str) else f"{TYPE_KEY}:{key!r}"
            out[safe_key] = _walk(item, max_inline, seen)
        return out

    if isinstance(value, (list, tuple, set, frozenset)):
        return [_walk(item, max_inline, seen) for item in value]

    if isinstance(value, (datetime.datetime, datetime.date, datetime.time)):
        return {TYPE_KEY: "datetime", "value": value.isoformat()}

    if isinstance(value, Decimal):
        return {TYPE_KEY: "decimal", "value": str(value)}

    tag = getattr(value, "tag", None)
    if tag is not None and hasattr(value, "value"):  # cbor2.CBORTag
        return {TYPE_KEY: "tag", "tag": tag, "value": _walk(value.value, max_inline, seen)}

    # Deliberately last, and deliberately not a raise: an export path
    # losing one field is recoverable, an export path raising loses the
    # whole report -- which is the failure this module exists to end.
    return {TYPE_KEY: "unrepresentable", "repr": repr(value)[:200]}


def from_json_safe(value: Any) -> Any:
    """Inverse of `json_safe` for the markers that round-trip losslessly.

    Only `bytes` does, and only when it wasn't truncated; every other
    marker describes a value JSON could not hold and is left as the marker
    dict it is. Written for test fixtures: a `probes` entry can carry a
    real blob as JSON and reach a parser as `bytes`.
    """
    if isinstance(value, list):
        return [from_json_safe(item) for item in value]
    if not isinstance(value, dict):
        return value
    if value.get(TYPE_KEY) == "bytes" and not value.get("truncated"):
        try:
            return base64.b64decode(value["base64"], validate=True)
        except (KeyError, ValueError, TypeError):
            return value
    return {key: from_json_safe(item) for key, item in value.items()}

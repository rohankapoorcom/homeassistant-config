"""Autolock timer subsystem.

Layered design:
    store.py     — Persistence. Owns the asyncio.Lock; atomic store ops.
    scheduler.py — Single async_call_later wrapper with awaitable cancel.
    timer.py     — Orchestration. Explicit state machine. The public API.

Public surface (importable from this package):
    AutolockTimer, TimerEntry, TimerState — orchestration + types
    TimerStore — persistence (one per coordinator)
    TIMER_STORAGE_VERSION, TIMER_STORAGE_KEY — Store wiring
"""

from .store import TIMER_STORAGE_KEY, TIMER_STORAGE_VERSION, TimerEntry, TimerStore
from .timer import AutolockTimer, TimerState

__all__ = [
    "TIMER_STORAGE_KEY",
    "TIMER_STORAGE_VERSION",
    "AutolockTimer",
    "TimerEntry",
    "TimerState",
    "TimerStore",
]

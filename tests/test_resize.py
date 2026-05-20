"""Tests for the on_resize SIGWINCH installer (POSIX only)."""

from __future__ import annotations

import os
import signal
import sys
import threading
import time

import pytest


@pytest.mark.skipif(
    sys.platform == "win32" or not hasattr(signal, "SIGWINCH"),
    reason="SIGWINCH is POSIX-only",
)
def test_on_resize_fires_and_can_be_removed() -> None:
    from codechu_term import on_resize

    fired = threading.Event()

    def cb() -> None:
        fired.set()

    remove = on_resize(cb)
    try:
        os.kill(os.getpid(), signal.SIGWINCH)
        # Generous timeout — signal delivery is async but usually <1ms.
        assert fired.wait(timeout=1.0), "callback did not fire"
    finally:
        remove()

    # After removal, our callback must not fire again. Re-arm and
    # send another SIGWINCH; the default disposition is ignore, so
    # nothing should set the event.
    fired.clear()
    os.kill(os.getpid(), signal.SIGWINCH)
    time.sleep(0.05)
    assert not fired.is_set()


@pytest.mark.skipif(
    sys.platform == "win32" or not hasattr(signal, "SIGWINCH"),
    reason="SIGWINCH is POSIX-only",
)
def test_on_resize_remover_restores_previous_handler() -> None:
    from codechu_term import on_resize

    sentinel: list[str] = []

    def previous_handler(_signum: int, _frame: object) -> None:
        sentinel.append("prev")

    old = signal.signal(signal.SIGWINCH, previous_handler)
    try:
        remove = on_resize(lambda: None)
        remove()
        # After removal the previous handler should be back.
        assert signal.getsignal(signal.SIGWINCH) is previous_handler
        os.kill(os.getpid(), signal.SIGWINCH)
        time.sleep(0.05)
        assert sentinel == ["prev"]
    finally:
        signal.signal(signal.SIGWINCH, old)

"""Tests for with_raw_mode. Most paths need a real TTY → skip when headless."""

from __future__ import annotations

import os
import sys

import pytest

from codechu_term import with_raw_mode


@pytest.mark.skipif(
    sys.platform == "win32", reason="with_raw_mode is POSIX-only"
)
def test_raw_mode_round_trip_on_pty() -> None:
    # Use os.openpty() so the test does not depend on the runner's stdin.
    pty = pytest.importorskip("pty")  # also confirms POSIX
    import termios

    master_fd, slave_fd = pty.openpty()
    try:
        before = termios.tcgetattr(slave_fd)
        with with_raw_mode(slave_fd) as fd:
            assert fd == slave_fd
            during = termios.tcgetattr(slave_fd)
            # In raw mode, ICANON and ECHO local-flag bits are cleared.
            assert not (during[3] & termios.ICANON)
            assert not (during[3] & termios.ECHO)
        after = termios.tcgetattr(slave_fd)
        assert after == before
    finally:
        os.close(slave_fd)
        os.close(master_fd)


@pytest.mark.skipif(
    sys.platform == "win32", reason="with_raw_mode is POSIX-only"
)
def test_raw_mode_restores_on_exception() -> None:
    pty = pytest.importorskip("pty")
    import termios

    master_fd, slave_fd = pty.openpty()
    try:
        before = termios.tcgetattr(slave_fd)
        with pytest.raises(RuntimeError):
            with with_raw_mode(slave_fd):
                raise RuntimeError("boom")
        after = termios.tcgetattr(slave_fd)
        assert after == before
    finally:
        os.close(slave_fd)
        os.close(master_fd)


@pytest.mark.skipif(
    sys.platform == "win32", reason="with_raw_mode is POSIX-only"
)
def test_raw_mode_rejects_non_tty_fd() -> None:
    import termios

    r, w = os.pipe()
    try:
        with pytest.raises(termios.error):
            with with_raw_mode(r):
                pass
    finally:
        os.close(r)
        os.close(w)

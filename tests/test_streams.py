"""Tests for is_tty, terminal_size, cursor / clear helpers."""

from __future__ import annotations

import io

import pytest

from codechu_term import (
    clear_line,
    clear_screen,
    hide_cursor,
    is_tty,
    show_cursor,
    terminal_size,
)


# --------------------------------------------------------------------- is_tty


def test_is_tty_none() -> None:
    assert is_tty(None) is False


def test_is_tty_stringio() -> None:
    assert is_tty(io.StringIO()) is False


def test_is_tty_truthy_isatty() -> None:
    class Fake:
        def isatty(self) -> bool:
            return True

    assert is_tty(Fake()) is True


def test_is_tty_swallows_exception() -> None:
    class Broken:
        def isatty(self) -> bool:
            raise RuntimeError("boom")

    assert is_tty(Broken()) is False


def test_is_tty_no_isatty_attr() -> None:
    class NoAttr:
        pass

    assert is_tty(NoAttr()) is False


# -------------------------------------------------------------- terminal_size


def test_terminal_size_env_fallback() -> None:
    # StringIO has no fileno, so we fall through to env.
    cols, rows = terminal_size(io.StringIO(), env={"COLUMNS": "120", "LINES": "40"})
    assert (cols, rows) == (120, 40)


def test_terminal_size_default_fallback() -> None:
    cols, rows = terminal_size(io.StringIO(), env={})
    assert (cols, rows) == (80, 24)


def test_terminal_size_ignores_garbage_env() -> None:
    cols, rows = terminal_size(io.StringIO(), env={"COLUMNS": "nope", "LINES": "-3"})
    assert (cols, rows) == (80, 24)


def test_terminal_size_partial_env_falls_to_default() -> None:
    # Both COLUMNS *and* LINES must be present for the env branch to fire.
    cols, rows = terminal_size(io.StringIO(), env={"COLUMNS": "100"})
    assert (cols, rows) == (80, 24)


def test_terminal_size_zero_env_rejected() -> None:
    cols, rows = terminal_size(io.StringIO(), env={"COLUMNS": "0", "LINES": "0"})
    assert (cols, rows) == (80, 24)


def test_terminal_size_fileno_exception_falls_through() -> None:
    class BadFileno:
        def fileno(self) -> int:
            raise OSError("no fd")

    cols, rows = terminal_size(BadFileno(), env={"COLUMNS": "77", "LINES": "33"})
    assert (cols, rows) == (77, 33)


# ----------------------------------------------------------- cursor / clears


@pytest.mark.parametrize(
    "func, seq",
    [
        (hide_cursor, "\x1b[?25l"),
        (show_cursor, "\x1b[?25h"),
        (clear_line, "\x1b[2K\r"),
        (clear_screen, "\x1b[2J\x1b[H"),
    ],
)
def test_emit_sequences(func, seq) -> None:  # type: ignore[no-untyped-def]
    buf = io.StringIO()
    func(buf)
    assert buf.getvalue() == seq


def test_emit_on_closed_stream_does_not_raise() -> None:
    buf = io.StringIO()
    buf.close()
    # Best-effort: must swallow the ValueError("I/O operation on closed file").
    hide_cursor(buf)
    clear_line(buf)

"""TTY checks, size queries, and stream-level ANSI helpers."""

from __future__ import annotations

import os
import sys
from typing import IO

__all__ = [
    "clear_line",
    "clear_screen",
    "hide_cursor",
    "is_tty",
    "show_cursor",
    "terminal_size",
]


def is_tty(stream: IO[str] | None) -> bool:
    """Return whether ``stream`` is a TTY. Swallows errors → ``False``.

    Accepts ``None`` and any object that may or may not implement
    ``isatty()``. A closed stream, a file-like wrapper without
    ``isatty``, or a raised exception all yield ``False``.
    """
    if stream is None:
        return False
    isatty = getattr(stream, "isatty", None)
    try:
        return bool(isatty and isatty())
    except Exception:
        return False


def _int_or_none(value: str | None) -> int | None:
    if value is None:
        return None
    try:
        n = int(value)
    except (TypeError, ValueError):
        return None
    return n if n > 0 else None


def terminal_size(
    stream: IO[str] | None = None,
    *,
    env: dict[str, str] | None = None,
) -> tuple[int, int]:
    """Return ``(cols, rows)`` for ``stream``.

    Resolution order:

    1. ``os.get_terminal_size(stream.fileno())`` when ``stream`` exposes
       a real ``fileno()`` attached to a TTY.
    2. ``COLUMNS`` and ``LINES`` from ``env`` (defaults to
       ``os.environ``).
    3. ``(80, 24)`` as a final fallback.

    Never raises.
    """
    if stream is None:
        stream = sys.stderr
    env_map = os.environ if env is None else env

    fd = None
    fileno = getattr(stream, "fileno", None)
    if callable(fileno):
        try:
            fd = fileno()
        except Exception:
            fd = None

    if fd is not None:
        try:
            size = os.get_terminal_size(fd)
            if size.columns > 0 and size.lines > 0:
                return (size.columns, size.lines)
        except (OSError, ValueError):
            pass

    cols = _int_or_none(env_map.get("COLUMNS"))
    rows = _int_or_none(env_map.get("LINES"))
    if cols is not None and rows is not None:
        return (cols, rows)

    return (80, 24)


def _write(stream: IO[str], data: str) -> None:
    try:
        stream.write(data)
        stream.flush()
    except Exception:
        # Best-effort: a closed or non-writable stream should not crash
        # callers that just want to "try to" emit a control sequence.
        pass


def hide_cursor(stream: IO[str] | None = None) -> None:
    """Emit DECTCEM cursor-hide (``\\x1b[?25l``) to ``stream``."""
    _write(stream if stream is not None else sys.stdout, "\x1b[?25l")


def show_cursor(stream: IO[str] | None = None) -> None:
    """Emit DECTCEM cursor-show (``\\x1b[?25h``) to ``stream``."""
    _write(stream if stream is not None else sys.stdout, "\x1b[?25h")


def clear_line(stream: IO[str] | None = None) -> None:
    """Erase the current line and return the carriage (``\\x1b[2K\\r``)."""
    _write(stream if stream is not None else sys.stdout, "\x1b[2K\r")


def clear_screen(stream: IO[str] | None = None) -> None:
    """Clear the screen and home the cursor (``\\x1b[2J\\x1b[H``)."""
    _write(stream if stream is not None else sys.stdout, "\x1b[2J\x1b[H")

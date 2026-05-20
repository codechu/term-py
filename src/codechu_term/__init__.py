"""codechu-term — stdlib-only terminal capability detection and control.

Re-exports:

- :func:`is_tty`         — robust ``isatty()`` wrapper.
- :func:`terminal_size`  — ``(cols, rows)`` with env/default fallback.
- :func:`capabilities`   — dict of detected terminal feature flags.
- :func:`with_alt_buffer` — context manager for the alt screen buffer.
- :func:`with_raw_mode`  — context manager for ``termios`` raw mode.
- :func:`on_resize`      — install a ``SIGWINCH`` handler; returns a remover.
- :func:`hide_cursor` / :func:`show_cursor` — DECTCEM cursor control.
- :func:`clear_line` / :func:`clear_screen` — ANSI clears.
"""

from __future__ import annotations

from .alt_buffer import with_alt_buffer
from .caps import capabilities
from .raw import with_raw_mode
from .resize import on_resize
from .streams import (
    clear_line,
    clear_screen,
    hide_cursor,
    is_tty,
    show_cursor,
    terminal_size,
)

__version__ = "0.1.0"

__all__ = [
    "__version__",
    "capabilities",
    "clear_line",
    "clear_screen",
    "hide_cursor",
    "is_tty",
    "on_resize",
    "show_cursor",
    "terminal_size",
    "with_alt_buffer",
    "with_raw_mode",
]

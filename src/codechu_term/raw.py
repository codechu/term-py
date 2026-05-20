"""``termios``-based raw-mode context manager (POSIX only)."""

from __future__ import annotations

import sys
from contextlib import contextmanager
from typing import Iterator

__all__ = ["with_raw_mode"]


@contextmanager
def with_raw_mode(fd: int | None = None) -> Iterator[int]:
    """Put file descriptor ``fd`` into raw mode for the block's lifetime.

    Uses :mod:`termios` + :mod:`tty`. The original terminal attributes
    are saved on entry and restored in a ``finally`` block — even on
    exception — so the terminal never gets stuck.

    POSIX only. Raises :class:`OSError` on Windows (the modules are
    unavailable) or when ``fd`` is not a real terminal descriptor.

    Yields the file descriptor so callers can ``os.read(fd, n)``
    without re-deriving it.
    """
    try:
        import termios
        import tty
    except ImportError as exc:  # pragma: no cover - non-POSIX only
        raise OSError("with_raw_mode requires POSIX termios/tty") from exc

    if fd is None:
        fd = sys.stdin.fileno()

    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        yield fd
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

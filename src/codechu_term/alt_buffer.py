"""Alt-screen-buffer context manager."""

from __future__ import annotations

import sys
from contextlib import contextmanager
from typing import IO, Iterator

__all__ = ["with_alt_buffer"]

_ENTER = "\x1b[?1049h"
_LEAVE = "\x1b[?1049l"


@contextmanager
def with_alt_buffer(stream: IO[str] | None = None) -> Iterator[IO[str]]:
    """Switch ``stream`` to the alt screen buffer for the block's lifetime.

    Emits ``\\x1b[?1049h`` on entry and ``\\x1b[?1049l`` on exit.
    The leave sequence is sent in a ``finally`` block so exceptions
    inside the ``with`` still restore the main buffer.

    Yields the stream so callers can write directly to it::

        with with_alt_buffer() as out:
            out.write("hello, alt buffer\\n")
            out.flush()
    """
    target = stream if stream is not None else sys.stdout
    target.write(_ENTER)
    target.flush()
    try:
        yield target
    finally:
        try:
            target.write(_LEAVE)
            target.flush()
        except Exception:
            # Stream may have been closed inside the block.
            pass

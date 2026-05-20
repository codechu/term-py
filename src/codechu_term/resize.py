"""``SIGWINCH`` resize-callback installer (POSIX only)."""

from __future__ import annotations

import signal
from typing import Callable

__all__ = ["on_resize"]


def on_resize(callback: Callable[[], None]) -> Callable[[], None]:
    """Install ``callback`` as a ``SIGWINCH`` handler.

    Returns a *remover* function — call it to restore the previous
    handler. The callback is invoked with no arguments; signal info
    is intentionally hidden because the only useful response is
    "re-query the terminal size".

    POSIX only. Raises :class:`OSError` on platforms without
    ``SIGWINCH`` (e.g. Windows).
    """
    sigwinch = getattr(signal, "SIGWINCH", None)
    if sigwinch is None:
        raise OSError("on_resize requires SIGWINCH (POSIX)")

    def _handler(_signum: int, _frame: object) -> None:
        callback()

    previous = signal.signal(sigwinch, _handler)

    def remove() -> None:
        signal.signal(sigwinch, previous)

    return remove

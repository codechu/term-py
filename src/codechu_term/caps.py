"""Terminal capability detection from env + stream state."""

from __future__ import annotations

import os
from typing import IO

from .streams import is_tty

__all__ = ["capabilities"]

# xterm-family TERM prefixes that we trust for mouse + alt-buffer support.
# Conservative on purpose — terminals that do not match still work; they
# just need to be added here or set ``COLORTERM=truecolor`` etc.
_XTERM_FAMILY = ("xterm", "screen", "tmux", "rxvt", "alacritty", "kitty", "wezterm")

_EMOJI_TERM_PROGRAMS = (
    "iTerm.app",
    "Apple_Terminal",
    "WezTerm",
    "kitty",
    "Hyper",
    "vscode",
)


def _is_xterm_family(term: str) -> bool:
    return any(term.startswith(prefix) for prefix in _XTERM_FAMILY)


def _has_utf8(*values: str) -> bool:
    for value in values:
        if not value:
            continue
        upper = value.upper()
        if "UTF-8" in upper or "UTF8" in upper:
            return True
    return False


def capabilities(
    stream: IO[str] | None = None,
    env: dict[str, str] | None = None,
) -> dict[str, bool]:
    """Return a dict of capability flags for ``stream`` + environment.

    Keys returned (all ``bool``):

    - ``color``     — ANSI 16-colour safe (TTY + ``TERM != "dumb"`` +
      no ``NO_COLOR``).
    - ``truecolor`` — 24-bit colour (``COLORTERM`` is ``truecolor`` /
      ``24bit``) and ``color`` is true.
    - ``unicode``   — locale advertises UTF-8 (``LC_ALL`` / ``LANG`` /
      ``LC_CTYPE``).
    - ``emoji``     — heuristic: ``unicode`` true and either
      ``TERM_PROGRAM`` looks like a modern emoji-capable emulator or
      ``TERM`` is in the xterm family.
    - ``mouse``     — TTY + xterm-family ``TERM``.
    - ``alt_buffer`` — xterm-family ``TERM`` (alt buffer is widely
      supported; does not require a TTY check because callers may
      pipe to a recorder).

    ``env`` is taken explicitly so callers control which environment
    they query. Pass ``env=os.environ`` for the live process env.
    """
    env_map = os.environ if env is None else env
    term = env_map.get("TERM", "") or ""
    colorterm = (env_map.get("COLORTERM", "") or "").lower()
    no_color = "NO_COLOR" in env_map
    term_program = env_map.get("TERM_PROGRAM", "") or ""

    tty = is_tty(stream)
    color = tty and term != "dumb" and not no_color
    truecolor = color and colorterm in {"truecolor", "24bit"}

    unicode_ok = _has_utf8(
        env_map.get("LC_ALL", "") or "",
        env_map.get("LC_CTYPE", "") or "",
        env_map.get("LANG", "") or "",
    )

    emoji = unicode_ok and (term_program in _EMOJI_TERM_PROGRAMS or _is_xterm_family(term))

    xterm_like = _is_xterm_family(term)
    mouse = tty and xterm_like
    alt_buffer = xterm_like

    return {
        "color": color,
        "truecolor": truecolor,
        "unicode": unicode_ok,
        "emoji": emoji,
        "mouse": mouse,
        "alt_buffer": alt_buffer,
    }

"""Tests for capabilities() with synthetic env dicts."""

from __future__ import annotations

import io

from codechu_term import capabilities


class _TTY:
    def isatty(self) -> bool:
        return True


class _NotTTY:
    def isatty(self) -> bool:
        return False


def test_dumb_term_disables_color() -> None:
    caps = capabilities(_TTY(), env={"TERM": "dumb", "LANG": "C"})
    assert caps["color"] is False
    assert caps["truecolor"] is False


def test_no_color_disables_color() -> None:
    caps = capabilities(_TTY(), env={"TERM": "xterm-256color", "NO_COLOR": "1"})
    assert caps["color"] is False
    assert caps["truecolor"] is False


def test_non_tty_disables_color_but_not_unicode() -> None:
    caps = capabilities(
        _NotTTY(), env={"TERM": "xterm-256color", "LANG": "en_US.UTF-8"}
    )
    assert caps["color"] is False
    assert caps["truecolor"] is False
    assert caps["unicode"] is True
    # alt_buffer is env-driven (xterm-family), independent of TTY.
    assert caps["alt_buffer"] is True
    # mouse needs TTY.
    assert caps["mouse"] is False


def test_truecolor_via_colorterm() -> None:
    caps = capabilities(
        _TTY(),
        env={"TERM": "xterm-256color", "COLORTERM": "truecolor", "LANG": "en_US.UTF-8"},
    )
    assert caps["color"] is True
    assert caps["truecolor"] is True


def test_truecolor_24bit_value() -> None:
    caps = capabilities(_TTY(), env={"TERM": "xterm", "COLORTERM": "24bit"})
    assert caps["truecolor"] is True


def test_truecolor_unknown_colorterm_value() -> None:
    caps = capabilities(_TTY(), env={"TERM": "xterm", "COLORTERM": "yes"})
    assert caps["color"] is True
    assert caps["truecolor"] is False


def test_unicode_from_lc_all_takes_precedence() -> None:
    caps = capabilities(_TTY(), env={"LC_ALL": "tr_TR.UTF-8", "LANG": "C"})
    assert caps["unicode"] is True


def test_unicode_from_lang_only() -> None:
    caps = capabilities(_TTY(), env={"LANG": "en_US.utf8"})
    assert caps["unicode"] is True


def test_unicode_false_for_ascii_lang() -> None:
    caps = capabilities(_TTY(), env={"LANG": "C", "LC_ALL": "C"})
    assert caps["unicode"] is False
    # No unicode → no emoji either.
    assert caps["emoji"] is False


def test_emoji_requires_unicode() -> None:
    caps = capabilities(
        _TTY(),
        env={"TERM": "xterm-256color", "TERM_PROGRAM": "iTerm.app", "LANG": "C"},
    )
    assert caps["emoji"] is False


def test_emoji_via_term_program() -> None:
    caps = capabilities(
        _TTY(),
        env={
            "TERM": "screen-256color",
            "TERM_PROGRAM": "iTerm.app",
            "LANG": "en_US.UTF-8",
        },
    )
    assert caps["emoji"] is True


def test_emoji_via_xterm_family_term() -> None:
    caps = capabilities(
        _TTY(), env={"TERM": "alacritty", "LANG": "en_US.UTF-8"}
    )
    assert caps["emoji"] is True


def test_mouse_requires_tty_and_xterm_family() -> None:
    assert capabilities(_TTY(), env={"TERM": "xterm"})["mouse"] is True
    assert capabilities(_TTY(), env={"TERM": "linux"})["mouse"] is False
    assert capabilities(_NotTTY(), env={"TERM": "xterm"})["mouse"] is False


def test_alt_buffer_for_tmux_screen() -> None:
    assert capabilities(_TTY(), env={"TERM": "tmux-256color"})["alt_buffer"] is True
    assert capabilities(_TTY(), env={"TERM": "screen"})["alt_buffer"] is True
    assert capabilities(_TTY(), env={"TERM": "linux"})["alt_buffer"] is False


def test_no_env_no_stream_returns_defaults() -> None:
    caps = capabilities(io.StringIO(), env={})
    assert caps == {
        "color": False,
        "truecolor": False,
        "unicode": False,
        "emoji": False,
        "mouse": False,
        "alt_buffer": False,
    }


def test_default_env_falls_back_to_os_environ(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    # When env is None, we should read os.environ. Smoke-test by setting
    # something distinctive and confirming the result reflects it.
    monkeypatch.setenv("TERM", "xterm-256color")
    monkeypatch.setenv("COLORTERM", "truecolor")
    monkeypatch.setenv("LANG", "en_US.UTF-8")
    monkeypatch.delenv("NO_COLOR", raising=False)
    caps = capabilities(_TTY())
    assert caps["color"] is True
    assert caps["truecolor"] is True
    assert caps["unicode"] is True

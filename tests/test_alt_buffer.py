"""Tests for the with_alt_buffer context manager."""

from __future__ import annotations

import io

import pytest

from codechu_term import with_alt_buffer


def test_emits_enter_and_leave() -> None:
    buf = io.StringIO()
    with with_alt_buffer(buf) as out:
        assert out is buf
        out.write("X")
    assert buf.getvalue() == "\x1b[?1049hX\x1b[?1049l"


def test_leave_emitted_on_exception() -> None:
    buf = io.StringIO()
    with pytest.raises(RuntimeError):
        with with_alt_buffer(buf):
            buf.write("Y")
            raise RuntimeError("boom")
    value = buf.getvalue()
    assert value.startswith("\x1b[?1049h")
    assert value.endswith("\x1b[?1049l")
    assert "Y" in value


def test_leave_swallows_closed_stream() -> None:
    buf = io.StringIO()
    # Close inside the block; the leave write would otherwise raise.
    with with_alt_buffer(buf):
        buf.close()
    # Nothing to assert beyond "did not raise".

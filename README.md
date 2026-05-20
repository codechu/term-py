```text
   ┌──────────────────────────────────────────────────┐
   │  c o d e c h u — t e r m                         │
   │  $ _                                             │
   │  ····TTY detection · alt buffer · raw mode······ │
   └──────────────────────────────────────────────────┘
```

[![PyPI](https://img.shields.io/pypi/v/codechu-term.svg)](https://pypi.org/project/codechu-term/)
[![Python](https://img.shields.io/pypi/pyversions/codechu-term.svg)](https://pypi.org/project/codechu-term/)
[![CI](https://github.com/codechu/term-py/actions/workflows/ci.yml/badge.svg)](https://github.com/codechu/term-py/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> *Terminal capability detection and low-level control, stdlib-only.*

# codechu-term

Stdlib-only terminal-capability detection and low-level terminal
control. The "what can this terminal actually do?" question
answered as a dictionary, plus the context managers you reach for
when you need full-screen mode, raw input, or resize handling.

```text
>>> capabilities(sys.stdout)
{'color':       True,   'truecolor':    True,
 'unicode':     True,   'emoji':        True,
 'mouse':       True,   'alt_buffer':   True}
```

## Install

```bash
pip install codechu-term
```

Python 3.10+. POSIX-first; no external dependencies.

## Quick example

```python
import os, sys
from codechu_term import capabilities, with_alt_buffer, with_raw_mode, on_resize

caps = capabilities(sys.stdout, env=os.environ)
if caps["alt_buffer"]:
    with with_alt_buffer() as out:
        out.write("full-screen view\n")
        out.flush()

with with_raw_mode() as fd:
    ch = os.read(fd, 1)   # char-by-char input

unsubscribe = on_resize(lambda: print("resized"))
unsubscribe()
```

## What you get

- **`is_tty(stream)` / `terminal_size()`** — the basic facts about
  the current stream.
- **`capabilities(stream, env)`** — color, truecolor, unicode,
  emoji, mouse, alt-buffer support, returned as one dict.
- **`with_alt_buffer()`** — context manager for full-screen mode.
- **`with_raw_mode(fd)`** — context manager for char-by-char input.
- **`on_resize(callback)`** — SIGWINCH subscription with an
  `unsubscribe()` return.
- **Cursor + line helpers** — `hide_cursor` / `show_cursor` /
  `clear_line` / `clear_screen` for the small ANSI tasks that
  always come up.

## Read more

- [API reference](docs/API.md) — every public symbol with full
  signatures and detection rules.
- [Changelog](CHANGELOG.md)

## Family

| Library | Purpose |
|---------|---------|
| [codechu-cli](https://pypi.org/project/codechu-cli/) | CLI primitives — colors, progress, spinners, prompts |
| [codechu-color](https://pypi.org/project/codechu-color/) | Color palettes, WCAG contrast, color-blind variants |
| [codechu-spark](https://pypi.org/project/codechu-spark/) | Unicode sparklines, mini bar charts, heatmaps |
| [codechu-fmt](https://pypi.org/project/codechu-fmt/) | Human-readable sizes, durations, rates |
| [codechu-meter](https://pypi.org/project/codechu-meter/) | Timing — stopwatch, ETA, rate, histogram |

Full ecosystem: [github.com/codechu](https://github.com/codechu).

## Credits

- Capability detection rules informed by
  [supports-color](https://github.com/chalk/supports-color) and
  [chalk](https://github.com/chalk/chalk).
- ANSI escape conventions per ECMA-48 and the `xterm` control
  sequence documentation.

## License

MIT — see [LICENSE](LICENSE).

Part of [Codechu](https://github.com/codechu).

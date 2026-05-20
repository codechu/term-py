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
control — extracted from the [codechu/cli-py](https://github.com/codechu/cli-py)
private `_term` module and expanded with the bits Codechu CLIs
actually use. No external dependencies. Python 3.10+, POSIX-first.

## Install

```bash
pip install codechu-term
```

## API

```python
import os, sys
from codechu_term import (
    is_tty, terminal_size, capabilities,
    with_alt_buffer, with_raw_mode, on_resize,
    hide_cursor, show_cursor, clear_line, clear_screen,
)

is_tty(sys.stderr)                          # → True / False

terminal_size()                             # → (cols, rows), e.g. (120, 40)
terminal_size(env={"COLUMNS": "100", "LINES": "30"})  # explicit env

capabilities(sys.stdout, env=os.environ)
# → {'color': True, 'truecolor': True, 'unicode': True,
#    'emoji': True, 'mouse': True, 'alt_buffer': True}

with with_alt_buffer() as out:              # full-screen mode
    out.write("hello, alt buffer\n"); out.flush()

with with_raw_mode() as fd:                 # char-by-char input
    ch = os.read(fd, 1)

remove = on_resize(lambda: print("resized!"))
# ... later
remove()

hide_cursor(); show_cursor()
clear_line(); clear_screen()
```

### `is_tty(stream)`

Defensive `isatty()` — accepts `None` and any object, swallows
exceptions, returns `False` for anything that isn't a confirmed TTY.

### `terminal_size(stream=sys.stderr, *, env=None)`

Resolution ladder:

1. `os.get_terminal_size(stream.fileno())` when available.
2. `COLUMNS` / `LINES` from `env` (defaults to `os.environ`).
3. `(80, 24)` as a final fallback.

Never raises.

### `capabilities(stream, env=None)`

Returns six boolean flags:

| Key          | True when                                                     |
| ------------ | ------------------------------------------------------------- |
| `color`      | `stream` is a TTY, `TERM != "dumb"`, and `NO_COLOR` is unset  |
| `truecolor`  | `color` and `COLORTERM` in `{"truecolor", "24bit"}`           |
| `unicode`    | `LC_ALL` / `LC_CTYPE` / `LANG` advertises UTF-8               |
| `emoji`      | `unicode` and (`TERM_PROGRAM` is a known emoji emulator or xterm-family) |
| `mouse`      | TTY and xterm-family `TERM`                                   |
| `alt_buffer` | xterm-family `TERM`                                           |

`env` is taken explicitly — pass `env=os.environ` for the live
process environment.

### `with_alt_buffer(stream=sys.stdout)`

Context manager that switches to the alt screen buffer
(`\x1b[?1049h`) on entry and restores the main buffer
(`\x1b[?1049l`) on exit — even when the block raises.

### `with_raw_mode(fd=sys.stdin.fileno())`

`termios`/`tty` raw mode for char-by-char input. Restores the
original terminal attributes in a `finally` block, so the terminal
never gets stuck. POSIX only.

### `on_resize(callback)`

Installs `callback` as a `SIGWINCH` handler and returns a remover
function that restores the previous handler. The callback is invoked
with no arguments. POSIX only.

### `hide_cursor() / show_cursor() / clear_line() / clear_screen()`

Best-effort emitters for the corresponding ANSI sequences
(`\x1b[?25l`, `\x1b[?25h`, `\x1b[2K\r`, `\x1b[2J\x1b[H`). They never
raise — a closed stream is silently ignored.

## Design

- **Pure stdlib.** Zero third-party dependencies.
- **Explicit env.** Capability detection never reads `os.environ`
  implicitly — the caller passes the dict. Makes testing trivial and
  avoids surprises in nested processes.
- **Defensive.** Helpers tolerate `None` streams, closed streams,
  and missing methods. They never raise from a "best-effort" path.
- **POSIX-first.** `with_raw_mode` and `on_resize` are POSIX-only
  (termios / SIGWINCH); they raise `OSError` on Windows rather than
  silently no-op.

## Tests

```bash
pip install -e ".[dev]"
pytest -q
```

Tests that require a real TTY (raw mode, SIGWINCH propagation) skip
themselves when running headless.

## Documentation

- [API reference](docs/API.md) — every public symbol, signatures, edge cases

## Codechu family

Companion libraries from the Codechu Python ecosystem:

| Library | Purpose |
|---------|---------|
| [codechu-fmt](https://pypi.org/project/codechu-fmt/) | Human-readable formatting — sizes, durations, rates, percent |
| [codechu-meter](https://pypi.org/project/codechu-meter/) | Timing primitives — Stopwatch, ETA, percentile, histogram |
| [codechu-spark](https://pypi.org/project/codechu-spark/) | Unicode sparklines, mini bar charts, heatmaps |
| [codechu-cli](https://pypi.org/project/codechu-cli/) | CLI primitives — colors, progress, spinners, prompts, table |
| [codechu-events](https://pypi.org/project/codechu-events/) | Thread-safe multi-channel pub/sub bus with replay |
| [codechu-xdg](https://pypi.org/project/codechu-xdg/) | XDG Base Directory helpers, vendor-namespaced |
| [codechu-treeviz](https://pypi.org/project/codechu-treeviz/) | Tree visualization — treemap, sunburst, icicle, flame |
| [codechu-fs](https://pypi.org/project/codechu-fs/) | Filesystem primitives — atomic write, XDG trash, safe walk |
| [codechu-color](https://pypi.org/project/codechu-color/) | Color palettes, WCAG contrast, color-blind variants |
| [codechu-treedata](https://pypi.org/project/codechu-treedata/) | N-ary tree data structures and algorithms |
| [codechu-log](https://pypi.org/project/codechu-log/) | Structured logging — context, JSON, rotation, redaction |
| [codechu-i18n](https://pypi.org/project/codechu-i18n/) | Internationalization — locale, plural rules, RTL |
| [codechu-ipc](https://pypi.org/project/codechu-ipc/) | Local IPC — Unix socket, FIFO, JSON-line protocol |
| [codechu-config](https://pypi.org/project/codechu-config/) | Schema-driven config — atomic save, migrations |

## Credits

- Built on stdlib termios + select; SIGWINCH handling per POSIX.

## License

MIT — see [LICENSE](LICENSE).

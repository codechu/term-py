# API Reference — codechu-term 0.1.0

Complete reference for every public symbol re-exported from the
`codechu_term` package.

The package exposes ten functions/context managers plus a version
string:

| Symbol                                          | Kind            | Module                       |
| ----------------------------------------------- | --------------- | ---------------------------- |
| [`__version__`](#__version__)                   | `str`           | `codechu_term`               |
| [`is_tty`](#is_tty)                             | function        | `codechu_term.streams`       |
| [`terminal_size`](#terminal_size)               | function        | `codechu_term.streams`       |
| [`capabilities`](#capabilities)                 | function        | `codechu_term.caps`          |
| [`with_alt_buffer`](#with_alt_buffer)           | context manager | `codechu_term.alt_buffer`    |
| [`with_raw_mode`](#with_raw_mode)               | context manager | `codechu_term.raw`           |
| [`on_resize`](#on_resize)                       | function        | `codechu_term.resize`        |
| [`hide_cursor`](#hide_cursor) / [`show_cursor`](#show_cursor) | function | `codechu_term.streams` |
| [`clear_line`](#clear_line) / [`clear_screen`](#clear_screen) | function | `codechu_term.streams` |

All helpers are stdlib-only and side-effect-free unless they
explicitly write to a stream. Stream-writers are best-effort: a closed
or non-writable stream is silently ignored rather than crashing the
caller.

---

## `__version__`

```python
__version__: str = "0.1.0"
```

Semantic-version string of the installed package.

---

## `is_tty`

```python
def is_tty(stream: IO[str] | None) -> bool: ...
```

Robust `isatty()` wrapper. Accepts `None`, closed streams, and
file-likes that lack `isatty`. Any failure path yields `False`.

```python
from codechu_term import is_tty
import sys
is_tty(sys.stdout)   # True under a real terminal
is_tty(None)         # False
```

---

## `terminal_size`

```python
def terminal_size(
    stream: IO[str] | None = None,
    *,
    env: dict[str, str] | None = None,
) -> tuple[int, int]: ...
```

Return `(cols, rows)` for `stream`. Resolution order:

1. `os.get_terminal_size(stream.fileno())` for real TTY descriptors.
2. `COLUMNS` / `LINES` from `env` (default: `os.environ`).
3. `(80, 24)` as a final fallback.

Never raises. `env` is taken explicitly so tests can inject a clean
dict without leaking process state.

```python
from codechu_term import terminal_size
terminal_size()                                  # (cols, rows) from the live TTY
terminal_size(env={"COLUMNS": "120", "LINES": "40"})  # (120, 40)
```

---

## `capabilities`

```python
def capabilities(
    stream: IO[str] | None = None,
    env: dict[str, str] | None = None,
) -> dict[str, bool]: ...
```

Return a dict of feature flags for `stream` + environment.

| Key          | Meaning                                                                              |
| ------------ | ------------------------------------------------------------------------------------ |
| `color`      | TTY + `TERM != "dumb"` + no `NO_COLOR`.                                              |
| `truecolor`  | `color` true *and* `COLORTERM` is `truecolor` / `24bit`.                             |
| `unicode`    | `LC_ALL` / `LC_CTYPE` / `LANG` advertises UTF-8.                                     |
| `emoji`      | `unicode` and either xterm-family `TERM` or a known emoji-capable `TERM_PROGRAM`.    |
| `mouse`      | TTY + xterm-family `TERM`.                                                           |
| `alt_buffer` | xterm-family `TERM` (no TTY required — pipe-to-recorder is valid).                   |

The xterm family is `xterm`, `screen`, `tmux`, `rxvt`, `alacritty`,
`kitty`, `wezterm`.

```python
from codechu_term import capabilities
caps = capabilities()
if caps["color"]:
    print("\x1b[32mhello\x1b[0m")
```

`NO_COLOR` is respected per <https://no-color.org>.

---

## `with_alt_buffer`

```python
@contextmanager
def with_alt_buffer(stream: IO[str] | None = None) -> Iterator[IO[str]]: ...
```

Switch `stream` (default `sys.stdout`) to the xterm alt screen buffer
for the duration of the block. Emits `\x1b[?1049h` on entry,
`\x1b[?1049l` on exit. The leave sequence runs in `finally`, so
exceptions still restore the main buffer.

```python
from codechu_term import with_alt_buffer
with with_alt_buffer() as out:
    out.write("fullscreen UI here\n")
    out.flush()
# Main screen restored on exit.
```

Yields the stream so the body can write to it directly.

---

## `with_raw_mode`

```python
@contextmanager
def with_raw_mode(fd: int | None = None) -> Iterator[int]: ...
```

Put file descriptor `fd` (default `sys.stdin.fileno()`) into raw mode.
Saves and restores the original `termios` attributes — even on
exception — so the terminal never gets stuck.

```python
import os
from codechu_term import with_raw_mode
with with_raw_mode() as fd:
    ch = os.read(fd, 1)  # one byte, no line buffering, no echo
```

POSIX only. Raises `OSError` on Windows or when `fd` is not a real
TTY descriptor.

---

## `on_resize`

```python
def on_resize(callback: Callable[[], None]) -> Callable[[], None]: ...
```

Install `callback` as a `SIGWINCH` handler. Returns a *remover*
function — call it to restore the previous handler.

```python
from codechu_term import on_resize, terminal_size

def redraw() -> None:
    cols, rows = terminal_size()
    ...

remove = on_resize(redraw)
try:
    main_loop()
finally:
    remove()
```

The callback is invoked with no arguments; signal info is hidden
because the only useful response is "re-query the size". POSIX only —
raises `OSError` on platforms without `SIGWINCH`.

---

## `hide_cursor`

```python
def hide_cursor(stream: IO[str] | None = None) -> None: ...
```

Emit DECTCEM cursor-hide (`\x1b[?25l`) to `stream` (default
`sys.stdout`). Errors are swallowed.

## `show_cursor`

```python
def show_cursor(stream: IO[str] | None = None) -> None: ...
```

Emit DECTCEM cursor-show (`\x1b[?25h`). Pair with `hide_cursor` in a
`try`/`finally` — or wrap with your own context manager — to keep the
cursor restored on exceptions.

```python
from codechu_term import hide_cursor, show_cursor
hide_cursor()
try:
    render_progress()
finally:
    show_cursor()
```

---

## `clear_line`

```python
def clear_line(stream: IO[str] | None = None) -> None: ...
```

Erase the current line and return the carriage (`\x1b[2K\r`). Useful
for rewriting a single-line progress indicator.

## `clear_screen`

```python
def clear_screen(stream: IO[str] | None = None) -> None: ...
```

Clear the entire screen and home the cursor (`\x1b[2J\x1b[H`).

```python
from codechu_term import clear_line, clear_screen
clear_line()         # rewrite the current line
clear_screen()       # full reset at start of a render pass
```

---

## Edge cases

- **No TTY**: every stream-writer (`hide_cursor`, `clear_line`, etc.)
  still writes the bytes. Combine with `capabilities()["color"]` /
  `is_tty()` if you want to skip control sequences when stdout is a
  pipe or file.
- **Closed streams**: writes are best-effort; exceptions inside the
  writer are caught.
- **Non-POSIX platforms**: `with_raw_mode` and `on_resize` raise
  `OSError` rather than silently no-op'ing. Detect with a `try`
  around the call.

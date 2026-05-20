# Changelog

[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) + [SemVer](https://semver.org/).

## [Unreleased]

## [0.1.0] — 2026-05-20

### Added

- Initial extraction from [codechu/cli-py](https://github.com/codechu/cli-py)
  (`_term.py`), expanded into a public API.
- `is_tty(stream)` — robust `isatty()` wrapper that never raises.
- `terminal_size(stream=sys.stderr)` — `(cols, rows)` with fallback
  ladder: `os.get_terminal_size` → env `COLUMNS`/`LINES` → `(80, 24)`.
- `capabilities(stream, env=None)` — dict of flags (`color`,
  `truecolor`, `unicode`, `emoji`, `mouse`, `alt_buffer`). Caller
  passes the env dict explicitly; `NO_COLOR` and `TERM=dumb` are
  honoured.
- `with_alt_buffer(stream=sys.stdout)` — context manager emitting
  `\x1b[?1049h` on enter and `\x1b[?1049l` on exit.
- `with_raw_mode(fd=sys.stdin.fileno())` — context manager using
  `termios` for char-by-char input. POSIX only.
- `on_resize(callback)` — install a `SIGWINCH` handler; returns a
  remover function that restores the previous handler. POSIX only.
- `hide_cursor(stream)` / `show_cursor(stream)` — emit `\x1b[?25l`
  / `\x1b[?25h`.
- `clear_line(stream)` / `clear_screen(stream)` — emit `\x1b[2K\r`
  / `\x1b[2J\x1b[H`.

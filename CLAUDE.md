# CLAUDE.md — codechu-term

Bootstrap per `codechu-org/ai/AGENTS.md` §0 before any work. Prefer
the local clone at `$org_home/codechu-org/ai/AGENTS.md` (if
`~/.config/codechu/config.toml` has `org_home` set); otherwise
WebFetch the public raw URL
<https://raw.githubusercontent.com/codechu/codechu-org/main/ai/AGENTS.md>.
This file lists only product-local overrides.

## Product-local notes

- Pure stdlib terminal-capability library. **No** external runtime
  dependencies. Python 3.10+.
- POSIX-first. `with_raw_mode` and `on_resize` are POSIX-only (use
  `termios` / `SIGWINCH`); they degrade gracefully on Windows (raise
  or no-op) but are not actively supported there.
- Public API: `is_tty`, `terminal_size`, `capabilities`,
  `with_alt_buffer`, `with_raw_mode`, `on_resize`, `hide_cursor`,
  `show_cursor`, `clear_line`, `clear_screen`. Anything else is
  internal.
- `capabilities()` takes an explicit `env` dict — no implicit
  `os.environ` reads. Callers pass `env=os.environ` when they want
  the live process environment.
- Output sequences (`\x1b[?1049h`, `\x1b[?25l`, …) are part of the
  public contract — changing them is a breaking change.

## Discipline reminders (org rules apply)

- Conventional Commits, no AI signature.
- No `--no-verify`, no force push, no unapproved publish.
- See `codechu-org/ai/AGENTS.md` for the full list.

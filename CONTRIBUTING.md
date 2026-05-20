# Contributing to codechu-term

Thanks for thinking about contributing. `codechu-term` is a tiny
stdlib-only terminal-capability library — capability detection,
alt-buffer / raw-mode context managers, resize handling, cursor and
screen control. Patches that stay focused, well-tested, and
dependency-free are warmly received.

This library was extracted from the [codechu/cli-py](https://github.com/codechu/cli-py)
private `_term` module and expanded with the bits Disk Cleaner and
other Codechu CLIs needed.

## Development setup

```bash
git clone https://github.com/codechu/codechu-term-py.git
cd codechu-term-py
pip install -e ".[dev]"
pytest -q
ruff check src tests
```

## Workflow

- Branch names: `feature/<short>`, `fix/<short>`, `refactor/<short>`,
  `docs/<short>`, `test/<short>`.
- Commit messages: [Conventional Commits](https://www.conventionalcommits.org/)
  (`feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`).
- Open a PR using the template; describe the *why* in the body.
- One change per PR — keep diffs reviewable.

## Bug reports

A useful bug report includes:

- OS + Python version, `TERM` / `COLORTERM` / `LANG` values.
- The exact call you made and the result.
- The behaviour you expected.

## Tests

- `pytest -q` must pass.
- New feature → new test. Cover the edge cases: non-TTY streams,
  unusual env values, missing env keys.
- Tests that require a real TTY (raw mode, SIGWINCH) must
  `pytest.skip()` cleanly when running headless.

## Public API discipline

The public surface is fixed at `is_tty`, `terminal_size`,
`capabilities`, `with_alt_buffer`, `with_raw_mode`, `on_resize`,
`hide_cursor`, `show_cursor`, `clear_line`, `clear_screen`. Emitted
ANSI sequences are part of the contract — changing them is a
breaking change.

No external runtime dependencies. If you need one, the answer is
almost always "no, write it in stdlib".

## Style

- `ruff check` + `ruff format` clean.
- Type hints on public APIs (`from __future__ import annotations`).

## Security

If you find a security issue, see [SECURITY.md](SECURITY.md) — do not
open a public issue for it.

## Developer Certificate of Origin (DCO)

Every commit must be signed off with the [DCO](https://developercertificate.org/).
The sign-off certifies that you wrote the patch, or otherwise have the
right to submit it under the project's license. Add a line to your
commit message:

```
Signed-off-by: Your Name <you@example.com>
```

`git commit -s` does this automatically. PRs without sign-off will
be asked to amend before merge.

Contributions are accepted under the project's license (see
[LICENSE](LICENSE)).

# Security policy

`codechu-term` is a pure-stdlib terminal-capability library. Its
public functions read environment dicts, inspect stream `isatty()`,
and emit ANSI escape sequences. No network I/O, no subprocess, no
deserialization. The attack surface is intentionally small.

## Supported versions

| Version | Supported |
|---|:---:|
| `main` branch | ✅ |
| Latest minor release (0.x) | ✅ |
| Older releases | ❌ |

Pre-1.0.0 — only the latest minor receives security fixes.

## Reporting a vulnerability

### Preferred path — GitHub Security Advisory (private)

Open a **private** advisory at
[github.com/codechu/codechu-term-py/security/advisories/new](https://github.com/codechu/codechu-term-py/security/advisories/new).

### Alternative — Email

Write to `security@codechu.com`.

## Scope — what to report

**In scope:**

- Inputs that crash a public function for plausible env / stream
  values (uncaught exceptions).
- Escape-sequence injection — any path where caller-supplied data is
  emitted as part of a CSI/OSC sequence without being treated as
  opaque text.
- Resource exhaustion — bounded-time helpers must stay bounded.

**Out of scope:**

- Terminal emulators that misinterpret valid ANSI sequences.
- Windows behaviour (POSIX-first library).

## Process

Reports are reviewed on a best-effort basis — no fixed SLA. We aim
for coordinated disclosure within **90 days** of the report.

Public disclosure is coordinated after the fix is released.

## Public disclosure

Once a confirmed fix is released:

- A summary is added to the CHANGELOG under the `### Security`
  category.
- A GitHub Security Advisory is published.
- If a CVE was assigned, its number is referenced.

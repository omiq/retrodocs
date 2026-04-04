# TRSE (Turbo Rascal)

**TRSE** (Turbo Rascal Syntax error, …) is an IDE and compiler for 8-bit (and more) systems. The main upstream project lives at **[github.com/leuat/TRSE](https://github.com/leuat/TRSE)**.

## In this repository

Your fork may include extra tooling (for example under `tools/flf_tool/` and `api/trse_compiler/`). The **in-IDE Help** in TRSE is driven by:

- `resources/text/syntax.txt` — index of methods, constants, etc.
- `resources/text/help/<type>/<name>.rtf` — HTML fragments (despite the `.rtf` extension)

## On this documentation site

- **[Methods (reference)](reference/methods-index.md)** — built-in methods from TRSE’s `syntax.txt` + `resources/text/help/m/*.rtf` (regenerate with `scripts/import_trse_reference.py`).
- **[How import works](help-import.md)** — sources, maintenance, and options.

For day-to-day use inside the app, the IDE **Help** tab is still the primary UI.

## Quick links

- [Methods index](reference/methods-index.md)
- [Import / regenerate reference](help-import.md)

# Importing TRSE help into MkDocs

This page explains **how** TRSE stores built-in documentation, **why** we have not fully automated import yet, and **what** you can do next.

## Where TRSE keeps help (in the main repo)

| Piece | Path | Role |
|-------|------|------|
| Index | `resources/text/syntax.txt` | Semicolon-separated rows: type, name, CPU scope, signatures… |
| Bodies | `resources/text/help/<letter>/<topic>.rtf` | HTML fragments (e.g. `m/abs.rtf` for method `Abs`) |

The IDE loads these at runtime (`formhelp.cpp`, `syntax.cpp`). See the discussion in project notes: the `.rtf` files are mostly **HTML**, not Word RTF.

## Why not commit 400+ generated pages here?

- **Duplication**: The source of truth stays in TRSE; generated Markdown would need **regeneration** on every upstream merge.
- **Search**: MkDocs Material’s search works on **built** HTML; a CI job can generate Markdown or HTML under `docs/trse/reference/` before `mkdocs build`.

## Recommended pipeline (future)

1. Add a script (Python) in `retrodocs/scripts/` that:
   - Parses `syntax.txt`
   - For each method (`m` rows), reads `resources/text/help/m/<name>.rtf`
   - Writes one Markdown file per topic (or one big page per section) with front matter `title` / `description`
2. Run the script **before** `mkdocs build` (locally or in CI).
3. Optionally **exclude** generated files from manual edits (`<!-- AUTO-GENERATED -->` banner).

## What you can do today

- Hand-write **conceptual** guides under `docs/trse/` (tutorials, “how projects work”).
- Link to **upstream** or your deployed IDE for live tools.
- When ready, implement the generator above and add `python retrodocs/scripts/import_trse_help.py` to `deploy.sh` before `mkdocs build`.

---

*Keeping generated docs in CI avoids bloating git history with huge auto-commits unless you choose to vendor them.*

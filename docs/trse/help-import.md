# TRSE reference in these docs

The **method reference** (`TRSE` → **Methods (reference)**) is **generated** from the TRSE repository so it stays aligned with the IDE.

## Sources (in TRSE repo root)

| File | Role |
|------|------|
| `resources/text/syntax.txt` | Lines starting with `m;` list each **method**, target systems, and parameter letters |
| `resources/text/help/m/<name>.rtf` | HTML body for that method (filename = lowercase method name) |

The `.rtf` extension is historical; content is **HTML** fragments, as in the IDE (`formhelp.cpp`).

## Regenerate

From the **repository root** (where `resources/text/` exists):

```bash
python3 retrodocs/scripts/import_trse_reference.py --skip-init
```

Or from `retrodocs/`:

```bash
python3 scripts/import_trse_reference.py --skip-init
```

Options:

| Flag | Meaning |
|------|--------|
| `--repo-root /path/to/TRSE` | If the script cannot find `resources/text/syntax.txt` by walking upward |
| `--skip-init` | Omit methods whose names start with `init` (matches the IDE help list more closely) |

Then build the site:

```bash
cd retrodocs
mkdocs build
```

`deploy.sh` runs the import automatically unless **`SKIP_TRSE_IMPORT=1`**.

## What gets written

- `docs/trse/reference/methods-index.md` — table of all methods with links
- `docs/trse/reference/methods/<slug>.md` — one page per method (HTML body embedded)

Each file starts with `<!-- AUTO-GENERATED ... -->` — **edit the generator**, not the Markdown, or your changes will be overwritten.

## Missing help files

If `syntax.txt` lists a method but `help/m/<name>.rtf` is missing, the page is still created with a short stub. Upstream may add the file later.

## Reserved words / constants / platform topics

Only **`m` (methods)** are imported for now. Extending the script to `r`, `c`, `p` rows is straightforward (same help tree, different `syntax.txt` prefixes and `help/` subfolders).

---

*Script: `retrodocs/scripts/import_trse_reference.py`*

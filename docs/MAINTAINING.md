# Maintaining the documentation site

This file is the **operator’s guide** for the MkDocs project under **`retrodocs/`** in the repository.

## What this is

- **Tool**: [MkDocs](https://www.mkdocs.org/) with [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) theme.
- **Source**: Markdown (`.md`) under `retrodocs/docs/`.
- **Config**: `retrodocs/mkdocs.yml`.
- **Output**: static HTML in `retrodocs/site/` after `mkdocs build` (ignored by git).

## Why MkDocs + Material (Python)

- No Node/npm for this subproject — only Python and `pip`.
- One command to preview locally, one to build static files suitable for any web server or static host.
- Built-in **search** (client-side index) without a database.

## First-time setup on your dev machine

```bash
cd retrodocs
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
mkdocs serve
```

Open **http://127.0.0.1:8000** — edits to `docs/**/*.md` reload automatically.

## Building for production

```bash
cd retrodocs
source .venv/bin/activate
mkdocs build
```

Upload the contents of **`retrodocs/site/`** to your web server (or use `deploy.sh` — see below).

## Editing navigation

The left sidebar and tabs come from **`mkdocs.yml`** → **`nav:`**. When you add a new page:

1. Create `docs/something/new-page.md`
2. Add an entry under `nav:` in `mkdocs.yml`

## TRSE auto-generated help

TRSE’s IDE help lives in the **parent** repo (`resources/text/...`). This MkDocs tree is **hand-written** unless you add a generator script. See **[trse/help-import.md](trse/help-import.md)** for the recommended approach.

## Deployment options

| Method | Notes |
|--------|--------|
| **`deploy.sh`** (rsync over SSH) | Good for a VPS you control; see script header for env vars. |
| **GitHub Actions + Pages** | Build `mkdocs build` in CI, publish `site/`. |
| **Cloudflare Pages / Netlify** | Point at repo; build command `mkdocs build`, publish directory `retrodocs/site`. |

## Files worth knowing

| Path | Purpose |
|------|---------|
| `retrodocs/mkdocs.yml` | Site name, theme, plugins, **nav** |
| `retrodocs/docs/` | All Markdown content |
| `retrodocs/requirements.txt` | Pinned MkDocs Material (adjust upper bound when upgrading) |
| `retrodocs/deploy.sh` | Optional SSH/rsync deploy |
| `retrodocs/README.md` | Short pointer (duplicate of this file in spirit) |

## Troubleshooting

- **`mkdocs: command not found`** — Activate the venv or use `python -m mkdocs build`.
- **Search not updating** — Run a clean build: `rm -rf site && mkdocs build`.
- **Theme looks wrong** — Check `mkdocs.yml` `theme:` block; upstream Material docs list breaking changes per major version.

---

*Last expanded when the `retrodocs/` scaffold was added to the repository.*

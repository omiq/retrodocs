# Maintaining the documentation site

This file is the **operator’s guide** for the MkDocs project under **`retrodocs/`** in the repository.

To maintain **`retrodocs`** as a **separate Git repo** from TRSE, see **`STANDALONE_REPO.md`** at the project root (splitting history, `TRSE_REPO_ROOT`, deploy). The public repo is **[github.com/omiq/retrodocs](https://github.com/omiq/retrodocs)**; **CI** (`.github/workflows/ci.yml`) builds on each push/PR.

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
# Refresh TRSE method pages from ../resources/text/ (omit if you did not change TRSE sources)
python3 scripts/import_trse_reference.py --skip-init
# Refresh bundled units list from ../units/
python3 scripts/import_trse_units.py
mkdocs build
```

`mkdocs build` may **list many pages under `trse/reference/methods/`** as “not in nav” — that is expected: only **[Methods (reference)](trse/reference/methods-index.md)** is in the sidebar; individual methods are linked from that index and searchable.

Upload the contents of **`retrodocs/site/`** to your web server (or use `deploy.sh` — see below).

## Editing navigation

The left sidebar and tabs come from **`mkdocs.yml`** → **`nav:`**. When you add a new page:

1. Create `docs/something/new-page.md`
2. Add an entry under `nav:` in `mkdocs.yml`

## Customising styles and templates

### Styles (CSS)

- **Source file**: `retrodocs/docs/stylesheets/extra.css` — edit this file; **`retrodocs/site/stylesheets/`** is build output only.
- **Registration**: `mkdocs.yml` → `extra_css:` lists stylesheets (paths are relative to `docs/`). Add more files there if you split CSS; order matters (later files override earlier ones).
- **Approach**: Prefer [Material’s CSS variables](https://squidfunk.github.io/mkdocs-material/setup/setting-up-navigation/) so theme upgrades stay predictable. This site uses **`primary: custom`** / **`accent: custom`** in `mkdocs.yml`; the `[data-md-color-primary="custom"]` and `[data-md-color-accent="custom"]` rules in `extra.css` define those colours.
- **Colour scheme**: The site uses **`palette.scheme: slate`** only (no light/dark toggle). Custom CSS should target **`[data-md-color-scheme="slate"]`**; rules for **`default`** (light) are unused unless you reintroduce a light palette.
- **Theme-only options**: Favicon and logo are set under `theme:` in `mkdocs.yml` (`favicon`, `logo`). Shared links and icons can also live under `extra:` (this project uses `homepage`, `social`).

### Templates (HTML / layout)

Material uses **Jinja2**. To change structure (extra regions in the layout, inject scripts in `<head>`, replace a partial), use **template overrides**:

1. Create a folder for overrides (common name: `overrides/` next to `mkdocs.yml`, or `docs/overrides/`).
2. In `mkdocs.yml`, under `theme:`, set `custom_dir:` to that folder **relative to `mkdocs.yml`** — e.g. `custom_dir: overrides` if the folder is `retrodocs/overrides/`, or `custom_dir: docs/overrides` if it lives under `docs/`.
3. Copy **only** the partials you need from the theme, keeping the **same path** inside `custom_dir` that Material expects. Start from **[Material — Customization → Template overrides](https://squidfunk.github.io/mkdocs-material/customization/#template-overrides)** for the file layout.
4. Often you add a **`main.html`** that does `{% extends "base.html" %}` and overrides specific `{% block ... %}` blocks, instead of forking the entire theme.
5. Rebuild with `mkdocs build` or `mkdocs serve` and verify the generated HTML if something does not appear (wrong partial path or block name).

Upstream reference: [MkDocs Material — Customization](https://squidfunk.github.io/mkdocs-material/customization/).

### What to use when

| Goal | Where to work |
|------|----------------|
| Colours, spacing, typography, borders | `docs/stylesheets/extra.css` + Material CSS variables |
| Favicon, default logo | `mkdocs.yml` → `theme:` |
| Extra markup in header/footer, analytics, `<head>` tweaks | `custom_dir` + `main.html` or the relevant partial under `partials/` |

## TRSE auto-generated help

TRSE’s IDE help lives in the **parent** repo (`resources/text/...`). This MkDocs tree is **hand-written** unless you add a generator script. See **[trse/help-import.md](trse/help-import.md)** for the recommended approach.

## Deployment options

| Method | Notes |
|--------|--------|
| **`deploy.sh`** (rsync over SSH) | Good for a VPS you control; see script header for env vars. |
| **GitHub Actions + Pages** | Build `mkdocs build` in CI, publish `site/`. |
| **Cloudflare Pages / Netlify** | Point at repo; build command `mkdocs build`, publish directory `retrodocs/site`. |
| **CloudPanel (VPS) — static site** | Create the site as **Static** / HTML, document root = directory containing **`index.html`** from `mkdocs build`. **Do not** use an application template that **`proxy_pass`**es to a port — MkDocs output has no backend; a proxy causes **502**. Upload/rsync the contents of **`retrodocs/site/`** into that directory. |

`mkdocs.yml` sets **`site_url: https://docs.retrogamecoders.com/`** so the built site knows its public URL (sitemap, etc.).

## Files worth knowing

| Path | Purpose |
|------|---------|
| `retrodocs/mkdocs.yml` | Site name, theme (**`custom_dir: overrides`**, **`theme.favicon`** from main site), plugins, **nav**, `extra_css`, social links |
| `retrodocs/docs/stylesheets/extra.css` | **Brand colours** (navy + gold) to match retrogamecoders.com; primary place for CSS — see **Customising styles and templates** |
| `retrodocs/overrides/main.html` | Extends Material `base.html`; favicon / PWA links + **Open Graph / Twitter** image (`docs/images/og-image.jpg` → `/images/og-image.jpg`) |
| `retrodocs/docs/images/og-image.jpg` | Social preview image (`og:image`, `twitter:image`); referenced via `site_url` in `overrides/main.html` |
| `retrodocs/docs/` | Markdown: `ide/`, `trse/`, `assembly/`, `c/`, `basic/`, … |
| `retrodocs/docs/basic/rgc-basic/` | **Hand-written** multi-page guide for [RGC BASIC](https://github.com/omiq/rgc-basic) (not generated) |
| `retrodocs/requirements.txt` | Pinned MkDocs Material (adjust upper bound when upgrading) |
| `retrodocs/deploy.sh` | SSH/rsync deploy; sets **`DEPLOY_CACHE_BUST`** so built pages use `extra.css?v=…` (avoids stale CDN/browser CSS without relying on purges) |
| `retrodocs/scripts/import_trse_units.py` | Generates `trse/reference/units-index.md` and `trse/reference/units/*.md` from `../units/**/*.tru` (signatures + block-comment notes) |
| `retrodocs/scripts/tru_extract.py` | Parses `.tru` text for `procedure` / `function` declarations (helper for `import_trse_units.py`) |
| `retrodocs/README.md` | Short pointer (duplicate of this file in spirit) |
| `retrodocs/STANDALONE_REPO.md` | Splitting `retrodocs` into its own GitHub repo; `TRSE_REPO_ROOT`, subtree split |
| `retrodocs/.github/workflows/ci.yml` | GitHub Actions: clone [omiq/trse](https://github.com/omiq/trse), run import scripts, `mkdocs build --strict`, upload `site-html` artifact |

## Troubleshooting

- **`mkdocs: command not found`** — Activate the venv or use `python -m mkdocs build`.
- **Search not updating** — Run a clean build: `rm -rf site && mkdocs build`.
- **Theme looks wrong** — Check `mkdocs.yml` `theme:` block; upstream Material docs list breaking changes per major version.
- **CSS edits never show (even after hard refresh)** — `mkdocs serve` builds into a **temporary** folder, not `retrodocs/site/`. The browser only sees what the **last rebuild** copied; refreshing cannot pick up new `extra.css` until the server rebuilds. After saving, the terminal should print **`Detected file changes`** then **`Reloading browsers`**. Use **`http://127.0.0.1:8000`** — not `file://` or `site/` on disk. **`hooks.py`** adds `realpath` watches, `mkdocs.yml` **`watch:`**, and `?v=` cache-bust while serving. **`start.sh`** runs **`scripts/touch_mkdocs_on_css_save.py`** in the background: it polls `docs/stylesheets/` and **`touch`es `mkdocs.yml`** when anything changes there, so MkDocs’ config watcher always triggers a rebuild even if native file events miss your editor’s save.

### Red “MkDocs 2.0” warning when you run `mkdocs serve`

Material for MkDocs may print a **warning box** about **MkDocs 2.0** (breaking changes, plugins, etc.). That is **not** a failure — your server still starts and the site builds. It is a **heads-up** from the Material maintainers about the future **upstream** MkDocs major release.

**This project** intentionally pins **`mkdocs` to 1.x** in `requirements.txt` (`mkdocs>=1.5,<2`) so you stay on the stable stack until there is a clear upgrade path. You can ignore the banner for day-to-day work, or read their analysis: [MkDocs 2.0 — Material blog](https://squidfunk.github.io/mkdocs-material/blog/2026/02/18/mkdocs-2.0/).

---

*Last updated: added **Customising styles and templates** (MkDocs Material CSS + `custom_dir` overrides).*

# RetroDocs — Retro Game Coders Educational & Reference Documentation

[![CI](https://github.com/omiq/retrodocs/actions/workflows/ci.yml/badge.svg)](https://github.com/omiq/retrodocs/actions/workflows/ci.yml)

Public repo: **[github.com/omiq/retrodocs](https://github.com/omiq/retrodocs)** — Retro Game Coders documentation (Markdown → static HTML), published at [docs.retrogamecoders.com](https://docs.retrogamecoders.com/).

## Quick start

```bash
git clone https://github.com/omiq/retrodocs.git
cd retrodocs
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve    # http://127.0.0.1:8000
```

If you see a **MkDocs 2.0** warning banner from Material: it is informational, not an error. This repo pins **MkDocs 1.x** in `requirements.txt`. See **Maintaining this site** → *Red “MkDocs 2.0” warning*.

## TRSE reference (auto-generated)

After cloning, regenerate method pages from the TRSE tree (requires `resources/text/` next to `retrodocs/`):

```bash
python3 scripts/import_trse_reference.py --skip-init
```

Committed copies may already be present; run the script when you merge TRSE upstream changes.

For a **standalone** clone, point at a TRSE checkout: `export TRSE_REPO_ROOT=/path/to/trse` (see **`STANDALONE_REPO.md`**).

## Continuous integration

GitHub Actions (`.github/workflows/ci.yml`) runs on pushes and pull requests: clones **[omiq/trse](https://github.com/omiq/trse)** for import scripts, then **`mkdocs build --strict`**. Download the **`site-html`** artifact from a workflow run to inspect the built output.

## Contributing

See **`CONTRIBUTING.md`**.

## Full maintainer guide

Read **`docs/MAINTAINING.md`** (or view it in the built site under **Maintaining this site**).

## Deploy to a server

From `retrodocs/`:

```bash
export DEPLOY_USER=you
export DEPLOY_HOST=your.server.example
export DEPLOY_PATH=/var/www/html/docs
./deploy.sh
```

See comments inside **`deploy.sh`** for SSH keys, dry-run, and safety options.

## Relationship to TRSE

This tree may live **inside** a TRSE fork or in its **own** GitHub repo. To split it out, see **`STANDALONE_REPO.md`**.

**TRSE’s built-in Help** is not copied here by default — see **`docs/trse/help-import.md`** for a future automated import.

Auto-generated TRSE reference pages need a checkout of **TRSE** (for `resources/text/` and `units/`). Set **`TRSE_REPO_ROOT`** or use **`--repo-root`** when `retrodocs` is not next to those paths — details in **`STANDALONE_REPO.md`**.

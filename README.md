# retrodocs — MkDocs site (educational documentation)

This directory builds the **Retro Game Coders** documentation site (Markdown → static HTML).

## Quick start

```bash
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

This repo may be a TRSE fork. **TRSE’s built-in Help** is *not* copied here by default — see **`docs/trse/help-import.md`** for how to add an automated import later.

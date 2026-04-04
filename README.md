# retrodocs — MkDocs site (educational documentation)

This directory builds the **Retro Game Coders** documentation site (Markdown → static HTML).

## Quick start

```bash
cd retrodocs
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve    # http://127.0.0.1:8000
```

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

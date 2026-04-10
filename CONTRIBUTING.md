# Contributing

The documentation source lives in **`docs/`** (Markdown). Configuration is in **`mkdocs.yml`**; styles in **`docs/stylesheets/extra.css`**.

1. Fork **[github.com/omiq/retrodocs](https://github.com/omiq/retrodocs)** and create a branch.
2. Install: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
3. For TRSE auto-generated pages, clone **[omiq/trse](https://github.com/omiq/trse)** and set `TRSE_REPO_ROOT`, then run the scripts in **`STANDALONE_REPO.md`**. For edits that only touch hand-written Markdown/CSS, `mkdocs build` is enough.
4. Run **`mkdocs build --strict`** locally (same as CI).
5. Open a pull request against **`main`**.

See **`docs/MAINTAINING.md`** for deploy, hooks, and troubleshooting.

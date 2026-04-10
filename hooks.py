"""
MkDocs hooks (see mkdocs.yml).

`mkdocs serve` writes to a **temporary** directory (prefix `mkdocs_`), not `./site`.
If the dev server has not **rebuilt** after you edit `docs/stylesheets/extra.css`, the
browser will keep getting the old file from that temp dir — force-refresh does not help
until you see “Detected file changes” / “Reloading browsers” in the terminal (or restart).

- **mkdocs serve** (temp `site_dir`): append `?v=` each rebuild.
- **MKDOCS_CSS_CACHE_BUST**: manual bust for local builds.
- **DEPLOY_CACHE_BUST**: set by `deploy.sh` so production HTML gets a new `extra.css?v=…`
  per deploy. Without this, Cloudflare/browsers often keep an old copy of the same URL
  even after rsync; purging caches is unreliable compared to a new query string.

`on_serve` additionally watches `os.path.realpath(docs_dir)` and each extra_css parent
directory. If `docs/` is a symlink (or the editor resolves paths differently), the default
watch on `docs_dir` alone can miss saves; an explicit real-path watch fixes that.

Plain `mkdocs build` (no env) leaves `extra.css` URLs unchanged; `deploy.sh` sets
`DEPLOY_CACHE_BUST` so production builds get a versioned URL.
"""

from __future__ import annotations

import os
import tempfile
import time

from mkdocs.config.defaults import MkDocsConfig


def _is_mkdocs_serve_staging_dir(site_dir: str) -> bool:
    """True when site_dir is the temp folder created by mkdocs serve (mkdocs_ prefix)."""
    if not site_dir:
        return False
    try:
        abs_site = os.path.normpath(os.path.abspath(site_dir))
        abs_tmp = os.path.normpath(os.path.abspath(tempfile.gettempdir()))
    except OSError:
        return False
    if abs_site == abs_tmp:
        return False
    if not abs_site.startswith(abs_tmp + os.sep):
        return False
    return os.path.basename(abs_site).startswith("mkdocs_")


def on_config(config: MkDocsConfig, **kwargs) -> MkDocsConfig | None:
    bust: str | None = None
    deploy = (os.environ.get("DEPLOY_CACHE_BUST") or "").strip()
    if deploy:
        bust = str(int(time.time() * 1000)) if deploy == "1" else deploy
    elif os.environ.get("MKDOCS_CSS_CACHE_BUST") or _is_mkdocs_serve_staging_dir(
        config.site_dir or ""
    ):
        bust = str(int(time.time() * 1000))
    if not bust:
        return None
    config.extra_css = [
        f"{path}?v={bust}" if "?" not in path else path for path in config.extra_css
    ]
    return config


def on_serve(server, *, config, builder, **kwargs):
    """Ensure CSS/static paths are watched even when docs_dir is a symlink."""
    abs_docs = os.path.abspath(config.docs_dir)
    real_docs = os.path.realpath(config.docs_dir)
    if real_docs != abs_docs:
        server.watch(real_docs)

    seen: set[str] = set()
    for raw in config.extra_css:
        rel = raw.split("?")[0].strip().replace("/", os.sep)
        parent = os.path.dirname(os.path.join(real_docs, rel))
        parent = os.path.normpath(parent)
        if parent in seen or not os.path.isdir(parent):
            continue
        seen.add(parent)
        server.watch(parent)

    return server

#!/usr/bin/env bash
# Deploy static MkDocs site to a remote server via rsync over SSH.
#
# Prerequisites (local):
#   - Python venv with mkdocs-material (see requirements.txt)
#   - ssh access to the server (key-based auth recommended)
#   - rsync installed (usually present on Linux/macOS)
#
# Usage:
   cd ~/github/trse/retrodocs
   source .venv/bin/activate
   export DEPLOY_HOST=server
   export DEPLOY_USER=docs
   export DEPLOY_PATH=/home/docs/htdocs/docs.retrogamecoders.com/
#   ./deploy.sh
#
# Optional:
#   DEPLOY_PORT=22          SSH port (default 22)
#   DEPLOY_KEY=~/.ssh/id_ed25519   Identity file for ssh/rsync
#   DRY_RUN=1               If set, rsync --dry-run only
#   SKIP_BUILD=1            If set, skip mkdocs build (use existing ./site)
#   SKIP_TRSE_IMPORT=1      If set, skip regenerating TRSE method + units pages
#   TRSE_REPO_ROOT=/path/to/TRSE   Required for standalone retrodocs repo (no ../trse layout); else auto-detect
#   NO_DEPLOY_CACHE_BUST=1  If set, do not set DEPLOY_CACHE_BUST (HTML will link stylesheets/extra.css
#                           with no ?v= — CDN/browser may keep an old CSS file at that URL)
#
# CloudPanel: DEPLOY_PATH must be the site’s actual document root for this host (the folder
# that contains index.html after upload). If CSS/HTML changes never appear, verify the path
# with: ssh user@host ls -la "$DEPLOY_PATH/stylesheets/extra.css"
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

DEPLOY_HOST="${DEPLOY_HOST:-}"
DEPLOY_USER="${DEPLOY_USER:-}"
DEPLOY_PATH="${DEPLOY_PATH:-}"
DEPLOY_PORT="${DEPLOY_PORT:-22}"
DEPLOY_KEY="${DEPLOY_KEY:-}"
DRY_RUN="${DRY_RUN:-}"
SKIP_BUILD="${SKIP_BUILD:-}"

if [[ -z "$DEPLOY_HOST" || -z "$DEPLOY_USER" || -z "$DEPLOY_PATH" ]]; then
  echo "Error: Set DEPLOY_HOST, DEPLOY_USER, and DEPLOY_PATH." >&2
  echo "Example:" >&2
  echo "  export DEPLOY_HOST=my.server" >&2
  echo "  export DEPLOY_USER=www-data" >&2
  echo "  export DEPLOY_PATH=/var/www/html/docs" >&2
  echo "  ./deploy.sh" >&2
  exit 1
fi

# Single ssh command string for rsync -e (must be one argument)
SSH_CMD="ssh -p ${DEPLOY_PORT} -o BatchMode=yes -o StrictHostKeyChecking=accept-new"
if [[ -n "$DEPLOY_KEY" ]]; then
  SSH_CMD+=" -i ${DEPLOY_KEY}"
fi

if [[ -z "${SKIP_BUILD:-}" ]]; then
  if ! command -v mkdocs >/dev/null 2>&1; then
    echo "Error: mkdocs not found. Activate your venv: source .venv/bin/activate" >&2
    exit 1
  fi
  if [[ -z "${SKIP_TRSE_IMPORT:-}" ]]; then
    if [[ -n "${TRSE_REPO_ROOT:-}" ]]; then
      export TRSE_REPO_ROOT
      echo "==> TRSE_REPO_ROOT=${TRSE_REPO_ROOT}"
    fi
    echo "==> import TRSE reference (syntax.txt + help/m/*.rtf)"
    python3 "$SCRIPT_DIR/scripts/import_trse_reference.py" --skip-init
    echo "==> import TRSE units catalog (units/**/*.tru)"
    python3 "$SCRIPT_DIR/scripts/import_trse_units.py"
  else
    echo "==> SKIP_TRSE_IMPORT: using existing docs/trse/reference/"
  fi
  # New ?v= on extra.css for this deploy so clients do not reuse a cached stylesheet at the
  # same URL (Cloudflare purge alone is often not enough). hooks.py reads DEPLOY_CACHE_BUST.
  if [[ -z "${NO_DEPLOY_CACHE_BUST:-}" ]]; then
    DEPLOY_CACHE_BUST="$(date -u +%Y%m%d%H%M%S)"
    export DEPLOY_CACHE_BUST
    echo "==> DEPLOY_CACHE_BUST=${DEPLOY_CACHE_BUST} (hooks append ?v= to extra_css)"
  else
    unset DEPLOY_CACHE_BUST 2>/dev/null || true
    echo "==> NO_DEPLOY_CACHE_BUST: extra.css URL unchanged (not recommended for production)"
  fi
  echo "==> mkdocs build"
  mkdocs build --strict
  echo "==> verify built CSS link (should include ?v= unless NO_DEPLOY_CACHE_BUST):"
  grep -o 'stylesheets/extra\.css[^"]*' site/index.html | head -1 || true
  ls -la site/stylesheets/extra.css 2>/dev/null || true
else
  echo "==> SKIP_BUILD: using existing ./site"
fi

if [[ ! -d site ]]; then
  echo "Error: ./site not found. Run mkdocs build first." >&2
  exit 1
fi

DEST="${DEPLOY_USER}@${DEPLOY_HOST}:${DEPLOY_PATH}"
RSYNC_FLAGS=( -avz --delete )
if [[ -n "$DRY_RUN" ]]; then
  RSYNC_FLAGS+=( --dry-run )
  echo "==> DRY RUN (no files changed on server)"
fi

echo "==> rsync site/ -> ${DEST}"
rsync "${RSYNC_FLAGS[@]}" -e "$SSH_CMD" site/ "$DEST"

echo "==> Done."

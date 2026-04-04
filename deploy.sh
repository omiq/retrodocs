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
  echo "==> mkdocs build"
  mkdocs build --strict
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

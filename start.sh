#!/bin/sh
# Local preview: MkDocs Material dev server.
# Usage: ./retrodocs/start.sh   or   cd retrodocs && ./start.sh
#        http://127.0.0.1:8000
cd "$(dirname "$0")" || exit 1

if [ ! -f .venv/bin/activate ]; then
  python3 -m venv .venv || exit 1
fi
. .venv/bin/activate
pip install -r requirements.txt

# Poll docs/stylesheets/ and touch mkdocs.yml on changes so `mkdocs serve` always rebuilds
# (native fs events often miss CSS saves from some editors on macOS).
python3 scripts/touch_mkdocs_on_css_save.py &
CSS_TOUCH_PID=$!
cleanup() {
  kill "$CSS_TOUCH_PID" 2>/dev/null
}
trap cleanup INT TERM EXIT

# Optional: force extra_css cache-bust (hooks.py also detects mkdocs serve temp dir).
# export MKDOCS_CSS_CACHE_BUST=1

mkdocs serve -w docs -w docs/stylesheets -w mkdocs.yml
STATUS=$?
cleanup
trap - INT TERM EXIT
exit "$STATUS"

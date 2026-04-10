#!/usr/bin/env python3
"""
Background helper for `start.sh`: when anything under docs/stylesheets/ changes,
touch mkdocs.yml so MkDocs' config watcher schedules a rebuild.

Some editors / OS setups miss CSS file events for the default server watcher; touching
the config file is a reliable nudge. Watchdog is already required by MkDocs.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

try:
    from watchdog.events import FileSystemEventHandler
    from watchdog.observers.polling import PollingObserver
except ImportError:
    print("touch_mkdocs_on_css_save: watchdog not installed (unexpected for MkDocs)", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]
STYLES = ROOT / "docs" / "stylesheets"
CONFIG = ROOT / "mkdocs.yml"

DEBOUNCE_S = 0.2
_last = 0.0


def _touch_config() -> None:
    global _last
    now = time.monotonic()
    if now - _last < DEBOUNCE_S:
        return
    _last = now
    try:
        CONFIG.touch()
    except OSError:
        pass


class _Handler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory:
            return
        _touch_config()


def main() -> None:
    STYLES.mkdir(parents=True, exist_ok=True)
    obs = PollingObserver(timeout=0.25)
    obs.schedule(_Handler(), str(STYLES), recursive=True)
    obs.start()
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        pass
    finally:
        obs.stop()
        obs.join(timeout=2)


if __name__ == "__main__":
    main()

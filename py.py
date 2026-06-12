#!/usr/bin/env python3
"""
DKG mobile homepage tweak:
Stop vertical scrolling from resetting mobile product autoscroll loops.

Cause:
- Mobile Safari/Chrome often fire window resize events while scrolling vertically
  because the browser address bar expands/collapses.
- The carousel script was rebuilding all mobile carousels on every resize.
- Rebuilding resets the autoscroll index/timer.

Fix:
- Ignore height-only resize events.
- Only rebuild when viewport width changes meaningfully, orientation changes,
  or the mobile breakpoint state changes.

Edits:
- assets/js/dkg-mobile-main-homepage-plates.js

Backups are created before edits.

Run from theme repo root:
    python mobile_stop_scroll_reset_autoscroll.py
"""

from __future__ import annotations

import re
import shutil
from datetime import datetime
from pathlib import Path


STABILITY_START = "  // === DKG MOBILE WIDTH-STABLE RESIZE START ==="
STABILITY_END = "  // === DKG MOBILE WIDTH-STABLE RESIZE END ==="


STABILITY_BLOCK = r'''  // === DKG MOBILE WIDTH-STABLE RESIZE START ===
  /*
    Mobile browsers can fire resize events during normal vertical scrolling when
    the address bar expands/collapses. That should NOT rebuild the carousel,
    because rebuilding resets the autoscroll loop.

    We only rebuild when:
    - the viewport width changes meaningfully,
    - the mobile/non-mobile breakpoint changes,
    - or orientationchange explicitly fires.
  */
  var dkgLastLayoutWidth = window.innerWidth || document.documentElement.clientWidth || 0;
  var dkgLastMobileMatch = matchesMobile();

  function dkgGetLayoutWidth() {
    return window.innerWidth || document.documentElement.clientWidth || 0;
  }

  function dkgShouldRebuildForViewportChange(event) {
    var force = !!(event && event.type === "orientationchange");
    var currentWidth = dkgGetLayoutWidth();
    var currentMobileMatch = matchesMobile();

    var widthDelta = Math.abs(currentWidth - dkgLastLayoutWidth);
    var mobileStateChanged = currentMobileMatch !== dkgLastMobileMatch;

    /*
      A few pixels can change from scrollbars/device rounding.
      On phones, height-only address-bar changes usually keep width the same.
    */
    var meaningfulWidthChange = widthDelta >= 24;

    if (!force && !mobileStateChanged && !meaningfulWidthChange) {
      return false;
    }

    dkgLastLayoutWidth = currentWidth;
    dkgLastMobileMatch = currentMobileMatch;

    return true;
  }
  // === DKG MOBILE WIDTH-STABLE RESIZE END ===
'''


NEW_SCHEDULE_FUNCTION = r'''  function scheduleSetup(event) {
    if (!dkgShouldRebuildForViewportChange(event)) {
      return;
    }

    if (resizeTimer) {
      window.clearTimeout(resizeTimer);
    }

    resizeTimer = window.setTimeout(setupAll, RESIZE_DEBOUNCE_MS);
  }
'''


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", errors="replace")


def remove_marker_block(text: str, start: str, end: str) -> tuple[str, int]:
    pattern = re.compile(
        re.escape(start) + r".*?" + re.escape(end),
        flags=re.DOTALL,
    )
    new_text, count = pattern.subn("", text)
    new_text = re.sub(r"\n{4,}", "\n\n\n", new_text)
    return new_text.rstrip() + "\n", count


def insert_stability_block(js: str) -> tuple[str, bool]:
    js, _ = remove_marker_block(js, STABILITY_START, STABILITY_END)

    anchor = "  var resizeTimer = null;"

    if anchor not in js:
        return js, False

    insert_at = js.find(anchor) + len(anchor)

    js = (
        js[:insert_at].rstrip()
        + "\n\n"
        + STABILITY_BLOCK.rstrip()
        + "\n"
        + js[insert_at:].lstrip()
    )

    return js, True


def replace_schedule_setup(js: str) -> tuple[str, bool]:
    pattern = re.compile(
        r"\n\s*function\s+scheduleSetup\s*\([^)]*\)\s*\{"
        r"(?:[^{}]|\{[^{}]*\})*?"
        r"\n\s*\}",
        flags=re.DOTALL,
    )

    new_js, count = pattern.subn("\n" + NEW_SCHEDULE_FUNCTION.rstrip(), js, count=1)
    return new_js, count == 1


def main() -> int:
    root = Path.cwd().resolve()
    js_path = root / "assets" / "js" / "dkg-mobile-main-homepage-plates.js"

    if not js_path.exists():
        raise SystemExit(
            "Missing assets/js/dkg-mobile-main-homepage-plates.js.\n\n"
            "Run this from the theme repo root:\n"
            r'  C:\Users\John\Desktop\shop dkg\dkg-shop-theme'
        )

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_dir = root / f"_dkg_mobile_stop_scroll_reset_backup_{timestamp}"
    backup_dir.mkdir(parents=True, exist_ok=False)

    backup_js = backup_dir / "assets" / "js" / "dkg-mobile-main-homepage-plates.js"
    backup_js.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(js_path, backup_js)

    old_js = read_text(js_path)

    new_js, inserted_stability = insert_stability_block(old_js)
    new_js, replaced_schedule = replace_schedule_setup(new_js)

    if not inserted_stability:
        raise SystemExit(
            "Could not find expected JS anchor:\n"
            "  var resizeTimer = null;\n\n"
            f"Backup was still created at:\n  {backup_js}\n\n"
            "No changes were written."
        )

    if not replaced_schedule:
        raise SystemExit(
            "Could not safely replace function scheduleSetup().\n\n"
            f"Backup was still created at:\n  {backup_js}\n\n"
            "No changes were written."
        )

    write_text(js_path, new_js)

    summary_path = backup_dir / "stop_scroll_reset_summary.txt"
    summary = [
        "DKG mobile stop scroll reset updater",
        f"Timestamp: {timestamp}",
        f"Repo root: {root}",
        "",
        "Backup:",
        f"- {backup_js}",
        "",
        "Changes:",
        "- Added width-stable resize detection.",
        "- Replaced scheduleSetup(event) so height-only resize events are ignored.",
        "- Vertical scrolling should no longer rebuild/reset the autoscroll loops.",
        "- Orientation changes and real width changes still rebuild correctly.",
        "",
        f"Inserted stability block: {inserted_stability}",
        f"Replaced scheduleSetup: {replaced_schedule}",
    ]

    write_text(summary_path, "\n".join(summary) + "\n")

    print("Done.")
    print(f"Backup folder: {backup_dir}")
    print("Added width-stable resize handling.")
    print("Vertical scroll/address-bar resize should no longer reset the product autoscroll loops.")
    print("")
    print("Next:")
    print("1. Upload/deploy assets/js/dkg-mobile-main-homepage-plates.js.")
    print("2. Clear cache.")
    print("3. Test by waiting for the carousel to advance, then slowly scrolling up/down.")
    print("4. The carousel should continue from where it was instead of jumping back to the first product.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
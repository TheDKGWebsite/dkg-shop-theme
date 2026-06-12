#!/usr/bin/env python3
"""
DKG mobile homepage tweak:
- Hide/remove the left slide-in overlay image on mobile.
- Speed up the mobile collection product auto-scroller.

Edits:
- assets/css/front-page.css
- assets/js/dkg-mobile-main-homepage-plates.js

Backups are created before edits.

Run from theme repo root:
    python mobile_hide_left_overlay_speed_carousel.py
"""

from __future__ import annotations

import re
import shutil
from datetime import datetime
from pathlib import Path


NEW_AUTOSCROLL_MS = 1900

CSS_START = "/* === DKG MOBILE HIDE LEFT OVERLAY START === */"
CSS_END = "/* === DKG MOBILE HIDE LEFT OVERLAY END === */"

JS_START = "  // === DKG MOBILE REMOVE LEFT OVERLAY START ==="
JS_END = "  // === DKG MOBILE REMOVE LEFT OVERLAY END ==="


CSS_BLOCK = r'''/* === DKG MOBILE HIDE LEFT OVERLAY START === */

/*
  Hide the desktop left slide-in overlay image on the normal homepage for mobile.
  This is intentionally narrow: it targets .dkg-left-overlay only.
  It does not hide the header picture rotator or product images.
*/

@media screen and (max-width: 767px) {
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .dkg-left-overlay,
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .dkg-left-overlay * {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;

    width: 0 !important;
    height: 0 !important;
    min-width: 0 !important;
    min-height: 0 !important;
    max-width: 0 !important;
    max-height: 0 !important;

    margin: 0 !important;
    padding: 0 !important;
    border: 0 !important;

    overflow: hidden !important;
    pointer-events: none !important;
    transform: none !important;
  }
}

/* === DKG MOBILE HIDE LEFT OVERLAY END === */
'''


JS_REMOVE_OVERLAY_FUNCTION = r'''  // === DKG MOBILE REMOVE LEFT OVERLAY START ===
  function removeMobileLeftOverlay() {
    if (!matchesMobile()) {
      return;
    }

    /*
      The desktop left slide-in overlay is not useful on mobile and can visually
      interfere with the normal homepage collection plates. Remove it from the
      mobile DOM instead of only hiding it with CSS.
    */
    toArray(document.querySelectorAll(".dkg-left-overlay")).forEach(function (node) {
      if (node && node.parentNode) {
        node.setAttribute("aria-hidden", "true");
        node.parentNode.removeChild(node);
      }
    });
  }
  // === DKG MOBILE REMOVE LEFT OVERLAY END ===
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


def append_css_block(css: str) -> str:
    cleaned, _ = remove_marker_block(css, CSS_START, CSS_END)
    return cleaned.rstrip() + "\n\n" + CSS_BLOCK.rstrip() + "\n"


def update_autoscroll_interval(js: str) -> tuple[str, int]:
    """
    Replaces:
      var AUTOSCROLL_MS = 2600;
    or any similar numeric value.
    """
    pattern = re.compile(
        r"(var\s+AUTOSCROLL_MS\s*=\s*)\d+(\s*;)",
        flags=re.IGNORECASE,
    )
    new_js, count = pattern.subn(
        rf"\g<1>{NEW_AUTOSCROLL_MS}\g<2>",
        js,
        count=1,
    )
    return new_js, count


def inject_mobile_overlay_removal(js: str) -> tuple[str, bool]:
    """
    Adds removeMobileLeftOverlay() and calls it at the start of setupAll().
    Designed for the current dkg-mobile-main-homepage-plates.js structure.
    """

    # Remove old copy of this injected block if rerun.
    js, _ = remove_marker_block(js, JS_START, JS_END)

    # Remove prior call if rerun.
    js = re.sub(
        r"\n\s*removeMobileLeftOverlay\(\);\s*\n",
        "\n",
        js,
        flags=re.IGNORECASE,
    )

    setup_match = re.search(r"\n\s*function\s+setupAll\s*\(\)\s*\{", js)

    if not setup_match:
        return js, False

    insert_at = setup_match.start()
    js = js[:insert_at].rstrip() + "\n\n" + JS_REMOVE_OVERLAY_FUNCTION.rstrip() + "\n" + js[insert_at:]

    # Add call immediately inside setupAll().
    js = re.sub(
        r"(\n\s*function\s+setupAll\s*\(\)\s*\{\s*)",
        r"\1\n    removeMobileLeftOverlay();\n",
        js,
        count=1,
    )

    return js, True


def main() -> int:
    root = Path.cwd().resolve()

    css_path = root / "assets" / "css" / "front-page.css"
    js_path = root / "assets" / "js" / "dkg-mobile-main-homepage-plates.js"

    if not css_path.exists() or not js_path.exists():
        raise SystemExit(
            "Missing required files. Run this from the theme repo root:\n"
            r'  C:\Users\John\Desktop\shop dkg\dkg-shop-theme'
        )

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_dir = root / f"_dkg_mobile_hide_left_overlay_speed_backup_{timestamp}"
    backup_dir.mkdir(parents=True, exist_ok=False)

    backup_css = backup_dir / "assets" / "css" / "front-page.css"
    backup_js = backup_dir / "assets" / "js" / "dkg-mobile-main-homepage-plates.js"

    backup_css.parent.mkdir(parents=True, exist_ok=True)
    backup_js.parent.mkdir(parents=True, exist_ok=True)

    shutil.copy2(css_path, backup_css)
    shutil.copy2(js_path, backup_js)

    old_css = read_text(css_path)
    new_css = append_css_block(old_css)
    write_text(css_path, new_css)

    old_js = read_text(js_path)
    new_js, interval_replacements = update_autoscroll_interval(old_js)
    new_js, overlay_injected = inject_mobile_overlay_removal(new_js)
    write_text(js_path, new_js)

    summary_path = backup_dir / "hide_left_overlay_speed_summary.txt"
    summary = [
        "DKG mobile hide left overlay + speed carousel updater",
        f"Timestamp: {timestamp}",
        f"Repo root: {root}",
        "",
        "Backups:",
        f"- {backup_css}",
        f"- {backup_js}",
        "",
        "Changes:",
        "- Added mobile CSS to hide .dkg-left-overlay on phone widths.",
        "- Added JS to remove .dkg-left-overlay from the mobile DOM.",
        f"- Set AUTOSCROLL_MS to {NEW_AUTOSCROLL_MS}.",
        "",
        f"Interval replacements made: {interval_replacements}",
        f"Overlay removal injected: {overlay_injected}",
        "",
        "If carousel still feels slow, lower NEW_AUTOSCROLL_MS to 1700.",
        "If carousel feels too fast, raise NEW_AUTOSCROLL_MS to 2100.",
    ]

    write_text(summary_path, "\n".join(summary) + "\n")

    print("Done.")
    print(f"Backup folder: {backup_dir}")
    print(f"Carousel interval set to: {NEW_AUTOSCROLL_MS}ms")
    print(f"Interval replacements made: {interval_replacements}")
    print(f"Overlay removal injected: {overlay_injected}")
    print("")
    print("Next:")
    print("1. Upload/deploy assets/css/front-page.css and assets/js/dkg-mobile-main-homepage-plates.js.")
    print("2. Clear cache.")
    print("3. Test the normal homepage on mobile.")
    print("")
    print("To tune speed later:")
    print("- Faster: set NEW_AUTOSCROLL_MS to 1700.")
    print("- Slower: set NEW_AUTOSCROLL_MS to 2100.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
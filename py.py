#!/usr/bin/env python3
"""
DKG mobile header rotator relocation updater.

Goal:
- On mobile only, move the existing framed header image rotator OUT of the header.
- Place it below all homepage collection plates.
- Do not clone it.
- Do not edit header.php.
- Restore it back to its original header position on desktop widths.
- Avoid position/flex/absolute issues by giving the relocated rotator its own stable zone.

Edits:
- assets/css/front-page.css
- assets/js/dkg-mobile-header-rotator-relocate.js
- functions.php

Backups are created first.

Run from theme repo root:
    python mobile_move_header_rotator_below_plates.py
"""

from __future__ import annotations

import re
import shutil
from datetime import datetime
from pathlib import Path


CSS_START = "/* === DKG MOBILE HEADER ROTATOR BELOW PLATES START === */"
CSS_END = "/* === DKG MOBILE HEADER ROTATOR BELOW PLATES END === */"

ENQUEUE_START = "// === DKG MOBILE HEADER ROTATOR RELOCATE ENQUEUE START ==="
ENQUEUE_END = "// === DKG MOBILE HEADER ROTATOR RELOCATE ENQUEUE END ==="

JS_FILENAME = "dkg-mobile-header-rotator-relocate.js"


NEW_CSS_BLOCK = r'''/* === DKG MOBILE HEADER ROTATOR BELOW PLATES START === */

/*
  Mobile-only relocation styling for the existing header picture rotator.

  The actual DOM move is handled by:
    assets/js/dkg-mobile-header-rotator-relocate.js

  Important:
  - This does not clone the rotator.
  - It only styles the rotator after JS moves it below the collection plates.
  - It does not change desktop header behavior.
  - It avoids using the header's flex sizing/overhang rules after relocation.
*/

@media screen and (max-width: 767px) {

  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .dkg-mobile-relocated-header-rotator-zone {
    width: 100% !important;
    max-width: 100% !important;

    margin: 18px auto 26px !important;
    padding: 0 10px !important;
    box-sizing: border-box !important;

    display: flex !important;
    justify-content: center !important;
    align-items: center !important;

    position: relative !important;
    z-index: 2 !important;

    overflow: visible !important;
    pointer-events: none !important;
    transform: none !important;
  }

  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .dkg-mobile-relocated-header-rotator-zone .dkg-header-picture-rotator,
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .dkg-header-picture-rotator.dkg-mobile-header-rotator-relocated {
    position: relative !important;

    flex: 0 0 auto !important;
    align-self: auto !important;

    width: min(calc(100vw - 24px), 420px) !important;
    max-width: 420px !important;
    min-width: 0 !important;

    height: clamp(122px, 41vw, 175px) !important;
    min-height: clamp(122px, 41vw, 175px) !important;
    max-height: 175px !important;

    margin: 0 auto !important;
    padding: 0 !important;
    box-sizing: border-box !important;

    display: block !important;
    overflow: visible !important;

    z-index: 2 !important;
    transform: none !important;
    pointer-events: none !important;
  }

  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .dkg-mobile-relocated-header-rotator-zone .dkg-header-picture-frame,
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .dkg-header-picture-rotator.dkg-mobile-header-rotator-relocated .dkg-header-picture-frame {
    position: absolute !important;

    left: 0 !important;
    top: 0 !important;
    right: auto !important;
    bottom: auto !important;

    width: 100% !important;
    max-width: 100% !important;
    min-width: 0 !important;

    height: 100% !important;
    min-height: 100% !important;
    max-height: 100% !important;

    margin: 0 !important;
    padding: 0 !important;
    box-sizing: border-box !important;

    display: block !important;
    overflow: visible !important;

    background-size: 100% 100% !important;
    background-position: center center !important;
    background-repeat: no-repeat !important;

    z-index: 2 !important;
    transform: none !important;
    pointer-events: none !important;
  }

  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .dkg-mobile-relocated-header-rotator-zone .dkg-header-picture-img,
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .dkg-header-picture-rotator.dkg-mobile-header-rotator-relocated .dkg-header-picture-img {
    position: absolute !important;

    left: 8% !important;
    top: 9% !important;

    width: 84% !important;
    height: 82% !important;
    max-width: none !important;
    max-height: none !important;

    display: block !important;
    object-fit: cover !important;
    object-position: center center !important;

    margin: 0 !important;
    padding: 0 !important;

    z-index: 1 !important;
    transform: none !important;
    pointer-events: none !important;
  }

  /*
    While mobile relocation is active, make sure the header does not reserve
    any old rotator space if a cached/duplicate style tries to keep it there.
  */
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .site-header .header-inner > .dkg-header-picture-rotator.dkg-mobile-header-rotator-relocated {
    display: none !important;
  }
}

/* === DKG MOBILE HEADER ROTATOR BELOW PLATES END === */
'''


NEW_JS = r'''/*
  DKG mobile header rotator relocate.

  Mobile only:
  - Move the existing .dkg-header-picture-rotator out of the header.
  - Insert it below all homepage collection plates.
  - Do not clone it.
  - Restore it back to its original header position on desktop.

  This intentionally avoids editing header.php.
*/

(function () {
  "use strict";

  var MOBILE_QUERY = "(max-width: 767px)";
  var ZONE_CLASS = "dkg-mobile-relocated-header-rotator-zone";
  var RELOCATED_CLASS = "dkg-mobile-header-rotator-relocated";
  var RESIZE_DEBOUNCE_MS = 160;

  var originalParent = null;
  var originalNextSibling = null;
  var originalWasCaptured = false;
  var resizeTimer = null;
  var lastLayoutWidth = window.innerWidth || document.documentElement.clientWidth || 0;
  var lastMobileMatch = matchesMobile();

  function matchesMobile() {
    if (!window.matchMedia) {
      return window.innerWidth <= 767;
    }

    return window.matchMedia(MOBILE_QUERY).matches;
  }

  function toArray(list) {
    return Array.prototype.slice.call(list || []);
  }

  function getLayoutWidth() {
    return window.innerWidth || document.documentElement.clientWidth || 0;
  }

  function shouldRunForViewportChange(event) {
    if (event && event.type === "orientationchange") {
      lastLayoutWidth = getLayoutWidth();
      lastMobileMatch = matchesMobile();
      return true;
    }

    var currentWidth = getLayoutWidth();
    var currentMobileMatch = matchesMobile();
    var widthDelta = Math.abs(currentWidth - lastLayoutWidth);
    var mobileChanged = currentMobileMatch !== lastMobileMatch;

    /*
      Ignore mobile browser height-only resize events from address-bar movement.
    */
    if (!mobileChanged && widthDelta < 24) {
      return false;
    }

    lastLayoutWidth = currentWidth;
    lastMobileMatch = currentMobileMatch;
    return true;
  }

  function getRotator() {
    return document.querySelector(".dkg-header-picture-rotator");
  }

  function captureOriginalPosition(rotator) {
    if (originalWasCaptured || !rotator || !rotator.parentNode) {
      return;
    }

    originalParent = rotator.parentNode;
    originalNextSibling = rotator.nextSibling;
    originalWasCaptured = true;
  }

  function getCollectionsSection() {
    return (
      document.querySelector("main.collections-section") ||
      document.querySelector(".collections-section") ||
      document.querySelector(".collections-stack")
    );
  }

  function getOrCreateZone() {
    var existing = document.querySelector("." + ZONE_CLASS);

    if (existing) {
      return existing;
    }

    var zone = document.createElement("div");
    zone.className = ZONE_CLASS;
    zone.setAttribute("aria-hidden", "true");

    return zone;
  }

  function insertZoneBelowCollections(zone) {
    var section = getCollectionsSection();

    if (!section || !section.parentNode) {
      return false;
    }

    /*
      If the selector fell back to .collections-stack, insert after its parent
      when the parent is the actual main.collections-section.
    */
    if (
      section.classList &&
      section.classList.contains("collections-stack") &&
      section.parentNode &&
      section.parentNode.classList &&
      section.parentNode.classList.contains("collections-section")
    ) {
      section = section.parentNode;
    }

    if (zone.parentNode === section.parentNode && zone.previousSibling === section) {
      return true;
    }

    section.parentNode.insertBefore(zone, section.nextSibling);
    return true;
  }

  function moveRotatorBelowPlates() {
    var rotator = getRotator();

    if (!rotator) {
      return;
    }

    captureOriginalPosition(rotator);

    var zone = getOrCreateZone();

    if (!insertZoneBelowCollections(zone)) {
      return;
    }

    if (rotator.parentNode !== zone) {
      zone.appendChild(rotator);
    }

    rotator.classList.add(RELOCATED_CLASS);
    rotator.setAttribute("data-dkg-mobile-relocated", "true");
    rotator.setAttribute("aria-hidden", "true");
  }

  function restoreRotatorToHeader() {
    var rotator = getRotator();

    if (!rotator || !originalParent) {
      removeEmptyZone();
      return;
    }

    rotator.classList.remove(RELOCATED_CLASS);
    rotator.removeAttribute("data-dkg-mobile-relocated");

    if (rotator.parentNode !== originalParent) {
      if (originalNextSibling && originalNextSibling.parentNode === originalParent) {
        originalParent.insertBefore(rotator, originalNextSibling);
      } else {
        originalParent.appendChild(rotator);
      }
    }

    removeEmptyZone();
  }

  function removeEmptyZone() {
    var zone = document.querySelector("." + ZONE_CLASS);

    if (!zone) {
      return;
    }

    if (!zone.children.length && zone.parentNode) {
      zone.parentNode.removeChild(zone);
    }
  }

  function applyLayout() {
    var rotator = getRotator();

    if (!rotator) {
      return;
    }

    captureOriginalPosition(rotator);

    if (matchesMobile()) {
      moveRotatorBelowPlates();
    } else {
      restoreRotatorToHeader();
    }
  }

  function scheduleApply(event) {
    if (!shouldRunForViewportChange(event)) {
      return;
    }

    if (resizeTimer) {
      window.clearTimeout(resizeTimer);
    }

    resizeTimer = window.setTimeout(applyLayout, RESIZE_DEBOUNCE_MS);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", applyLayout);
  } else {
    applyLayout();
  }

  window.addEventListener("resize", scheduleApply);
  window.addEventListener("orientationchange", scheduleApply);

  if (window.matchMedia) {
    try {
      var mq = window.matchMedia(MOBILE_QUERY);

      if (mq.addEventListener) {
        mq.addEventListener("change", scheduleApply);
      } else if (mq.addListener) {
        mq.addListener(scheduleApply);
      }
    } catch (error) {
      /*
        Non-critical. Resize/orientation listeners still handle changes.
      */
    }
  }

  /*
    If the collection plates are built late by another script/cache layer,
    give the relocation one extra pass after load.
  */
  window.addEventListener("load", function () {
    window.setTimeout(applyLayout, 80);
  });
})();
'''


NEW_ENQUEUE_BLOCK = r'''// === DKG MOBILE HEADER ROTATOR RELOCATE ENQUEUE START ===

function dkg_enqueue_mobile_header_rotator_relocate() {
    if (is_admin()) {
        return;
    }

    /*
     * This is for the normal homepage only.
     * It moves the existing framed header rotator below the homepage collection plates on mobile.
     */
    if (!is_front_page()) {
        return;
    }

    $script_path = get_template_directory() . '/assets/js/dkg-mobile-header-rotator-relocate.js';
    $script_uri  = get_template_directory_uri() . '/assets/js/dkg-mobile-header-rotator-relocate.js';

    if (file_exists($script_path)) {
        wp_enqueue_script(
            'dkg-mobile-header-rotator-relocate',
            $script_uri,
            array(),
            filemtime($script_path),
            true
        );
    }
}
add_action('wp_enqueue_scripts', 'dkg_enqueue_mobile_header_rotator_relocate', 40);

// === DKG MOBILE HEADER ROTATOR RELOCATE ENQUEUE END ===
'''


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", errors="replace")


def make_backup(root: Path, backup_dir: Path, rel_path: str) -> None:
    src = root / rel_path

    if not src.exists():
        return

    dest = backup_dir / rel_path
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)


def remove_marker_block(text: str, start: str, end: str) -> tuple[str, int]:
    pattern = re.compile(
        re.escape(start) + r".*?" + re.escape(end),
        flags=re.DOTALL,
    )
    new_text, count = pattern.subn("", text)
    new_text = re.sub(r"\n{4,}", "\n\n\n", new_text)
    return new_text.rstrip() + "\n", count


def append_or_replace_css(root: Path) -> str:
    css_path = root / "assets" / "css" / "front-page.css"

    if not css_path.exists():
        raise FileNotFoundError(f"Missing CSS file: {css_path}")

    old_css = read_text(css_path)
    cleaned_css, removed_count = remove_marker_block(old_css, CSS_START, CSS_END)
    new_css = cleaned_css.rstrip() + "\n\n" + NEW_CSS_BLOCK.rstrip() + "\n"

    if new_css != old_css:
        write_text(css_path, new_css)

    return f"CSS updated: removed old relocation blocks={removed_count}, appended clean relocation CSS."


def write_js(root: Path) -> str:
    js_dir = root / "assets" / "js"
    js_dir.mkdir(parents=True, exist_ok=True)

    js_path = js_dir / JS_FILENAME
    old_js = read_text(js_path) if js_path.exists() else ""

    if old_js != NEW_JS:
        write_text(js_path, NEW_JS)

    return f"JS updated: wrote assets/js/{JS_FILENAME}."


def update_functions_enqueue(root: Path) -> str:
    functions_path = root / "functions.php"

    if not functions_path.exists():
        raise FileNotFoundError(f"Missing functions.php: {functions_path}")

    old = read_text(functions_path)

    cleaned, removed_count = remove_marker_block(old, ENQUEUE_START, ENQUEUE_END)

    if "dkg_enqueue_mobile_header_rotator_relocate" in cleaned or "dkg-mobile-header-rotator-relocate" in cleaned:
        # Avoid duplicating if some unexpected old version exists without markers.
        new_text = cleaned
        message = (
            "functions.php: found existing mobile header rotator relocate enqueue outside expected markers; "
            "removed marked blocks only and did not append another enqueue."
        )
    else:
        new_text = cleaned.rstrip() + "\n\n" + NEW_ENQUEUE_BLOCK.rstrip() + "\n"
        message = f"functions.php updated: removed old enqueue blocks={removed_count}, appended clean enqueue."

    if new_text != old:
        write_text(functions_path, new_text)

    return message


def sanity_check(root: Path) -> None:
    missing = []

    for rel in ["functions.php", "assets/css/front-page.css", "header.php", "front-page.php"]:
        if not (root / rel).exists():
            missing.append(rel)

    if missing:
        raise SystemExit(
            "This does not look like the theme repo root, or required files are missing:\n"
            + "\n".join(f"  - {item}" for item in missing)
            + "\n\nRun from:\n"
            + r'  C:\Users\John\Desktop\shop dkg\dkg-shop-theme'
        )


def main() -> int:
    root = Path.cwd().resolve()
    sanity_check(root)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_dir = root / f"_dkg_mobile_header_rotator_below_plates_backup_{timestamp}"
    backup_dir.mkdir(parents=True, exist_ok=False)

    files_to_backup = [
        "functions.php",
        "assets/css/front-page.css",
        f"assets/js/{JS_FILENAME}",
    ]

    for rel in files_to_backup:
        make_backup(root, backup_dir, rel)

    messages = [
        append_or_replace_css(root),
        write_js(root),
        update_functions_enqueue(root),
    ]

    summary_path = backup_dir / "mobile_header_rotator_below_plates_summary.txt"
    summary = [
        "DKG mobile header rotator below plates updater",
        f"Timestamp: {timestamp}",
        f"Repo root: {root}",
        f"Backup folder: {backup_dir}",
        "",
        "Actions:",
    ]
    summary.extend(f"- {msg}" for msg in messages)
    summary.extend(
        [
            "",
            "Expected mobile behavior:",
            "- The existing framed header image rotator is moved out of the header.",
            "- It appears below all homepage collection plates.",
            "- The move happens only at max-width 767px.",
            "- Desktop restores the rotator to its original position inside .header-inner.",
            "- The rotator is not cloned; existing image/frame/data attributes are preserved.",
            "- The relocated frame gets stable relative sizing so it does not use header flex/overhang positioning.",
            "",
            "Files backed up:",
        ]
    )
    summary.extend(f"- {rel}" for rel in files_to_backup)

    write_text(summary_path, "\n".join(summary) + "\n")

    print("Done.")
    print(f"Backup folder: {backup_dir}")
    print("")
    for msg in messages:
        print(f"- {msg}")

    print("")
    print("Next:")
    print("1. Upload/deploy functions.php, assets/css/front-page.css, and assets/js/dkg-mobile-header-rotator-relocate.js.")
    print("2. Clear site/plugin/browser cache.")
    print("3. Test normal homepage on mobile width.")
    print("4. Confirm the framed rotator appears after the last collection plate and not inside the sticky header.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
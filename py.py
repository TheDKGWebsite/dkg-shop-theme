#!/usr/bin/env python3
"""
DKG mobile homepage cleanup updater.

Goal:
- Keep mobile users on the normal homepage.
- Replace the old/stacked mobile homepage collection-plate CSS block.
- Replace assets/js/dkg-mobile-main-homepage-plates.js with a stricter version.
- Keep .collection-bg decorative only.
- Insert the mobile carousel INSIDE .collection-content, after .collection-label.
- Hide the original .carousel-shell only on mobile and only after JS successfully builds the cloned layer.
- Disable any active mobile redirect hook if it has reappeared.
- Ensure the mobile JS enqueue exists and is front-page-only.

Run from the root of the theme repo:
    python mobile_main_homepage_cleanup_updater.py

This script edits:
    assets/css/front-page.css
    assets/js/dkg-mobile-main-homepage-plates.js
    functions.php

It creates backups first.
"""

from __future__ import annotations

import os
import re
import shutil
from datetime import datetime
from pathlib import Path


CSS_START = "/* === DKG MOBILE MAIN HOMEPAGE COLLECTION PLATES START === */"
CSS_END = "/* === DKG MOBILE MAIN HOMEPAGE COLLECTION PLATES END === */"

ENQUEUE_START = "// === DKG MOBILE MAIN HOMEPAGE COLLECTION PLATES ENQUEUE START ==="
ENQUEUE_END = "// === DKG MOBILE MAIN HOMEPAGE COLLECTION PLATES ENQUEUE END ==="


NEW_CSS_BLOCK = r'''/* === DKG MOBILE MAIN HOMEPAGE COLLECTION PLATES START === */

/*
  DKG mobile homepage collection plates - cleanup layer.

  Important structure from front-page.php:

  .collection-box
    .collection-bg
      img
    .collection-content
      .collection-label
      .carousel-shell
        .product-viewport
          .product-track
            .product-card
              img.product-image

  Rules:
  - .collection-bg stays decorative only.
  - .collection-label stays stable and centered.
  - JS inserts .dkg-mobile-carousel-viewport inside .collection-content after .collection-label.
  - JS hides only the original .carousel-shell after clone layer is built.
  - Nothing here targets /mobile-shop/ specific classes.
  - Header overhaul is intentionally not handled here.
*/

@media screen and (max-width: 767px) {

  html,
  body {
    overflow-x: hidden !important;
  }

  .page-overlay,
  .collections-section {
    width: 100% !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
    overflow-x: hidden !important;
  }

  .collections-section {
    padding-left: 0 !important;
    padding-right: 0 !important;
  }

  .collections-stack {
    width: 100% !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    gap: 16px !important;
    overflow: visible !important;
  }

  .collection-link {
    width: 100% !important;
    max-width: 520px !important;
    display: block !important;
    box-sizing: border-box !important;
    text-decoration: none !important;
    overflow: visible !important;
  }

  .collection-box {
    --dkg-mobile-card-gap: 8px;

    position: relative !important;
    width: calc(100vw - 20px) !important;
    max-width: 520px !important;
    min-height: 0 !important;
    height: auto !important;

    margin-left: auto !important;
    margin-right: auto !important;
    padding: 14px 12px 14px !important;

    display: block !important;
    box-sizing: border-box !important;
    overflow: hidden !important;
    border-radius: 24px !important;

    transform: none !important;
    background: transparent !important;
  }

  /*
    The background is a real child element with an img.
    Keep it below everything and never use it as a product/carousel container.
  */
  .collection-box > .collection-bg {
    position: absolute !important;
    inset: 0 !important;
    z-index: 0 !important;

    width: 100% !important;
    height: 100% !important;
    min-width: 0 !important;
    min-height: 0 !important;

    display: block !important;
    overflow: hidden !important;
    pointer-events: none !important;
    border-radius: inherit !important;

    transform: none !important;
    background: transparent !important;
  }

  .collection-box > .collection-bg img {
    position: absolute !important;
    inset: 0 !important;

    width: 100% !important;
    height: 100% !important;
    max-width: none !important;
    max-height: none !important;

    display: block !important;
    object-fit: fill !important;
    object-position: center center !important;

    transform: none !important;
    opacity: 1 !important;
  }

  .collection-content {
    position: relative !important;
    z-index: 2 !important;

    width: 100% !important;
    max-width: 100% !important;
    min-width: 0 !important;
    min-height: 0 !important;

    display: flex !important;
    flex-direction: column !important;
    align-items: stretch !important;
    justify-content: flex-start !important;
    gap: 10px !important;

    box-sizing: border-box !important;
    overflow: visible !important;
    transform: none !important;
  }

  .collection-label {
    position: relative !important;
    z-index: 3 !important;

    left: auto !important;
    right: auto !important;
    top: auto !important;
    bottom: auto !important;
    transform: none !important;

    width: calc(100% - 16px) !important;
    max-width: 440px !important;
    min-width: 0 !important;

    margin: 0 auto 2px !important;
    padding: 8px 10px !important;
    box-sizing: border-box !important;

    display: block !important;
    overflow: visible !important;

    text-align: center !important;
    white-space: normal !important;
    line-height: 1.12 !important;

    border-radius: 14px !important;
  }

  /*
    Hide original homepage product layer only after JS marks it as the source.
    This avoids hiding the background/title if JS fails or selectors change.
  */
  .collection-content > .carousel-shell.dkg-mobile-original-product-source {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
    min-height: 0 !important;
    max-height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
    overflow: hidden !important;
    pointer-events: none !important;
  }

  .collection-content > .dkg-mobile-carousel-viewport {
    position: relative !important;
    z-index: 2 !important;

    width: 100% !important;
    max-width: 100% !important;
    min-width: 0 !important;

    margin: 0 auto !important;
    padding: 0 !important;
    box-sizing: border-box !important;

    display: block !important;
    overflow: hidden !important;

    background: transparent !important;
    border: 0 !important;
    transform: none !important;
    contain: paint !important;
  }

  .dkg-mobile-product-track {
    width: 100% !important;
    min-width: 0 !important;

    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    align-items: stretch !important;
    justify-content: flex-start !important;
    gap: var(--dkg-mobile-card-gap) !important;

    margin: 0 !important;
    padding: 0 !important;
    box-sizing: border-box !important;

    list-style: none !important;
    will-change: transform !important;
    transform: translate3d(0, 0, 0);
  }

  .dkg-mobile-carousel-viewport.dkg-mobile-static .dkg-mobile-product-track {
    justify-content: center !important;
    transform: translate3d(0, 0, 0) !important;
    transition: none !important;
  }

  .dkg-mobile-product-item {
    flex: 0 0 calc((100% - (var(--dkg-mobile-card-gap) * 2)) / 3) !important;
    width: calc((100% - (var(--dkg-mobile-card-gap) * 2)) / 3) !important;
    min-width: 0 !important;
    max-width: calc((100% - (var(--dkg-mobile-card-gap) * 2)) / 3) !important;

    height: clamp(96px, 28vw, 132px) !important;
    min-height: clamp(96px, 28vw, 132px) !important;
    max-height: clamp(96px, 28vw, 132px) !important;

    margin: 0 !important;
    padding: 0 !important;
    box-sizing: border-box !important;

    display: flex !important;
    align-items: center !important;
    justify-content: center !important;

    overflow: hidden !important;
    transform: none !important;
  }

  .dkg-mobile-product-item .product-card,
  .dkg-mobile-product-item .dkg-mobile-product-card-inner {
    width: 100% !important;
    height: 100% !important;
    min-width: 0 !important;
    min-height: 0 !important;

    margin: 0 !important;
    padding: 5px !important;
    box-sizing: border-box !important;

    display: flex !important;
    align-items: center !important;
    justify-content: center !important;

    overflow: hidden !important;
    border-radius: 14px !important;
    transform: none !important;
  }

  .dkg-mobile-product-item img,
  .dkg-mobile-product-item .product-image {
    width: 100% !important;
    height: 100% !important;
    max-width: 100% !important;
    max-height: 100% !important;

    display: block !important;
    object-fit: contain !important;
    object-position: center center !important;

    margin: 0 auto !important;
    padding: 0 !important;
    transform: none !important;
  }

  .dkg-mobile-product-item .product-card--empty {
    visibility: hidden !important;
  }

  @media screen and (max-width: 390px) {
    .collections-stack {
      gap: 13px !important;
    }

    .collection-box {
      --dkg-mobile-card-gap: 7px;
      width: calc(100vw - 14px) !important;
      padding: 12px 9px 12px !important;
      border-radius: 20px !important;
    }

    .collection-content {
      gap: 8px !important;
    }

    .collection-label {
      width: calc(100% - 10px) !important;
      padding: 7px 8px !important;
      font-size: clamp(0.72rem, 3.45vw, 0.92rem) !important;
    }

    .dkg-mobile-product-item {
      height: clamp(88px, 27vw, 118px) !important;
      min-height: clamp(88px, 27vw, 118px) !important;
      max-height: clamp(88px, 27vw, 118px) !important;
    }

    .dkg-mobile-product-item .product-card,
    .dkg-mobile-product-item .dkg-mobile-product-card-inner {
      padding: 4px !important;
      border-radius: 12px !important;
    }
  }
}

/* === DKG MOBILE MAIN HOMEPAGE COLLECTION PLATES END === */
'''


NEW_JS = r'''/*
  DKG mobile homepage collection plates.

  Cleanup version:
  - Uses the real front-page.php structure.
  - Reads products only from .collection-content .product-track > .product-card.
  - Inserts the mobile viewport inside .collection-content after .collection-label.
  - Never inserts into .collection-bg.
  - Never clones .collection-label.
  - Removes old mobile carousel wrappers before rebuilding.
  - Hides only the original .carousel-shell after a clone layer has been built.
*/

(function () {
  "use strict";

  var MOBILE_QUERY = "(max-width: 767px)";
  var VISIBLE_SLOTS = 3;
  var AUTOSCROLL_MS = 2600;
  var TRANSITION_MS = 420;
  var RESIZE_DEBOUNCE_MS = 180;

  var stateByBox = new WeakMap();
  var resizeTimer = null;

  function matchesMobile() {
    if (!window.matchMedia) {
      return window.innerWidth <= 767;
    }

    return window.matchMedia(MOBILE_QUERY).matches;
  }

  function toArray(list) {
    return Array.prototype.slice.call(list || []);
  }

  function directChildWithClass(parent, className) {
    if (!parent) {
      return null;
    }

    var children = parent.children || [];

    for (var i = 0; i < children.length; i += 1) {
      if (children[i].classList && children[i].classList.contains(className)) {
        return children[i];
      }
    }

    return null;
  }

  function queryDirect(parent, selector, fallbackSelector) {
    if (!parent) {
      return null;
    }

    try {
      var direct = parent.querySelector(":scope > " + selector);
      if (direct) {
        return direct;
      }
    } catch (error) {
      /* Some older browsers may not support :scope. */
    }

    return parent.querySelector(fallbackSelector || selector);
  }

  function clearTimer(box) {
    var oldState = stateByBox.get(box);

    if (oldState && oldState.timer) {
      window.clearInterval(oldState.timer);
    }

    stateByBox.delete(box);
  }

  function removeMobileLayer(box) {
    if (!box) {
      return;
    }

    clearTimer(box);

    toArray(box.querySelectorAll(".dkg-mobile-carousel-viewport")).forEach(function (node) {
      if (node && node.parentNode) {
        node.parentNode.removeChild(node);
      }
    });

    toArray(box.querySelectorAll(".dkg-mobile-original-product-source")).forEach(function (node) {
      node.classList.remove("dkg-mobile-original-product-source");
    });

    toArray(box.querySelectorAll(".dkg-mobile-original-track-source")).forEach(function (node) {
      node.classList.remove("dkg-mobile-original-track-source");
    });

    box.removeAttribute("data-dkg-mobile-plates-ready");
  }

  function getParts(box) {
    var bg = directChildWithClass(box, "collection-bg");
    var content = directChildWithClass(box, "collection-content") || box.querySelector(".collection-content");

    if (!content) {
      return null;
    }

    var label = directChildWithClass(content, "collection-label") || content.querySelector(".collection-label");

    /*
      Important:
      Original products are inside .collection-content, not inside .collection-bg.
      This intentionally avoids querying through .collection-bg.
    */
    var shell = queryDirect(content, ".carousel-shell", ".carousel-shell");
    var viewport = shell ? shell.querySelector(".product-viewport") : content.querySelector(".product-viewport");
    var track = viewport ? viewport.querySelector(".product-track") : null;

    if (!track) {
      track = content.querySelector(".product-track");
    }

    var cards = track
      ? toArray(track.children).filter(function (child) {
          return (
            child &&
            child.classList &&
            child.classList.contains("product-card") &&
            !child.classList.contains("product-card--empty") &&
            child.querySelector("img")
          );
        })
      : [];

    return {
      box: box,
      bg: bg,
      content: content,
      label: label,
      shell: shell,
      viewport: viewport,
      track: track,
      cards: cards
    };
  }

  function cloneCardIntoItem(card, index, isLoopClone) {
    var item = document.createElement("div");
    item.className = "dkg-mobile-product-item";
    item.setAttribute("data-dkg-mobile-product-index", String(index));

    if (isLoopClone) {
      item.classList.add("dkg-mobile-product-clone");
      item.setAttribute("aria-hidden", "true");
    }

    var clone = card.cloneNode(true);
    clone.classList.add("dkg-mobile-product-card-inner");

    /*
      Remove IDs from cloned markup so duplicate IDs cannot appear.
    */
    if (clone.id) {
      clone.removeAttribute("id");
    }

    toArray(clone.querySelectorAll("[id]")).forEach(function (node) {
      node.removeAttribute("id");
    });

    item.appendChild(clone);
    return item;
  }

  function insertAfterLabel(parts, viewport) {
    var content = parts.content;
    var label = parts.label;

    if (label && label.parentNode === content && label.nextSibling) {
      content.insertBefore(viewport, label.nextSibling);
      return;
    }

    if (label && label.parentNode === content) {
      content.appendChild(viewport);
      return;
    }

    content.insertBefore(viewport, content.firstChild);
  }

  function measureStep(track) {
    if (!track || !track.children || !track.children.length) {
      return 0;
    }

    var first = track.children[0];
    var rect = first.getBoundingClientRect();
    var styles = window.getComputedStyle(track);
    var gap = parseFloat(styles.columnGap || styles.gap || "0");

    if (!isFinite(gap)) {
      gap = 0;
    }

    return rect.width + gap;
  }

  function setTrackPosition(track, index, step, animate) {
    if (!track) {
      return;
    }

    if (animate) {
      track.style.transition = "transform " + TRANSITION_MS + "ms ease";
    } else {
      track.style.transition = "none";
    }

    track.style.transform = "translate3d(" + (-Math.round(index * step)) + "px, 0, 0)";
  }

  function buildStatic(parts, viewport, track) {
    viewport.classList.add("dkg-mobile-static");
    viewport.classList.add("dkg-mobile-count-" + parts.cards.length);
    track.style.transition = "none";
    track.style.transform = "translate3d(0, 0, 0)";
  }

  function buildAutoscroll(parts, viewport, track) {
    var index = 0;
    var totalReal = parts.cards.length;
    var step = 0;

    viewport.classList.add("dkg-mobile-autoscroll");
    viewport.setAttribute("data-dkg-mobile-real-count", String(totalReal));

    function recalc() {
      step = measureStep(track);
      setTrackPosition(track, index, step, false);
    }

    function advance() {
      if (!matchesMobile() || !document.body.contains(parts.box)) {
        return;
      }

      step = measureStep(track);

      if (!step) {
        return;
      }

      index += 1;
      setTrackPosition(track, index, step, true);

      /*
        When index reaches totalReal, the visible items are the appended clones
        of the first 3 products. Snap back to real index 0 after transition.
      */
      if (index >= totalReal) {
        window.setTimeout(function () {
          index = 0;
          step = measureStep(track);
          setTrackPosition(track, index, step, false);
        }, TRANSITION_MS + 40);
      }
    }

    window.requestAnimationFrame(function () {
      recalc();
      window.setTimeout(recalc, 80);
    });

    var timer = window.setInterval(advance, AUTOSCROLL_MS);

    stateByBox.set(parts.box, {
      timer: timer,
      recalc: recalc
    });
  }

  function setupBox(box) {
    if (!box) {
      return;
    }

    removeMobileLayer(box);

    var parts = getParts(box);

    if (!parts || !parts.content || !parts.track || !parts.cards.length) {
      return;
    }

    /*
      Do not ever use .collection-bg as the mobile insertion point.
    */
    if (parts.bg && parts.bg.contains(parts.track)) {
      return;
    }

    var viewport = document.createElement("div");
    viewport.className = "dkg-mobile-carousel-viewport";
    viewport.setAttribute("aria-hidden", "true");

    var mobileTrack = document.createElement("div");
    mobileTrack.className = "dkg-mobile-product-track";

    parts.cards.forEach(function (card, index) {
      mobileTrack.appendChild(cloneCardIntoItem(card, index, false));
    });

    if (parts.cards.length > VISIBLE_SLOTS) {
      for (var i = 0; i < VISIBLE_SLOTS; i += 1) {
        mobileTrack.appendChild(cloneCardIntoItem(parts.cards[i], i, true));
      }
    }

    viewport.appendChild(mobileTrack);
    insertAfterLabel(parts, viewport);

    /*
      Hide only the original product shell/track, not the whole content area,
      not the label, and never the background.
    */
    if (parts.shell) {
      parts.shell.classList.add("dkg-mobile-original-product-source");
    }

    if (parts.track) {
      parts.track.classList.add("dkg-mobile-original-track-source");
    }

    box.setAttribute("data-dkg-mobile-plates-ready", "true");

    if (parts.cards.length <= VISIBLE_SLOTS) {
      buildStatic(parts, viewport, mobileTrack);
    } else {
      buildAutoscroll(parts, viewport, mobileTrack);
    }
  }

  function setupAll() {
    var boxes = toArray(document.querySelectorAll(".collections-stack .collection-box"));

    if (!matchesMobile()) {
      boxes.forEach(removeMobileLayer);
      return;
    }

    boxes.forEach(setupBox);
  }

  function scheduleSetup() {
    if (resizeTimer) {
      window.clearTimeout(resizeTimer);
    }

    resizeTimer = window.setTimeout(setupAll, RESIZE_DEBOUNCE_MS);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", setupAll);
  } else {
    setupAll();
  }

  window.addEventListener("resize", scheduleSetup);
  window.addEventListener("orientationchange", scheduleSetup);

  if (window.matchMedia) {
    try {
      var mq = window.matchMedia(MOBILE_QUERY);

      if (mq.addEventListener) {
        mq.addEventListener("change", scheduleSetup);
      } else if (mq.addListener) {
        mq.addListener(scheduleSetup);
      }
    } catch (error) {
      /* Non-critical. Resize listener still handles changes. */
    }
  }
})();
'''


NEW_ENQUEUE_BLOCK = r'''// === DKG MOBILE MAIN HOMEPAGE COLLECTION PLATES ENQUEUE START ===

function dkg_enqueue_mobile_main_homepage_collection_plates() {
    if (is_admin()) {
        return;
    }

    /*
     * This script is only for the normal homepage collection plates.
     * Mobile users should stay on the normal homepage, not /mobile-shop/.
     */
    if (!is_front_page()) {
        return;
    }

    $script_path = get_template_directory() . '/assets/js/dkg-mobile-main-homepage-plates.js';
    $script_uri  = get_template_directory_uri() . '/assets/js/dkg-mobile-main-homepage-plates.js';

    if (file_exists($script_path)) {
        wp_enqueue_script(
            'dkg-mobile-main-homepage-plates',
            $script_uri,
            array(),
            filemtime($script_path),
            true
        );
    }
}
add_action('wp_enqueue_scripts', 'dkg_enqueue_mobile_main_homepage_collection_plates', 30);

// === DKG MOBILE MAIN HOMEPAGE COLLECTION PLATES ENQUEUE END ===
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


def replace_marker_block(text: str, start_marker: str, end_marker: str, new_block: str) -> tuple[str, int]:
    """
    Replaces from the first start marker through the last end marker.
    This intentionally collapses duplicate leftover blocks into one clean block.
    """
    start_positions = [m.start() for m in re.finditer(re.escape(start_marker), text)]
    end_positions = [m.end() for m in re.finditer(re.escape(end_marker), text)]

    if not start_positions or not end_positions:
        cleaned = text.rstrip() + "\n\n" + new_block.rstrip() + "\n"
        return cleaned, 0

    first_start = min(start_positions)
    last_end = max(end_positions)

    if first_start > last_end:
        cleaned = text.rstrip() + "\n\n" + new_block.rstrip() + "\n"
        return cleaned, 0

    replaced = text[:first_start].rstrip() + "\n\n" + new_block.rstrip() + "\n\n" + text[last_end:].lstrip()
    return replaced, len(start_positions)


def update_css(root: Path) -> str:
    css_path = root / "assets" / "css" / "front-page.css"

    if not css_path.exists():
        raise FileNotFoundError(f"Missing CSS file: {css_path}")

    old = read_text(css_path)
    new, replaced_count = replace_marker_block(old, CSS_START, CSS_END, NEW_CSS_BLOCK)

    if new != old:
        write_text(css_path, new)

    if replaced_count:
        return f"Updated CSS: replaced/collapsed {replaced_count} mobile block start marker(s)."
    return "Updated CSS: no old marker block found, appended new mobile block."


def update_js(root: Path) -> str:
    js_dir = root / "assets" / "js"
    js_dir.mkdir(parents=True, exist_ok=True)

    js_path = js_dir / "dkg-mobile-main-homepage-plates.js"
    old = read_text(js_path) if js_path.exists() else ""

    if old != NEW_JS:
        write_text(js_path, NEW_JS)

    return "Updated JS: replaced assets/js/dkg-mobile-main-homepage-plates.js with cleanup carousel script."


def disable_mobile_redirect_hook(functions_text: str) -> tuple[str, int]:
    """
    Comments active add_action('template_redirect', 'dkg_redirect_mobile_shop_visitors', ...)
    lines if they exist.

    Already-commented lines are ignored.
    """
    changed = 0
    output_lines = []

    redirect_line_re = re.compile(
        r"add_action\s*\(\s*['\"]template_redirect['\"]\s*,\s*['\"]dkg_redirect_mobile_shop_visitors['\"]",
        re.IGNORECASE,
    )

    for line in functions_text.splitlines():
        stripped = line.lstrip()

        if redirect_line_re.search(line) and not stripped.startswith("//") and not stripped.startswith("#") and not stripped.startswith("/*"):
            indent = line[: len(line) - len(stripped)]
            output_lines.append(
                indent + "// DKG disabled by mobile_main_homepage_cleanup_updater.py: " + stripped
            )
            changed += 1
        else:
            output_lines.append(line)

    return "\n".join(output_lines) + ("\n" if functions_text.endswith("\n") else ""), changed


def update_enqueue_block(functions_text: str) -> tuple[str, str]:
    if ENQUEUE_START in functions_text and ENQUEUE_END in functions_text:
        new_text, count = replace_marker_block(functions_text, ENQUEUE_START, ENQUEUE_END, NEW_ENQUEUE_BLOCK)
        return new_text, f"Updated functions.php enqueue block: replaced/collapsed {count} enqueue marker block(s)."

    if "dkg-mobile-main-homepage-plates" in functions_text:
        # Existing enqueue exists but marker shape was unexpected. Do not risk duplicating it.
        return functions_text, (
            "functions.php enqueue: found dkg-mobile-main-homepage-plates but did not find expected markers; "
            "left existing enqueue in place to avoid duplication."
        )

    appended = functions_text.rstrip() + "\n\n" + NEW_ENQUEUE_BLOCK.rstrip() + "\n"
    return appended, "functions.php enqueue: no existing mobile enqueue found, appended clean front-page-only enqueue block."


def update_functions(root: Path) -> str:
    functions_path = root / "functions.php"

    if not functions_path.exists():
        raise FileNotFoundError(f"Missing functions.php: {functions_path}")

    old = read_text(functions_path)

    text, redirect_disabled_count = disable_mobile_redirect_hook(old)
    text, enqueue_message = update_enqueue_block(text)

    if text != old:
        write_text(functions_path, text)

    redirect_message = (
        f"Disabled {redirect_disabled_count} active mobile redirect hook(s)."
        if redirect_disabled_count
        else "Mobile redirect hook: no active add_action line found; likely already disabled."
    )

    return redirect_message + " " + enqueue_message


def sanity_check_repo(root: Path) -> None:
    expected = [
        root / "functions.php",
        root / "assets" / "css" / "front-page.css",
    ]

    missing = [str(path) for path in expected if not path.exists()]

    if missing:
        raise SystemExit(
            "This does not look like the theme repo root, or required files are missing:\n"
            + "\n".join("  - " + item for item in missing)
            + "\n\nRun this from:\n"
            + r'  C:\Users\John\Desktop\shop dkg\dkg-shop-theme'
        )


def main() -> int:
    root = Path.cwd().resolve()
    sanity_check_repo(root)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_dir = root / f"_dkg_mobile_homepage_cleanup_backup_{timestamp}"
    backup_dir.mkdir(parents=True, exist_ok=False)

    files_to_backup = [
        "functions.php",
        "assets/css/front-page.css",
        "assets/js/dkg-mobile-main-homepage-plates.js",
    ]

    for rel_path in files_to_backup:
        make_backup(root, backup_dir, rel_path)

    messages = []
    messages.append(update_css(root))
    messages.append(update_js(root))
    messages.append(update_functions(root))

    summary_path = backup_dir / "cleanup_update_summary.txt"
    summary = [
        "DKG mobile homepage cleanup updater summary",
        f"Timestamp: {timestamp}",
        f"Repo root: {root}",
        f"Backup folder: {backup_dir}",
        "",
        "Actions:",
    ]
    summary.extend(f"- {message}" for message in messages)
    summary.extend(
        [
            "",
            "Expected result:",
            "- Mobile users remain on the normal homepage.",
            "- .collection-bg remains decorative only.",
            "- .collection-label stays centered and outside the moving product track.",
            "- Mobile carousel layer is inserted inside .collection-content after .collection-label.",
            "- Original .carousel-shell is hidden only after JS successfully builds the mobile clone layer.",
            "- Collections with 1 or 2 products are centered.",
            "- Collections with 3 products are static.",
            "- Collections with more than 3 products auto-scroll one product at a time.",
            "",
            "Files backed up:",
        ]
    )
    summary.extend(f"- {rel_path}" for rel_path in files_to_backup)
    write_text(summary_path, "\n".join(summary) + "\n")

    print("\nDone.")
    print(f"Backup folder: {backup_dir}")
    print("")
    for message in messages:
        print(f"- {message}")

    print("")
    print("Next:")
    print("1. Upload/deploy the changed theme files.")
    print("2. Clear any site/plugin/browser cache.")
    print("3. Test the normal homepage on phone width, not /mobile-shop/.")
    print("4. If anything is off, send a screenshot plus the new CSS/JS snippets or rerun the inspector.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
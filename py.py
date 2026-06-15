#!/usr/bin/env python3
"""
DKG mobile frame fit + header rotator fade/shuffle fix.

Goals:
- On mobile, make the framed image inner photo a little shorter and wider.
- Replace the header-picture-rotator.js logic with a safer two-layer crossfade.
- Keep group 1 and group 2 both visible in the loop.
- Avoid group 1 flicker by preloading the next image before fading.
- Avoid blank flashes by keeping one image layer active at all times.
- Do not edit header.php.

Edits:
- assets/css/front-page.css
- assets/js/header-picture-rotator.js

Backups are created first.

Run from theme repo root:
    python mobile_frame_fit_and_rotator_fade_fix.py
"""

from __future__ import annotations

import re
import shutil
from datetime import datetime
from pathlib import Path


CSS_START = "/* === DKG MOBILE HEADER FRAME IMAGE FIT FADE START === */"
CSS_END = "/* === DKG MOBILE HEADER FRAME IMAGE FIT FADE END === */"

JS_PATH_REL = "assets/js/header-picture-rotator.js"


NEW_CSS_BLOCK = r'''/* === DKG MOBILE HEADER FRAME IMAGE FIT FADE START === */

/*
  Mobile framed image tune.

  Current header.php default image opening:
    left: 8%;
    top: 9%;
    width: 84%;
    height: 82%;

  Mobile issue:
    inner image is a little too tall and not wide enough.

  This mobile-only tune makes the inner image:
    - wider
    - shorter
    - slightly lower
    - smoothly crossfade when the rotator script swaps layers
*/

@media screen and (max-width: 767px) {

  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .dkg-mobile-relocated-header-rotator-zone .dkg-header-picture-frame,
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .dkg-header-picture-rotator.dkg-mobile-header-rotator-relocated .dkg-header-picture-frame {
    overflow: hidden !important;
  }

  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .dkg-mobile-relocated-header-rotator-zone .dkg-header-picture-img,
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .dkg-mobile-relocated-header-rotator-zone .dkg-header-picture-img-layer,
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .dkg-header-picture-rotator.dkg-mobile-header-rotator-relocated .dkg-header-picture-img,
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .dkg-header-picture-rotator.dkg-mobile-header-rotator-relocated .dkg-header-picture-img-layer {
    /*
      Wider + shorter than the original 8/9/84/82.
      Tweak these four values later if needed.
    */
    left: 5.25% !important;
    top: 12.25% !important;
    width: 89.5% !important;
    height: 73.5% !important;

    object-fit: cover !important;
    object-position: center center !important;

    display: block !important;
    position: absolute !important;

    opacity: 0 !important;
    transition: opacity 720ms ease-in-out !important;
    will-change: opacity !important;

    transform: none !important;
    backface-visibility: hidden !important;
    -webkit-backface-visibility: hidden !important;
  }

  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .dkg-mobile-relocated-header-rotator-zone .dkg-header-picture-img-layer.is-active,
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .dkg-header-picture-rotator.dkg-mobile-header-rotator-relocated .dkg-header-picture-img-layer.is-active {
    opacity: 1 !important;
  }

  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .dkg-mobile-relocated-header-rotator-zone .dkg-header-picture-img-layer:not(.is-active),
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .dkg-header-picture-rotator.dkg-mobile-header-rotator-relocated .dkg-header-picture-img-layer:not(.is-active) {
    opacity: 0 !important;
  }

  @media screen and (max-width: 390px) {
    body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .dkg-mobile-relocated-header-rotator-zone .dkg-header-picture-img,
    body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .dkg-mobile-relocated-header-rotator-zone .dkg-header-picture-img-layer,
    body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .dkg-header-picture-rotator.dkg-mobile-header-rotator-relocated .dkg-header-picture-img,
    body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .dkg-header-picture-rotator.dkg-mobile-header-rotator-relocated .dkg-header-picture-img-layer {
      left: 5% !important;
      top: 12.75% !important;
      width: 90% !important;
      height: 72.5% !important;
    }
  }
}

/*
  Generic layer states for desktop too.
  Dimensions are not changed here; this only ensures the fade classes work.
*/
.dkg-header-picture-frame .dkg-header-picture-img-layer {
  opacity: 0;
  transition: opacity 720ms ease-in-out;
  will-change: opacity;
}

.dkg-header-picture-frame .dkg-header-picture-img-layer.is-active {
  opacity: 1;
}

/* === DKG MOBILE HEADER FRAME IMAGE FIT FADE END === */
'''


NEW_JS = r'''/*
  DKG header picture rotator - repaired crossfade/shuffle version.

  Fixes:
  - Uses the existing data-image-group-1, data-image-group-2, and data-images attrs.
  - Keeps group 1 and group 2 both in the loop.
  - Preloads each next image before swapping, preventing one-frame flickers.
  - Uses two persistent image layers and opacity crossfade.
  - Does not clone multiple layers on repeated init.
*/

(function () {
  "use strict";

  var ROTATOR_SELECTOR = ".dkg-header-picture-rotator";
  var FRAME_SELECTOR = ".dkg-header-picture-frame";
  var IMG_SELECTOR = ".dkg-header-picture-img";
  var LAYER_CLASS = "dkg-header-picture-img-layer";
  var ACTIVE_CLASS = "is-active";
  var READY_ATTR = "data-dkg-rotator-ready-v2";
  var DEFAULT_INTERVAL = 3000;
  var MIN_INTERVAL = 1200;
  var FADE_MS = 720;

  function parseImages(raw) {
    if (!raw) {
      return [];
    }

    var text = String(raw)
      .replace(/&quot;/g, '"')
      .replace(/&#034;/g, '"')
      .replace(/&#34;/g, '"')
      .trim();

    try {
      var parsed = JSON.parse(text);

      if (Array.isArray(parsed)) {
        return parsed.filter(Boolean).map(String);
      }

      if (typeof parsed === "string") {
        return [parsed];
      }
    } catch (error) {
      /*
        Fallback below.
      */
    }

    return text
      .split(/[,\n]/)
      .map(function (item) {
        return item.trim().replace(/^['"]|['"]$/g, "");
      })
      .filter(Boolean);
  }

  function uniqueImages(images) {
    var seen = {};
    var out = [];

    images.forEach(function (src) {
      src = String(src || "").trim();

      if (!src || seen[src]) {
        return;
      }

      seen[src] = true;
      out.push(src);
    });

    return out;
  }

  function preload(src) {
    return new Promise(function (resolve) {
      if (!src) {
        resolve(false);
        return;
      }

      var img = new Image();

      img.onload = function () {
        resolve(true);
      };

      img.onerror = function () {
        resolve(false);
      };

      img.src = src;
    });
  }

  function preloadMany(images) {
    images.forEach(function (src) {
      var img = new Image();
      img.src = src;
    });
  }

  function containsImage(list, src) {
    return list.indexOf(src) !== -1;
  }

  function pickRandom(list, avoid) {
    if (!list || !list.length) {
      return "";
    }

    if (list.length === 1) {
      return list[0];
    }

    var choices = list.filter(function (src) {
      return src !== avoid;
    });

    if (!choices.length) {
      choices = list.slice();
    }

    return choices[Math.floor(Math.random() * choices.length)];
  }

  function makeFallbackDeck(images, currentSrc) {
    var deck = images.filter(function (src) {
      return src && src !== currentSrc;
    });

    if (!deck.length) {
      deck = images.slice();
    }

    for (var i = deck.length - 1; i > 0; i -= 1) {
      var j = Math.floor(Math.random() * (i + 1));
      var temp = deck[i];
      deck[i] = deck[j];
      deck[j] = temp;
    }

    return deck;
  }

  function buildGroupState(rotator, currentSrc) {
    var group1 = uniqueImages(parseImages(rotator.getAttribute("data-image-group-1")));
    var group2 = uniqueImages(parseImages(rotator.getAttribute("data-image-group-2")));
    var oldImages = uniqueImages(parseImages(rotator.getAttribute("data-images")));
    var combined = uniqueImages(group1.concat(group2).concat(oldImages));

    var hasGroups = group1.length > 0 || group2.length > 0;

    var activeGroupIndex = 0;

    /*
      If current image is from group 1, next should come from group 2.
      If current image is from group 2, next should come from group 1.
      This prevents the group 2 only behavior.
    */
    if (group1.length && group2.length) {
      activeGroupIndex = containsImage(group1, currentSrc) ? 1 : 0;
    }

    return {
      group1: group1,
      group2: group2,
      combined: combined,
      hasGroups: hasGroups,
      nextGroupIndex: activeGroupIndex,
      lastByGroup: {
        group1: containsImage(group1, currentSrc) ? currentSrc : "",
        group2: containsImage(group2, currentSrc) ? currentSrc : ""
      },
      fallbackDeck: makeFallbackDeck(combined, currentSrc)
    };
  }

  function chooseNextFromState(state, currentSrc) {
    if (!state.combined.length) {
      return "";
    }

    if (state.group1.length && state.group2.length) {
      var useGroup1 = state.nextGroupIndex === 0;
      var groupName = useGroup1 ? "group1" : "group2";
      var group = useGroup1 ? state.group1 : state.group2;

      state.nextGroupIndex = useGroup1 ? 1 : 0;

      var next = pickRandom(group, state.lastByGroup[groupName] || currentSrc);
      state.lastByGroup[groupName] = next;
      return next;
    }

    if (state.group1.length || state.group2.length) {
      var onlyGroupName = state.group1.length ? "group1" : "group2";
      var onlyGroup = state.group1.length ? state.group1 : state.group2;
      var onlyNext = pickRandom(onlyGroup, state.lastByGroup[onlyGroupName] || currentSrc);
      state.lastByGroup[onlyGroupName] = onlyNext;
      return onlyNext;
    }

    if (!state.fallbackDeck.length) {
      state.fallbackDeck = makeFallbackDeck(state.combined, currentSrc);
    }

    return state.fallbackDeck.shift() || "";
  }

  function applyLayerBaseStyles(img) {
    img.classList.add(LAYER_CLASS);
    img.style.position = "absolute";
    img.style.opacity = img.classList.contains(ACTIVE_CLASS) ? "1" : "0";
    img.style.transition = "opacity " + FADE_MS + "ms ease-in-out";
    img.style.willChange = "opacity";
    img.style.backfaceVisibility = "hidden";
    img.style.webkitBackfaceVisibility = "hidden";
  }

  function cleanupExtraLayers(frame, keepA, keepB) {
    Array.prototype.slice.call(frame.querySelectorAll("." + LAYER_CLASS)).forEach(function (node) {
      if (node !== keepA && node !== keepB && node.parentNode) {
        node.parentNode.removeChild(node);
      }
    });
  }

  function startRotator(rotator) {
    if (!rotator || rotator.getAttribute(READY_ATTR) === "1") {
      return;
    }

    var frame = rotator.querySelector(FRAME_SELECTOR) || rotator;
    var firstImg = rotator.querySelector(IMG_SELECTOR);

    if (!firstImg) {
      return;
    }

    rotator.setAttribute(READY_ATTR, "1");

    var currentSrc = firstImg.getAttribute("src") || "";
    var state = buildGroupState(rotator, currentSrc);

    if (state.combined.length < 2) {
      return;
    }

    var interval = parseInt(rotator.getAttribute("data-interval") || String(DEFAULT_INTERVAL), 10);

    if (!interval || interval < MIN_INTERVAL) {
      interval = DEFAULT_INTERVAL;
    }

    preloadMany(state.combined);

    firstImg.classList.add(LAYER_CLASS, ACTIVE_CLASS);
    firstImg.setAttribute("data-dkg-rotator-layer", "active");
    firstImg.style.zIndex = "2";
    applyLayerBaseStyles(firstImg);

    var secondImg = firstImg.cloneNode(true);
    secondImg.classList.remove(ACTIVE_CLASS);
    secondImg.setAttribute("aria-hidden", "true");
    secondImg.setAttribute("data-dkg-rotator-layer", "standby");
    secondImg.style.zIndex = "1";
    secondImg.style.opacity = "0";
    applyLayerBaseStyles(secondImg);

    frame.appendChild(secondImg);
    cleanupExtraLayers(frame, firstImg, secondImg);

    var activeLayer = firstImg;
    var hiddenLayer = secondImg;
    var isAnimating = false;
    var current = currentSrc;

    function finishSwap(nextSrc) {
      var oldActive = activeLayer;

      activeLayer = hiddenLayer;
      hiddenLayer = oldActive;
      current = nextSrc;

      activeLayer.style.zIndex = "2";
      hiddenLayer.style.zIndex = "1";

      activeLayer.setAttribute("data-dkg-rotator-layer", "active");
      hiddenLayer.setAttribute("data-dkg-rotator-layer", "standby");

      isAnimating = false;
    }

    function swapToNext() {
      if (isAnimating) {
        return;
      }

      var nextSrc = chooseNextFromState(state, current);

      if (!nextSrc || nextSrc === current) {
        return;
      }

      isAnimating = true;

      preload(nextSrc).then(function (loaded) {
        if (!loaded) {
          isAnimating = false;
          return;
        }

        hiddenLayer.src = nextSrc;
        hiddenLayer.classList.remove(ACTIVE_CLASS);
        hiddenLayer.style.opacity = "0";
        hiddenLayer.style.zIndex = "3";

        /*
          Force browser to apply opacity 0 before fade-in.
        */
        hiddenLayer.offsetHeight;

        hiddenLayer.classList.add(ACTIVE_CLASS);
        hiddenLayer.style.opacity = "1";

        activeLayer.classList.remove(ACTIVE_CLASS);
        activeLayer.style.opacity = "0";

        window.setTimeout(function () {
          finishSwap(nextSrc);
        }, FADE_MS + 80);
      });
    }

    /*
      Use a timeout loop instead of setInterval so an image that takes longer
      to load cannot cause overlapping/flickering swaps.
    */
    function scheduleNext() {
      window.setTimeout(function () {
        swapToNext();
        scheduleNext();
      }, interval);
    }

    scheduleNext();
  }

  function init() {
    Array.prototype.slice.call(document.querySelectorAll(ROTATOR_SELECTOR)).forEach(startRotator);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  /*
    Relocation scripts may move the existing node after this script has run.
    That is fine because the same node keeps its layers/timer.
    This extra init only covers late-rendered/cached rotators.
  */
  window.addEventListener("load", function () {
    window.setTimeout(init, 120);
  });
})();
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


def update_css(root: Path) -> str:
    css_path = root / "assets" / "css" / "front-page.css"

    if not css_path.exists():
        raise FileNotFoundError(f"Missing CSS file: {css_path}")

    old_css = read_text(css_path)
    cleaned_css, removed = remove_marker_block(old_css, CSS_START, CSS_END)
    new_css = cleaned_css.rstrip() + "\n\n" + NEW_CSS_BLOCK.rstrip() + "\n"

    if new_css != old_css:
        write_text(css_path, new_css)

    return f"CSS updated: removed old frame fit/fade tune blocks={removed}, appended clean mobile frame image tune."


def update_js(root: Path) -> str:
    js_path = root / JS_PATH_REL

    if not js_path.exists():
        raise FileNotFoundError(f"Missing JS file: {js_path}")

    old_js = read_text(js_path)

    if old_js != NEW_JS:
      write_text(js_path, NEW_JS)

    return "JS updated: replaced assets/js/header-picture-rotator.js with repaired crossfade/shuffle logic."


def main() -> int:
    root = Path.cwd().resolve()

    required = [
        root / "assets" / "css" / "front-page.css",
        root / JS_PATH_REL,
        root / "header.php",
    ]

    missing = [str(path) for path in required if not path.exists()]

    if missing:
        raise SystemExit(
            "Missing required files. Run from the theme repo root:\n"
            r'  C:\Users\John\Desktop\shop dkg\dkg-shop-theme'
            + "\n\nMissing:\n"
            + "\n".join("  - " + item for item in missing)
        )

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_dir = root / f"_dkg_mobile_frame_fit_rotator_fade_backup_{timestamp}"
    backup_dir.mkdir(parents=True, exist_ok=False)

    backup_css = backup_dir / "assets" / "css" / "front-page.css"
    backup_js = backup_dir / JS_PATH_REL

    backup_css.parent.mkdir(parents=True, exist_ok=True)
    backup_js.parent.mkdir(parents=True, exist_ok=True)

    shutil.copy2(root / "assets" / "css" / "front-page.css", backup_css)
    shutil.copy2(root / JS_PATH_REL, backup_js)

    messages = [
        update_css(root),
        update_js(root),
    ]

    summary_path = backup_dir / "mobile_frame_fit_rotator_fade_summary.txt"
    summary = [
        "DKG mobile frame fit + rotator fade/shuffle fix",
        f"Timestamp: {timestamp}",
        f"Repo root: {root}",
        "",
        "Backups:",
        f"- {backup_css}",
        f"- {backup_js}",
        "",
        "Actions:",
    ]
    summary.extend(f"- {msg}" for msg in messages)
    summary.extend(
        [
            "",
            "Expected behavior:",
            "- Mobile relocated framed image inner photo becomes wider and shorter.",
            "- Header rotator fades smoothly instead of flickering.",
            "- Group 1 and group 2 both appear in the loop.",
            "- Next image preloads before fade begins.",
            "- No header.php changes.",
            "",
            "Tuning knobs in CSS:",
            "- left/top/width/height inside the DKG MOBILE HEADER FRAME IMAGE FIT FADE block.",
            "- Current mobile values: left 5.25%, top 12.25%, width 89.5%, height 73.5%.",
        ]
    )

    write_text(summary_path, "\n".join(summary) + "\n")

    print("Done.")
    print(f"Backup folder: {backup_dir}")
    print("")
    for msg in messages:
        print(f"- {msg}")

    print("")
    print("Next:")
    print("1. Upload/deploy assets/css/front-page.css and assets/js/header-picture-rotator.js.")
    print("2. Clear cache.")
    print("3. Test mobile homepage.")
    print("4. Confirm the inner image is wider/shorter and the rotator fades smoothly.")
    print("")
    print("If inner image is still too tall:")
    print("- lower height from 73.5% to 70–72%")
    print("- raise top from 12.25% to 13–14%")
    print("")
    print("If inner image is still not wide enough:")
    print("- increase width from 89.5% to 91–92%")
    print("- lower left from 5.25% to 4–4.5%")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
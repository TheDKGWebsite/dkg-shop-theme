#!/usr/bin/env python3
"""
DKG Fix 10 - Mobile Homepage Product Image Runtime Fill Lock
------------------------------------------------------------

Purpose:
    Mobile homepage only.

    If CSS appears correct briefly but is later overridden/replaced after the
    mobile carousel finishes loading, this adds a tiny runtime JS lock that
    re-applies "image fills the product border/frame" to the generated carousel
    layer after load, timers, resize/orientation, and DOM mutations.

What it changes:
    1. Creates/updates:
        assets/js/dkg-mobile-homepage-product-image-fill-lock.js

    2. Updates functions.php:
        Adds a wp_enqueue_scripts block that loads that JS on the front page only.

Safety:
    - Makes timestamped backups before writing changed files.
    - Idempotent: safe to run repeatedly.
    - Mobile homepage only at runtime.
    - Does not touch product data, WooCommerce settings, PHP templates,
      existing carousel JS, or desktop layout.
    - The JS does not change card width/height; it only forces inner wrappers
      and images to fill the already-existing card border/frame.

Run from theme root:
    python dkg_fix_10_mobile_image_runtime_fill_lock.py

Or:
    python dkg_fix_10_mobile_image_runtime_fill_lock.py --root "C:\\Users\\John\\Desktop\\shop dkg\\dkg-shop-theme"

Dry run:
    python dkg_fix_10_mobile_image_runtime_fill_lock.py --dry-run
"""

from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path


PHP_START = "// === DKG MOBILE HOMEPAGE PRODUCT IMAGE FILL LOCK ENQUEUE START ==="
PHP_END = "// === DKG MOBILE HOMEPAGE PRODUCT IMAGE FILL LOCK ENQUEUE END ==="

JS_FILENAME = "dkg-mobile-homepage-product-image-fill-lock.js"

JS_CODE = '/*\nDKG Mobile Homepage Product Image Fill Lock\n-------------------------------------------\n\nMobile homepage only.\n\nForces product image wrappers/images in the generated mobile carousel layer\nto fill the current product-card border/frame. Re-applies after late carousel\nbuilds, load, resize/orientation, and DOM mutations.\n*/\n\n(function () {\n  "use strict";\n\n  var RUN_MS = 6500;\n  var OBSERVER_STOP_MS = 9000;\n  var APPLY_DEBOUNCE_MS = 40;\n\n  var applyTimer = null;\n  var startedAt = Date.now();\n\n  function isMobile() {\n    if (window.matchMedia) {\n      return window.matchMedia("(max-width: 767px)").matches;\n    }\n    return window.innerWidth <= 767;\n  }\n\n  function isTargetPage() {\n    var b = document.body;\n    if (!b) return false;\n\n    var isHome =\n      b.classList.contains("home") ||\n      b.classList.contains("front-page") ||\n      b.classList.contains("page-template-front-page");\n\n    var isMobileShop =\n      b.classList.contains("page-mobile-shop") ||\n      b.classList.contains("page-template-page-mobile-shop");\n\n    return isHome && !isMobileShop;\n  }\n\n  function setImportant(el, prop, value) {\n    if (!el || !el.style) return;\n    el.style.setProperty(prop, value, "important");\n  }\n\n  function forceFrame(el) {\n    if (!el) return;\n\n    setImportant(el, "position", "relative");\n    setImportant(el, "overflow", "hidden");\n    setImportant(el, "box-sizing", "border-box");\n  }\n\n  function forceFullWrapper(el) {\n    if (!el) return;\n\n    setImportant(el, "display", "block");\n    setImportant(el, "position", "absolute");\n    setImportant(el, "inset", "0");\n    setImportant(el, "width", "100%");\n    setImportant(el, "height", "100%");\n    setImportant(el, "min-width", "100%");\n    setImportant(el, "min-height", "100%");\n    setImportant(el, "max-width", "none");\n    setImportant(el, "max-height", "none");\n    setImportant(el, "margin", "0");\n    setImportant(el, "padding", "0");\n    setImportant(el, "overflow", "hidden");\n    setImportant(el, "box-sizing", "border-box");\n  }\n\n  function forceImage(el) {\n    if (!el) return;\n\n    setImportant(el, "display", "block");\n    setImportant(el, "position", "absolute");\n    setImportant(el, "inset", "0");\n    setImportant(el, "width", "100%");\n    setImportant(el, "height", "100%");\n    setImportant(el, "min-width", "100%");\n    setImportant(el, "min-height", "100%");\n    setImportant(el, "max-width", "none");\n    setImportant(el, "max-height", "none");\n    setImportant(el, "object-fit", "fill");\n    setImportant(el, "object-position", "center center");\n    setImportant(el, "margin", "0");\n    setImportant(el, "padding", "0");\n    setImportant(el, "border", "0");\n    setImportant(el, "transform", "none");\n    setImportant(el, "box-sizing", "border-box");\n  }\n\n  function applyFillLock() {\n    if (!isMobile() || !isTargetPage()) return;\n\n    var boxes = document.querySelectorAll(".collection-box");\n\n    boxes.forEach(function (box) {\n      var frames = box.querySelectorAll([\n        ".product-card",\n        ".dkg-mobile-product-card",\n        ".dkg-mobile-product-card-inner"\n      ].join(","));\n\n      frames.forEach(function (frame) {\n        forceFrame(frame);\n\n        var wrappers = frame.querySelectorAll([\n          ":scope > a",\n          "a.woocommerce-LoopProduct-link",\n          "a.woocommerce-loop-product__link",\n          ".woocommerce-LoopProduct-link",\n          ".woocommerce-loop-product__link",\n          "picture",\n          "figure"\n        ].join(","));\n\n        wrappers.forEach(forceFullWrapper);\n\n        var images = frame.querySelectorAll([\n          "img",\n          ".product-image",\n          ".attachment-woocommerce_thumbnail",\n          ".wp-post-image"\n        ].join(","));\n\n        images.forEach(forceImage);\n      });\n    });\n  }\n\n  function scheduleApply() {\n    if (applyTimer) {\n      window.clearTimeout(applyTimer);\n    }\n\n    applyTimer = window.setTimeout(function () {\n      applyTimer = null;\n      applyFillLock();\n    }, APPLY_DEBOUNCE_MS);\n  }\n\n  function burst() {\n    [0, 50, 120, 250, 500, 900, 1400, 2200, 3400, 5000, 6500].forEach(function (ms) {\n      window.setTimeout(applyFillLock, ms);\n    });\n  }\n\n  function start() {\n    if (!isTargetPage()) return;\n\n    applyFillLock();\n    burst();\n\n    window.addEventListener("load", burst, { passive: true });\n    window.addEventListener("resize", scheduleApply, { passive: true });\n    window.addEventListener("orientationchange", burst, { passive: true });\n\n    if (window.MutationObserver) {\n      var observer = new MutationObserver(function () {\n        if (Date.now() - startedAt <= RUN_MS) {\n          scheduleApply();\n        }\n      });\n\n      observer.observe(document.documentElement, {\n        subtree: true,\n        childList: true,\n        attributes: true,\n        attributeFilter: ["class", "style", "src", "srcset"]\n      });\n\n      window.setTimeout(function () {\n        observer.disconnect();\n      }, OBSERVER_STOP_MS);\n    }\n  }\n\n  if (document.readyState === "loading") {\n    document.addEventListener("DOMContentLoaded", start);\n  } else {\n    start();\n  }\n})();\n'

PHP_BLOCK_TEMPLATE = """__PHP_START__
add_action('wp_enqueue_scripts', function () {
    if (!is_front_page()) {
        return;
    }

    $dkg_mobile_fill_lock_path = get_template_directory() . '/assets/js/__JS_FILENAME__';
    $dkg_mobile_fill_lock_uri  = get_template_directory_uri() . '/assets/js/__JS_FILENAME__';

    wp_enqueue_script(
        'dkg-mobile-homepage-product-image-fill-lock',
        $dkg_mobile_fill_lock_uri,
        array(),
        file_exists($dkg_mobile_fill_lock_path) ? filemtime($dkg_mobile_fill_lock_path) : null,
        true
    );
}, 120);
__PHP_END__"""

PHP_BLOCK = (
    PHP_BLOCK_TEMPLATE
    .replace("__PHP_START__", PHP_START)
    .replace("__PHP_END__", PHP_END)
    .replace("__JS_FILENAME__", JS_FILENAME)
)


def read_text(path: Path) -> str:
    raw = path.read_bytes()
    for enc in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def make_backup(path: Path, label: str) -> Path:
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = path.with_name(path.name + f".backup-before-fix10-{label}-{stamp}")
    backup.write_bytes(path.read_bytes())
    return backup


def remove_old_php_block(text: str) -> tuple[str, int]:
    removed = 0

    while True:
        start = text.find(PHP_START)
        if start == -1:
            return text, removed

        end = text.find(PHP_END, start)
        if end == -1:
            raise RuntimeError(
                "Found Fix 10 PHP START marker but not END marker. "
                "Please inspect functions.php manually."
            )

        end += len(PHP_END)
        before = text[:start].rstrip()
        after = text[end:].lstrip()
        text = before + ("\n\n" + after if after else "\n")
        removed += 1


def update_functions_php(functions_path: Path) -> tuple[str, bool, dict]:
    original = read_text(functions_path)
    cleaned, removed = remove_old_php_block(original)

    cleaned = cleaned.rstrip()
    if cleaned.endswith("?>"):
        cleaned = cleaned[:-2].rstrip()

    updated = cleaned + "\n\n" + PHP_BLOCK + "\n"

    return updated, updated != original, {"old_php_blocks_removed": removed}


def update_js(js_path: Path) -> tuple[str, bool]:
    original = read_text(js_path) if js_path.exists() else ""
    updated = JS_CODE.rstrip() + "\n"
    return updated, updated != original


def apply(root: Path, dry_run: bool) -> int:
    functions_path = root / "functions.php"
    js_dir = root / "assets" / "js"
    js_path = js_dir / JS_FILENAME

    if not functions_path.exists():
        print("ERROR: Could not find functions.php")
        print(f"Looked here: {functions_path}")
        return 2

    if not js_dir.exists():
        print("ERROR: Could not find assets/js folder")
        print(f"Looked here: {js_dir}")
        return 2

    try:
        new_functions, functions_changed, details = update_functions_php(functions_path)
        new_js, js_changed = update_js(js_path)
    except Exception as exc:
        print(f"ERROR: {exc}")
        return 2

    if not functions_changed and not js_changed:
        print("No change needed. Fix 10 already appears installed.")
        return 0

    if dry_run:
        print("DRY RUN: no files changed.")
        print(f"Would update functions.php: {'yes' if functions_changed else 'no'}")
        print(f"Would update JS file:       {'yes' if js_changed else 'no'}")
        print(f"JS file path: {js_path}")
        print("")
        print("Details:")
        for key, value in details.items():
            print(f"  - {key}: {value}")
        return 0

    backups = []

    if functions_changed:
        backups.append(make_backup(functions_path, "functions"))
        functions_path.write_text(new_functions, encoding="utf-8", newline="")

    if js_changed:
        if js_path.exists():
            backups.append(make_backup(js_path, "runtime-js"))
        js_path.write_text(new_js, encoding="utf-8", newline="")

    print("DKG Fix 10 complete.")
    print("")
    print("Updated files:")
    if functions_changed:
        print(f"  - {functions_path}")
    if js_changed:
        print(f"  - {js_path}")

    print("")
    print("Backups:")
    if backups:
        for backup in backups:
            print(f"  - {backup}")
    else:
        print("  - none needed")

    print("")
    print("What changed:")
    print("  - Added a mobile-homepage-only runtime image fill lock.")
    print("  - It runs after DOMContentLoaded, load, startup timers, resize/orientation, and startup DOM mutations.")
    print("  - It forces product links/wrappers/images to fill the current product-card border/frame.")
    print("  - It does not change product-card width or height.")
    print("  - Desktop/non-mobile is untouched.")

    print("")
    print("Recommended checks:")
    print("  1. Hard refresh the mobile homepage.")
    print("  2. Wait several seconds after page load.")
    print("  3. Confirm images still fill their borders after the carousel initializes/autoscrolls.")
    print("  4. Check desktop homepage is unchanged.")
    print("")
    print("If you use a cache/minify plugin, clear the site cache after uploading this change.")

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Add mobile homepage runtime image fill lock.")
    parser.add_argument("--root", default=".", help="Theme root folder. Default: current folder.")
    parser.add_argument("--dry-run", action="store_true", help="Show what would change without writing files.")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()

    if not root.exists() or not root.is_dir():
        print(f"ERROR: Root folder does not exist or is not a directory: {root}")
        return 2

    return apply(root, args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""
DKG mobile homepage product size / border tune.

Purpose:
- Keep the good fixes from the previous cleanup updater.
- Make the 3 visible mobile product spots actually fill their equal slots.
- Stop cloned product cards from inheriting narrow desktop pill sizing.
- Make product card borders match the collection plate accent color.
- Enlarge product images inside the cloned mobile carousel cards.

Edits:
- assets/css/front-page.css only

Backs up:
- assets/css/front-page.css

Run from theme repo root:
    python mobile_product_size_border_tune.py
"""

from __future__ import annotations

import re
import shutil
from datetime import datetime
from pathlib import Path


TUNE_START = "/* === DKG MOBILE PRODUCT SIZE BORDER TUNE START === */"
TUNE_END = "/* === DKG MOBILE PRODUCT SIZE BORDER TUNE END === */"

MAIN_MOBILE_END = "/* === DKG MOBILE MAIN HOMEPAGE COLLECTION PLATES END === */"


NEW_TUNE_BLOCK = r'''/* === DKG MOBILE PRODUCT SIZE BORDER TUNE START === */

/*
  Mobile product card size / border tuning.

  This block intentionally comes AFTER the main mobile homepage collection
  plate block. It does not change the JS or the DOM structure.

  It fixes the visible issue where cloned product cards inherit older desktop
  .product-card sizing/borders and become skinny black capsules with tiny images.

  Tuning knobs:
  - --dkg-mobile-product-image-scale controls how much the product image canvas is enlarged.
  - --dkg-mobile-product-card-border controls inner product frame thickness.
*/

@media screen and (max-width: 767px) {

  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .collection-box {
    --dkg-mobile-product-image-scale: 1.62;
    --dkg-mobile-product-card-border: 5px;
    --dkg-mobile-product-card-radius: 19px;
    --dkg-mobile-plate-accent: currentColor;
  }

  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .collection-box.red {
    --dkg-mobile-plate-accent: #ff4f59;
  }

  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .collection-box.blue {
    --dkg-mobile-plate-accent: #4da3ff;
  }

  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .collection-box.green {
    --dkg-mobile-plate-accent: #45d985;
  }

  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .collection-box.yellow {
    --dkg-mobile-plate-accent: #ffd84d;
  }

  /*
    Give the product row enough vertical space to feel like part of the plate,
    while still keeping exactly 3 visible slots across.
  */
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .collection-content > .dkg-mobile-carousel-viewport {
    width: 100% !important;
    max-width: 100% !important;
    min-height: clamp(142px, 38vw, 178px) !important;
    height: clamp(142px, 38vw, 178px) !important;

    margin: 0 auto !important;
    padding: 0 !important;

    display: block !important;
    overflow: hidden !important;

    background: transparent !important;
    border: 0 !important;
    box-sizing: border-box !important;
  }

  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .dkg-mobile-product-track {
    height: 100% !important;
    align-items: stretch !important;
  }

  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .dkg-mobile-product-item {
    height: 100% !important;
    min-height: 100% !important;
    max-height: 100% !important;

    display: flex !important;
    align-items: stretch !important;
    justify-content: center !important;

    overflow: visible !important;
    box-sizing: border-box !important;
  }

  /*
    Critical override:
    The cloned .product-card was still behaving like the old desktop carousel card.
    Force it to fill the mobile slot instead of becoming a narrow vertical capsule.
  */
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .collection-box .dkg-mobile-carousel-viewport .dkg-mobile-product-item > .product-card,
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .collection-box .dkg-mobile-carousel-viewport .dkg-mobile-product-item > .product-card.dkg-mobile-product-card-inner,
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .collection-box .dkg-mobile-carousel-viewport .dkg-mobile-product-item > .dkg-mobile-product-card-inner {
    flex: 0 0 100% !important;

    width: 100% !important;
    min-width: 100% !important;
    max-width: 100% !important;

    height: 100% !important;
    min-height: 100% !important;
    max-height: 100% !important;

    aspect-ratio: auto !important;

    margin: 0 !important;
    padding: 5px !important;
    box-sizing: border-box !important;

    display: flex !important;
    align-items: center !important;
    justify-content: center !important;

    overflow: hidden !important;

    border-style: solid !important;
    border-width: var(--dkg-mobile-product-card-border) !important;
    border-color: var(--dkg-mobile-plate-accent) !important;
    border-radius: var(--dkg-mobile-product-card-radius) !important;

    background: rgba(0, 0, 0, 0.68) !important;
    box-shadow:
      0 0 0 1px rgba(0,0,0,0.55),
      0 5px 12px rgba(0,0,0,0.42) !important;

    transform: none !important;
    pointer-events: none !important;
  }

  /*
    Product images are often on a square product-photo canvas with whitespace.
    Scale the image element so the actual product appears larger.
    This still uses object-fit: contain so it does not behave like a crop-fill image.
  */
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .collection-box .dkg-mobile-carousel-viewport .dkg-mobile-product-item img,
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .collection-box .dkg-mobile-carousel-viewport .dkg-mobile-product-item img.product-image,
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .collection-box .dkg-mobile-carousel-viewport .dkg-mobile-product-item .product-image {
    width: 100% !important;
    min-width: 100% !important;
    max-width: 100% !important;

    height: 100% !important;
    min-height: 100% !important;
    max-height: 100% !important;

    display: block !important;

    object-fit: contain !important;
    object-position: center center !important;

    margin: 0 auto !important;
    padding: 0 !important;

    background: transparent !important;

    transform: scale(var(--dkg-mobile-product-image-scale)) !important;
    transform-origin: center center !important;

    image-rendering: auto !important;
  }

  /*
    Make 1-product and 2-product collections feel centered and intentional.
  */
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .dkg-mobile-carousel-viewport.dkg-mobile-static .dkg-mobile-product-track {
    justify-content: center !important;
  }

  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .dkg-mobile-carousel-viewport.dkg-mobile-static .dkg-mobile-product-item {
    flex-grow: 0 !important;
    flex-shrink: 0 !important;
  }

  /*
    Slightly taller cards on normal phones; tighter on tiny phones.
  */
  @media screen and (max-width: 390px) {
    body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .collection-box {
      --dkg-mobile-product-image-scale: 1.58;
      --dkg-mobile-product-card-border: 4px;
      --dkg-mobile-product-card-radius: 16px;
    }

    body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .collection-content > .dkg-mobile-carousel-viewport {
      min-height: clamp(126px, 36vw, 158px) !important;
      height: clamp(126px, 36vw, 158px) !important;
    }

    body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .collection-box .dkg-mobile-carousel-viewport .dkg-mobile-product-item > .product-card,
    body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .collection-box .dkg-mobile-carousel-viewport .dkg-mobile-product-item > .product-card.dkg-mobile-product-card-inner,
    body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .collection-box .dkg-mobile-carousel-viewport .dkg-mobile-product-item > .dkg-mobile-product-card-inner {
      padding: 4px !important;
    }
  }
}

/* === DKG MOBILE PRODUCT SIZE BORDER TUNE END === */
'''


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", errors="replace")


def remove_existing_tune_blocks(text: str) -> tuple[str, int]:
    pattern = re.compile(
        re.escape(TUNE_START) + r".*?" + re.escape(TUNE_END),
        flags=re.DOTALL,
    )
    new_text, count = pattern.subn("", text)
    new_text = re.sub(r"\n{4,}", "\n\n\n", new_text)
    return new_text.rstrip() + "\n", count


def insert_tune_block(text: str) -> str:
    if MAIN_MOBILE_END in text:
        index = text.rfind(MAIN_MOBILE_END) + len(MAIN_MOBILE_END)
        return (
            text[:index].rstrip()
            + "\n\n"
            + NEW_TUNE_BLOCK.rstrip()
            + "\n\n"
            + text[index:].lstrip()
        )

    return text.rstrip() + "\n\n" + NEW_TUNE_BLOCK.rstrip() + "\n"


def main() -> int:
    root = Path.cwd().resolve()
    css_path = root / "assets" / "css" / "front-page.css"

    if not css_path.exists():
        raise SystemExit(
            "Missing assets/css/front-page.css.\n\n"
            "Run this from the theme repo root:\n"
            r'  C:\Users\John\Desktop\shop dkg\dkg-shop-theme'
        )

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_dir = root / f"_dkg_mobile_product_size_border_tune_backup_{timestamp}"
    backup_dir.mkdir(parents=True, exist_ok=False)

    backup_css = backup_dir / "assets" / "css" / "front-page.css"
    backup_css.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(css_path, backup_css)

    old_css = read_text(css_path)
    cleaned_css, removed_count = remove_existing_tune_blocks(old_css)
    new_css = insert_tune_block(cleaned_css)

    write_text(css_path, new_css)

    summary = [
        "DKG mobile product size / border tune",
        f"Timestamp: {timestamp}",
        f"Repo root: {root}",
        f"Backed up CSS to: {backup_css}",
        "",
        f"Removed existing tune blocks: {removed_count}",
        "Inserted new product size / border tune block.",
        "",
        "What changed:",
        "- Product cards inside the mobile clone layer are forced to fill their 1/3-width slots.",
        "- Product card borders now use collection accent colors instead of inherited black-only desktop borders.",
        "- Product images are scaled larger inside the frame while keeping object-fit: contain.",
        "- The carousel viewport is taller so products use more of the collection plate space.",
        "",
        "Notes:",
        "- This only edits assets/css/front-page.css.",
        "- It does not change the JS, redirect behavior, header, or page-mobile-shop.php.",
    ]

    summary_path = backup_dir / "product_size_border_tune_summary.txt"
    write_text(summary_path, "\n".join(summary) + "\n")

    print("Done.")
    print(f"Backup folder: {backup_dir}")
    print(f"Removed existing tune blocks: {removed_count}")
    print("Inserted mobile product size / border tune block into assets/css/front-page.css.")
    print("")
    print("Next:")
    print("1. Upload/deploy assets/css/front-page.css.")
    print("2. Clear cache.")
    print("3. Test the normal homepage on phone width.")
    print("4. If product images are still too small, increase --dkg-mobile-product-image-scale from 1.62 to about 1.75.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
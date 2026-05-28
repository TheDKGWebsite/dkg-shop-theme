from pathlib import Path
from datetime import datetime
import shutil
import re

ROOT = Path(__file__).resolve().parent
MOBILE_PAGE = ROOT / "page-mobile-shop.php"

START = "/* === DKG MOBILE SHOP REAL OVERRIDE START === */"
END = "/* === DKG MOBILE SHOP REAL OVERRIDE END === */"

PATCH = r"""
/* === DKG MOBILE SHOP REAL OVERRIDE START === */

/*
  REAL FIX:
  This CSS is inside page-mobile-shop.php, so it only loads on /mobile-shop/.
  Do NOT depend on body.page-mobile-shop or body.page-template-page-mobile-shop,
  because WordPress may not add those body classes when this file is used as
  a slug template.
*/

/* Force the mobile-shop header thin. */
.site-header {
  height: 52px !important;
  min-height: 52px !important;
  max-height: 52px !important;
  padding: 3px 7px !important;
  margin: 0 !important;
  overflow: hidden !important;
  display: flex !important;
  align-items: center !important;
  box-sizing: border-box !important;
}

.site-header .header-inner {
  height: 46px !important;
  min-height: 46px !important;
  max-height: 46px !important;
  width: 100% !important;
  max-width: 100% !important;

  padding: 0 !important;
  margin: 0 !important;

  display: flex !important;
  flex-direction: row !important;
  flex-wrap: nowrap !important;
  align-items: center !important;
  justify-content: space-between !important;
  gap: 6px !important;

  overflow: hidden !important;
  transform: none !important;
  box-sizing: border-box !important;
}

/* Keep logo small. */
.site-header .logo,
.site-header .site-logo,
.site-header .custom-logo-link,
.site-header .site-branding {
  height: 42px !important;
  max-height: 42px !important;
  min-height: 0 !important;
  display: flex !important;
  align-items: center !important;
  flex: 0 0 auto !important;
  overflow: hidden !important;
}

.site-header .logo img,
.site-header .custom-logo,
.site-header .custom-logo-link img,
.site-header .site-branding img {
  width: auto !important;
  height: auto !important;
  max-width: 98px !important;
  max-height: 38px !important;
  display: block !important;
  object-fit: contain !important;
}

/* Hide desktop header extras on mobile-shop. */
.dkg-header-picture-rotator,
.dkg-header-picture-frame,
.dkg-header-picture-img,
.dkg-header-picture-img-layer,
.dkg-left-overlay,
.dkg-header-lights-image-wrap,
.dkg-header-lights-image {
  display: none !important;
  width: 0 !important;
  height: 0 !important;
  max-width: 0 !important;
  max-height: 0 !important;
  min-width: 0 !important;
  min-height: 0 !important;
  opacity: 0 !important;
  overflow: hidden !important;
  pointer-events: none !important;
}

/* Make the nav fit in one thin row. */
.site-header .nav {
  height: 42px !important;
  min-height: 0 !important;
  max-height: 42px !important;
  flex: 1 1 auto !important;
  min-width: 0 !important;

  margin: 0 !important;
  padding: 0 !important;

  display: flex !important;
  flex-direction: row !important;
  flex-wrap: nowrap !important;
  align-items: center !important;
  justify-content: flex-end !important;
  gap: 8px !important;

  overflow: hidden !important;
}

.site-header .nav a {
  font-size: 0.72rem !important;
  line-height: 1 !important;
  padding: 4px 3px !important;
  margin: 0 !important;
  white-space: nowrap !important;

  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
}

/* Hide social icons on mobile-shop to keep header short. */
.site-header .nav a.nav-social {
  display: none !important;
}

/* Make sure content starts close to the thinner header. */
.dkg-mobile-plates-main {
  padding-top: 12px !important;
}

/*
  PLATE/LABEL FIX:
  The first overhaul made labels float like desktop labels.
  On phone they need to be inside the plate, directly connected to the product images.
*/
.dkg-mobile-collection-plate {
  position: relative !important;
  min-height: 0 !important;
  height: auto !important;

  padding: 11px 9px 10px !important;
  overflow: hidden !important;
  border-radius: 21px !important;

  display: flex !important;
  flex-direction: column !important;
  gap: 9px !important;

  box-sizing: border-box !important;
}

.dkg-mobile-collection-label {
  position: relative !important;
  left: auto !important;
  top: auto !important;
  right: auto !important;
  bottom: auto !important;
  transform: none !important;

  z-index: 3 !important;

  width: 100% !important;
  max-width: none !important;
  margin: 0 !important;
  padding: 8px 9px !important;

  display: block !important;
  box-sizing: border-box !important;

  border-radius: 13px !important;
  background: rgba(0, 0, 0, 0.78) !important;
  border: 1px solid rgba(255, 255, 255, 0.16) !important;
  box-shadow: 0 4px 12px rgba(0,0,0,0.38) !important;

  color: #fff !important;
  text-align: center !important;
  text-transform: uppercase !important;
  letter-spacing: 0.045em !important;
  font-weight: 800 !important;
  font-size: clamp(0.76rem, 3.45vw, 0.96rem) !important;
  line-height: 1.12 !important;
  white-space: normal !important;
}

/* Product image grid now belongs visually to the label above it. */
.dkg-mobile-product-row {
  position: relative !important;
  z-index: 2 !important;

  width: 100% !important;
  height: auto !important;
  margin: 0 !important;

  display: grid !important;
  grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
  gap: 8px !important;
}

.dkg-mobile-product-card {
  height: 116px !important;
  min-height: 116px !important;
  max-height: 116px !important;
  border-radius: 13px !important;

  position: relative !important;
  overflow: hidden !important;
}

.dkg-mobile-product-card img {
  width: 100% !important;
  height: 100% !important;
  display: block !important;
  object-fit: cover !important;
}

/* Background stays inside the plate. */
.dkg-mobile-collection-bg {
  position: absolute !important;
  inset: 0 !important;
  border-radius: inherit !important;
  overflow: hidden !important;
  z-index: 0 !important;
}

.dkg-mobile-collection-bg img {
  width: 100% !important;
  height: 100% !important;
  object-fit: fill !important;
  filter: brightness(0.66) contrast(1.04) !important;
}

/* Tiny phones. */
@media (max-width: 390px) {
  .site-header {
    height: 48px !important;
    min-height: 48px !important;
    max-height: 48px !important;
    padding: 3px 6px !important;
  }

  .site-header .header-inner {
    height: 42px !important;
    min-height: 42px !important;
    max-height: 42px !important;
  }

  .site-header .logo img,
  .site-header .custom-logo,
  .site-header .custom-logo-link img,
  .site-header .site-branding img {
    max-width: 84px !important;
    max-height: 33px !important;
  }

  .site-header .nav {
    gap: 6px !important;
  }

  .site-header .nav a {
    font-size: 0.66rem !important;
    padding: 3px 2px !important;
  }

  .dkg-mobile-plates-main {
    padding-left: 7px !important;
    padding-right: 7px !important;
  }

  .dkg-mobile-collection-plate {
    padding: 9px 7px 8px !important;
    gap: 7px !important;
    border-radius: 18px !important;
  }

  .dkg-mobile-product-row {
    gap: 7px !important;
  }

  .dkg-mobile-product-card {
    height: 104px !important;
    min-height: 104px !important;
    max-height: 104px !important;
    border-radius: 11px !important;
  }
}

/* === DKG MOBILE SHOP REAL OVERRIDE END === */
"""

def backup(path: Path) -> Path:
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_path = path.with_name(f"{path.name}.backup-before-real-mobile-fix-{ts}")
    shutil.copy2(path, backup_path)
    return backup_path

def insert_patch(text: str) -> str:
    # Remove old copy if rerun.
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
    text = pattern.sub("", text)

    # Put this as late as possible inside the existing main style block.
    style_id = 'id="dkg-mobile-homepage-plates-overhaul"'
    style_pos = text.find(style_id)

    if style_pos != -1:
        close_pos = text.find("</style>", style_pos)
        if close_pos != -1:
            return text[:close_pos] + "\n\n" + PATCH.strip() + "\n\n" + text[close_pos:]

    # Fallback: insert a new style block before main content.
    main_pos = text.find('<main class="dkg-mobile-plates-main"')
    style_block = "\n<style id=\"dkg-mobile-shop-real-override\">\n" + PATCH.strip() + "\n</style>\n"

    if main_pos != -1:
        return text[:main_pos] + style_block + "\n" + text[main_pos:]

    # Last fallback.
    footer_pos = text.find("<?php get_footer(); ?>")
    if footer_pos != -1:
        return text[:footer_pos] + style_block + "\n" + text[footer_pos:]

    return text + style_block

def main():
    if not MOBILE_PAGE.exists():
        raise FileNotFoundError(f"Could not find {MOBILE_PAGE}")

    original = MOBILE_PAGE.read_text(encoding="utf-8", errors="replace")
    backup_path = backup(MOBILE_PAGE)

    updated = insert_patch(original)
    MOBILE_PAGE.write_text(updated, encoding="utf-8", newline="\n")

    print("Done.")
    print(f"Backup created: {backup_path}")
    print("Added final unscoped /mobile-shop/ override.")
    print("")
    print("Test this exact URL on your phone:")
    print("https://shop.dkg.zone/mobile-shop/?mobile-real-fix=1")
    print("")
    print("If it still looks unchanged, then the phone is seeing cached HTML or WordPress is not using page-mobile-shop.php.")

if __name__ == "__main__":
    main()
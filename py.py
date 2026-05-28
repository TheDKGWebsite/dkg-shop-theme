from pathlib import Path
from datetime import datetime
import shutil
import re

ROOT = Path(__file__).resolve().parent
MOBILE_PAGE = ROOT / "page-mobile-shop.php"

START = "/* === DKG MOBILE PHONE FIX V2 START === */"
END = "/* === DKG MOBILE PHONE FIX V2 END === */"

PATCH_CSS = r"""
/* === DKG MOBILE PHONE FIX V2 START === */

/*
  This block is intentionally scoped to /mobile-shop/.
  It should come late in page-mobile-shop.php so it beats the older global
  mobile header rules from front-page.css/style.css.
*/

/* Make the actual phone header thin, even when global 640px header rules try to stack it. */
html body.page-mobile-shop header.site-header,
html body.page-template-page-mobile-shop header.site-header,
html body.page-mobile-shop .site-header,
html body.page-template-page-mobile-shop .site-header {
  height: 54px !important;
  min-height: 54px !important;
  max-height: 54px !important;
  padding: 3px 7px !important;
  margin: 0 !important;
  overflow: hidden !important;
  display: flex !important;
  align-items: center !important;
  box-sizing: border-box !important;
}

html body.page-mobile-shop .site-header .header-inner,
html body.page-template-page-mobile-shop .site-header .header-inner,
html body.page-mobile-shop header.site-header .header-inner,
html body.page-template-page-mobile-shop header.site-header .header-inner {
  height: 48px !important;
  min-height: 48px !important;
  max-height: 48px !important;
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

/* Keep logo short. */
html body.page-mobile-shop .site-header .logo,
html body.page-template-page-mobile-shop .site-header .logo,
html body.page-mobile-shop .site-header .custom-logo-link,
html body.page-template-page-mobile-shop .site-header .custom-logo-link,
html body.page-mobile-shop .site-header .site-branding,
html body.page-template-page-mobile-shop .site-header .site-branding {
  height: 44px !important;
  max-height: 44px !important;
  min-height: 0 !important;
  display: flex !important;
  align-items: center !important;
  flex: 0 0 auto !important;
  overflow: hidden !important;
}

html body.page-mobile-shop .site-header .logo img,
html body.page-template-page-mobile-shop .site-header .logo img,
html body.page-mobile-shop .site-header .custom-logo,
html body.page-template-page-mobile-shop .site-header .custom-logo,
html body.page-mobile-shop .site-header .custom-logo-link img,
html body.page-template-page-mobile-shop .site-header .custom-logo-link img,
html body.page-mobile-shop .site-header .site-branding img,
html body.page-template-page-mobile-shop .site-header .site-branding img {
  width: auto !important;
  height: auto !important;
  max-width: 104px !important;
  max-height: 40px !important;
  display: block !important;
  object-fit: contain !important;
}

/*
  The rotator and big side overlay are desktop/header extras.
  On real phones they make the header impossible to keep thin.
*/
html body.page-mobile-shop .dkg-header-picture-rotator,
html body.page-template-page-mobile-shop .dkg-header-picture-rotator,
html body.page-mobile-shop .dkg-header-picture-frame,
html body.page-template-page-mobile-shop .dkg-header-picture-frame,
html body.page-mobile-shop .dkg-left-overlay,
html body.page-template-page-mobile-shop .dkg-left-overlay {
  display: none !important;
  width: 0 !important;
  height: 0 !important;
  max-width: 0 !important;
  max-height: 0 !important;
  overflow: hidden !important;
}

/*
  Keep just practical nav text on mobile-shop.
  This is the most reliable way to make the real phone header thinner.
*/
html body.page-mobile-shop .site-header .nav,
html body.page-template-page-mobile-shop .site-header .nav {
  height: 44px !important;
  min-height: 0 !important;
  max-height: 44px !important;
  flex: 1 1 auto !important;
  min-width: 0 !important;
  margin: 0 !important;
  padding: 0 !important;

  display: flex !important;
  flex-direction: row !important;
  flex-wrap: nowrap !important;
  align-items: center !important;
  justify-content: flex-end !important;
  gap: 7px !important;

  overflow: hidden !important;
}

html body.page-mobile-shop .site-header .nav a,
html body.page-template-page-mobile-shop .site-header .nav a {
  font-size: 0.72rem !important;
  line-height: 1 !important;
  padding: 4px 3px !important;
  margin: 0 !important;
  white-space: nowrap !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
}

/* Hide socials on /mobile-shop/ so the phone header stops becoming a giant strip. */
html body.page-mobile-shop .site-header .nav a.nav-social,
html body.page-template-page-mobile-shop .site-header .nav a.nav-social {
  display: none !important;
}

/* Pull the content up now that the header is thinner. */
html body.page-mobile-shop .dkg-mobile-plates-main,
html body.page-template-page-mobile-shop .dkg-mobile-plates-main {
  padding-top: 14px !important;
}

/*
  COLLECTION PLATE FIX:
  The label is no longer a floating blob outside the plate.
  It becomes an internal title bar connected to the product images below it.
*/
html body.page-mobile-shop .dkg-mobile-collection-plate,
html body.page-template-page-mobile-shop .dkg-mobile-collection-plate {
  min-height: 0 !important;
  height: auto !important;
  padding: 12px 10px 11px !important;
  overflow: hidden !important;
  border-radius: 22px !important;
  display: flex !important;
  flex-direction: column !important;
  gap: 10px !important;
}

html body.page-mobile-shop .dkg-mobile-collection-label,
html body.page-template-page-mobile-shop .dkg-mobile-collection-label {
  position: relative !important;
  left: auto !important;
  top: auto !important;
  right: auto !important;
  bottom: auto !important;
  transform: none !important;

  z-index: 3 !important;
  width: calc(100% - 8px) !important;
  max-width: none !important;
  margin: 0 auto 2px !important;
  padding: 8px 10px !important;

  display: block !important;
  box-sizing: border-box !important;

  border-radius: 14px !important;
  background: rgba(0, 0, 0, 0.74) !important;
  border: 1px solid rgba(255,255,255,0.16) !important;
  box-shadow: 0 4px 12px rgba(0,0,0,0.38) !important;

  color: #fff !important;
  text-align: center !important;
  text-transform: uppercase !important;
  letter-spacing: 0.045em !important;
  font-weight: 800 !important;
  font-size: clamp(0.78rem, 3.5vw, 0.98rem) !important;
  line-height: 1.12 !important;
  white-space: normal !important;
}

/* Keep product images spatially attached to the label/plate. */
html body.page-mobile-shop .dkg-mobile-product-row,
html body.page-template-page-mobile-shop .dkg-mobile-product-row {
  position: relative !important;
  z-index: 2 !important;
  display: grid !important;
  grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
  gap: 8px !important;
  width: 100% !important;
  margin: 0 !important;
}

html body.page-mobile-shop .dkg-mobile-product-card,
html body.page-template-page-mobile-shop .dkg-mobile-product-card {
  height: 118px !important;
  min-height: 118px !important;
  max-height: 118px !important;
  border-radius: 13px !important;
}

/* Make background plate fill the actual card area, not visually detach the title. */
html body.page-mobile-shop .dkg-mobile-collection-bg,
html body.page-template-page-mobile-shop .dkg-mobile-collection-bg {
  inset: 0 !important;
  border-radius: inherit !important;
}

html body.page-mobile-shop .dkg-mobile-collection-bg img,
html body.page-template-page-mobile-shop .dkg-mobile-collection-bg img {
  object-fit: fill !important;
  filter: brightness(0.68) contrast(1.04) !important;
}

/* Tiny phones. */
@media (max-width: 390px) {
  html body.page-mobile-shop header.site-header,
  html body.page-template-page-mobile-shop header.site-header,
  html body.page-mobile-shop .site-header,
  html body.page-template-page-mobile-shop .site-header {
    height: 50px !important;
    min-height: 50px !important;
    max-height: 50px !important;
    padding: 3px 6px !important;
  }

  html body.page-mobile-shop .site-header .header-inner,
  html body.page-template-page-mobile-shop .site-header .header-inner {
    height: 44px !important;
    min-height: 44px !important;
    max-height: 44px !important;
  }

  html body.page-mobile-shop .site-header .logo img,
  html body.page-template-page-mobile-shop .site-header .logo img,
  html body.page-mobile-shop .site-header .custom-logo,
  html body.page-template-page-mobile-shop .site-header .custom-logo,
  html body.page-mobile-shop .site-header .custom-logo-link img,
  html body.page-template-page-mobile-shop .site-header .custom-logo-link img {
    max-width: 88px !important;
    max-height: 34px !important;
  }

  html body.page-mobile-shop .site-header .nav a,
  html body.page-template-page-mobile-shop .site-header .nav a {
    font-size: 0.66rem !important;
    padding: 3px 2px !important;
  }

  html body.page-mobile-shop .dkg-mobile-collection-plate,
  html body.page-template-page-mobile-shop .dkg-mobile-collection-plate {
    padding: 10px 8px 9px !important;
    gap: 8px !important;
    border-radius: 19px !important;
  }

  html body.page-mobile-shop .dkg-mobile-product-card,
  html body.page-template-page-mobile-shop .dkg-mobile-product-card {
    height: 106px !important;
    min-height: 106px !important;
    max-height: 106px !important;
  }
}

/* === DKG MOBILE PHONE FIX V2 END === */
"""

def backup(path: Path) -> Path:
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    out = path.with_name(f"{path.name}.backup-before-phone-fix-{ts}")
    shutil.copy2(path, out)
    return out

def insert_patch(text: str) -> str:
    # Remove old copy of this patch if rerun.
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
    text = pattern.sub("", text)

    # Best place: inside the existing <style id="dkg-mobile-homepage-plates-overhaul"> block,
    # right before </style>, so it loads after the first overhaul CSS.
    style_id = 'id="dkg-mobile-homepage-plates-overhaul"'
    style_pos = text.find(style_id)

    if style_pos != -1:
        close_pos = text.find("</style>", style_pos)
        if close_pos != -1:
            return text[:close_pos] + "\n\n" + PATCH_CSS.strip() + "\n\n" + text[close_pos:]

    # Fallback: add a new style block before the main mobile markup.
    main_pos = text.find('<main class="dkg-mobile-plates-main"')
    style_block = "\n<style id=\"dkg-mobile-phone-fix-v2\">\n" + PATCH_CSS.strip() + "\n</style>\n"

    if main_pos != -1:
        return text[:main_pos] + style_block + "\n" + text[main_pos:]

    # Last resort: add before get_footer.
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
    print("Patched page-mobile-shop.php with stronger real-phone header and plate-label fixes.")
    print("")
    print("Test:")
    print("https://shop.dkg.zone/mobile-shop/")
    print("")
    print("Important: clear/cache-bust if your phone still shows the old version.")
    print("Try adding ?v=phonefix2 to the URL once:")
    print("https://shop.dkg.zone/mobile-shop/?v=phonefix2")

if __name__ == "__main__":
    main()
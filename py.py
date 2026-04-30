from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
WOO_PHP = ROOT / "woocommerce.php"
WOO_CSS = ROOT / "assets" / "css" / "woocommerce.css"

if not WOO_PHP.exists():
    raise FileNotFoundError("woocommerce.php not found. Run this from your theme root.")

php = WOO_PHP.read_text(encoding="utf-8", errors="replace")
css = WOO_CSS.read_text(encoding="utf-8", errors="replace") if WOO_CSS.exists() else ""

# 1. Replace/normalize the collection background map.
php = re.sub(
    r"\$collection_backgrounds\s*=\s*array\s*\(.*?\);\s*",
    """$collection_backgrounds = array(
    'shirts'   => 'col1.png',
    'posters'  => 'col1.png',
    'stickers' => 'col1.png',
    'hats'     => 'col1.png',
);

""",
    php,
    flags=re.DOTALL
)

# 2. Replace/normalize the background lookup logic.
php = re.sub(
    r"\$shop_bg\s*=\s*'';\s*if\s*\(\$featured_collection.*?\}\s*",
    """$shop_bg = '';

if ($featured_collection && isset($collection_backgrounds[$featured_collection])) {
    $bg_file = $collection_backgrounds[$featured_collection];
    $bg_path = get_template_directory() . '/assets/images/' . $bg_file;

    if (file_exists($bg_path)) {
        $shop_bg = get_template_directory_uri() . '/assets/images/' . $bg_file;
    }
}

""",
    php,
    flags=re.DOTALL
)

# 3. Remove older background div/style experiments to avoid conflicts.
php = re.sub(
    r"if\s*\(\$shop_bg\)\s*\{\s*echo '<style id=\"dkg-dynamic-shop-bg\">';.*?echo '</style>';\s*\}\s*",
    "",
    php,
    flags=re.DOTALL
)

php = re.sub(
    r"if\s*\(\$shop_bg\)\s*\{\s*echo '<div class=\"dkg-real-shop-bg\".*?echo '<div class=\"dkg-real-shop-bg-overlay\"></div>';\s*\}\s*",
    "",
    php,
    flags=re.DOTALL
)

php = re.sub(
    r"\$bg_style\s*=\s*\$shop_bg\s*\?.*?echo\s+'<main class=\"dkg-shop-main\"'\s*\.\s*\$bg_style\s*\.\s*'>';\s*",
    "echo '<main class=\"dkg-shop-main\">';\n",
    php,
    flags=re.DOTALL
)

# 4. Insert direct body background override after get_header/background calculation and before main.
direct_style = """if ($shop_bg) {
    echo '<!-- DKG DEBUG: dynamic shop background loaded: ' . esc_html($shop_bg) . ' -->';
    echo '<style id="dkg-force-body-shop-bg">
        body {
            background-image: linear-gradient(rgba(0,0,0,0.55), rgba(0,0,0,0.55)), url("' . esc_url($shop_bg) . '") !important;
            background-size: cover !important;
            background-position: center center !important;
            background-repeat: no-repeat !important;
            background-attachment: fixed !important;
            background-color: #000 !important;
        }
    </style>';
}

"""

if "dkg-force-body-shop-bg" not in php:
    php = php.replace("echo '<main class=\"dkg-shop-main\">';", direct_style + "echo '<main class=\"dkg-shop-main\">';", 1)

WOO_PHP.write_text(php, encoding="utf-8")

# 5. Add CSS cleanup for any previous pseudo-background attempts.
cleanup_css = """
/* === DKG CLEANUP: disable old dynamic background layering attempts === */
.dkg-shop-main::before,
.dkg-shop-main::after,
.dkg-real-shop-bg,
.dkg-real-shop-bg-overlay,
body:has(.dkg-shop-main)::before,
body:has(.dkg-shop-main)::after {
    display: none !important;
    content: none !important;
}
/* === DKG CLEANUP END === */
"""

if "DKG CLEANUP: disable old dynamic background layering attempts" not in css:
    WOO_CSS.parent.mkdir(parents=True, exist_ok=True)
    css += "\n" + cleanup_css
    WOO_CSS.write_text(css, encoding="utf-8")

print("Done.")
print("This version directly overrides the BODY background.")
print("Test this exact URL after deploying:")
print("https://shop.dkg.zone/shop/?featured_collection=shirts")
#!/usr/bin/env python3
"""
Patch a local WordPress/WooCommerce theme repo so the custom homepage
uses real WooCommerce categories/products instead of hardcoded cards.

What it does:
- backs up front-page.php and assets/css/front-page.css if they exist
- overwrites front-page.php with a dynamic WooCommerce category/product loop
- patches front-page.css so product cards can be clickable links
- optionally ensures the front-page stylesheet/script enqueue exists in functions.php

Usage:
    python apply_wc_homepage.py "C:\path\to\dkg-shop-theme"

Assumptions:
- Theme structure is like:
    theme/
      front-page.php
      functions.php
      assets/css/front-page.css
      assets/js/front-page.js
- WooCommerce category slugs exist for the configured homepage rows
- Your JS carousel already targets:
    .auto-loop
    .product-track
    .product-card
"""

from __future__ import annotations

import argparse
import re
import shutil
from datetime import datetime
from pathlib import Path


FRONT_PAGE_TEMPLATE = """<?php
/**
 * Front page template generated for dynamic WooCommerce homepage rows.
 */

get_header();

$home_collections = array(
    array(
        'slug'  => 'shirts',
        'class' => 'red',
        'label' => 'Shirts',
        'bg'    => get_template_directory_uri() . '/assets/images/bricks.png',
    ),
    array(
        'slug'  => 'posters',
        'class' => 'blue',
        'label' => 'Posters',
        'bg'    => get_template_directory_uri() . '/assets/images/collection-bg-2.jpg',
    ),
    array(
        'slug'  => 'stickers',
        'class' => 'green',
        'label' => 'Stickers',
        'bg'    => get_template_directory_uri() . '/assets/images/collection-bg-3.jpg',
    ),
    array(
        'slug'  => 'hats',
        'class' => 'yellow',
        'label' => 'Hats',
        'bg'    => get_template_directory_uri() . '/assets/images/collection-bg-4.jpg',
    ),
);
?>

<div class="page-overlay">
  <main class="collections-section">
    <div class="collections-stack">

      <?php foreach ($home_collections as $collection) : ?>
        <?php
        $term = get_term_by('slug', $collection['slug'], 'product_cat');

        if (!$term || is_wp_error($term)) {
            continue;
        }

        $term_link = get_term_link($term);
        if (is_wp_error($term_link)) {
            continue;
        }

        $products = new WP_Query(array(
            'post_type'      => 'product',
            'posts_per_page' => 8,
            'post_status'    => 'publish',
            'tax_query'      => array(
                array(
                    'taxonomy' => 'product_cat',
                    'field'    => 'term_id',
                    'terms'    => $term->term_id,
                ),
            ),
            'orderby'        => 'menu_order title',
            'order'          => 'ASC',
        ));
        ?>

        <a class="collection-link" href="<?php echo esc_url($term_link); ?>" aria-label="<?php echo esc_attr($collection['label']); ?>">
          <section class="collection-box <?php echo esc_attr($collection['class']); ?>">
            <div class="collection-bg">
              <img src="<?php echo esc_url($collection['bg']); ?>" alt="">
            </div>

            <div class="collection-content">
              <div class="collection-label"><?php echo esc_html($collection['label']); ?></div>

              <div class="carousel-shell auto-loop">
                <div class="product-viewport">
                  <div class="product-track">

                    <?php if ($products->have_posts()) : ?>
                      <?php while ($products->have_posts()) : $products->the_post(); ?>
                        <?php
                        global $product;

                        if (!$product instanceof WC_Product) {
                            continue;
                        }

                        $image_url = get_the_post_thumbnail_url(get_the_ID(), 'medium');
                        if (!$image_url) {
                            $image_url = wc_placeholder_img_src('medium');
                        }

                        if ($product->managing_stock() && !is_null($product->get_stock_quantity())) {
                            $stock_text = 'Stock: ' . $product->get_stock_quantity();
                        } else {
                            $stock_text = $product->is_in_stock() ? 'Available' : 'Out of stock';
                        }
                        ?>
                        <a class="product-card" href="<?php the_permalink(); ?>" aria-label="<?php the_title_attribute(); ?>">
                          <div class="product-titlebar">
                            <div class="product-title"><?php the_title(); ?></div>
                          </div>
                          <div class="product-meta">
                            <img class="product-image" src="<?php echo esc_url($image_url); ?>" alt="<?php the_title_attribute(); ?>">
                            <div class="product-stock"><?php echo esc_html($stock_text); ?></div>
                          </div>
                        </a>
                      <?php endwhile; ?>
                      <?php wp_reset_postdata(); ?>
                    <?php else : ?>
                      <div class="product-card product-card--empty">
                        <div class="product-titlebar">
                          <div class="product-title">No products yet</div>
                        </div>
                        <div class="product-meta">
                          <div class="product-stock">Add products to <?php echo esc_html($collection['label']); ?></div>
                        </div>
                      </div>
                    <?php endif; ?>

                  </div>
                </div>
              </div>
            </div>
          </section>
        </a>

      <?php endforeach; ?>

    </div>
  </main>
</div>

<?php get_footer(); ?>
"""

ENQUEUE_SNIPPET = """

if (!function_exists('dkg_shop_enqueue_front_page_assets')) {
    function dkg_shop_enqueue_front_page_assets() {
        if (is_front_page()) {
            wp_enqueue_style(
                'dkg-shop-front-page',
                get_template_directory_uri() . '/assets/css/front-page.css',
                array(),
                file_exists(get_template_directory() . '/assets/css/front-page.css')
                    ? filemtime(get_template_directory() . '/assets/css/front-page.css')
                    : null
            );

            wp_enqueue_script(
                'dkg-shop-front-page',
                get_template_directory_uri() . '/assets/js/front-page.js',
                array(),
                file_exists(get_template_directory() . '/assets/js/front-page.js')
                    ? filemtime(get_template_directory() . '/assets/js/front-page.js')
                    : null,
                true
            );
        }
    }
    add_action('wp_enqueue_scripts', 'dkg_shop_enqueue_front_page_assets');
}
""".lstrip()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def backup_file(path: Path) -> Path | None:
    if not path.exists():
        return None
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = path.with_suffix(path.suffix + f".bak-{stamp}")
    shutil.copy2(path, backup)
    return backup


def ensure_enqueue(functions_php: Path) -> bool:
    existing = read_text(functions_php) if functions_php.exists() else "<?php\n"
    if "dkg_shop_enqueue_front_page_assets" in existing:
        return False

    new_content = existing.rstrip() + "\n\n" + ENQUEUE_SNIPPET
    write_text(functions_php, new_content)
    return True


def patch_css(css: str) -> str:
    original = css

    # Remove pointer-events none from product cards.
    css = re.sub(
        r"(?ms)(\.product-card\s*\{.*?)(\s*pointer-events\s*:\s*none;\s*)(.*?\})",
        r"\1\3",
        css,
    )

    # Ensure product cards can be links.
    if ".product-card {" in css:
        css = re.sub(
            r"(\.product-card\s*\{)",
            r"\\1\n      text-decoration: none;\n      color: inherit;",
            css,
            count=1,
        )

    # Ensure hover state exists.
    if ".product-card:hover" not in css:
        css += """

.product-card:hover,
.product-card:focus {
  transform: translateY(-2px);
  border-color: rgba(255,255,255,0.22);
}

.product-card--empty {
  justify-content: center;
}

.product-card--empty .product-meta {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}
"""

    # If the previous substitution failed because the block doesn't exist,
    # append a safe override block.
    if original == css:
        css += """

.product-card {
  text-decoration: none;
  color: inherit;
  pointer-events: auto;
}

.product-card:hover,
.product-card:focus {
  transform: translateY(-2px);
  border-color: rgba(255,255,255,0.22);
}

.product-card--empty {
  justify-content: center;
}

.product-card--empty .product-meta {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}
"""
    return css


def main() -> None:
    parser = argparse.ArgumentParser(description="Patch a local WP theme to use dynamic WooCommerce homepage rows.")
    parser.add_argument("theme_dir", help="Path to the theme directory")
    args = parser.parse_args()

    theme_dir = Path(args.theme_dir).expanduser().resolve()
    if not theme_dir.exists():
        raise FileNotFoundError(f"Theme directory not found: {theme_dir}")

    front_page = theme_dir / "front-page.php"
    functions_php = theme_dir / "functions.php"
    css_file = theme_dir / "assets" / "css" / "front-page.css"

    backups = []

    backup = backup_file(front_page)
    if backup:
        backups.append(backup)

    backup = backup_file(css_file)
    if backup:
        backups.append(backup)

    write_text(front_page, FRONT_PAGE_TEMPLATE)

    if css_file.exists():
        css = read_text(css_file)
        write_text(css_file, patch_css(css))
        css_status = f"patched {css_file}"
    else:
        css_status = f"missing {css_file} (front-page.php updated, but you need a front-page.css file for styling)"

    enqueue_added = ensure_enqueue(functions_php)

    print("Done.")
    print(f"Theme dir: {theme_dir}")
    print(f"Updated:   {front_page}")
    print(f"CSS:       {css_status}")
    print(f"Functions: {'enqueue added' if enqueue_added else 'enqueue already present'}")

    if backups:
        print("Backups:")
        for item in backups:
            print(f"  - {item}")
    else:
        print("No existing files needed backups.")


if __name__ == "__main__":
    main()

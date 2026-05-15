<?php
defined('ABSPATH') || exit;

get_header();

$featured_collection = isset($_GET['featured_collection'])
    ? sanitize_title(wp_unslash($_GET['featured_collection']))
    : '';

$collection_backgrounds = array(
    'shirts'   => 'col1.png',
    'posters'  => 'col1.png',
    'stickers' => 'col1.png',
    'hats'     => 'col1.png',
);

$bg_file = 'col1.png';

if ($featured_collection && isset($collection_backgrounds[$featured_collection])) {
    $bg_file = $collection_backgrounds[$featured_collection];
}

$bg_path = get_template_directory() . '/assets/images/' . $bg_file;
$shop_bg = '';

if (file_exists($bg_path)) {
    $shop_bg = get_template_directory_uri() . '/assets/images/' . $bg_file;
}

/*
 * Fully inline background system.
 * This avoids broken/old CSS rules in woocommerce.css hiding the background.
 */
if ($shop_bg) {
    echo '<style id="dkg-inline-shop-bg-force">
        html, body {
            background: #000 !important;
            background-image: none !important;
        }

        .dkg-inline-shop-bg {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            z-index: 0 !important;
            background-image: url(' . esc_url($shop_bg) . ') !important;
            background-size: cover !important;
            background-position: center center !important;
            background-repeat: no-repeat !important;
            opacity: 0.85 !important;
            pointer-events: none !important;
        }

        .dkg-inline-shop-bg-overlay {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            z-index: 1 !important;
            background: rgba(0,0,0,0.38) !important;
            pointer-events: none !important;
        }

        .site-header,
        .dkg-shop-main,
        .site-footer {
            position: relative !important;
            z-index: 10 !important;
        }

        .dkg-real-shop-bg,
        .dkg-real-shop-bg-overlay,
        .dkg-shop-main::before,
        .dkg-shop-main::after {
            display: none !important;
            content: none !important;
        }

        .dkg-shop-main {
            width: 100% !important;
            max-width: 100% !important;
            padding: 70px 20px 110px !important;
            color: #fff !important;
        }

        .dkg-shop-plate,
        .dkg-shop-section {
            width: min(1180px, calc(100vw - 80px)) !important;
            margin: 0 auto 70px !important;
            padding: 34px !important;
            border: 2px solid rgba(255,255,255,0.22) !important;
            border-radius: 34px !important;
            background: rgba(20,20,20,0.72) !important;
            box-shadow: 0 24px 80px rgba(0,0,0,0.45) !important;
        }

        body.single-product .dkg-shop-plate {
            background-image: url(' . esc_url(get_template_directory_uri() . '/assets/images/plate-bg.png') . ') !important;
            background-color: #000 !important;
            background-size: cover !important;
            background-position: center center !important;
            background-repeat: no-repeat !important;
            opacity: 1 !important;
            overflow: hidden !important;
            backdrop-filter: none !important;
            -webkit-backdrop-filter: none !important;
        }

        body.single-product .dkg-shop-plate > * {
            position: relative !important;
            z-index: 2 !important;
        }
    </style>';

    echo '<div class="dkg-inline-shop-bg"></div>';
    echo '<div class="dkg-inline-shop-bg-overlay"></div>';
}

echo '<main class="dkg-shop-main">';

if (is_shop() && $featured_collection) {
    $term = get_term_by('slug', $featured_collection, 'product_cat');

    if ($term && !is_wp_error($term)) {
        echo '<section class="dkg-shop-plate dkg-featured-collection">';
        echo '<h1>' . esc_html($term->name) . '</h1>';
        echo do_shortcode('[products category="' . esc_attr($term->slug) . '" columns="4" limit="-1"]');
        echo '</section>';

        $featured_ids = wc_get_products(array(
            'status'   => 'publish',
            'limit'    => -1,
            'category' => array($term->slug),
            'return'   => 'ids',
        ));

        echo '<section class="dkg-shop-plate dkg-more-products">';
        echo '<h2>More Products</h2>';

        if (!empty($featured_ids)) {
            echo do_shortcode('[products columns="4" limit="-1" exclude="' . esc_attr(implode(',', $featured_ids)) . '"]');
        } else {
            echo do_shortcode('[products columns="4" limit="-1"]');
        }

        echo '</section>';
    } else {
        echo '<section class="dkg-shop-plate">';
        woocommerce_content();
        echo '</section>';
    }
} else {
    echo '<section class="dkg-shop-plate">';
    woocommerce_content();
    echo '</section>';
}

echo '</main>';

get_footer();

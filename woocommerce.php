<?php
defined('ABSPATH') || exit;

get_header();

$featured_collection = isset($_GET['featured_collection'])
    ? sanitize_title(wp_unslash($_GET['featured_collection']))
    : '';



$collection_backgrounds = array(
    'shirts'   => get_template_directory_uri() . '/assets/images/col1.png',
    'posters'  => get_template_directory_uri() . '/assets/images/collection-bg-2.jpg',
    'stickers' => get_template_directory_uri() . '/assets/images/collection-bg-3.jpg',
    'hats'     => get_template_directory_uri() . '/assets/images/collection-bg-4.jpg',
);

$shop_bg = '';

if ($featured_collection && isset($collection_backgrounds[$featured_collection])) {
    $shop_bg = $collection_backgrounds[$featured_collection];
}

if ($shop_bg) {
    echo '<style id="dkg-dynamic-shop-bg">';
    echo 'body { --dkg-shop-bg: url("' . esc_url($shop_bg) . '"); }';
    echo '</style>';
}

echo '<main class="dkg-shop-main">';

if (is_shop() && $featured_collection) {
    $term = get_term_by('slug', $featured_collection, 'product_cat');

    if ($term && !is_wp_error($term)) {
        echo '<section class="dkg-shop-section dkg-featured-collection">';
        echo '<h1>' . esc_html($term->name) . '</h1>';
        echo do_shortcode('[products category="' . esc_attr($term->slug) . '" columns="4" limit="-1"]');
        echo '</section>';

        $featured_ids = wc_get_products([
            'status'   => 'publish',
            'limit'    => -1,
            'category' => [$term->slug],
            'return'   => 'ids',
        ]);

        echo '<section class="dkg-shop-section dkg-more-products">';
        echo '<h2>More Products</h2>';

        if (!empty($featured_ids)) {
            echo do_shortcode('[products columns="4" limit="-1" exclude="' . esc_attr(implode(',', $featured_ids)) . '"]');
        } else {
            echo do_shortcode('[products columns="4" limit="-1"]');
        }

        echo '</section>';
    } else {
        woocommerce_content();
    }
} else {
    woocommerce_content();
}

echo '</main>';

get_footer();

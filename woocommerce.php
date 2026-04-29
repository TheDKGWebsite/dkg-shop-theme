<?php
defined('ABSPATH') || exit;

get_header();

$featured_collection = isset($_GET['featured_collection'])
    ? sanitize_title(wp_unslash($_GET['featured_collection']))
    : '';

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

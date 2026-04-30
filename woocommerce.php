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

$shop_bg_url = '';

if ($featured_collection && isset($collection_backgrounds[$featured_collection])) {
    $bg_file = $collection_backgrounds[$featured_collection];
    $bg_path = get_template_directory() . '/assets/images/' . $bg_file;

    if (file_exists($bg_path)) {
        $shop_bg_url = get_template_directory_uri() . '/assets/images/' . $bg_file;
    }
}

if ($shop_bg_url) {
    ?>
    <!-- DKG DEBUG: dynamic shop background loaded -->
    <style id="dkg-force-shop-bg">
        body {
            background-image:
                linear-gradient(rgba(0,0,0,0.55), rgba(0,0,0,0.55)),
                url("<?php echo esc_url($shop_bg_url); ?>") !important;
            background-size: cover !important;
            background-position: center center !important;
            background-repeat: no-repeat !important;
            background-attachment: fixed !important;
            background-color: #000 !important;
        }
    </style>
    <?php
}

echo '<main class="dkg-shop-main">';

if (is_shop() && $featured_collection) {
    $term = get_term_by('slug', $featured_collection, 'product_cat');

    if ($term && !is_wp_error($term)) {
        echo '<section class="dkg-shop-section dkg-featured-collection">';
        echo '<h1>' . esc_html($term->name) . '</h1>';
        echo do_shortcode('[products category="' . esc_attr($term->slug) . '" columns="4" limit="-1"]');
        echo '</section>';

        $featured_ids = wc_get_products(array(
            'status'   => 'publish',
            'limit'    => -1,
            'category' => array($term->slug),
            'return'   => 'ids',
        ));

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
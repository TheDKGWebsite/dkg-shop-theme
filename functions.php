<?php
/**
 * DKG One Product theme bootstrap.
 */

defined('ABSPATH') || exit;

require get_template_directory() . '/inc/setup.php';
require get_template_directory() . '/inc/enqueue.php';
require get_template_directory() . '/inc/woocommerce.php';

/**
 * Return the product ID used on the homepage.
 *
 * Priority:
 * 1. Explicit Product ID set in Appearance > Customize.
 * 2. Newest product marked Featured in WooCommerce.
 * 3. Newest published WooCommerce product.
 */
function dkg_get_home_product_id() {
    if (!class_exists('WooCommerce')) {
        return 0;
    }

    $override_id = absint(get_theme_mod('dkg_home_product_id', 0));
    if ($override_id) {
        $override = wc_get_product($override_id);
        if ($override && 'publish' === get_post_status($override_id)) {
            return $override_id;
        }
    }

    $featured = new WP_Query(array(
        'post_type'              => 'product',
        'post_status'            => 'publish',
        'posts_per_page'         => 1,
        'orderby'                => 'date',
        'order'                  => 'DESC',
        'fields'                 => 'ids',
        'no_found_rows'          => true,
        'update_post_meta_cache' => false,
        'update_post_term_cache' => false,
        'tax_query'              => array(
            array(
                'taxonomy' => 'product_visibility',
                'field'    => 'name',
                'terms'    => array('featured'),
            ),
        ),
    ));

    if (!empty($featured->posts[0])) {
        return absint($featured->posts[0]);
    }

    $latest = get_posts(array(
        'post_type'      => 'product',
        'post_status'    => 'publish',
        'posts_per_page' => 1,
        'orderby'        => 'date',
        'order'          => 'DESC',
        'fields'         => 'ids',
    ));

    return !empty($latest[0]) ? absint($latest[0]) : 0;
}

/**
 * Small Customizer control for pinning a homepage product.
 */
function dkg_customize_register($wp_customize) {
    $wp_customize->add_section('dkg_one_product_home', array(
        'title'       => __('One Product Homepage', 'dkg-shop-theme'),
        'priority'    => 35,
        'description' => __('Optional: enter a WooCommerce Product ID to pin it to the homepage. Leave blank to use the newest Featured product.', 'dkg-shop-theme'),
    ));

    $wp_customize->add_setting('dkg_home_product_id', array(
        'default'           => 0,
        'sanitize_callback' => 'absint',
        'transport'         => 'refresh',
    ));

    $wp_customize->add_control('dkg_home_product_id', array(
        'section'     => 'dkg_one_product_home',
        'label'       => __('Homepage Product ID', 'dkg-shop-theme'),
        'description' => __('Find the ID in WooCommerce > Products. Use 0 or leave blank for automatic Featured-product selection.', 'dkg-shop-theme'),
        'type'        => 'number',
        'input_attrs' => array('min' => 0, 'step' => 1),
    ));
}
add_action('customize_register', 'dkg_customize_register');

/**
 * Keep the cart count in the header accurate when WooCommerce refreshes fragments.
 */
function dkg_cart_count_fragment($fragments) {
    if (!function_exists('WC') || !WC()->cart) {
        return $fragments;
    }

    ob_start();
    ?>
    <span class="dkg-cart-count"><?php echo esc_html(WC()->cart->get_cart_contents_count()); ?></span>
    <?php
    $fragments['.dkg-cart-count'] = ob_get_clean();

    return $fragments;
}
add_filter('woocommerce_add_to_cart_fragments', 'dkg_cart_count_fragment');

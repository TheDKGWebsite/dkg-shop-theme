<?php

function dkg_shop_woocommerce_setup() {
    add_theme_support('woocommerce', [
        'thumbnail_image_width' => 400,
        'single_image_width'    => 800,
        'product_grid'          => [
            'default_rows'    => 4,
            'min_rows'        => 1,
            'default_columns' => 4,
            'min_columns'     => 1,
            'max_columns'     => 4,
        ],
    ]);
}
add_action('after_setup_theme', 'dkg_shop_woocommerce_setup');

function dkg_shop_loop_columns() {
    return 4;
}
add_filter('loop_shop_columns', 'dkg_shop_loop_columns');
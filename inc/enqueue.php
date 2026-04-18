<?php

function dkg_shop_enqueue_assets() {
    $theme_version = wp_get_theme()->get('Version');

    wp_enqueue_style(
        'dkg-shop-style',
        get_stylesheet_uri(),
        [],
        $theme_version
    );

    wp_enqueue_style(
        'dkg-shop-main',
        get_template_directory_uri() . '/assets/css/main.css',
        ['dkg-shop-style'],
        $theme_version
    );

    wp_enqueue_style(
        'dkg-shop-woocommerce',
        get_template_directory_uri() . '/assets/css/woocommerce.css',
        ['dkg-shop-main'],
        $theme_version
    );

    wp_enqueue_script(
        'dkg-shop-main',
        get_template_directory_uri() . '/assets/js/main.js',
        [],
        $theme_version,
        true
    );
}
add_action('wp_enqueue_scripts', 'dkg_shop_enqueue_assets');
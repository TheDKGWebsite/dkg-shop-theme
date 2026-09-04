<?php

defined('ABSPATH') || exit;

function dkg_enqueue_assets() {
    $style_path = get_stylesheet_directory() . '/style.css';
    $site_path  = get_template_directory() . '/assets/css/site.css';
    $home_path  = get_template_directory() . '/assets/css/one-product-home.css';
    $js_path    = get_template_directory() . '/assets/js/one-product-home.js';

    wp_enqueue_style(
        'dkg-style',
        get_stylesheet_uri(),
        array(),
        file_exists($style_path) ? filemtime($style_path) : wp_get_theme()->get('Version')
    );

    wp_enqueue_style(
        'dkg-site',
        get_template_directory_uri() . '/assets/css/site.css',
        array('dkg-style'),
        file_exists($site_path) ? filemtime($site_path) : wp_get_theme()->get('Version')
    );

    if (is_front_page()) {
        wp_enqueue_style(
            'dkg-one-product-home',
            get_template_directory_uri() . '/assets/css/one-product-home.css',
            array('dkg-site'),
            file_exists($home_path) ? filemtime($home_path) : wp_get_theme()->get('Version')
        );

        wp_enqueue_script(
            'dkg-one-product-home',
            get_template_directory_uri() . '/assets/js/one-product-home.js',
            array(),
            file_exists($js_path) ? filemtime($js_path) : wp_get_theme()->get('Version'),
            true
        );

        // Variable-product add-to-cart forms need WooCommerce's variation script
        // because the homepage is not technically a single-product route.
        if (class_exists('WooCommerce')) {
            wp_enqueue_script('wc-add-to-cart-variation');
        }
    }
}
add_action('wp_enqueue_scripts', 'dkg_enqueue_assets', 20);

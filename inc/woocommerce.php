<?php

defined('ABSPATH') || exit;

/**
 * Remove the default WooCommerce sidebar for this stripped-down theme.
 */
function dkg_remove_woocommerce_sidebar() {
    remove_action('woocommerce_sidebar', 'woocommerce_get_sidebar', 10);
}
add_action('wp', 'dkg_remove_woocommerce_sidebar');

/**
 * Use our simple content wrapper on standard WooCommerce routes.
 */
function dkg_woocommerce_wrapper_start() {
    echo '<main class="dkg-standard-main"><div class="dkg-standard-shell">';
}

function dkg_woocommerce_wrapper_end() {
    echo '</div></main>';
}

function dkg_replace_woocommerce_wrappers() {
    remove_action('woocommerce_before_main_content', 'woocommerce_output_content_wrapper', 10);
    remove_action('woocommerce_after_main_content', 'woocommerce_output_content_wrapper_end', 10);
    add_action('woocommerce_before_main_content', 'dkg_woocommerce_wrapper_start', 10);
    add_action('woocommerce_after_main_content', 'dkg_woocommerce_wrapper_end', 10);
}
add_action('after_setup_theme', 'dkg_replace_woocommerce_wrappers', 20);

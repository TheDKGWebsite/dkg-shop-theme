<?php

require get_template_directory() . '/inc/setup.php';
require get_template_directory() . '/inc/enqueue.php';
require get_template_directory() . '/inc/woocommerce.php';



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

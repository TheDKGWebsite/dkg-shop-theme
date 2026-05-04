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

// === DKG CART INLINE BACKGROUND START ===

/*
 * Force a custom cart-page background after all normal CSS loads.
 * Image expected at:
 * assets/images/cart-bg.png
 */
function dkg_force_cart_background_inline_style() {
    if (!function_exists('is_cart') || !is_cart()) {
        return;
    }

    $cart_bg_url = get_template_directory_uri() . '/assets/images/cart-bg.png';
    ?>
    <style id="dkg-cart-bg-force">
      html,
      body {
        background-color: #000 !important;
        background-image: url('<?php echo esc_url($cart_bg_url); ?>') !important;
        background-size: cover !important;
        background-position: center center !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
      }

      body.woocommerce-cart,
      body.page,
      body {
        background-color: #000 !important;
        background-image: url('<?php echo esc_url($cart_bg_url); ?>') !important;
        background-size: cover !important;
        background-position: center center !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
      }

      body::before {
        content: "" !important;
        position: fixed !important;
        inset: 0 !important;
        background: rgba(0, 0, 0, 0.35) !important;
        pointer-events: none !important;
        z-index: 0 !important;
      }

      .site-header,
      .site-main,
      .site-footer {
        position: relative !important;
        z-index: 2 !important;
      }

      .site-main {
        min-height: calc(100vh - 140px) !important;
        color: #fff !important;
      }

      .site-main .container {
        background: rgba(20, 20, 20, 0.72) !important;
        border: 2px solid rgba(255, 255, 255, 0.22) !important;
        border-radius: 34px !important;
        box-shadow: 0 24px 80px rgba(0, 0, 0, 0.45) !important;
        padding: 34px !important;
        margin-top: 70px !important;
        margin-bottom: 70px !important;
        backdrop-filter: blur(2px) !important;
      }

      .woocommerce,
      .woocommerce table.shop_table,
      .woocommerce .cart_totals,
      .woocommerce .woocommerce-cart-form {
        color: #fff !important;
      }

      .woocommerce table.shop_table,
      .woocommerce .cart_totals,
      .woocommerce .woocommerce-cart-form {
        background: rgba(0, 0, 0, 0.45) !important;
        border-radius: 18px !important;
      }

      .woocommerce table.shop_table th,
      .woocommerce table.shop_table td {
        color: #fff !important;
        border-color: rgba(255, 255, 255, 0.18) !important;
      }

      .woocommerce a {
        color: #fff !important;
      }

      .woocommerce .button,
      .woocommerce button.button,
      .woocommerce input.button,
      .woocommerce a.button {
        background: #fff !important;
        color: #000 !important;
        border-radius: 999px !important;
        font-weight: 700 !important;
        border: none !important;
      }

      .woocommerce .button:hover,
      .woocommerce button.button:hover,
      .woocommerce input.button:hover,
      .woocommerce a.button:hover {
        background: #dcdcdc !important;
        color: #000 !important;
      }

      @media (max-width: 700px) {
        .site-main .container {
          margin-top: 30px !important;
          margin-bottom: 40px !important;
          padding: 20px !important;
          border-radius: 24px !important;
        }
      }
    </style>
    <?php
}
add_action('wp_head', 'dkg_force_cart_background_inline_style', 999);

// === DKG CART INLINE BACKGROUND END ===

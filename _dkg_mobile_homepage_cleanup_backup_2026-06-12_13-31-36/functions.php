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

// === DKG CHECKOUT BLACK BACKGROUND START ===

/*
 * Force the checkout page to use a solid black background.
 * This overrides the globally loaded bricks.png background.
 */
function dkg_force_checkout_white_background() {
    if (!function_exists('is_checkout') || !is_checkout()) {
        return;
    }

    if (function_exists('is_order_received_page') && is_order_received_page()) {
        return;
    }
    ?>
    <style id="dkg-checkout-white-bg-force">
      html,
      body,
      body.woocommerce-checkout {
        background: #fff !important;
        background-color: #fff !important;
        background-image: none !important;
        color: #000 !important;
      }

      body.woocommerce-checkout::before,
      body.woocommerce-checkout::after {
        content: none !important;
        display: none !important;
        background: none !important;
      }

      body.woocommerce-checkout .site-main {
        min-height: calc(100vh - 140px) !important;
        color: #000 !important;
        background: #fff !important;
      }

      body.woocommerce-checkout .site-main .container {
        background: #fff !important;
        border: 1px solid rgba(0, 0, 0, 0.16) !important;
        border-radius: 24px !important;
        box-shadow: none !important;
        padding: 34px !important;
        margin-top: 50px !important;
        margin-bottom: 70px !important;
      }

      body.woocommerce-checkout .woocommerce,
      body.woocommerce-checkout .woocommerce form,
      body.woocommerce-checkout .woocommerce table,
      body.woocommerce-checkout .woocommerce label,
      body.woocommerce-checkout .woocommerce h1,
      body.woocommerce-checkout .woocommerce h2,
      body.woocommerce-checkout .woocommerce h3,
      body.woocommerce-checkout .woocommerce p,
      body.woocommerce-checkout .woocommerce span,
      body.woocommerce-checkout .woocommerce td,
      body.woocommerce-checkout .woocommerce th {
        color: #000 !important;
      }

      body.woocommerce-checkout input,
      body.woocommerce-checkout textarea,
      body.woocommerce-checkout select {
        background: #fff !important;
        color: #000 !important;
        border: 1px solid rgba(0,0,0,0.35) !important;
      }

      body.woocommerce-checkout .button,
      body.woocommerce-checkout button.button,
      body.woocommerce-checkout input.button,
      body.woocommerce-checkout a.button,
      body.woocommerce-checkout #place_order {
        background: #000 !important;
        color: #fff !important;
        border-radius: 999px !important;
        font-weight: 700 !important;
        border: none !important;
      }

      body.woocommerce-checkout .button:hover,
      body.woocommerce-checkout button.button:hover,
      body.woocommerce-checkout input.button:hover,
      body.woocommerce-checkout a.button:hover,
      body.woocommerce-checkout #place_order:hover {
        background: #333 !important;
        color: #fff !important;
      }
    </style>
    <?php
}
add_action('wp_head', 'dkg_force_checkout_white_background', 999);

// === DKG CHECKOUT BLACK BACKGROUND END ===

// === DKG MOBILE SHOP REDIRECT START ===

/*
 * Redirect mobile visitors from the homepage or normal shop page
 * to the custom mobile shop page:
 *
 * /             -> /mobile-shop/
 * /shop/        -> /mobile-shop/
 *
 * Desktop visitors stay on the normal pages.
 */
function dkg_redirect_mobile_shop_visitors() {
    if (is_admin()) {
        return;
    }

    if (wp_doing_ajax()) {
        return;
    }

    if (!function_exists('wp_is_mobile') || !wp_is_mobile()) {
        return;
    }

    /*
     * Do not redirect WooCommerce account/cart/checkout pages.
     * This keeps buying flow safe.
     */
    if (
        (function_exists('is_cart') && is_cart()) ||
        (function_exists('is_checkout') && is_checkout()) ||
        (function_exists('is_account_page') && is_account_page())
    ) {
        return;
    }

    $request_path = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
    $request_path = trailingslashit($request_path);

    $mobile_shop_path = trailingslashit(parse_url(home_url('/mobile-shop/'), PHP_URL_PATH));

    /*
     * Prevent redirect loop.
     */
    if ($request_path === $mobile_shop_path) {
        return;
    }

    $is_homepage = is_front_page() || $request_path === '/';
    $is_shop_page = function_exists('is_shop') && is_shop();

    if ($is_homepage || $is_shop_page || $request_path === '/shop/') {
        wp_safe_redirect(home_url('/mobile-shop/'), 302);
        exit;
    }
}
// DKG disabled by mobile_main_homepage_overhaul_step1.py: add_action('template_redirect', 'dkg_redirect_mobile_shop_visitors', 1);

// === DKG MOBILE SHOP REDIRECT END ===

// === DKG CART CHECKOUT BUTTON FIRST START ===

function dkg_cart_checkout_button_first() {
    if (!function_exists('is_cart') || !is_cart()) {
        return;
    }
    ?>
    <script>
      (function () {
        function dkgDirectChildUnder(root, el) {
          if (!root || !el || el === root) {
            return null;
          }

          let current = el;

          while (current && current.parentElement && current.parentElement !== root) {
            current = current.parentElement;
          }

          return current && current.parentElement === root ? current : null;
        }

        function dkgLooksLikeExpressPayment(el) {
          if (!el || !el.textContent) {
            return false;
          }

          const text = (el.textContent || '').replace(/\s+/g, ' ').trim().toLowerCase();
          const cls = String(el.className || '').toLowerCase();
          const id = String(el.id || '').toLowerCase();
          const html = (cls + ' ' + id + ' ' + text);

          if (text === 'or') {
            return false;
          }

          if (el.matches && el.matches('a.checkout-button, .checkout-button')) {
            return false;
          }

          return (
            html.includes('amazon') ||
            html.includes('apple pay') ||
            html.includes('google pay') ||
            html.includes('g pay') ||
            html.includes('pay with link') ||
            html.includes(' link') ||
            html.includes('wcpay') ||
            html.includes('stripe') ||
            html.includes('express') ||
            html.includes('payment-request') ||
            html.includes('payment_request') ||
            html.includes('wc-stripe') ||
            html.includes('paypal')
          );
        }

        function dkgFindOrSeparator(root) {
          const candidates = root.querySelectorAll('p, div, span');

          for (const el of candidates) {
            const text = (el.textContent || '').replace(/\s+/g, ' ').trim().toLowerCase();

            if (text === 'or') {
              return el;
            }
          }

          return null;
        }

        function dkgReorderCartPayments() {
          const checkoutButton = document.querySelector(
            '.woocommerce-cart a.checkout-button, .woocommerce-cart .checkout-button, a.checkout-button, .checkout-button'
          );

          if (!checkoutButton) {
            return false;
          }

          const checkoutGroup =
            checkoutButton.closest('.wc-proceed-to-checkout') ||
            checkoutButton.parentElement;

          if (!checkoutGroup) {
            return false;
          }

          const root =
            checkoutGroup.closest('.cart_totals') ||
            checkoutGroup.closest('.cart-collaterals') ||
            checkoutGroup.closest('.woocommerce') ||
            document.querySelector('.woocommerce-cart .woocommerce') ||
            document.querySelector('.woocommerce') ||
            document.body;

          if (!root) {
            return false;
          }

          let wrapper = root.querySelector(':scope > .dkg-cart-payment-order');

          if (!wrapper) {
            wrapper = document.createElement('div');
            wrapper.className = 'dkg-cart-payment-order';

            const firstRelevant =
              dkgDirectChildUnder(root, checkoutGroup) ||
              root.firstElementChild;

            if (firstRelevant) {
              root.insertBefore(wrapper, firstRelevant);
            } else {
              root.appendChild(wrapper);
            }
          }

          const expressBlocks = [];
          const possibleExpress = root.querySelectorAll('div, section, p');

          possibleExpress.forEach(function (el) {
            if (el === wrapper || wrapper.contains(el) || el.contains(wrapper)) {
              return;
            }

            if (checkoutGroup.contains(el) || el.contains(checkoutGroup)) {
              return;
            }

            if (!dkgLooksLikeExpressPayment(el)) {
              return;
            }

            const block = dkgDirectChildUnder(root, el);

            if (
              block &&
              block !== wrapper &&
              block !== checkoutGroup &&
              !expressBlocks.includes(block)
            ) {
              expressBlocks.push(block);
            }
          });

          const existingOr = dkgFindOrSeparator(root);
          let orBlock = existingOr ? dkgDirectChildUnder(root, existingOr) : null;

          if (!orBlock || orBlock === checkoutGroup || orBlock === wrapper) {
            orBlock = wrapper.querySelector('.dkg-cart-or-separator');

            if (!orBlock) {
              orBlock = document.createElement('div');
              orBlock.className = 'dkg-cart-or-separator';
              orBlock.textContent = 'OR';
            }
          }

          wrapper.appendChild(checkoutGroup);
          wrapper.appendChild(orBlock);

          expressBlocks.forEach(function (block) {
            wrapper.appendChild(block);
          });

          checkoutGroup.classList.add('dkg-normal-checkout-first');

          return true;
        }

        function dkgRunRepeatedly() {
          dkgReorderCartPayments();

          setTimeout(dkgReorderCartPayments, 300);
          setTimeout(dkgReorderCartPayments, 800);
          setTimeout(dkgReorderCartPayments, 1600);
          setTimeout(dkgReorderCartPayments, 3000);
          setTimeout(dkgReorderCartPayments, 5000);
        }

        if (document.readyState === 'loading') {
          document.addEventListener('DOMContentLoaded', dkgRunRepeatedly);
        } else {
          dkgRunRepeatedly();
        }

        let dkgCartPaymentTimer = null;

        const observer = new MutationObserver(function () {
          clearTimeout(dkgCartPaymentTimer);
          dkgCartPaymentTimer = setTimeout(dkgReorderCartPayments, 120);
        });

        observer.observe(document.body, {
          childList: true,
          subtree: true
        });
      })();
    </script>
    <?php
}
add_action('wp_footer', 'dkg_cart_checkout_button_first', 999);

// === DKG CART CHECKOUT BUTTON FIRST END ===

// === DKG MOBILE MAIN HOMEPAGE COLLECTION PLATES ENQUEUE START ===

function dkg_enqueue_mobile_main_homepage_collection_plates() {
    if (is_admin()) {
        return;
    }

    $script_path = get_template_directory() . '/assets/js/dkg-mobile-main-homepage-plates.js';
    $script_uri  = get_template_directory_uri() . '/assets/js/dkg-mobile-main-homepage-plates.js';

    if (file_exists($script_path)) {
        wp_enqueue_script(
            'dkg-mobile-main-homepage-plates',
            $script_uri,
            array(),
            filemtime($script_path),
            true
        );
    }
}
add_action('wp_enqueue_scripts', 'dkg_enqueue_mobile_main_homepage_collection_plates', 30);

// === DKG MOBILE MAIN HOMEPAGE COLLECTION PLATES ENQUEUE END ===

<?php
/**
 * Custom mobile shop page.
 * Mobile-specific product grid layout.
 * Automatically used for /mobile-shop/
 */

defined('ABSPATH') || exit;

get_header();

$bg_file = 'col1.png';
$bg_path = get_template_directory() . '/assets/images/' . $bg_file;
$shop_bg = '';

if (file_exists($bg_path)) {
    $shop_bg = get_template_directory_uri() . '/assets/images/' . $bg_file;
}

if ($shop_bg) {
    echo '<style id="dkg-mobile-shop-layout-force">
        html,
        body {
            background: #000 !important;
            background-image: none !important;
        }

        body.page-mobile-shop,
        body.page-template-page-mobile-shop {
            background: #000 !important;
            color: #fff !important;
            overflow-x: hidden !important;
        }

        .dkg-mobile-shop-bg {
            position: fixed !important;
            inset: 0 !important;
            z-index: 0 !important;
            background-image: url(' . esc_url($shop_bg) . ') !important;
            background-size: cover !important;
            background-position: center center !important;
            background-repeat: no-repeat !important;
            opacity: 0.45 !important;
            pointer-events: none !important;
        }

        .dkg-mobile-shop-bg-overlay {
            position: fixed !important;
            inset: 0 !important;
            z-index: 1 !important;
            background: rgba(0,0,0,0.55) !important;
            pointer-events: none !important;
        }

        .site-header,
        .site-footer {
            position: relative !important;
            z-index: 10 !important;
        }

        .dkg-mobile-shop-main {
            position: relative !important;
            z-index: 5 !important;
            width: 100% !important;
            max-width: 100% !important;
            min-height: calc(100vh - 100px) !important;
            padding: 10px 10px 60px !important;
            margin: 0 !important;
            color: #fff !important;
        }

        .dkg-mobile-shop-title {
            display: none !important;
        }

        .dkg-mobile-products-wrap {
            width: 100% !important;
            max-width: 100% !important;
            margin: 0 !important;
            padding: 0 !important;
            background: transparent !important;
            border: 0 !important;
            box-shadow: none !important;
            border-radius: 0 !important;
        }

        .dkg-mobile-shop-main .woocommerce {
            width: 100% !important;
            max-width: 100% !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        .dkg-mobile-shop-main .woocommerce-notices-wrapper,
        .dkg-mobile-shop-main .woocommerce-result-count,
        .dkg-mobile-shop-main .woocommerce-ordering {
            display: none !important;
        }

        .dkg-mobile-shop-main ul.products {
            display: grid !important;
            grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
            gap: 10px !important;
            width: 100% !important;
            margin: 0 !important;
            padding: 0 !important;
            list-style: none !important;
        }

        .dkg-mobile-shop-main ul.products li.product {
            width: auto !important;
            float: none !important;
            clear: none !important;
            margin: 0 !important;
            padding: 8px !important;
            border-radius: 16px !important;
            background: rgba(0,0,0,0.62) !important;
            border: 1px solid rgba(255,255,255,0.14) !important;
            box-shadow: none !important;
            overflow: hidden !important;
            display: flex !important;
            flex-direction: column !important;
            min-height: 0 !important;
        }

        .dkg-mobile-shop-main ul.products li.product a {
            color: #fff !important;
            text-decoration: none !important;
        }

        .dkg-mobile-shop-main ul.products li.product a img {
            width: 100% !important;
            aspect-ratio: 1 / 1 !important;
            height: auto !important;
            object-fit: cover !important;
            display: block !important;
            border-radius: 12px !important;
            margin: 0 0 8px !important;
            background: rgba(255,255,255,0.08) !important;
        }

        .dkg-mobile-shop-main ul.products li.product .woocommerce-loop-product__title {
            color: #fff !important;
            font-size: 0.86rem !important;
            line-height: 1.15 !important;
            margin: 0 0 5px !important;
            padding: 0 !important;
            min-height: 2.1em !important;
            text-transform: none !important;
            letter-spacing: 0 !important;
        }

        .dkg-mobile-shop-main ul.products li.product .price {
            color: rgba(255,255,255,0.88) !important;
            font-size: 0.82rem !important;
            line-height: 1.2 !important;
            margin: 0 0 8px !important;
        }

        .dkg-mobile-shop-main ul.products li.product .button,
        .dkg-mobile-shop-main ul.products li.product a.button {
            width: 100% !important;
            margin: auto 0 0 !important;
            padding: 8px 8px !important;
            border-radius: 999px !important;
            background: #fff !important;
            color: #000 !important;
            font-size: 0.76rem !important;
            line-height: 1.1 !important;
            text-align: center !important;
            font-weight: 800 !important;
            border: none !important;
        }

        .dkg-mobile-shop-main ul.products li.product .button:hover,
        .dkg-mobile-shop-main ul.products li.product a.button:hover {
            background: #dcdcdc !important;
            color: #000 !important;
        }

        @media (max-width: 380px) {
            .dkg-mobile-shop-main {
                padding-left: 7px !important;
                padding-right: 7px !important;
            }

            .dkg-mobile-shop-main ul.products {
                gap: 7px !important;
            }

            .dkg-mobile-shop-main ul.products li.product {
                padding: 7px !important;
                border-radius: 14px !important;
            }

            .dkg-mobile-shop-main ul.products li.product .woocommerce-loop-product__title {
                font-size: 0.78rem !important;
            }

            .dkg-mobile-shop-main ul.products li.product .price {
                font-size: 0.76rem !important;
            }

            .dkg-mobile-shop-main ul.products li.product .button,
            .dkg-mobile-shop-main ul.products li.product a.button {
                font-size: 0.7rem !important;
                padding: 7px 5px !important;
            }
        }
    </style>';

    echo '<div class="dkg-mobile-shop-bg"></div>';
    echo '<div class="dkg-mobile-shop-bg-overlay"></div>';
}

echo '<main class="dkg-mobile-shop-main">';
echo '<div class="dkg-mobile-products-wrap">';
echo '<h1 class="dkg-mobile-shop-title">Shop</h1>';
echo do_shortcode('[products columns="2" limit="-1"]');
echo '</div>';
echo '</main>';

get_footer();

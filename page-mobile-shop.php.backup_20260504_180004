<?php
/**
 * Custom mobile shop page.
 * Currently mirrors the normal /shop/ layout.
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
    echo '<style id="dkg-mobile-shop-bg-force">
        html, body {
            background: #000 !important;
            background-image: none !important;
        }

        .dkg-inline-shop-bg {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            z-index: 0 !important;
            background-image: url(' . esc_url($shop_bg) . ') !important;
            background-size: cover !important;
            background-position: center center !important;
            background-repeat: no-repeat !important;
            opacity: 0.85 !important;
            pointer-events: none !important;
        }

        .dkg-inline-shop-bg-overlay {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            z-index: 1 !important;
            background: rgba(0,0,0,0.38) !important;
            pointer-events: none !important;
        }

        .site-header,
        .dkg-shop-main,
        .site-footer {
            position: relative !important;
            z-index: 10 !important;
        }

        .dkg-shop-main {
            width: 100% !important;
            max-width: 100% !important;
            padding: 70px 20px 110px !important;
            color: #fff !important;
        }

        .dkg-shop-plate {
            width: min(1180px, calc(100vw - 80px)) !important;
            margin: 0 auto 70px !important;
            padding: 34px !important;
            border: 2px solid rgba(255,255,255,0.22) !important;
            border-radius: 34px !important;
            background: rgba(20,20,20,0.72) !important;
            box-shadow: 0 24px 80px rgba(0,0,0,0.45) !important;
        }

        .dkg-shop-plate h1,
        .dkg-shop-plate h2 {
            margin: 0 0 28px !important;
            text-transform: uppercase !important;
            letter-spacing: 0.08em !important;
            color: #fff !important;
        }

        @media (max-width: 900px) {
            .dkg-shop-main {
                padding: 38px 0 80px !important;
            }

            .dkg-shop-plate {
                width: min(100%, calc(100vw - 36px)) !important;
                padding: 22px !important;
                border-radius: 26px !important;
            }

            .woocommerce ul.products {
                grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
                gap: 1rem !important;
            }
        }
    </style>';

    echo '<div class="dkg-inline-shop-bg"></div>';
    echo '<div class="dkg-inline-shop-bg-overlay"></div>';
}

echo '<main class="dkg-shop-main">';
echo '<section class="dkg-shop-plate">';
echo '<h1>Shop</h1>';
echo do_shortcode('[products columns="4" limit="-1"]');
echo '</section>';
echo '</main>';

get_footer();

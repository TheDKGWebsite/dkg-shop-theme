<!doctype html>
<html <?php language_attributes(); ?>>
<head>
  <meta charset="<?php bloginfo('charset'); ?>">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>

<?php
/**
 * DKG header setup.
 *
 * This file outputs:
 * 1. The main site header.
 * 2. The framed header image rotator.
 * 3. The main navigation/social links.
 * 4. The front-page-only left overlay.
 */

if (!function_exists('dkg_theme_asset_url')) {
  /**
   * Return a theme asset URL, adding filemtime cache-busting when the file exists.
   */
  function dkg_theme_asset_url($relative_path) {
    $relative_path = '/' . ltrim($relative_path, '/');
    $absolute_path = get_template_directory() . $relative_path;
    $version       = file_exists($absolute_path) ? filemtime($absolute_path) : time();

    return get_template_directory_uri() . $relative_path . '?v=' . $version;
  }
}

if (!function_exists('dkg_clean_url_list')) {
  /**
   * Trim URLs, remove blanks, remove duplicates, and preserve original order.
   */
  function dkg_clean_url_list($urls) {
    $clean_urls = array();

    foreach ((array) $urls as $url) {
      $url = trim((string) $url);

      if ($url === '' || in_array($url, $clean_urls, true)) {
        continue;
      }

      $clean_urls[] = $url;
    }

    return $clean_urls;
  }
}

if (!function_exists('dkg_pick_random_url')) {
  /**
   * Pick a random URL from the first non-empty group.
   */
  function dkg_pick_random_url($primary_urls, $fallback_urls = array()) {
    $urls = !empty($primary_urls) ? $primary_urls : $fallback_urls;

    if (empty($urls)) {
      return '';
    }

    return $urls[array_rand($urls)];
  }
}

/* --------------------------------------------------------------------------
 * Header picture rotator configuration.
 * --------------------------------------------------------------------------
 * Group 1 is the preferred first-image pool.
 * Group 2 is the larger secondary pool.
 * JavaScript can alternate between group 1 and group 2 using the data attrs.
 */
$dkg_header_rotator = array(
  'interval' => 3000,
  'frame'    => dkg_theme_asset_url('/assets/images/cframe.png'),
  'group_1'  => dkg_clean_url_list(array(
    'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202618_071-300x125.webp',
    'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202615_069-300x125.webp',
	'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202437_002-300x120.webp'
  )),
	'group_2' => dkg_clean_url_list(array(
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202627_074-300x219.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202625_073-300x240.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202620_072-300x168.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202617_070-300x143.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202613_068-300x169.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202612_067-225x300.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202611_066-300x300.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202609_065-297x300.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202608_064-300x225.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202607_063-300x207.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202605_062-300x163.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202603_061-300x225.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202602_060-300x187.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202601_059-300x187.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202600_058-300x159.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202558_057-300x225.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202556_056-300x300.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202555_055-300x225.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202554_054-300x300.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202553_053-300x225.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202551_052-300x199.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202549_051-300x225.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202548_050-300x225.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202544_049-300x166.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202542_048-300x225.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202541_047-300x168.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202540_046-300x225.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202538_045-300x225.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202537_044-300x219.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202536_043-300x225.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202534_042-300x187.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202533_041-300x168.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202531_040-300x160.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202530_039-300x223.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202528_038-300x225.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202527_037-150x150.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202526_036-300x168.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202525_035-300x287.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202523_034-150x150.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202522_033-150x150.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202520_032-300x167.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202519_031-300x184.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202517_030-150x150.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202516_029-300x168.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202515_028-300x225.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202514_027-300x163.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202512_026-300x168.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202511_025-300x220.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202510_024-300x176.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202508_023-225x300.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202506_022-300x168.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202505_021-150x150.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202504_020-150x150.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202502_019-150x150.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202500_018-300x214.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202459_017-300x234.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202458_016-150x150.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202456_015-116x300.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202455_014-300x287.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202453_013-225x300.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202452_012-300x294.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202450_011-300x214.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202449_010-300x300.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202447_009-300x138.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202446_008-243x300.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202444_007-300x225.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202443_006-300x290.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202441_005-243x300.webp',
		'https://shop.dkg.zone/wp-content/uploads/2026/08/imgur_20260811_202440_004-300x237.webp'
	)),
);

$dkg_header_rotator['all_images']   = dkg_clean_url_list(array_merge($dkg_header_rotator['group_1'], $dkg_header_rotator['group_2']));
$dkg_header_rotator['first_image']  = dkg_pick_random_url($dkg_header_rotator['group_1'], $dkg_header_rotator['group_2']);
$dkg_header_rotator['should_show']  = $dkg_header_rotator['first_image'] !== '';
?>

<?php
// === DKG CURRENT STORE HEADER INDICATOR START ===
// Finds the current DKG "store" name while keeping WordPress/WooCommerce
// collection/category logic intact behind the scenes.
$dkg_current_store_name = '';

if (function_exists('is_shop') && is_shop() && isset($_GET['featured_collection'])) {
    $dkg_featured_collection_slug = sanitize_title(wp_unslash($_GET['featured_collection']));
    $dkg_featured_collection_term = get_term_by('slug', $dkg_featured_collection_slug, 'product_cat');

    if ($dkg_featured_collection_term && !is_wp_error($dkg_featured_collection_term)) {
        $dkg_current_store_name = $dkg_featured_collection_term->name;
    }
}

if (!$dkg_current_store_name && function_exists('is_product_category') && is_product_category()) {
    $dkg_queried_store_term = get_queried_object();

    if (
        $dkg_queried_store_term instanceof WP_Term &&
        isset($dkg_queried_store_term->taxonomy) &&
        $dkg_queried_store_term->taxonomy === 'product_cat'
    ) {
        $dkg_current_store_name = $dkg_queried_store_term->name;
    }
}
// === DKG CURRENT STORE HEADER INDICATOR END ===
?>
<header class="site-header">
  <style id="dkg-header-picture-rotator-size-fix">
    /*
      Header rotator sizing/stacking.

      The frame is allowed to extend above and below the normal header box,
      but the header still occupies its normal space in the page layout.
    */

    html,
    body {
      overflow-x: hidden;
    }

    .site-header {
      position: relative !important;
      overflow: visible !important;
      z-index: 99999 !important;
    }

    .site-header .header-inner {
      position: relative !important;
      overflow: visible !important;
      z-index: 100000 !important;
    }

    .dkg-header-picture-rotator {
      position: relative !important;
      align-self: stretch;
      flex: 0 0 330px;
      width: 330px;
      height: 100%;
      min-height: 100%;
      overflow: visible !important;
      z-index: 100001 !important;
      pointer-events: none;
    }

    .dkg-header-picture-frame {
      position: absolute !important;
      left: 0;
      top: 1px;
      width: 420px;
      height: 175px;
      background-position: center;
      background-repeat: no-repeat;
      background-size: 100% 100%;
      overflow: visible !important;
      z-index: 100002 !important;
      pointer-events: none;
    }

    .dkg-header-picture-img {
      position: absolute;
      left: 8%;
      top: 9%;
      width: 84%;
      height: 82%;
      object-fit: cover;
      display: block;
      z-index: 1;
      pointer-events: none;
    }
  </style>

  <div class="header-inner">
    <div class="logo">
      <a class="site-logo" href="<?php echo esc_url(home_url('/')); ?>" aria-label="DKG Zone home">
        <img class="site-logo-img" src="<?php echo esc_url(dkg_theme_asset_url('/assets/images/dkg-logo-main.png')); ?>" alt="DKG Zone">
<!-- === DKG CURRENT STORE HEADER INDICATOR MARKUP START === -->
<?php if (!empty($dkg_current_store_name)) : ?>
  <span class="dkg-current-store-indicator dkg-current-store-indicator--mobile-logo" aria-label="<?php echo esc_attr('You are viewing: ' . $dkg_current_store_name); ?>">
    <span class="dkg-current-store-kicker">you are viewing:</span>
    <span class="dkg-current-store-name"><?php echo esc_html($dkg_current_store_name); ?></span>
  </span>
<?php endif; ?>
<!-- === DKG CURRENT STORE HEADER INDICATOR MARKUP END === -->
</a>
    </div>

    <?php if ($dkg_header_rotator['should_show']) : ?>
      <div class="dkg-header-picture-rotator"
           data-interval="<?php echo esc_attr($dkg_header_rotator['interval']); ?>"
           data-image-group-1="<?php echo esc_attr(wp_json_encode($dkg_header_rotator['group_1'])); ?>"
           data-image-group-2="<?php echo esc_attr(wp_json_encode($dkg_header_rotator['group_2'])); ?>"
           data-images="<?php echo esc_attr(wp_json_encode($dkg_header_rotator['all_images'])); ?>"
           aria-hidden="true">

        <div class="dkg-header-picture-frame"
             style="background-image: url('<?php echo esc_url($dkg_header_rotator['frame']); ?>');">
          <img class="dkg-header-picture-img"
               src="<?php echo esc_url($dkg_header_rotator['first_image']); ?>"
               alt=""
               loading="eager"
               decoding="async">
        </div>
      </div>
    <?php endif; ?>

<!-- === DKG CURRENT STORE HEADER DESKTOP SLOT START === -->
<?php if (!empty($dkg_current_store_name)) : ?>
  <div class="dkg-current-store-indicator dkg-current-store-indicator--desktop-slot" aria-label="<?php echo esc_attr('You are viewing: ' . $dkg_current_store_name); ?>">
    <span class="dkg-current-store-kicker">you are viewing:</span>
    <span class="dkg-current-store-name"><?php echo esc_html($dkg_current_store_name); ?></span>
  </div>
<?php endif; ?>
<!-- === DKG CURRENT STORE HEADER DESKTOP SLOT END === -->

<nav class="nav" aria-label="Main navigation">
      <a href="<?php echo esc_url(home_url('/')); ?>">Home</a>
      <a href="<?php echo esc_url(wc_get_page_permalink('shop')); ?>">Shop</a>
      <a href="<?php echo esc_url(wc_get_cart_url()); ?>">Cart</a>
      <a href="<?php echo esc_url(home_url('/contact/')); ?>">Contact</a>

      <a class="nav-social nav-discord" href="https://discord.gg/UfWn2DWvwC" aria-label="Discord">
        <img src="<?php echo esc_url(dkg_theme_asset_url('/assets/images/adiscord.png')); ?>" alt="Discord">
      </a>

      <a class="nav-social nav-instagram" href="https://www.instagram.com/shop.dkg.zone/" aria-label="Instagram">
        <img src="<?php echo esc_url(dkg_theme_asset_url('/assets/images/ainstagram.png')); ?>" alt="Instagram">
      </a>

      <a class="nav-social nav-youtube" href="https://docs.google.com/document/d/145X-afmLjJ_aIrrjInkJdHooxUz4BkSVuNQM4bhaB6w/edit?usp=sharing" aria-label="YouTube">
        <img src="<?php echo esc_url(dkg_theme_asset_url('/assets/images/ayoutube.png')); ?>" alt="YouTube">
      </a>
    </nav>
  </div>
</header>

<?php if (is_front_page()) : ?>
  <div class="dkg-left-overlay" aria-hidden="true">
    <img src="<?php echo esc_url(dkg_theme_asset_url('/assets/images/aleft-overlay.png')); ?>" alt="">
  </div>
<?php endif; ?>

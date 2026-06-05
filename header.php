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
    'https://i.imgur.com/WZBNYWa.png',
    'https://i.imgur.com/XXBVERU.png',
  )),
  'group_2'  => dkg_clean_url_list(array(
    'https://i.imgur.com/BP6yOQZ.jpeg',
    'https://i.imgur.com/gwcI3wv.png',
    'https://i.imgur.com/wIDieFh.png',
    'https://i.imgur.com/BIChMw9.png',
    'https://i.imgur.com/UYvoyoN.png',
    'https://i.imgur.com/Y780dCv.png',
    'https://i.imgur.com/M5i1Dia.png',
    'https://i.imgur.com/HHddteB.png',
    'https://i.imgur.com/z6Gq99h.png',
    'https://i.imgur.com/ImPmwFE.png',
    'https://i.imgur.com/Pu3xm1o.png',
    'https://i.imgur.com/edpT2W4.png',
    'https://i.imgur.com/VUSjN4l.png',
    'https://i.imgur.com/LcOTbzq.png',
    'https://i.imgur.com/Kv8rbJm.png',
    'https://i.imgur.com/75T2bgG.png',
    'https://i.imgur.com/zKLR4k1.png',
    'https://i.imgur.com/esVjdnZ.png',
    'https://i.imgur.com/kYJX41f.png',
    'https://i.imgur.com/xMKSKkr.png',
    'https://i.imgur.com/7s9OB8Y.png',
    'https://i.imgur.com/ImNWFXM.png',
    'https://i.imgur.com/2JAf8lB.png',
    'https://i.imgur.com/V5GM303.png',
    'https://i.imgur.com/NXPuaqP.png',
    'https://i.imgur.com/ZhHJLL1.png',
    'https://i.imgur.com/OgyjhIq.png',
    'https://i.imgur.com/UAJx9Cz.jpeg',
    'https://i.imgur.com/yjY73Pt.png',
    'https://i.imgur.com/zJDKkXA.png',
    'https://i.imgur.com/okqBONl.png',
    'https://i.imgur.com/5eF9xwV.png',
    'https://i.imgur.com/1XfTx1i.png',
    'https://i.imgur.com/4S20vfJ.png',
    'https://i.imgur.com/cX4Wez3.png',
    'https://i.imgur.com/yE29L2d.png',
    'https://i.imgur.com/QRfgGg1.png',
    'https://i.imgur.com/jHxhdCg.png',
    'https://i.imgur.com/6VI4wpp.png',
    'https://i.imgur.com/20ZUOs6.png',
    'https://i.imgur.com/PjSP4qq.png',
    'https://i.imgur.com/iebYzK5.jpeg',
    'https://i.imgur.com/abchvRc.jpeg',
    'https://i.imgur.com/ylBfxaf.jpeg',
    'https://i.imgur.com/u2tFPxX.jpeg',
    'https://i.imgur.com/joFlYh4.jpeg',
    'https://i.imgur.com/I7bPblm.jpeg',
    'https://i.imgur.com/caKBY31.jpeg',
    'https://i.imgur.com/5aKJKGb.jpeg',
    'https://i.imgur.com/ytn2TlT.jpeg',
    'https://i.imgur.com/t9Jjfdu.png',
    'https://i.imgur.com/VOtBuyV.jpeg',
    'https://i.imgur.com/m5cNf6J.png',
    'https://i.imgur.com/AsTjsO6.png',
    'https://i.imgur.com/xuf07Pb.png',
    'https://i.imgur.com/hQwSO8v.png',
    'https://i.imgur.com/7pL3s86.png',
    'https://i.imgur.com/6YblOj4.png',
    'https://i.imgur.com/4kHxfHU.png',
    'https://i.imgur.com/OD0AhgI.png',
    'https://i.imgur.com/M8Hotqk.png',
    'https://i.imgur.com/RLhqID1.png',
    'https://i.imgur.com/a2nrLD1.png',
    'https://i.imgur.com/skBtsV6.png',
    'https://i.imgur.com/l4UyoXa.png',
    'https://i.imgur.com/unvAxc2.png',
    'https://i.imgur.com/GChVAlI.png',
    'https://i.imgur.com/ezFUo9T.png',
    'https://i.imgur.com/7H2UEG0.png',
    'https://i.imgur.com/glt0cbU.png',
  )),
);

$dkg_header_rotator['all_images']   = dkg_clean_url_list(array_merge($dkg_header_rotator['group_1'], $dkg_header_rotator['group_2']));
$dkg_header_rotator['first_image']  = dkg_pick_random_url($dkg_header_rotator['group_1'], $dkg_header_rotator['group_2']);
$dkg_header_rotator['should_show']  = $dkg_header_rotator['first_image'] !== '';
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
      top: -10px;
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

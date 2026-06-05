<!doctype html>
<html <?php language_attributes(); ?>>
<head>
  <meta charset="<?php bloginfo('charset'); ?>">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>

<header class="site-header">

<style id="dkg-header-picture-rotator-size-fix">
  /*
    DKG HEADER ROTATOR OVERFLOW + STACKING FIX

    Goal:
    - Make the picture shuffle/frame larger.
    - Allow it to pass outside the header vertically.
    - Keep it visually above the page content below.
    - Avoid moving/resizing the logo, nav, or social icons too much.
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
    flex: 0 0 300px;
    width: 300px;
    height: 100%;
    min-height: 100%;
    overflow: visible !important;
    z-index: 100001 !important;
    pointer-events: none;
  }

  .dkg-header-picture-frame {
    position: absolute !important;
    left: 0;
    top: -16px;
    width: 390px;
    height: calc(100% + 32px);
    min-height: 145px;
    background-size: 100% 100%;
    background-repeat: no-repeat;
    background-position: center;
    overflow: hidden;
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

<!-- DKG header lights disabled --><div class="header-inner">
    <div class="logo">
      <?php
      $__dkg_logo_rel = '/assets/images/dkg-logo-main.png';
      $__dkg_logo_abs = get_template_directory() . $__dkg_logo_rel;
      $__dkg_logo_ver = file_exists($__dkg_logo_abs) ? filemtime($__dkg_logo_abs) : time();
      $__dkg_logo_url = get_template_directory_uri() . $__dkg_logo_rel . '?v=' . $__dkg_logo_ver;
      ?>
      <a class="site-logo" href="<?php echo esc_url(home_url('/')); ?>" aria-label="DKG Zone home">
        <img class="site-logo-img" src="<?php echo esc_url($__dkg_logo_url); ?>" alt="DKG Zone">
      </a>
    </div>

<!-- === DKG HEADER PICTURE ROTATOR START === -->
    <?php
      /*
        Header picture rotator image groups.

        The rotator alternates:
          random group 1 image
          random group 2 image
          random group 1 image
          random group 2 image
          etc.

        Add/remove URLs inside the arrays below.
      */

      $__dkg_header_rotator_group_1 = array(
        'https://i.imgur.com/WZBNYWa.png',
        'https://i.imgur.com/XXBVERU.png'
      );

      $__dkg_header_rotator_group_2 = array(
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
      );

      $__dkg_header_rotator_group_1 = array_values(array_filter($__dkg_header_rotator_group_1));
      $__dkg_header_rotator_group_2 = array_values(array_filter($__dkg_header_rotator_group_2));

      $__dkg_header_rotator_all_images = array_merge(
        $__dkg_header_rotator_group_1,
        $__dkg_header_rotator_group_2
      );

      $__dkg_header_rotator_first_image = '';
      if (!empty($__dkg_header_rotator_group_1)) {
        $__dkg_header_rotator_first_image = $__dkg_header_rotator_group_1[array_rand($__dkg_header_rotator_group_1)];
      } elseif (!empty($__dkg_header_rotator_group_2)) {
        $__dkg_header_rotator_first_image = $__dkg_header_rotator_group_2[array_rand($__dkg_header_rotator_group_2)];
      }

      $__dkg_header_rotator_frame = get_template_directory_uri() . '/assets/images/cframe.png';
    ?>

    <?php if (!empty($__dkg_header_rotator_first_image)) : ?>
      <div class="dkg-header-picture-rotator"
           data-interval="3000"
           data-image-group-1="<?php echo esc_attr(wp_json_encode($__dkg_header_rotator_group_1)); ?>"
           data-image-group-2="<?php echo esc_attr(wp_json_encode($__dkg_header_rotator_group_2)); ?>"
           data-images="<?php echo esc_attr(wp_json_encode($__dkg_header_rotator_all_images)); ?>"
           aria-hidden="true">

        <div class="dkg-header-picture-frame"
             style="background-image: url('<?php echo esc_url($__dkg_header_rotator_frame); ?>');">

          <img class="dkg-header-picture-img"
               src="<?php echo esc_url($__dkg_header_rotator_first_image); ?>"
               alt=""
               loading="eager"
               decoding="async">
        </div>
      </div>
    <?php endif; ?>
<!-- === DKG HEADER PICTURE ROTATOR END === -->

    <nav class="nav" aria-label="Main navigation">
      <a href="<?php echo esc_url(home_url('/')); ?>">Home</a>
      <a href="<?php echo esc_url(wc_get_page_permalink('shop')); ?>">Shop</a>
      <a href="<?php echo esc_url(wc_get_cart_url()); ?>">Cart</a>
      <a href="<?php echo esc_url(home_url('/contact/')); ?>">Contact</a>

      <a class="nav-social nav-discord" href="https://discord.gg/UfWn2DWvwC" aria-label="Discord">
        <img src="<?php echo esc_url(get_template_directory_uri() . '/assets/images/adiscord.png'); ?>" alt="Discord">
      </a>

      <a class="nav-social nav-instagram" href="https://www.instagram.com/shop.dkg.zone/" aria-label="Instagram">
        <img src="<?php echo esc_url(get_template_directory_uri() . '/assets/images/ainstagram.png'); ?>" alt="Instagram">
      </a>

      <a class="nav-social nav-youtube" href="https://docs.google.com/document/d/145X-afmLjJ_aIrrjInkJdHooxUz4BkSVuNQM4bhaB6w/edit?usp=sharing" aria-label="YouTube">
        <img src="<?php echo esc_url(get_template_directory_uri() . '/assets/images/ayoutube.png'); ?>" alt="YouTube">
      </a>
    </nav>
  </div>
</header>

<?php if (is_front_page()) : ?>
  <!-- DKG left floating overlay start -->
  <div class="dkg-left-overlay" aria-hidden="true">
    <img src="<?php echo esc_url(get_template_directory_uri() . '/assets/images/aleft-overlay.png'); ?>" alt="">
  </div>
  <!-- DKG left floating overlay end -->
<?php endif; ?>
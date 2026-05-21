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

        The rotator now alternates:
          random group 1 image
          random group 2 image
          random group 1 image
          random group 2 image
          etc.

        Add/remove URLs inside the arrays below.
      */

      $__dkg_header_rotator_group_1 = array(
        'https://i.imgur.com/IXp82Sd.png'
      );

      $__dkg_header_rotator_group_2 = array(
        'https://i.imgur.com/BP6yOQZ.jpeg',
		'https://i.imgur.com/gwcI3wv.png'
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
           data-interval="5000"
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

      <a class="nav-social nav-instagram" href="#" aria-label="Instagram">
        <img src="<?php echo esc_url(get_template_directory_uri() . '/assets/images/ainstagram.png'); ?>" alt="Instagram">
      </a>

      <a class="nav-social nav-youtube" href="#" aria-label="YouTube">
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


<?php
defined('ABSPATH') || exit;
?><!doctype html>
<html <?php language_attributes(); ?>>
<head>
  <meta charset="<?php bloginfo('charset'); ?>">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>

<header class="dkg-header" role="banner">
  <div class="dkg-header-inner">
    <a class="dkg-brand" href="<?php echo esc_url(home_url('/')); ?>" aria-label="<?php echo esc_attr(get_bloginfo('name')); ?> home">
      <?php if (has_custom_logo()) : ?>
        <?php
        $logo_id = get_theme_mod('custom_logo');
        echo wp_get_attachment_image($logo_id, 'full', false, array('class' => 'dkg-brand-image', 'alt' => get_bloginfo('name')));
        ?>
      <?php else : ?>
        <img class="dkg-brand-image" src="<?php echo esc_url(get_template_directory_uri() . '/assets/images/dkg-logo-main.png'); ?>" alt="<?php echo esc_attr(get_bloginfo('name')); ?>">
      <?php endif; ?>
    </a>

    <div class="dkg-header-statement" aria-hidden="true">ONE PRODUCT. FULL ATTENTION.</div>

    <nav class="dkg-header-actions" aria-label="Store navigation">
      <?php if (class_exists('WooCommerce')) : ?>
        <a class="dkg-cart-link" href="<?php echo esc_url(wc_get_cart_url()); ?>">
          Cart <span class="dkg-cart-count"><?php echo function_exists('WC') && WC()->cart ? esc_html(WC()->cart->get_cart_contents_count()) : '0'; ?></span>
        </a>
      <?php endif; ?>
    </nav>
  </div>
</header>

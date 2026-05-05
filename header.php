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
  <div class="header-inner">
    <div class="logo">
      <a href="<?php echo esc_url(home_url('/')); ?>" aria-label="DKG ZONE Home">
        <img src="<?php echo esc_url(get_template_directory_uri() . '/assets/images/alogo.png'); ?>" alt="DKG ZONE">
      </a>
    </div>

    <nav class="nav" aria-label="Main navigation">
      <a href="<?php echo esc_url(home_url('/')); ?>">Home</a>
      <a href="<?php echo esc_url(wc_get_page_permalink('shop')); ?>">Shop</a>
      <a href="<?php echo esc_url(wc_get_cart_url()); ?>">Cart</a>
    </nav>
  </div>
</header>

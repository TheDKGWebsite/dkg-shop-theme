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
		  <img src="<?php echo get_template_directory_uri(); ?>/assets/images/logo.png" alt="Your Store">
		</div>
        <nav class="nav">
          <a href="#">Home</a>
          <a href="#">Shop</a>
          <a href="#">Collections</a>
          <a href="#">Cart</a>
        </nav>
      </div>
    </header>

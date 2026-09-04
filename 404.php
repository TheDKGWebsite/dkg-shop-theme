<?php
defined('ABSPATH') || exit;
get_header();
?>
<main class="dkg-home-error">
  <div>
    <p class="dkg-kicker">404</p>
    <h1>Not here.</h1>
    <p><a href="<?php echo esc_url(home_url('/')); ?>">Return to the product.</a></p>
  </div>
</main>
<?php get_footer(); ?>

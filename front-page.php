<?php get_header(); ?>

<main class="site-main">
  <section class="home-products">
    <div class="container">
      <h2>Homepage</h2>
      <?php
      if (shortcode_exists('products')) {
          echo do_shortcode('[products limit="4" columns="4"]');
      }
      ?>
    </div>
  </section>
</main>

<?php get_footer(); ?>
<?php
defined('ABSPATH') || exit;
get_header();
?>
<main class="dkg-standard-main">
  <div class="dkg-standard-shell">
    <?php if (have_posts()) : ?>
      <?php while (have_posts()) : the_post(); ?>
        <article <?php post_class('dkg-entry'); ?>>
          <h1><?php the_title(); ?></h1>
          <?php the_content(); ?>
        </article>
      <?php endwhile; ?>
    <?php else : ?>
      <p>Nothing found.</p>
    <?php endif; ?>
  </div>
</main>
<?php get_footer(); ?>

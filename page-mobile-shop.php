<?php
/**
 * Custom mobile shop page.
 * Automatically used for /mobile-shop/
 */

defined('ABSPATH') || exit;

get_header();

$mobile_categories = array(
    array(
        'slug'  => 'shirts',
        'label' => 'Shirts',
        'image' => get_template_directory_uri() . '/assets/images/col1.png',
    ),
    array(
        'slug'  => 'posters',
        'label' => 'Posters',
        'image' => get_template_directory_uri() . '/assets/images/col1.png',
    ),
    array(
        'slug'  => 'stickers',
        'label' => 'Stickers',
        'image' => get_template_directory_uri() . '/assets/images/col1.png',
    ),
    array(
        'slug'  => 'hats',
        'label' => 'Hats',
        'image' => get_template_directory_uri() . '/assets/images/col1.png',
    ),
);
?>

<main class="dkg-mobile-shop">
  <section class="dkg-mobile-hero">
    <h1>Shop</h1>
    <p>Choose a collection.</p>
  </section>

  <section class="dkg-mobile-collections">
    <?php foreach ($mobile_categories as $cat) : ?>
      <?php
      $term = get_term_by('slug', $cat['slug'], 'product_cat');

      if (!$term || is_wp_error($term)) {
          continue;
      }

      $shop_url = get_permalink(wc_get_page_id('shop'));
      $link = add_query_arg('featured_collection', $cat['slug'], $shop_url);
      ?>

      <a class="dkg-mobile-collection-card" href="<?php echo esc_url($link); ?>">
        <img src="<?php echo esc_url($cat['image']); ?>" alt="">
        <div class="dkg-mobile-collection-label">
          <?php echo esc_html($cat['label']); ?>
        </div>
      </a>
    <?php endforeach; ?>
  </section>
</main>

<?php get_footer(); ?>

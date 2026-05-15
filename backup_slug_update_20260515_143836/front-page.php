<?php
/**
 * Front page template generated for dynamic WooCommerce homepage rows.
 */

get_header();

$home_collections = array(
    array(
        'slug'  => 'shirts',
        'class' => 'red',
        'label' => 'Shirts',
        'bg'    => get_template_directory_uri() . '/assets/images/col1.png',
    ),
    array(
        'slug'  => 'posters',
        'class' => 'blue',
        'label' => 'Posters',
        'bg'    => get_template_directory_uri() . '/assets/images/collection-bg-2.jpg',
    ),
    array(
        'slug'  => 'stickers',
        'class' => 'green',
        'label' => 'Stickers',
        'bg'    => get_template_directory_uri() . '/assets/images/collection-bg-3.jpg',
    ),
    array(
        'slug'  => 'hats',
        'class' => 'yellow',
        'label' => 'Hats',
        'bg'    => get_template_directory_uri() . '/assets/images/collection-bg-4.jpg',
    ),
);
?>

<div class="page-overlay">
  <main class="collections-section">
    <div class="collections-stack">

      <?php foreach ($home_collections as $collection) : ?>
        <?php
        $term = get_term_by('slug', $collection['slug'], 'product_cat');

        if (!$term || is_wp_error($term)) {
            continue;
        }

		$shop_url = get_permalink(wc_get_page_id('shop'));

		$term_link = add_query_arg(
			'featured_collection',
			$collection['slug'],
			$shop_url
		);

        $products = new WP_Query(array(
            'post_type'      => 'product',
            'posts_per_page' => 8,
            'post_status'    => 'publish',
            'tax_query'      => array(
                array(
                    'taxonomy' => 'product_cat',
                    'field'    => 'term_id',
                    'terms'    => $term->term_id,
                ),
            ),
            'orderby'        => 'menu_order title',
            'order'          => 'ASC',
        ));
        ?>

        <a class="collection-link" href="<?php echo esc_url($term_link); ?>" aria-label="<?php echo esc_attr($collection['label']); ?>">


        <section class="collection-box <?php echo esc_attr($collection['class']); ?>">
            <div class="collection-bg">
              <img src="<?php echo esc_url($collection['bg']); ?>" alt="">
            </div>

            <div class="collection-content">
              <div class="collection-label"><?php echo esc_html($collection['label']); ?></div>

              <div class="carousel-shell auto-loop">
                <div class="product-viewport">
                  <div class="product-track">

                    <?php if ($products->have_posts()) : ?>
                      <?php while ($products->have_posts()) : $products->the_post(); ?>
                        <?php
                        global $product;

                        if (!$product instanceof WC_Product) {
                            continue;
                        }

                        $image_url = get_the_post_thumbnail_url(get_the_ID(), 'medium');
                        if (!$image_url) {
                            $image_url = wc_placeholder_img_src('medium');
                        }

                        if ($product->managing_stock() && !is_null($product->get_stock_quantity())) {
                            $stock_text = 'Stock: ' . $product->get_stock_quantity();
                        } else {
                            $stock_text = $product->is_in_stock() ? 'Available' : 'Out of stock';
                        }
                        ?>
						<div class="product-card" aria-label="<?php the_title_attribute(); ?>">
						  <img class="product-image" src="<?php echo esc_url($image_url); ?>" alt="<?php the_title_attribute(); ?>">
						</div>
                      <?php endwhile; ?>
                      <?php wp_reset_postdata(); ?>
                    <?php else : ?>
						<div class="product-card product-card--empty"></div>
                    <?php endif; ?>

                  </div>
                </div>
              </div>
            </div>
          </section>


        </a>

      <?php endforeach; ?>

    </div>
  </main>
</div>

<?php get_footer(); ?>

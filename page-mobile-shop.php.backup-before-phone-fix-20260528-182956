<?php
/**
 * Template Name: Mobile Shop
 * Custom mobile shop page.
 *
 * Overhauled by mobile_shop_overhaul_updater.py.
 * Purpose:
 * - Make /mobile-shop/ behave like a mobile version of the desktop homepage.
 * - Show collection plates instead of one giant all-products grid.
 * - Keep the mobile header thinner and less crowded.
 */

get_header();

$mobile_collections = array(
    array(
        'label' => 'Applied Parts Shop',
        'slug'  => 'aps',
        'bg'    => get_template_directory_uri() . '/assets/images/',
        'class' => 'red',
    ),
    array(
        'label' => 'shop.dkg.zone prints',
        'slug'  => 'sdzp',
        'bg'    => get_template_directory_uri() . '/assets/images/',
        'class' => 'blue',
    ),
    array(
        'label' => 'Stickers',
        'slug'  => 'stickers',
        'bg'    => get_template_directory_uri() . '/assets/images/',
        'class' => 'green',
    ),
    array(
        'label' => 'Hats',
        'slug'  => 'hats',
        'bg'    => get_template_directory_uri() . '/assets/images/',
        'class' => 'yellow',
    ),
);

$bg_file = 'cbricks.png';
$bg_path = get_template_directory() . '/assets/images/' . $bg_file;
$mobile_bg = file_exists($bg_path)
    ? get_template_directory_uri() . '/assets/images/' . $bg_file
    : '';

?>

<style id="dkg-mobile-homepage-plates-overhaul">
  body.page-mobile-shop,
  body.page-template-page-mobile-shop {
    margin: 0 !important;
    min-height: 100vh !important;
    overflow-x: hidden !important;
    background-color: #050505 !important;
    <?php if ($mobile_bg) : ?>
    background-image: url('<?php echo esc_url($mobile_bg); ?>') !important;
    background-size: 360px auto !important;
    background-repeat: repeat !important;
    background-position: top left !important;
    <?php endif; ?>
  }

  body.page-mobile-shop::before,
  body.page-template-page-mobile-shop::before {
    content: "" !important;
    position: fixed !important;
    inset: 0 !important;
    background: rgba(0, 0, 0, 0.38) !important;
    pointer-events: none !important;
    z-index: 0 !important;
  }

  /*
    MOBILE-SHOP HEADER FIX:
    Only affects /mobile-shop/.
    This overrides the older mobile rules that made the header stack and become thick.
  */
  body.page-mobile-shop .site-header,
  body.page-template-page-mobile-shop .site-header {
    position: sticky !important;
    top: 0 !important;
    z-index: 100 !important;
    min-height: 58px !important;
    height: auto !important;
    padding: 5px 8px !important;
    overflow: visible !important;
    box-sizing: border-box !important;
    background-size: cover !important;
    background-position: center !important;
  }

  body.page-mobile-shop .site-header .header-inner,
  body.page-template-page-mobile-shop .site-header .header-inner {
    width: 100% !important;
    max-width: 100% !important;
    min-height: 48px !important;
    display: flex !important;
    flex-direction: row !important;
    align-items: center !important;
    justify-content: space-between !important;
    gap: 8px !important;
    padding: 0 !important;
    margin: 0 !important;
    box-sizing: border-box !important;
  }

  body.page-mobile-shop .site-header .logo,
  body.page-template-page-mobile-shop .site-header .logo,
  body.page-mobile-shop .site-header .site-logo,
  body.page-template-page-mobile-shop .site-header .site-logo,
  body.page-mobile-shop .site-header .custom-logo-link,
  body.page-template-page-mobile-shop .site-header .custom-logo-link {
    flex: 0 0 auto !important;
    display: flex !important;
    align-items: center !important;
  }

  body.page-mobile-shop .site-header .logo img,
  body.page-template-page-mobile-shop .site-header .logo img,
  body.page-mobile-shop .site-header .custom-logo,
  body.page-template-page-mobile-shop .site-header .custom-logo,
  body.page-mobile-shop .site-header .custom-logo-link img,
  body.page-template-page-mobile-shop .site-header .custom-logo-link img,
  body.page-mobile-shop .site-header .site-branding img,
  body.page-template-page-mobile-shop .site-header .site-branding img {
    width: auto !important;
    max-width: 118px !important;
    max-height: 44px !important;
    height: auto !important;
    display: block !important;
  }

  body.page-mobile-shop .site-header .nav,
  body.page-template-page-mobile-shop .site-header .nav {
    flex: 1 1 auto !important;
    min-width: 0 !important;
    display: flex !important;
    flex-direction: row !important;
    align-items: center !important;
    justify-content: flex-end !important;
    flex-wrap: nowrap !important;
    gap: 6px !important;
    margin: 0 !important;
    padding: 0 !important;
    overflow: visible !important;
  }

  body.page-mobile-shop .site-header .nav a,
  body.page-template-page-mobile-shop .site-header .nav a {
    font-size: 0.76rem !important;
    line-height: 1 !important;
    padding: 5px 4px !important;
    white-space: nowrap !important;
  }

  body.page-mobile-shop .site-header .nav a.nav-social,
  body.page-template-page-mobile-shop .site-header .nav a.nav-social {
    width: 34px !important;
    height: 34px !important;
    padding: 0 !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
  }

  body.page-mobile-shop .site-header .nav a.nav-social img,
  body.page-template-page-mobile-shop .site-header .nav a.nav-social img {
    width: 30px !important;
    height: 30px !important;
    object-fit: contain !important;
  }

  /*
    The desktop header rotator is nice on PC, but it makes mobile-shop too tall/crowded.
    Hide it only on /mobile-shop/.
  */
  body.page-mobile-shop .dkg-header-picture-rotator,
  body.page-template-page-mobile-shop .dkg-header-picture-rotator,
  body.page-mobile-shop .dkg-left-overlay,
  body.page-template-page-mobile-shop .dkg-left-overlay {
    display: none !important;
  }

  .dkg-mobile-plates-main {
    position: relative !important;
    z-index: 5 !important;
    width: 100% !important;
    max-width: 100% !important;
    padding: 18px 10px 70px !important;
    box-sizing: border-box !important;
  }

  .dkg-mobile-plates-stack {
    width: 100% !important;
    max-width: 520px !important;
    margin: 0 auto !important;
    display: flex !important;
    flex-direction: column !important;
    gap: 26px !important;
  }

  .dkg-mobile-collection-link,
  .dkg-mobile-collection-link:visited,
  .dkg-mobile-collection-link:hover,
  .dkg-mobile-collection-link:active {
    color: inherit !important;
    text-decoration: none !important;
    display: block !important;
  }

  .dkg-mobile-collection-plate {
    position: relative !important;
    width: 100% !important;
    min-height: 184px !important;
    border-radius: 24px !important;
    overflow: visible !important;
    box-sizing: border-box !important;
    padding: 24px 10px 11px !important;
    background: rgba(0, 0, 0, 0.58) !important;
    box-shadow: 0 10px 26px rgba(0, 0, 0, 0.50) !important;
    border: 1px solid rgba(255, 255, 255, 0.16) !important;
  }

  .dkg-mobile-collection-bg {
    position: absolute !important;
    inset: 0 !important;
    border-radius: inherit !important;
    overflow: hidden !important;
    z-index: 0 !important;
    pointer-events: none !important;
  }

  .dkg-mobile-collection-bg img {
    width: 100% !important;
    height: 100% !important;
    object-fit: fill !important;
    display: block !important;
    filter: brightness(0.74) contrast(1.03) !important;
  }

  .dkg-mobile-collection-label {
    position: absolute !important;
    left: 50% !important;
    top: 0 !important;
    transform: translate(-50%, -50%) !important;
    z-index: 4 !important;
    max-width: calc(100% - 30px) !important;
    padding: 7px 14px !important;
    border-radius: 999px !important;
    background: rgba(0, 0, 0, 0.84) !important;
    color: #fff !important;
    text-align: center !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    font-weight: 800 !important;
    font-size: clamp(0.76rem, 3.3vw, 1rem) !important;
    line-height: 1.12 !important;
    box-shadow: 0 5px 15px rgba(0,0,0,0.55) !important;
    white-space: normal !important;
  }

  .dkg-mobile-product-row {
    position: relative !important;
    z-index: 2 !important;
    width: 100% !important;
    height: 100% !important;
    display: grid !important;
    grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
    gap: 9px !important;
  }

  .dkg-mobile-product-card {
    min-width: 0 !important;
    height: 132px !important;
    border-radius: 14px !important;
    overflow: hidden !important;
    position: relative !important;
    background: rgba(0, 0, 0, 0.45) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
  }

  .dkg-mobile-product-card img {
    width: 100% !important;
    height: 100% !important;
    display: block !important;
    object-fit: cover !important;
  }

  .dkg-mobile-product-card.is-empty {
    background: rgba(0, 0, 0, 0.22) !important;
  }

  .dkg-mobile-product-meta {
    position: absolute !important;
    left: 0 !important;
    right: 0 !important;
    bottom: 0 !important;
    display: flex !important;
    justify-content: space-between !important;
    gap: 5px !important;
    align-items: flex-end !important;
    padding: 20px 6px 6px !important;
    background: linear-gradient(to top, rgba(0,0,0,0.88), rgba(0,0,0,0)) !important;
    color: #fff !important;
    font-size: 0.62rem !important;
    line-height: 1.05 !important;
    box-sizing: border-box !important;
  }

  .dkg-mobile-product-title {
    overflow: hidden !important;
    display: -webkit-box !important;
    -webkit-line-clamp: 2 !important;
    -webkit-box-orient: vertical !important;
  }

  .dkg-mobile-product-stock {
    flex: 0 0 auto !important;
    opacity: 0.88 !important;
    text-align: right !important;
    white-space: nowrap !important;
    font-size: 0.58rem !important;
  }

  .dkg-mobile-empty-note {
    position: relative !important;
    z-index: 2 !important;
    color: rgba(255,255,255,0.78) !important;
    font-size: 0.85rem !important;
    padding: 20px 8px !important;
    text-align: center !important;
  }

  @media (max-width: 390px) {
    body.page-mobile-shop .site-header .logo img,
    body.page-template-page-mobile-shop .site-header .logo img,
    body.page-mobile-shop .site-header .custom-logo,
    body.page-template-page-mobile-shop .site-header .custom-logo,
    body.page-mobile-shop .site-header .custom-logo-link img,
    body.page-template-page-mobile-shop .site-header .custom-logo-link img {
      max-width: 96px !important;
      max-height: 38px !important;
    }

    body.page-mobile-shop .site-header .nav,
    body.page-template-page-mobile-shop .site-header .nav {
      gap: 4px !important;
    }

    body.page-mobile-shop .site-header .nav a,
    body.page-template-page-mobile-shop .site-header .nav a {
      font-size: 0.68rem !important;
      padding: 4px 2px !important;
    }

    body.page-mobile-shop .site-header .nav a.nav-social,
    body.page-template-page-mobile-shop .site-header .nav a.nav-social {
      width: 28px !important;
      height: 28px !important;
    }

    body.page-mobile-shop .site-header .nav a.nav-social img,
    body.page-template-page-mobile-shop .site-header .nav a.nav-social img {
      width: 25px !important;
      height: 25px !important;
    }

    .dkg-mobile-plates-main {
      padding-left: 7px !important;
      padding-right: 7px !important;
    }

    .dkg-mobile-collection-plate {
      min-height: 170px !important;
      border-radius: 20px !important;
      padding-left: 8px !important;
      padding-right: 8px !important;
    }

    .dkg-mobile-product-row {
      gap: 7px !important;
    }

    .dkg-mobile-product-card {
      height: 120px !important;
      border-radius: 12px !important;
    }
  }
</style>

<main class="dkg-mobile-plates-main" aria-label="Mobile shop collections">
  <div class="dkg-mobile-plates-stack">

    <?php foreach ($mobile_collections as $collection) : ?>
      <?php
        $slug = isset($collection['slug']) ? sanitize_title($collection['slug']) : '';
        $label = isset($collection['label']) ? $collection['label'] : '';
        $term = $slug ? get_term_by('slug', $slug, 'product_cat') : false;

        if (!$term || is_wp_error($term)) {
            continue;
        }

        $term_link = get_term_link($term);
        if (is_wp_error($term_link)) {
            continue;
        }

        $products = new WP_Query(array(
            'post_type'      => 'product',
            'posts_per_page' => 4,
            'post_status'    => 'publish',
            'tax_query'      => array(
                array(
                    'taxonomy' => 'product_cat',
                    'field'    => 'slug',
                    'terms'    => $slug,
                ),
            ),
            'orderby'        => 'menu_order title',
            'order'          => 'ASC',
        ));

        $plate_class = !empty($collection['class']) ? sanitize_html_class($collection['class']) : '';
      ?>

      <a class="dkg-mobile-collection-link" href="<?php echo esc_url($term_link); ?>" aria-label="<?php echo esc_attr($label); ?>">
        <section class="dkg-mobile-collection-plate <?php echo esc_attr($plate_class); ?>">
          <?php if (!empty($collection['bg'])) : ?>
            <div class="dkg-mobile-collection-bg">
              <img src="<?php echo esc_url($collection['bg']); ?>" alt="">
            </div>
          <?php endif; ?>

          <div class="dkg-mobile-collection-label">
            <?php echo esc_html($label); ?>
          </div>

          <?php if ($products->have_posts()) : ?>
            <div class="dkg-mobile-product-row">
              <?php while ($products->have_posts()) : $products->the_post(); ?>
                <?php
                  global $product;

                  if (!$product instanceof WC_Product) {
                      continue;
                  }

                  $image_id = $product->get_image_id();
                  $image_url = $image_id
                      ? wp_get_attachment_image_url($image_id, 'woocommerce_thumbnail')
                      : wc_placeholder_img_src('woocommerce_thumbnail');

                  if ($product->managing_stock() && !is_null($product->get_stock_quantity())) {
                      $stock_text = 'Stock: ' . $product->get_stock_quantity();
                  } else {
                      $stock_text = $product->is_in_stock() ? 'Available' : 'Out';
                  }
                ?>

                <div class="dkg-mobile-product-card" aria-label="<?php the_title_attribute(); ?>">
                  <img src="<?php echo esc_url($image_url); ?>" alt="<?php the_title_attribute(); ?>">
                  <div class="dkg-mobile-product-meta">
                    <span class="dkg-mobile-product-title"><?php echo esc_html(get_the_title()); ?></span>
                    <span class="dkg-mobile-product-stock"><?php echo esc_html($stock_text); ?></span>
                  </div>
                </div>
              <?php endwhile; ?>

              <?php
                $shown = (int) $products->post_count;
                for ($i = $shown; $i < 4; $i++) :
              ?>
                <div class="dkg-mobile-product-card is-empty" aria-hidden="true"></div>
              <?php endfor; ?>
            </div>
          <?php else : ?>
            <div class="dkg-mobile-empty-note">No products in this collection yet.</div>
          <?php endif; ?>

          <?php wp_reset_postdata(); ?>
        </section>
      </a>
    <?php endforeach; ?>

  </div>
</main>

<?php get_footer(); ?>

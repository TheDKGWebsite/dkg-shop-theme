<?php
/**
 * Homepage: one product, and nothing competing with it.
 */

defined('ABSPATH') || exit;

get_header();

if (!class_exists('WooCommerce')) :
    ?>
    <main class="dkg-home-error">
      <div>
        <p class="dkg-kicker">DKG.ZONE</p>
        <h1>WooCommerce is required.</h1>
        <p>Activate WooCommerce to display the homepage product.</p>
      </div>
    </main>
    <?php
    get_footer();
    return;
endif;

$product_id = dkg_get_home_product_id();
$product    = $product_id ? wc_get_product($product_id) : false;

if (!$product) :
    ?>
    <main class="dkg-home-error">
      <div>
        <p class="dkg-kicker">DKG.ZONE</p>
        <h1>One product goes here.</h1>
        <p>Publish a WooCommerce product and mark it Featured, or set a Product ID in Appearance → Customize → One Product Homepage.</p>
      </div>
    </main>
    <?php
    get_footer();
    return;
endif;

// WooCommerce template functions depend on the global product/post context.
$GLOBALS['post'] = get_post($product_id);
setup_postdata($GLOBALS['post']);
$GLOBALS['product'] = $product;

$main_image_id = $product->get_image_id();
$gallery_ids   = $product->get_gallery_image_ids();
$image_ids     = array_values(array_unique(array_filter(array_merge(array($main_image_id), $gallery_ids))));

/*
 * HOMEPAGE PRODUCT VIDEO
 * Paste the full MP4 URL between the quotes below whenever you want to change it.
 * Example: https://shop.dkg.zone/wp-content/uploads/2026/09/product-video.mp4
 * Leave it blank to fall back to the normal WooCommerce product image.
 */
$product_video_url = 'https://imgur.com/a/veHWVVb';
$has_product_video = !empty($product_video_url);

$short_desc    = $product->get_short_description();
$full_desc     = $product->get_description();
$sku           = $product->get_sku();
?>

<main class="dkg-product-home" data-product-id="<?php echo esc_attr($product_id); ?>">
  <section class="dkg-product-media" aria-label="Product media">
    <div class="dkg-product-stage">
      <?php if ($has_product_video) : ?>
        <video
          class="dkg-main-product-media dkg-main-product-video"
          data-main-video="1"
          autoplay
          muted
          loop
          playsinline
          preload="metadata"
          aria-label="<?php echo esc_attr($product->get_name()); ?> product video"
        >
          <source src="<?php echo esc_url($product_video_url); ?>" type="video/mp4">
        </video>
      <?php endif; ?>

      <?php if ($main_image_id) : ?>
        <?php
        $main_image_attrs = array(
            'class'         => 'dkg-main-product-media dkg-main-product-image',
            'data-main-img' => '1',
            'alt'           => $product->get_name(),
            'loading'       => 'eager',
            'fetchpriority' => $has_product_video ? 'auto' : 'high',
        );
        if ($has_product_video) {
            $main_image_attrs['hidden'] = 'hidden';
        }

        echo wp_get_attachment_image(
            $main_image_id,
            'full',
            false,
            $main_image_attrs
        );
        ?>
      <?php else : ?>
        <img
          class="dkg-main-product-media dkg-main-product-image"
          data-main-img="1"
          src="<?php echo esc_url(wc_placeholder_img_src('woocommerce_single')); ?>"
          alt="<?php echo esc_attr($product->get_name()); ?>"
          <?php echo $has_product_video ? 'hidden' : ''; ?>
        >
      <?php endif; ?>
    </div>

    <?php if ($has_product_video || count($image_ids) > 1) : ?>
      <div class="dkg-product-thumbs" role="list" aria-label="Choose product media">
        <?php if ($has_product_video) : ?>
          <button
            class="dkg-thumb dkg-video-thumb is-active"
            type="button"
            role="listitem"
            data-media-type="video"
            aria-label="View product video"
            aria-pressed="true"
          >
            <?php if ($main_image_id) : ?>
              <?php echo wp_get_attachment_image($main_image_id, 'woocommerce_thumbnail', false, array('alt' => '')); ?>
            <?php endif; ?>
            <span class="dkg-video-thumb-icon" aria-hidden="true">▶</span>
          </button>
        <?php endif; ?>

        <?php foreach ($image_ids as $index => $image_id) :
            $full = wp_get_attachment_image_url($image_id, 'full');
            $alt  = get_post_meta($image_id, '_wp_attachment_image_alt', true);
            if (!$alt) {
                $alt = $product->get_name();
            }
            $image_is_active = !$has_product_video && 0 === $index;
            ?>
          <button
            class="dkg-thumb<?php echo $image_is_active ? ' is-active' : ''; ?>"
            type="button"
            role="listitem"
            data-media-type="image"
            data-full="<?php echo esc_url($full); ?>"
            data-alt="<?php echo esc_attr($alt); ?>"
            aria-label="View image <?php echo esc_attr($index + 1); ?>"
            aria-pressed="<?php echo $image_is_active ? 'true' : 'false'; ?>"
          >
            <?php echo wp_get_attachment_image($image_id, 'woocommerce_thumbnail', false, array('alt' => $alt)); ?>
          </button>
        <?php endforeach; ?>
      </div>
    <?php endif; ?>

  </section>

  <section class="dkg-product-info" aria-label="Product information">
    <div class="dkg-product-info-inner">
      <p class="dkg-kicker">CURRENT PRODUCT</p>
      <h1 class="dkg-product-title"><?php echo esc_html($product->get_name()); ?></h1>

      <div class="dkg-product-price"><?php echo wp_kses_post($product->get_price_html()); ?></div>

      <?php if ($short_desc) : ?>
        <div class="dkg-product-lede"><?php echo wp_kses_post(wpautop($short_desc)); ?></div>
      <?php endif; ?>

      <div class="dkg-buy-zone" id="buy">
        <?php if ($product->is_purchasable()) : ?>
          <?php woocommerce_template_single_add_to_cart(); ?>
        <?php else : ?>
          <p class="stock out-of-stock">This item is not currently available for purchase.</p>
        <?php endif; ?>
      </div>

      <div class="dkg-micro-info">
        <span><?php echo wp_kses_post(wc_get_stock_html($product)); ?></span>
        <?php if ($sku) : ?><span>SKU <?php echo esc_html($sku); ?></span><?php endif; ?>
      </div>

      <div class="dkg-details-stack">
        <?php if ($full_desc) : ?>
          <details open>
            <summary>About this item</summary>
            <div class="dkg-detail-body"><?php echo wp_kses_post(apply_filters('the_content', $full_desc)); ?></div>
          </details>
        <?php endif; ?>

        <details>
          <summary>Shipping + returns</summary>
          <div class="dkg-detail-body">
            <p>See the store policies for current shipping, return, and refund information.</p>
            <p>
              <a href="<?php echo esc_url(home_url('/shipping-policy/')); ?>">Shipping policy</a>
              &nbsp;·&nbsp;
              <a href="<?php echo esc_url(home_url('/refund_returns/')); ?>">Returns policy</a>
            </p>
          </div>
        </details>

      </div>

    </div>
  </section>
</main>

<?php
wp_reset_postdata();
get_footer();

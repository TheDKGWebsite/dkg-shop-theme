<?php defined('ABSPATH') || exit; ?>
<footer class="dkg-footer">
  <div class="dkg-footer-inner">
    <div class="dkg-footer-mark">DKG.ZONE</div>
    <div class="dkg-footer-links">
      <a href="<?php echo esc_url(home_url('/privacy-policy/')); ?>">Privacy</a>
      <a href="<?php echo esc_url(home_url('/refund_returns/')); ?>">Returns</a>
      <a href="<?php echo esc_url(home_url('/shipping-policy/')); ?>">Shipping</a>
      <a href="<?php echo esc_url(home_url('/terms-of-service/')); ?>">Terms</a>
      <a href="<?php echo esc_url(home_url('/contact/')); ?>">Contact</a>
    </div>
    <div class="dkg-footer-copy">© <?php echo esc_html(wp_date('Y')); ?> DKG ZONE</div>
  </div>
</footer>
<?php wp_footer(); ?>
</body>
</html>

(function () {
  'use strict';

  /*
    DKG mobile main homepage collection-plate controller.

    What it does:
    - Only runs on phone-sized screens.
    - Does not run on /mobile-shop/.
    - Finds homepage collection plates.
    - Marks only the first 3 product-looking items as visible.
    - Marks product 4+ as hidden.
    - Adds a class to each plate so CSS can scale the row as 1x3.

    Header work is intentionally separate and not touched here.
  */

  var MOBILE_QUERY = '(max-width: 767px)';
  var mq = window.matchMedia ? window.matchMedia(MOBILE_QUERY) : null;

  var PLATE_SELECTOR = [
    '.collections-stack .collection-box',
    '.collection-link .collection-box',
    '.dkg-collection-plate',
    '.dkg-home-collection-plate'
  ].join(',');

  var PRODUCT_SELECTOR = [
    'li.product',
    '.product',
    '.wc-block-grid__product',
    '.product-card',
    '.collection-product',
    '.dkg-product-card',
    'a[href*="/product/"]'
  ].join(',');

  function isOldMobileShopPage() {
    return document.body.classList.contains('page-mobile-shop') ||
      document.body.classList.contains('page-template-page-mobile-shop');
  }

  function isProbablyHomepage() {
    return document.body.classList.contains('home') ||
      document.body.classList.contains('front-page') ||
      document.body.classList.contains('page-template-front-page') ||
      document.querySelector('.collections-stack');
  }

  function uniqueElements(list) {
    var seen = [];
    var out = [];

    Array.prototype.forEach.call(list, function (el) {
      if (!el || seen.indexOf(el) !== -1) {
        return;
      }

      seen.push(el);
      out.push(el);
    });

    return out;
  }

  function closestProductElement(node, plate) {
    if (!node || !plate) {
      return null;
    }

    var current = node;

    while (current && current !== plate && current.nodeType === 1) {
      if (
        current.matches &&
        current.matches('li.product, .product, .wc-block-grid__product, .product-card, .collection-product, .dkg-product-card')
      ) {
        return current;
      }

      current = current.parentElement;
    }

    /*
      For direct product links, use the link itself if there is no obvious card wrapper.
    */
    if (
      node.matches &&
      node.matches('a[href*="/product/"]') &&
      plate.contains(node)
    ) {
      return node;
    }

    return null;
  }

  function findProductsInPlate(plate) {
    var raw = plate.querySelectorAll(PRODUCT_SELECTOR);
    var mapped = [];

    Array.prototype.forEach.call(raw, function (node) {
      var product = closestProductElement(node, plate);
      if (product) {
        mapped.push(product);
      }
    });

    return uniqueElements(mapped).filter(function (product) {
      /*
        Avoid accidentally treating the entire plate link as a product if it is
        only the collection link itself.
      */
      if (product.classList.contains('collection-link')) {
        return false;
      }

      /*
        Avoid labels/buttons that are not product cards.
      */
      if (product.classList.contains('collection-label')) {
        return false;
      }

      return true;
    });
  }

  function resetPlate(plate) {
    plate.classList.remove('dkg-mobile-main-plate-prepared');

    var marked = plate.querySelectorAll(
      '.dkg-mobile-main-visible-product, .dkg-mobile-main-extra-product'
    );

    Array.prototype.forEach.call(marked, function (el) {
      el.classList.remove('dkg-mobile-main-visible-product');
      el.classList.remove('dkg-mobile-main-extra-product');
      el.removeAttribute('aria-hidden');
    });
  }

  function preparePlate(plate) {
    var products = findProductsInPlate(plate);

    if (!products.length) {
      return;
    }

    plate.classList.add('dkg-mobile-main-plate-prepared');

    products.forEach(function (product, index) {
      product.classList.remove('dkg-mobile-main-visible-product');
      product.classList.remove('dkg-mobile-main-extra-product');

      if (index < 3) {
        product.classList.add('dkg-mobile-main-visible-product');
        product.removeAttribute('aria-hidden');
      } else {
        product.classList.add('dkg-mobile-main-extra-product');
        product.setAttribute('aria-hidden', 'true');
      }
    });
  }

  function applyMobilePlateLayout() {
    if (isOldMobileShopPage() || !isProbablyHomepage()) {
      return;
    }

    var plates = document.querySelectorAll(PLATE_SELECTOR);

    Array.prototype.forEach.call(plates, function (plate) {
      resetPlate(plate);

      if (!mq || mq.matches) {
        preparePlate(plate);
      }
    });
  }

  function scheduleApply() {
    window.requestAnimationFrame(applyMobilePlateLayout);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', scheduleApply);
  } else {
    scheduleApply();
  }

  window.addEventListener('load', scheduleApply);
  window.addEventListener('resize', scheduleApply);
  window.addEventListener('orientationchange', scheduleApply);

  if (mq && mq.addEventListener) {
    mq.addEventListener('change', scheduleApply);
  } else if (mq && mq.addListener) {
    mq.addListener(scheduleApply);
  }
})();

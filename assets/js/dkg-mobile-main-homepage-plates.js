(function () {
  'use strict';

  /*
    DKG mobile main homepage collection plate controller - Step 3.

    This version uses measured math:
      visibleWidth = track.clientWidth - leftPadding - rightPadding
      slotWidth = floor((visibleWidth - (gap * 2)) / 3)

    Therefore:
      3 slots + 2 gaps = exactly the visible interior width.
    Product 4 starts after that and is reached by scrolling.
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
    '.product-card',
    '.collection-product',
    '.dkg-product-card',
    '.wc-block-grid__product',
    'a[href*="/product/"]'
  ].join(',');

  var TRACK_SELECTOR = [
    'ul.products',
    '.products',
    '.product-row',
    '.collection-products',
    '.wc-block-grid__products'
  ].join(',');

  function isOldMobileShopPage() {
    return document.body.classList.contains('page-mobile-shop') ||
      document.body.classList.contains('page-template-page-mobile-shop');
  }

  function isProbablyHomepage() {
    return document.body.classList.contains('home') ||
      document.body.classList.contains('front-page') ||
      document.body.classList.contains('page-template-front-page') ||
      !!document.querySelector('.collections-stack');
  }

  function isMobile() {
    return !mq || mq.matches;
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

  function hasProductClass(el) {
    return !!(
      el &&
      el.matches &&
      el.matches('li.product, .product-card, .collection-product, .dkg-product-card, .wc-block-grid__product')
    );
  }

  function closestProductElement(node, plate) {
    var current;

    if (!node || !plate) {
      return null;
    }

    current = node;

    while (current && current !== plate && current.nodeType === 1) {
      if (hasProductClass(current)) {
        return current;
      }

      current = current.parentElement;
    }

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
      if (!product || !product.classList) {
        return false;
      }

      if (product.classList.contains('collection-link')) {
        return false;
      }

      if (product.classList.contains('collection-label')) {
        return false;
      }

      if (product.closest('.site-header')) {
        return false;
      }

      return true;
    });
  }

  function findTrack(plate, products) {
    var existing = plate.querySelector(TRACK_SELECTOR);

    if (existing) {
      return existing;
    }

    if (products.length && products[0].parentElement && products[0].parentElement !== plate) {
      return products[0].parentElement;
    }

    return null;
  }

  function clearPlateClasses(plate) {
    plate.classList.remove('dkg-mobile-main-plate-prepared');
    plate.classList.remove('dkg-mobile-main-scrolls-after-3');
    plate.classList.remove('dkg-mobile-main-no-scroll');

    var marked = plate.querySelectorAll(
      '.dkg-mobile-product-track, .dkg-mobile-product-item, .dkg-mobile-main-visible-product, .dkg-mobile-main-extra-product'
    );

    Array.prototype.forEach.call(marked, function (el) {
      el.classList.remove('dkg-mobile-product-track');
      el.classList.remove('dkg-mobile-product-item');
      el.classList.remove('dkg-mobile-main-visible-product');
      el.classList.remove('dkg-mobile-main-extra-product');
      el.removeAttribute('aria-hidden');

      el.style.removeProperty('flex');
      el.style.removeProperty('width');
      el.style.removeProperty('min-width');
      el.style.removeProperty('max-width');
      el.style.removeProperty('height');
      el.style.removeProperty('max-height');
    });
  }

  function getNumberFromCssValue(value, fallback) {
    var parsed = parseFloat(String(value || '').replace('px', ''));

    if (Number.isFinite(parsed)) {
      return parsed;
    }

    return fallback;
  }

  function calculateAndApplyExactSlotMath(plate, track, products) {
    var computed;
    var trackWidth;
    var padLeft;
    var padRight;
    var gap;
    var visibleInterior;
    var slotWidth;

    /*
      First apply classes so CSS gives the track its mobile dimensions.
    */
    plate.classList.add('dkg-mobile-main-plate-prepared');

    if (products.length > 3) {
      plate.classList.add('dkg-mobile-main-scrolls-after-3');
    } else {
      plate.classList.add('dkg-mobile-main-no-scroll');
    }

    track.classList.add('dkg-mobile-product-track');

    products.forEach(function (product, index) {
      product.classList.add('dkg-mobile-product-item');

      if (index < 3) {
        product.classList.add('dkg-mobile-main-visible-product');
      } else {
        product.classList.add('dkg-mobile-main-extra-product');
      }

      product.removeAttribute('aria-hidden');
    });

    /*
      Force layout once before measuring.
    */
    track.getBoundingClientRect();

    computed = window.getComputedStyle(track);

    trackWidth = Math.floor(track.clientWidth);
    padLeft = getNumberFromCssValue(computed.paddingLeft, 8);
    padRight = getNumberFromCssValue(computed.paddingRight, 8);
    gap = getNumberFromCssValue(computed.columnGap || computed.gap, 6);

    /*
      Exact math:
      Three slots and two gaps must fit inside the visible interior.
    */
    visibleInterior = Math.max(0, trackWidth - padLeft - padRight);
    slotWidth = Math.floor((visibleInterior - (gap * 2)) / 3);

    /*
      Safety fallback for extremely narrow widths.
    */
    if (!Number.isFinite(slotWidth) || slotWidth < 40) {
      slotWidth = Math.floor((Math.max(240, trackWidth) - 16 - 12) / 3);
    }

    plate.style.setProperty('--dkg-mobile-slot-px', slotWidth + 'px');
    plate.style.setProperty('--dkg-mobile-gap-px', gap + 'px');
    plate.style.setProperty('--dkg-mobile-pad-x-px', Math.round(padLeft) + 'px');

    products.forEach(function (product) {
      product.style.setProperty('flex', '0 0 ' + slotWidth + 'px', 'important');
      product.style.setProperty('width', slotWidth + 'px', 'important');
      product.style.setProperty('min-width', slotWidth + 'px', 'important');
      product.style.setProperty('max-width', slotWidth + 'px', 'important');
      product.style.setProperty('height', '100%', 'important');
      product.style.setProperty('max-height', '100%', 'important');
    });

    /*
      Reset scroll position so the first 3 are exactly visible after refresh/orientation.
    */
    track.scrollLeft = 0;

    /*
      Give a useful diagnostic in DevTools without affecting visitors.
    */
    plate.setAttribute('data-dkg-mobile-products', String(products.length));
    plate.setAttribute('data-dkg-mobile-slot-width', String(slotWidth));
    plate.setAttribute('data-dkg-mobile-track-width', String(trackWidth));
  }

  function preparePlate(plate) {
    var products = findProductsInPlate(plate);
    var track;

    if (!products.length) {
      return;
    }

    track = findTrack(plate, products);

    if (!track) {
      return;
    }

    calculateAndApplyExactSlotMath(plate, track, products);
  }

  function hideMobileLeftDecorImages() {
    var header = document.querySelector('.site-header');
    var headerBottom = header ? header.getBoundingClientRect().bottom : 0;
    var imgs = document.querySelectorAll('img');

    Array.prototype.forEach.call(imgs, function (img) {
      var rect;
      var srcAltClass;

      if (!img || img.closest('.site-header') || img.closest('.collection-box') || img.closest('.collections-stack')) {
        return;
      }

      rect = img.getBoundingClientRect();

      srcAltClass = [
        img.getAttribute('src') || '',
        img.getAttribute('alt') || '',
        img.className || '',
        img.parentElement ? img.parentElement.className || '' : ''
      ].join(' ').toLowerCase();

      /*
        Hide obvious mobile decorative left-side image, not product/header imagery.
      */
      if (
        srcAltClass.indexOf('palm') !== -1 ||
        srcAltClass.indexOf('glide') !== -1 ||
        srcAltClass.indexOf('left') !== -1 ||
        (
          rect.width >= 70 &&
          rect.height >= 120 &&
          rect.left < 45 &&
          rect.top > headerBottom - 10
        )
      ) {
        img.classList.add('dkg-mobile-hide-left-decor');
      }
    });
  }

  function centerCollectionStack() {
    var stack = document.querySelector('.collections-stack');

    if (!stack) {
      return;
    }

    stack.style.setProperty('left', '50%', 'important');
    stack.style.setProperty('right', 'auto', 'important');
    stack.style.setProperty('transform', 'translateX(-50%)', 'important');
    stack.style.setProperty('margin-left', '0', 'important');
    stack.style.setProperty('margin-right', '0', 'important');
  }

  function applyMobilePlateLayout() {
    var plates;

    if (isOldMobileShopPage() || !isProbablyHomepage()) {
      return;
    }

    plates = document.querySelectorAll(PLATE_SELECTOR);

    Array.prototype.forEach.call(plates, function (plate) {
      clearPlateClasses(plate);

      if (isMobile()) {
        preparePlate(plate);
      }
    });

    if (isMobile()) {
      centerCollectionStack();
      hideMobileLeftDecorImages();
    }
  }

  function scheduleApply() {
    window.requestAnimationFrame(function () {
      applyMobilePlateLayout();

      /*
        Second pass after images/fonts settle, because image loading can change dimensions.
      */
      window.setTimeout(applyMobilePlateLayout, 120);
    });
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

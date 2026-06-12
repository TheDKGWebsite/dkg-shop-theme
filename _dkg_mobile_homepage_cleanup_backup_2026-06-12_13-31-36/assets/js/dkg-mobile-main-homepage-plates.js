(function () {
  'use strict';

  /*
    DKG mobile main homepage collection plate controller - Step 7 cloned layer.

    Safer strategy:
    - Do not move original product DOM.
    - Mark original products/tracks hidden on mobile.
    - Clone product cards into a separate mobile carousel viewport.
    - Background and labels stay in their original DOM positions.
  */

  var MOBILE_QUERY = '(max-width: 767px)';
  var AUTOSCROLL_MS = 2600;
  var TRANSITION_MS = 520;

  var mq = window.matchMedia ? window.matchMedia(MOBILE_QUERY) : null;
  var plateTimers = new WeakMap();

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

  function stopPlateTimer(plate) {
    var timer = plateTimers.get(plate);

    if (timer) {
      window.clearInterval(timer);
      plateTimers.delete(plate);
    }
  }

  function removeMobileCarousel(plate) {
    var viewports = plate.querySelectorAll(':scope > .dkg-mobile-carousel-viewport');

    Array.prototype.forEach.call(viewports, function (viewport) {
      viewport.remove();
    });
  }

  function clearPlate(plate) {
    var marked;

    stopPlateTimer(plate);
    removeMobileCarousel(plate);

    plate.classList.remove('dkg-mobile-main-plate-prepared');
    plate.classList.remove('dkg-mobile-main-scrolls-after-3');
    plate.classList.remove('dkg-mobile-main-no-scroll');
    plate.classList.remove('dkg-mobile-main-count-1');
    plate.classList.remove('dkg-mobile-main-count-2');
    plate.classList.remove('dkg-mobile-main-count-3');

    marked = plate.querySelectorAll(
      '.dkg-mobile-original-product-source, .dkg-mobile-original-track-source, .dkg-mobile-main-visible-product, .dkg-mobile-main-extra-product'
    );

    Array.prototype.forEach.call(marked, function (el) {
      el.classList.remove('dkg-mobile-original-product-source');
      el.classList.remove('dkg-mobile-original-track-source');
      el.classList.remove('dkg-mobile-main-visible-product');
      el.classList.remove('dkg-mobile-main-extra-product');
      el.removeAttribute('aria-hidden');
    });
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

      if (product.closest('.dkg-mobile-carousel-viewport')) {
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

  function markOriginalSources(plate, products) {
    products.forEach(function (product, index) {
      product.classList.add('dkg-mobile-original-product-source');

      if (index < 3) {
        product.classList.add('dkg-mobile-main-visible-product');
      } else {
        product.classList.add('dkg-mobile-main-extra-product');
      }

      var track = product.closest(TRACK_SELECTOR);
      if (track && track !== plate && !track.classList.contains('collection-bg')) {
        track.classList.add('dkg-mobile-original-track-source');
      }
    });
  }

  function createViewportAndTrack(plate, products) {
    var viewport = document.createElement('div');
    var track = document.createElement('div');

    viewport.className = 'dkg-mobile-carousel-viewport';
    track.className = 'dkg-mobile-product-track dkg-mobile-track-no-animate';

    products.forEach(function (product) {
      var clone = product.cloneNode(true);

      clone.classList.remove('dkg-mobile-original-product-source');
      clone.classList.remove('dkg-mobile-original-track-source');
      clone.classList.add('dkg-mobile-product-item');
      clone.setAttribute('data-dkg-mobile-display-clone', '1');

      track.appendChild(clone);
    });

    viewport.appendChild(track);
    plate.appendChild(viewport);

    return {
      viewport: viewport,
      track: track,
      displayItems: Array.prototype.slice.call(track.children)
    };
  }

  function makeLoopClones(track, displayItems) {
    var clones = [];

    displayItems.slice(0, 3).forEach(function (item) {
      var clone = item.cloneNode(true);

      clone.classList.add('dkg-mobile-product-clone');
      clone.setAttribute('data-dkg-mobile-loop-clone', '1');

      track.appendChild(clone);
      clones.push(clone);
    });

    return clones;
  }

  function setTrackPosition(track, index, stepPx, animate) {
    var x = -(index * stepPx);

    track.classList.toggle('dkg-mobile-track-animate', !!animate);
    track.classList.toggle('dkg-mobile-track-no-animate', !animate);

    track.style.setProperty(
      'transform',
      'translate3d(' + x + 'px, 0, 0)',
      'important'
    );
  }

  function styleProductItems(items, slotWidth) {
    items.forEach(function (product) {
      product.classList.add('dkg-mobile-product-item');

      product.style.setProperty('flex', '0 0 ' + slotWidth + 'px', 'important');
      product.style.setProperty('width', slotWidth + 'px', 'important');
      product.style.setProperty('min-width', slotWidth + 'px', 'important');
      product.style.setProperty('max-width', slotWidth + 'px', 'important');
      product.style.setProperty('height', '100%', 'important');
      product.style.setProperty('max-height', '100%', 'important');

      product.removeAttribute('aria-hidden');
    });
  }

  function startAutoScroll(plate, track, originalCount, stepPx) {
    var index = 0;
    var timer;

    stopPlateTimer(plate);

    if (originalCount <= 3) {
      setTrackPosition(track, 0, stepPx, false);
      return;
    }

    setTrackPosition(track, 0, stepPx, false);

    timer = window.setInterval(function () {
      index += 1;
      setTrackPosition(track, index, stepPx, true);

      if (index >= originalCount) {
        window.setTimeout(function () {
          index = 0;
          setTrackPosition(track, 0, stepPx, false);
        }, TRANSITION_MS + 40);
      }
    }, AUTOSCROLL_MS);

    plateTimers.set(plate, timer);
  }

  function preparePlate(plate) {
    var products = findProductsInPlate(plate);
    var setup;
    var viewport;
    var track;
    var displayItems;
    var loopClones = [];
    var allDisplayItems;
    var viewportWidth;
    var gap;
    var slotWidth;
    var stepPx;

    if (!products.length) {
      return;
    }

    plate.classList.add('dkg-mobile-main-plate-prepared');

    if (products.length === 1) {
      plate.classList.add('dkg-mobile-main-count-1');
    } else if (products.length === 2) {
      plate.classList.add('dkg-mobile-main-count-2');
    } else if (products.length === 3) {
      plate.classList.add('dkg-mobile-main-count-3');
    } else {
      plate.classList.add('dkg-mobile-main-scrolls-after-3');
    }

    markOriginalSources(plate, products);

    setup = createViewportAndTrack(plate, products);
    viewport = setup.viewport;
    track = setup.track;
    displayItems = setup.displayItems;

    gap = window.innerWidth <= 390 ? 6 : 8;

    viewport.getBoundingClientRect();
    viewportWidth = viewport.getBoundingClientRect().width;

    if (products.length < 3) {
      slotWidth = Math.min(
        170,
        Math.max(96, (viewportWidth - gap) / 2)
      );
    } else {
      slotWidth = (viewportWidth - (gap * 2)) / 3;
    }

    if (!Number.isFinite(slotWidth) || slotWidth < 40) {
      slotWidth = 100;
    }

    stepPx = slotWidth + gap;

    if (products.length > 3) {
      loopClones = makeLoopClones(track, displayItems);
    }

    allDisplayItems = displayItems.concat(loopClones);

    plate.style.setProperty('--dkg-mobile-gap-px', gap + 'px');
    plate.style.setProperty('--dkg-mobile-slot-px', slotWidth + 'px');
    plate.style.setProperty('--dkg-mobile-step-px', stepPx + 'px');

    styleProductItems(allDisplayItems, slotWidth);
    setTrackPosition(track, 0, stepPx, false);

    plate.setAttribute('data-dkg-mobile-products', String(products.length));
    plate.setAttribute('data-dkg-mobile-slot-width', String(slotWidth));
    plate.setAttribute('data-dkg-mobile-step-width', String(stepPx));
    plate.setAttribute('data-dkg-mobile-viewport-width', String(viewportWidth));
    plate.setAttribute('data-dkg-mobile-autoscroll', products.length > 3 ? 'yes' : 'no');

    startAutoScroll(plate, track, products.length, stepPx);
  }

  function hideMobileLeftDecorImages() {
    var header = document.querySelector('.site-header');
    var headerBottom = header ? header.getBoundingClientRect().bottom : 0;
    var imgs = document.querySelectorAll('img');

    Array.prototype.forEach.call(imgs, function (img) {
      var rect;
      var srcAltClass;

      if (
        !img ||
        img.closest('.site-header') ||
        img.closest('.collection-box') ||
        img.closest('.collections-stack')
      ) {
        return;
      }

      rect = img.getBoundingClientRect();

      srcAltClass = [
        img.getAttribute('src') || '',
        img.getAttribute('alt') || '',
        img.className || '',
        img.parentElement ? img.parentElement.className || '' : ''
      ].join(' ').toLowerCase();

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
      clearPlate(plate);

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
        Second pass after images/fonts settle.
      */
      window.setTimeout(applyMobilePlateLayout, 180);
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

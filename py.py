#!/usr/bin/env python3
"""
mobile_main_homepage_overhaul_step4_autoscroll.py

Goal:
- Keep mobile visitors on the normal homepage, not /mobile-shop/.
- Keep collection plates vertically stacked.
- On mobile, each collection plate shows exactly 3 equal product spots.
- If a collection has more than 3 products, it auto-scrolls/carousels one product at a time.
- Auto-scroll loops forever.
- Product 4 should not peek/sliver into the initial 3-product view.
- Product images fit inside their slots instead of cropping.
- Hide the left decorative glide/palm image on mobile only.
- Header layout remains untouched.

Run from the root of dkg-shop-theme:

    python mobile_main_homepage_overhaul_step4_autoscroll.py
"""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path


MARKER_CSS_START = "/* === DKG MOBILE MAIN HOMEPAGE COLLECTION PLATES START === */"
MARKER_CSS_END = "/* === DKG MOBILE MAIN HOMEPAGE COLLECTION PLATES END === */"

MARKER_PHP_START = "// === DKG MOBILE MAIN HOMEPAGE COLLECTION PLATES ENQUEUE START ==="
MARKER_PHP_END = "// === DKG MOBILE MAIN HOMEPAGE COLLECTION PLATES ENQUEUE END ==="


CSS_BLOCK = """
/* === DKG MOBILE MAIN HOMEPAGE COLLECTION PLATES START === */

/*
  DKG mobile homepage collection plates - Step 4.

  Main behavior:
  - Exactly 3 equal product spots are visible on mobile.
  - Collections with 4+ products auto-scroll one product at a time.
  - Auto-scroll loops forever.
  - Product 4+ should not peek into the initial 3-product view.
  - Product images fit with object-fit: contain.
  - Header is intentionally untouched.
*/

@media screen and (max-width: 767px) {

  html,
  body {
    overflow-x: hidden !important;
  }

  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop).home,
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop).front-page,
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop).page-template-front-page {
    width: 100% !important;
    max-width: 100% !important;
    overflow-x: hidden !important;
  }

  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .collections-stack {
    width: calc(100vw - 16px) !important;
    max-width: calc(100vw - 16px) !important;

    margin-left: 0 !important;
    margin-right: 0 !important;

    position: relative !important;
    left: 50% !important;
    right: auto !important;
    transform: translateX(-50%) !important;

    display: flex !important;
    flex-direction: column !important;
    align-items: stretch !important;

    gap: clamp(20px, 5vw, 32px) !important;
    padding-left: 0 !important;
    padding-right: 0 !important;

    box-sizing: border-box !important;
    overflow: visible !important;
  }

  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .collection-link {
    width: 100% !important;
    max-width: 100% !important;
    display: block !important;
    overflow: visible !important;
    box-sizing: border-box !important;
    margin-left: auto !important;
    margin-right: auto !important;
  }

  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .collection-box {
    width: 100% !important;
    max-width: 100% !important;

    min-height: clamp(134px, 38vw, 184px) !important;
    height: clamp(134px, 38vw, 184px) !important;

    position: relative !important;
    overflow: hidden !important;
    box-sizing: border-box !important;

    transform: none !important;
    margin-left: auto !important;
    margin-right: auto !important;
  }

  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .collection-bg {
    width: 100% !important;
    height: 100% !important;
    min-height: inherit !important;
    overflow: hidden !important;
    border-radius: clamp(16px, 5vw, 28px) !important;
    box-sizing: border-box !important;
  }

  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .collection-box.dkg-mobile-main-plate-prepared {
    --dkg-mobile-visible-count: 3;
    --dkg-mobile-gap-px: 6px;
    --dkg-mobile-pad-x-px: 8px;
    --dkg-mobile-pad-y-px: 10px;
    --dkg-mobile-slot-px: 100px;
    --dkg-mobile-step-px: 106px;
  }

  /*
    Product track.
    This is transformed by JS for automated carousel motion.
    Manual scrolling is not the intended behavior here.
  */
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .collection-box.dkg-mobile-main-plate-prepared .dkg-mobile-product-track {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    align-items: stretch !important;
    justify-content: flex-start !important;

    gap: var(--dkg-mobile-gap-px) !important;

    width: max-content !important;
    max-width: none !important;
    height: 100% !important;

    margin: 0 !important;
    padding: var(--dkg-mobile-pad-y-px) var(--dkg-mobile-pad-x-px) !important;

    box-sizing: border-box !important;

    overflow: visible !important;
    transform: translate3d(0, 0, 0) !important;
    will-change: transform !important;

    touch-action: pan-y !important;
    scrollbar-width: none !important;
  }

  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .collection-box.dkg-mobile-main-plate-prepared .dkg-mobile-product-track.dkg-mobile-track-animate {
    transition: transform 520ms ease-in-out !important;
  }

  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .collection-box.dkg-mobile-main-plate-prepared .dkg-mobile-product-track.dkg-mobile-track-no-animate {
    transition: none !important;
  }

  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .collection-box.dkg-mobile-main-plate-prepared .dkg-mobile-product-track::-webkit-scrollbar {
    display: none !important;
  }

  /*
    Exact product slot.
    JS writes --dkg-mobile-slot-px from real measurements.
  */
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .collection-box.dkg-mobile-main-plate-prepared .dkg-mobile-product-item {
    flex: 0 0 var(--dkg-mobile-slot-px) !important;
    width: var(--dkg-mobile-slot-px) !important;
    min-width: var(--dkg-mobile-slot-px) !important;
    max-width: var(--dkg-mobile-slot-px) !important;

    height: 100% !important;
    max-height: 100% !important;

    margin: 0 !important;
    padding: 0 !important;

    float: none !important;
    clear: none !important;

    display: flex !important;
    align-items: center !important;
    justify-content: center !important;

    box-sizing: border-box !important;
    overflow: hidden !important;
  }

  /*
    Clones are used only to make the loop seamless.
  */
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .collection-box.dkg-mobile-main-plate-prepared .dkg-mobile-product-clone {
    pointer-events: auto !important;
  }

  /*
    Product image fit:
    Mobile should contain the product artwork inside the frame, not crop it.
  */
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .collection-box.dkg-mobile-main-plate-prepared .dkg-mobile-product-item img,
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .collection-box.dkg-mobile-main-plate-prepared .dkg-mobile-product-item .product-image,
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .collection-box.dkg-mobile-main-plate-prepared .product-image {
    width: 100% !important;
    height: 100% !important;
    max-width: 100% !important;
    max-height: 100% !important;

    object-fit: contain !important;
    object-position: center center !important;

    display: block !important;
    box-sizing: border-box !important;
  }

  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .collection-box.dkg-mobile-main-plate-prepared .dkg-mobile-product-item a,
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .collection-box.dkg-mobile-main-plate-prepared .dkg-mobile-product-item picture,
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .collection-box.dkg-mobile-main-plate-prepared .dkg-mobile-product-item figure,
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .collection-box.dkg-mobile-main-plate-prepared .dkg-mobile-product-item .woocommerce-loop-product__link {
    width: 100% !important;
    height: 100% !important;
    max-width: 100% !important;
    max-height: 100% !important;

    display: flex !important;
    align-items: center !important;
    justify-content: center !important;

    box-sizing: border-box !important;
  }

  /*
    Label sizing only.
  */
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .collection-label {
    max-width: calc(100% - 24px) !important;
    left: 50% !important;
    right: auto !important;
    transform: translateX(-50%) translateY(-50%) !important;

    font-size: clamp(0.74rem, 3.2vw, 1rem) !important;
    line-height: 1.05 !important;
    padding: clamp(5px, 1.8vw, 8px) clamp(9px, 3vw, 14px) !important;
    white-space: nowrap !important;
    text-align: center !important;
    box-sizing: border-box !important;
  }

  /*
    Hide decorative left-side glide/palm-type image on mobile only.
    Scoped away from product cards and header by JS too.
  */
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .dkg-mobile-hide-left-decor,
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .dkg-home-left-glide,
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .home-left-glide,
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .left-glide,
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .glide-left,
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .palm,
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .palm-tree,
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .home-palm,
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .dkg-palm,
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .floating-palm,
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .side-palm {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
  }
}

@media screen and (max-width: 390px) {
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .collections-stack {
    width: calc(100vw - 10px) !important;
    max-width: calc(100vw - 10px) !important;
  }

  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .collection-box {
    min-height: clamp(124px, 37vw, 158px) !important;
    height: clamp(124px, 37vw, 158px) !important;
  }

  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .collection-box.dkg-mobile-main-plate-prepared {
    --dkg-mobile-gap-px: 5px;
    --dkg-mobile-pad-x-px: 7px;
    --dkg-mobile-pad-y-px: 9px;
  }
}

/* === DKG MOBILE MAIN HOMEPAGE COLLECTION PLATES END === */
""".strip()


JS_BLOCK = r"""
(function () {
  'use strict';

  /*
    DKG mobile main homepage collection plate controller - Step 4.

    This version uses automated carousel behavior.

    Math:
      visibleInterior = plateWidth - leftPadding - rightPadding
      slotWidth = floor((visibleInterior - (gap * 2)) / 3)

    Exactly:
      3 slots + 2 gaps = visible area

    Auto-scroll:
      - Only if product count > 3
      - Advances one product at a time
      - Loops forever
      - Uses clones of the first 3 products for seamless looping
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

  function removeExistingClones(plate) {
    var clones = plate.querySelectorAll('.dkg-mobile-product-clone');

    Array.prototype.forEach.call(clones, function (clone) {
      if (clone && clone.parentNode) {
        clone.parentNode.removeChild(clone);
      }
    });
  }

  function findProductsInPlate(plate) {
    var raw;
    var mapped = [];

    removeExistingClones(plate);

    raw = plate.querySelectorAll(PRODUCT_SELECTOR);

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

      if (product.classList.contains('dkg-mobile-product-clone')) {
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

  function stopPlateTimer(plate) {
    var timer = plateTimers.get(plate);

    if (timer) {
      window.clearInterval(timer);
      plateTimers.delete(plate);
    }
  }

  function clearPlateClassesAndStyles(plate) {
    var marked;

    stopPlateTimer(plate);
    removeExistingClones(plate);

    plate.classList.remove('dkg-mobile-main-plate-prepared');
    plate.classList.remove('dkg-mobile-main-scrolls-after-3');
    plate.classList.remove('dkg-mobile-main-no-scroll');

    marked = plate.querySelectorAll(
      '.dkg-mobile-product-track, .dkg-mobile-product-item, .dkg-mobile-main-visible-product, .dkg-mobile-main-extra-product'
    );

    Array.prototype.forEach.call(marked, function (el) {
      el.classList.remove('dkg-mobile-product-track');
      el.classList.remove('dkg-mobile-product-item');
      el.classList.remove('dkg-mobile-main-visible-product');
      el.classList.remove('dkg-mobile-main-extra-product');
      el.classList.remove('dkg-mobile-track-animate');
      el.classList.remove('dkg-mobile-track-no-animate');

      el.removeAttribute('aria-hidden');

      el.style.removeProperty('flex');
      el.style.removeProperty('width');
      el.style.removeProperty('min-width');
      el.style.removeProperty('max-width');
      el.style.removeProperty('height');
      el.style.removeProperty('max-height');
      el.style.removeProperty('transform');
      el.style.removeProperty('transition');
    });
  }

  function getNumberFromCssValue(value, fallback) {
    var parsed = parseFloat(String(value || '').replace('px', ''));

    if (Number.isFinite(parsed)) {
      return parsed;
    }

    return fallback;
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

  function makeLoopClones(track, products) {
    var clones = [];

    products.slice(0, 3).forEach(function (product) {
      var clone = product.cloneNode(true);

      clone.classList.add('dkg-mobile-product-clone');
      clone.classList.add('dkg-mobile-product-item');
      clone.setAttribute('data-dkg-mobile-clone', '1');

      track.appendChild(clone);
      clones.push(clone);
    });

    return clones;
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

      /*
        When we move from the last real product into the cloned first products,
        let the transition finish, then instantly jump back to the true beginning.
      */
      if (index >= originalCount) {
        window.setTimeout(function () {
          index = 0;
          setTrackPosition(track, 0, stepPx, false);
        }, TRANSITION_MS + 40);
      }
    }, AUTOSCROLL_MS);

    plateTimers.set(plate, timer);

    /*
      Briefly pause if the user touches the plate, then resume.
      This prevents fighting with a tap.
    */
    plate.addEventListener('touchstart', function () {
      stopPlateTimer(plate);
    }, { passive: true });

    plate.addEventListener('touchend', function () {
      window.setTimeout(function () {
        startAutoScroll(plate, track, originalCount, stepPx);
      }, 1800);
    }, { passive: true });
  }

  function calculateAndApplyExactSlotMath(plate, track, products) {
    var computed;
    var plateWidth;
    var padLeft;
    var padRight;
    var gap;
    var visibleInterior;
    var slotWidth;
    var stepPx;
    var clones = [];
    var allItems;

    plate.classList.add('dkg-mobile-main-plate-prepared');

    if (products.length > 3) {
      plate.classList.add('dkg-mobile-main-scrolls-after-3');
    } else {
      plate.classList.add('dkg-mobile-main-no-scroll');
    }

    track.classList.add('dkg-mobile-product-track');

    products.forEach(function (product, index) {
      if (index < 3) {
        product.classList.add('dkg-mobile-main-visible-product');
      } else {
        product.classList.add('dkg-mobile-main-extra-product');
      }
    });

    /*
      Force layout before measuring.
    */
    track.getBoundingClientRect();

    computed = window.getComputedStyle(track);

    /*
      Use the plate width, not track scroll width, because the track becomes wider
      than the visible viewport when there are 4+ products.
    */
    plateWidth = Math.floor(plate.clientWidth);
    padLeft = getNumberFromCssValue(computed.paddingLeft, 8);
    padRight = getNumberFromCssValue(computed.paddingRight, 8);
    gap = getNumberFromCssValue(computed.columnGap || computed.gap, 6);

    visibleInterior = Math.max(0, plateWidth - padLeft - padRight);
    slotWidth = Math.floor((visibleInterior - (gap * 2)) / 3);

    if (!Number.isFinite(slotWidth) || slotWidth < 40) {
      slotWidth = Math.floor((Math.max(240, plateWidth) - 16 - 12) / 3);
    }

    stepPx = slotWidth + gap;

    /*
      Create clones only after slot math is known and only when looping is needed.
    */
    if (products.length > 3) {
      clones = makeLoopClones(track, products);
    }

    allItems = products.concat(clones);

    plate.style.setProperty('--dkg-mobile-slot-px', slotWidth + 'px');
    plate.style.setProperty('--dkg-mobile-gap-px', gap + 'px');
    plate.style.setProperty('--dkg-mobile-pad-x-px', Math.round(padLeft) + 'px');
    plate.style.setProperty('--dkg-mobile-step-px', stepPx + 'px');

    styleProductItems(allItems, slotWidth);

    setTrackPosition(track, 0, stepPx, false);

    plate.setAttribute('data-dkg-mobile-products', String(products.length));
    plate.setAttribute('data-dkg-mobile-slot-width', String(slotWidth));
    plate.setAttribute('data-dkg-mobile-step-width', String(stepPx));
    plate.setAttribute('data-dkg-mobile-plate-width', String(plateWidth));
    plate.setAttribute('data-dkg-mobile-autoscroll', products.length > 3 ? 'yes' : 'no');

    startAutoScroll(plate, track, products.length, stepPx);
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
      clearPlateClassesAndStyles(plate);

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
      window.setTimeout(applyMobilePlateLayout, 160);
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
""".strip()


PHP_ENQUEUE_BLOCK = """
// === DKG MOBILE MAIN HOMEPAGE COLLECTION PLATES ENQUEUE START ===

function dkg_enqueue_mobile_main_homepage_collection_plates() {
    if (is_admin()) {
        return;
    }

    $script_path = get_template_directory() . '/assets/js/dkg-mobile-main-homepage-plates.js';
    $script_uri  = get_template_directory_uri() . '/assets/js/dkg-mobile-main-homepage-plates.js';

    if (file_exists($script_path)) {
        wp_enqueue_script(
            'dkg-mobile-main-homepage-plates',
            $script_uri,
            array(),
            filemtime($script_path),
            true
        );
    }
}
add_action('wp_enqueue_scripts', 'dkg_enqueue_mobile_main_homepage_collection_plates', 30);

// === DKG MOBILE MAIN HOMEPAGE COLLECTION PLATES ENQUEUE END ===
""".strip()


def timestamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def backup_file(path: Path) -> Path:
    backup = path.with_name(path.name + f".bak-{timestamp()}")
    backup.write_text(path.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
    return backup


def require_file(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Required file not found: {path}")


def replace_marked_block(original: str, start_marker: str, end_marker: str, new_block: str) -> str:
    pattern = re.compile(
        re.escape(start_marker) + r".*?" + re.escape(end_marker),
        re.DOTALL,
    )

    if pattern.search(original):
        return pattern.sub(new_block, original)

    return original.rstrip() + "\n\n" + new_block + "\n"


def disable_mobile_redirect(functions_php: Path) -> bool:
    text = functions_php.read_text(encoding="utf-8", errors="replace")
    original = text

    exact = "add_action('template_redirect', 'dkg_redirect_mobile_shop_visitors', 1);"
    commented = "// DKG disabled by mobile_main_homepage_overhaul_step1.py: " + exact

    if commented in text:
        return False

    if exact in text:
        text = text.replace(exact, commented)
    else:
        text = re.sub(
            r"(?m)^(\s*)add_action\s*\(\s*['\"]template_redirect['\"]\s*,\s*['\"]dkg_redirect_mobile_shop_visitors['\"]\s*,\s*1\s*\)\s*;",
            r"\1// DKG disabled by mobile_main_homepage_overhaul_step1.py: add_action('template_redirect', 'dkg_redirect_mobile_shop_visitors', 1);",
            text,
        )

    if text != original:
        backup_file(functions_php)
        functions_php.write_text(text, encoding="utf-8")
        return True

    return False


def add_enqueue_block(functions_php: Path) -> bool:
    text = functions_php.read_text(encoding="utf-8", errors="replace")
    new_text = replace_marked_block(text, MARKER_PHP_START, MARKER_PHP_END, PHP_ENQUEUE_BLOCK)

    if new_text != text:
        backup_file(functions_php)
        functions_php.write_text(new_text, encoding="utf-8")
        return True

    return False


def add_css_block(front_page_css: Path) -> bool:
    text = front_page_css.read_text(encoding="utf-8", errors="replace")
    new_text = replace_marked_block(text, MARKER_CSS_START, MARKER_CSS_END, CSS_BLOCK)

    if new_text != text:
        backup_file(front_page_css)
        front_page_css.write_text(new_text, encoding="utf-8")
        return True

    return False


def write_js_file(js_path: Path) -> bool:
    js_path.parent.mkdir(parents=True, exist_ok=True)

    old = js_path.read_text(encoding="utf-8", errors="replace") if js_path.exists() else ""

    if old.strip() == JS_BLOCK.strip():
        return False

    if js_path.exists():
        backup_file(js_path)

    js_path.write_text(JS_BLOCK + "\n", encoding="utf-8")
    return True


def main() -> int:
    root = Path.cwd()

    functions_php = root / "functions.php"
    front_page_css = root / "assets" / "css" / "front-page.css"
    js_path = root / "assets" / "js" / "dkg-mobile-main-homepage-plates.js"

    print("")
    print("DKG mobile main homepage overhaul - step 4 autoscroll")
    print("Repo root:", root)
    print("")

    require_file(functions_php)
    require_file(front_page_css)

    changed = []

    if disable_mobile_redirect(functions_php):
        changed.append("Disabled mobile redirect template_redirect hook in functions.php")
    else:
        changed.append("Mobile redirect hook already disabled or exact hook not found")

    if write_js_file(js_path):
        changed.append("Updated assets/js/dkg-mobile-main-homepage-plates.js with looped autoscroll")
    else:
        changed.append("JS file already current")

    if add_enqueue_block(functions_php):
        changed.append("Added/updated JS enqueue block in functions.php")
    else:
        changed.append("JS enqueue block already current")

    if add_css_block(front_page_css):
        changed.append("Replaced mobile collection plate CSS in assets/css/front-page.css")
    else:
        changed.append("CSS block already current")

    print("Completed:")
    for item in changed:
        print(" -", item)

    print("")
    print("Next checks:")
    print(" 1. Clear cache / hard refresh.")
    print(" 2. Confirm plates are centered.")
    print(" 3. Confirm exactly 3 equal product spots are visible.")
    print(" 4. Confirm product 4 does NOT show as a sliver before the auto-scroll.")
    print(" 5. Confirm collections with 4+ products automatically advance one product at a time.")
    print(" 6. Confirm the auto-scroll loops back to the beginning cleanly.")
    print(" 7. Confirm product images fit inside their frames without cropping.")
    print(" 8. Confirm the left-side decorative glide/palm image is gone on mobile only.")
    print("")
    print("Header layout remains untouched.")
    print("")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("")
        print("ERROR:", exc)
        print("")
        raise
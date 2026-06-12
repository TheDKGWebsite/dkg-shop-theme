#!/usr/bin/env python3
"""
mobile_main_homepage_overhaul_step6_safe_viewport.py

Purpose:
Fix Step 5 layout damage.

Mobile behavior:
- Keep mobile users on the normal homepage.
- Keep collection plates vertically stacked.
- Do NOT reposition collection labels/titles in this step.
- Do NOT let carousel rules affect collection backgrounds.
- Create a dedicated inner viewport for products only.
- Show exactly 3 equal product slots when a collection has 3+ products.
- If a collection has 4+ products, auto-scroll one product at a time and loop.
- If a collection has 1 or 2 products, center them cleanly and do not autoscroll.
- Keep product images contained/centered, not cropped.
- Hide left decorative glide/palm image on mobile only.
- Header remains untouched.

Run from dkg-shop-theme root:

    python mobile_main_homepage_overhaul_step6_safe_viewport.py
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
  DKG mobile homepage collection plates - Step 6 safe viewport.

  Fixes:
  - Do not move titles/labels.
  - Do not treat collection background as the product track.
  - Do not stretch 1-2 item collections weirdly.
  - Create a dedicated .dkg-mobile-carousel-viewport inside each plate.
  - Product track moves only inside that viewport.
  - 4+ products auto-scroll one at a time.
  - 1-2 products are centered and static.
  - 3 products are static and equal.
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

  /*
    Center the collection stack, but do not alter the header.
  */
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

  /*
    Keep collection backgrounds stable.
    These are visual layers, not carousel tracks.
  */
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .collection-bg {
    width: 100% !important;
    height: 100% !important;
    min-height: inherit !important;
    overflow: hidden !important;
    border-radius: clamp(16px, 5vw, 28px) !important;
    box-sizing: border-box !important;
    position: relative !important;
  }

  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .collection-box.dkg-mobile-main-plate-prepared {
    --dkg-mobile-gap-px: 8px;
    --dkg-mobile-slot-px: 100px;
    --dkg-mobile-step-px: 108px;
    --dkg-mobile-viewport-pad-x: 14px;
    --dkg-mobile-viewport-pad-y: 24px;
  }

  /*
    This is the new safe clipping area.
    It is separate from collection-bg and avoids messing up the background.
  */
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .dkg-mobile-carousel-viewport {
    position: absolute !important;
    inset: var(--dkg-mobile-viewport-pad-y) var(--dkg-mobile-viewport-pad-x) var(--dkg-mobile-viewport-pad-y) var(--dkg-mobile-viewport-pad-x) !important;

    overflow: hidden !important;
    box-sizing: border-box !important;

    display: block !important;
    z-index: 2 !important;
    pointer-events: auto !important;
  }

  /*
    Moving product track.
    Only this track moves.
  */
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .dkg-mobile-carousel-viewport .dkg-mobile-product-track {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    align-items: stretch !important;

    gap: var(--dkg-mobile-gap-px) !important;

    width: max-content !important;
    max-width: none !important;
    height: 100% !important;

    margin: 0 !important;
    padding: 0 !important;

    position: relative !important;
    left: 0 !important;
    right: auto !important;

    box-sizing: border-box !important;

    overflow: visible !important;
    transform: translate3d(0, 0, 0) !important;
    will-change: transform !important;

    touch-action: pan-y !important;
    scrollbar-width: none !important;
  }

  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .dkg-mobile-carousel-viewport .dkg-mobile-product-track.dkg-mobile-track-animate {
    transition: transform 520ms ease-in-out !important;
  }

  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .dkg-mobile-carousel-viewport .dkg-mobile-product-track.dkg-mobile-track-no-animate {
    transition: none !important;
  }

  /*
    Static collections with fewer than 3 products should be centered.
  */
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .collection-box.dkg-mobile-main-count-1 .dkg-mobile-carousel-viewport .dkg-mobile-product-track,
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .collection-box.dkg-mobile-main-count-2 .dkg-mobile-carousel-viewport .dkg-mobile-product-track {
    width: 100% !important;
    justify-content: center !important;
  }

  /*
    Collections with 3+ products should fill the 3-slot viewport exactly.
  */
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .collection-box.dkg-mobile-main-count-3 .dkg-mobile-carousel-viewport .dkg-mobile-product-track,
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .collection-box.dkg-mobile-main-scrolls-after-3 .dkg-mobile-carousel-viewport .dkg-mobile-product-track {
    justify-content: flex-start !important;
  }

  /*
    Product slots.
  */
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .dkg-mobile-carousel-viewport .dkg-mobile-product-item {
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

  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .dkg-mobile-carousel-viewport .dkg-mobile-product-item > *,
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .dkg-mobile-carousel-viewport .dkg-mobile-product-item a,
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .dkg-mobile-carousel-viewport .dkg-mobile-product-item picture,
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .dkg-mobile-carousel-viewport .dkg-mobile-product-item figure,
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .dkg-mobile-carousel-viewport .dkg-mobile-product-item .woocommerce-loop-product__link {
    width: 100% !important;
    height: 100% !important;
    max-width: 100% !important;
    max-height: 100% !important;

    display: flex !important;
    align-items: center !important;
    justify-content: center !important;

    margin: 0 !important;
    padding: 0 !important;

    box-sizing: border-box !important;
    overflow: hidden !important;
  }

  /*
    Product image fit:
    Contain and center. No cropping.
  */
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .dkg-mobile-carousel-viewport .dkg-mobile-product-item img,
  body:not(.page-mobile-shop):not(.page-template-page-mobile-shop) .dkg-mobile-carousel-viewport .dkg-mobile-product-item .product-image {
    width: 100% !important;
    height: 100% !important;
    max-width: 100% !important;
    max-height: 100% !important;

    object-fit: contain !important;
    object-position: center center !important;

    display: block !important;
    margin: 0 auto !important;
    padding: 0 !important;

    box-sizing: border-box !important;
  }

  /*
    IMPORTANT:
    Do not reposition .collection-label here.
    Titles were shifting in Step 5, so this block intentionally leaves labels alone.
  */

  /*
    Hide decorative left-side glide/palm-type image on mobile only.
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
    --dkg-mobile-gap-px: 6px;
    --dkg-mobile-viewport-pad-x: 10px;
    --dkg-mobile-viewport-pad-y: 22px;
  }
}

/* === DKG MOBILE MAIN HOMEPAGE COLLECTION PLATES END === */
""".strip()


JS_BLOCK = r"""
(function () {
  'use strict';

  /*
    DKG mobile main homepage collection plate controller - Step 6 safe viewport.

    Safer model:
    - Find product items inside each collection box.
    - Move the product track into a dedicated viewport.
    - Do NOT move collection-bg or labels.
    - Do NOT position labels.
    - 1-2 products: centered, static.
    - 3 products: exact three slots, static.
    - 4+ products: exact three visible slots, automated one-by-one loop.
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

  function removeClones(plate) {
    var clones = plate.querySelectorAll('.dkg-mobile-product-clone');

    Array.prototype.forEach.call(clones, function (clone) {
      if (clone && clone.parentNode) {
        clone.parentNode.removeChild(clone);
      }
    });
  }

  function unwrapMobileViewport(plate) {
    var viewport = plate.querySelector(':scope > .dkg-mobile-carousel-viewport');

    if (!viewport) {
      return;
    }

    var track = viewport.querySelector('.dkg-mobile-product-track');

    if (track) {
      while (track.firstChild) {
        plate.appendChild(track.firstChild);
      }
    }

    viewport.remove();
  }

  function clearPlate(plate) {
    var marked;

    stopPlateTimer(plate);
    removeClones(plate);
    unwrapMobileViewport(plate);

    plate.classList.remove('dkg-mobile-main-plate-prepared');
    plate.classList.remove('dkg-mobile-main-scrolls-after-3');
    plate.classList.remove('dkg-mobile-main-no-scroll');
    plate.classList.remove('dkg-mobile-main-count-1');
    plate.classList.remove('dkg-mobile-main-count-2');
    plate.classList.remove('dkg-mobile-main-count-3');

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
      el.style.removeProperty('left');
      el.style.removeProperty('right');
      el.style.removeProperty('margin-left');
      el.style.removeProperty('margin-right');
      el.style.removeProperty('padding-left');
      el.style.removeProperty('padding-right');
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

      if (product.closest('.dkg-mobile-carousel-viewport')) {
        return true;
      }

      /*
        Avoid selecting purely decorative/background elements.
      */
      if (product.closest('.collection-bg') && !product.matches('a[href*="/product/"]')) {
        /*
          A real product/card can still live inside collection-bg,
          but this guards against catching the background wrapper itself.
        */
        return hasProductClass(product);
      }

      return true;
    });
  }

  function findExistingTrack(plate, products) {
    var existing = plate.querySelector(TRACK_SELECTOR);

    if (existing) {
      return existing;
    }

    if (products.length && products[0].parentElement && products[0].parentElement !== plate) {
      return products[0].parentElement;
    }

    return null;
  }

  function createViewportAndTrack(plate, products) {
    var viewport = document.createElement('div');
    var track = document.createElement('div');

    viewport.className = 'dkg-mobile-carousel-viewport';
    track.className = 'dkg-mobile-product-track dkg-mobile-track-no-animate';

    plate.appendChild(viewport);
    viewport.appendChild(track);

    products.forEach(function (product) {
      track.appendChild(product);
    });

    return {
      viewport: viewport,
      track: track
    };
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
    var viewportWidth;
    var gap;
    var slotWidth;
    var stepPx;
    var clones = [];
    var allItems;

    if (!products.length) {
      return;
    }

    /*
      Confirm there is some product structure before moving it.
      This avoids using a background wrapper as the track.
    */
    findExistingTrack(plate, products);

    setup = createViewportAndTrack(plate, products);
    viewport = setup.viewport;
    track = setup.track;

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

    gap = window.innerWidth <= 390 ? 6 : 8;

    /*
      Force layout after creating viewport.
    */
    viewport.getBoundingClientRect();
    viewportWidth = viewport.getBoundingClientRect().width;

    /*
      If 1 or 2 products, size them like normal cards but centered.
      If 3+ products, use exact three-slot math.
    */
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
      clones = makeLoopClones(track, products);
    }

    allItems = products.concat(clones);

    plate.style.setProperty('--dkg-mobile-gap-px', gap + 'px');
    plate.style.setProperty('--dkg-mobile-slot-px', slotWidth + 'px');
    plate.style.setProperty('--dkg-mobile-step-px', stepPx + 'px');

    styleProductItems(allItems, slotWidth);
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
    print("DKG mobile main homepage overhaul - step 6 safe viewport")
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
        changed.append("Updated assets/js/dkg-mobile-main-homepage-plates.js with safe viewport carousel")
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
    print(" 2. Confirm collection backgrounds look normal again.")
    print(" 3. Confirm labels/titles are no longer shifted by this mobile block.")
    print(" 4. Confirm 1-2 item collections are centered and static.")
    print(" 5. Confirm 3 item collections show 3 equal static slots.")
    print(" 6. Confirm 4+ item collections auto-scroll one product at a time.")
    print(" 7. Confirm product images are centered and uncropped.")
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
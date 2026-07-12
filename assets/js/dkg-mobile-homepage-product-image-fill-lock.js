/*
DKG Mobile Homepage Product Image Fill Lock
-------------------------------------------

Mobile homepage only.

Forces product image wrappers/images in the generated mobile carousel layer
to fill the current product-card border/frame. Re-applies after late carousel
builds, load, resize/orientation, and DOM mutations.
*/

(function () {
  "use strict";

  var RUN_MS = 6500;
  var OBSERVER_STOP_MS = 9000;
  var APPLY_DEBOUNCE_MS = 40;

  var applyTimer = null;
  var startedAt = Date.now();

  function isMobile() {
    if (window.matchMedia) {
      return window.matchMedia("(max-width: 767px)").matches;
    }
    return window.innerWidth <= 767;
  }

  function isTargetPage() {
    var b = document.body;
    if (!b) return false;

    var isHome =
      b.classList.contains("home") ||
      b.classList.contains("front-page") ||
      b.classList.contains("page-template-front-page");

    var isMobileShop =
      b.classList.contains("page-mobile-shop") ||
      b.classList.contains("page-template-page-mobile-shop");

    return isHome && !isMobileShop;
  }

  function setImportant(el, prop, value) {
    if (!el || !el.style) return;
    el.style.setProperty(prop, value, "important");
  }

  function forceFrame(el) {
    if (!el) return;

    setImportant(el, "position", "relative");
    setImportant(el, "overflow", "hidden");
    setImportant(el, "box-sizing", "border-box");
  }

  function forceFullWrapper(el) {
    if (!el) return;

    setImportant(el, "display", "block");
    setImportant(el, "position", "absolute");
    setImportant(el, "inset", "0");
    setImportant(el, "width", "100%");
    setImportant(el, "height", "100%");
    setImportant(el, "min-width", "100%");
    setImportant(el, "min-height", "100%");
    setImportant(el, "max-width", "none");
    setImportant(el, "max-height", "none");
    setImportant(el, "margin", "0");
    setImportant(el, "padding", "0");
    setImportant(el, "overflow", "hidden");
    setImportant(el, "box-sizing", "border-box");
  }

  function forceImage(el) {
    if (!el) return;

    setImportant(el, "display", "block");
    setImportant(el, "position", "absolute");
    setImportant(el, "inset", "0");
    setImportant(el, "width", "100%");
    setImportant(el, "height", "100%");
    setImportant(el, "min-width", "100%");
    setImportant(el, "min-height", "100%");
    setImportant(el, "max-width", "none");
    setImportant(el, "max-height", "none");
    setImportant(el, "object-fit", "fill");
    setImportant(el, "object-position", "center center");
    setImportant(el, "margin", "0");
    setImportant(el, "padding", "0");
    setImportant(el, "border", "0");
    setImportant(el, "transform", "none");
    setImportant(el, "box-sizing", "border-box");
  }

  function applyFillLock() {
    if (!isMobile() || !isTargetPage()) return;

    var boxes = document.querySelectorAll(".collection-box");

    boxes.forEach(function (box) {
      var frames = box.querySelectorAll([
        ".product-card",
        ".dkg-mobile-product-card",
        ".dkg-mobile-product-card-inner"
      ].join(","));

      frames.forEach(function (frame) {
        forceFrame(frame);

        var wrappers = frame.querySelectorAll([
          ":scope > a",
          "a.woocommerce-LoopProduct-link",
          "a.woocommerce-loop-product__link",
          ".woocommerce-LoopProduct-link",
          ".woocommerce-loop-product__link",
          "picture",
          "figure"
        ].join(","));

        wrappers.forEach(forceFullWrapper);

        var images = frame.querySelectorAll([
          "img",
          ".product-image",
          ".attachment-woocommerce_thumbnail",
          ".wp-post-image"
        ].join(","));

        images.forEach(forceImage);
      });
    });
  }

  function scheduleApply() {
    if (applyTimer) {
      window.clearTimeout(applyTimer);
    }

    applyTimer = window.setTimeout(function () {
      applyTimer = null;
      applyFillLock();
    }, APPLY_DEBOUNCE_MS);
  }

  function burst() {
    [0, 50, 120, 250, 500, 900, 1400, 2200, 3400, 5000, 6500].forEach(function (ms) {
      window.setTimeout(applyFillLock, ms);
    });
  }

  function start() {
    if (!isTargetPage()) return;

    applyFillLock();
    burst();

    window.addEventListener("load", burst, { passive: true });
    window.addEventListener("resize", scheduleApply, { passive: true });
    window.addEventListener("orientationchange", burst, { passive: true });

    if (window.MutationObserver) {
      var observer = new MutationObserver(function () {
        if (Date.now() - startedAt <= RUN_MS) {
          scheduleApply();
        }
      });

      observer.observe(document.documentElement, {
        subtree: true,
        childList: true,
        attributes: true,
        attributeFilter: ["class", "style", "src", "srcset"]
      });

      window.setTimeout(function () {
        observer.disconnect();
      }, OBSERVER_STOP_MS);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();

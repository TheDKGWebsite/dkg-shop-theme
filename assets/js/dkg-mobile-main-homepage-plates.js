/*
  DKG mobile homepage collection plates.

  Cleanup version:
  - Uses the real front-page.php structure.
  - Reads products only from .collection-content .product-track > .product-card.
  - Inserts the mobile viewport inside .collection-content after .collection-label.
  - Never inserts into .collection-bg.
  - Never clones .collection-label.
  - Removes old mobile carousel wrappers before rebuilding.
  - Hides only the original .carousel-shell after a clone layer has been built.
*/

(function () {
  "use strict";

  var MOBILE_QUERY = "(max-width: 767px)";
  var VISIBLE_SLOTS = 3;
  var AUTOSCROLL_MS = 1900;
  var TRANSITION_MS = 420;
  var RESIZE_DEBOUNCE_MS = 180;

  var stateByBox = new WeakMap();
  var resizeTimer = null;

  // === DKG MOBILE WIDTH-STABLE RESIZE START ===
  /*
    Mobile browsers can fire resize events during normal vertical scrolling when
    the address bar expands/collapses. That should NOT rebuild the carousel,
    because rebuilding resets the autoscroll loop.

    We only rebuild when:
    - the viewport width changes meaningfully,
    - the mobile/non-mobile breakpoint changes,
    - or orientationchange explicitly fires.
  */
  var dkgLastLayoutWidth = window.innerWidth || document.documentElement.clientWidth || 0;
  var dkgLastMobileMatch = matchesMobile();

  function dkgGetLayoutWidth() {
    return window.innerWidth || document.documentElement.clientWidth || 0;
  }

  function dkgShouldRebuildForViewportChange(event) {
    var force = !!(event && event.type === "orientationchange");
    var currentWidth = dkgGetLayoutWidth();
    var currentMobileMatch = matchesMobile();

    var widthDelta = Math.abs(currentWidth - dkgLastLayoutWidth);
    var mobileStateChanged = currentMobileMatch !== dkgLastMobileMatch;

    /*
      A few pixels can change from scrollbars/device rounding.
      On phones, height-only address-bar changes usually keep width the same.
    */
    var meaningfulWidthChange = widthDelta >= 24;

    if (!force && !mobileStateChanged && !meaningfulWidthChange) {
      return false;
    }

    dkgLastLayoutWidth = currentWidth;
    dkgLastMobileMatch = currentMobileMatch;

    return true;
  }
  // === DKG MOBILE WIDTH-STABLE RESIZE END ===
function matchesMobile() {
    if (!window.matchMedia) {
      return window.innerWidth <= 767;
    }

    return window.matchMedia(MOBILE_QUERY).matches;
  }

  function toArray(list) {
    return Array.prototype.slice.call(list || []);
  }

  function directChildWithClass(parent, className) {
    if (!parent) {
      return null;
    }

    var children = parent.children || [];

    for (var i = 0; i < children.length; i += 1) {
      if (children[i].classList && children[i].classList.contains(className)) {
        return children[i];
      }
    }

    return null;
  }

  function queryDirect(parent, selector, fallbackSelector) {
    if (!parent) {
      return null;
    }

    try {
      var direct = parent.querySelector(":scope > " + selector);
      if (direct) {
        return direct;
      }
    } catch (error) {
      /* Some older browsers may not support :scope. */
    }

    return parent.querySelector(fallbackSelector || selector);
  }

  function clearTimer(box) {
    var oldState = stateByBox.get(box);

    if (oldState && oldState.timer) {
      window.clearInterval(oldState.timer);
    }

    stateByBox.delete(box);
  }

  function removeMobileLayer(box) {
    if (!box) {
      return;
    }

    clearTimer(box);

    toArray(box.querySelectorAll(".dkg-mobile-carousel-viewport")).forEach(function (node) {
      if (node && node.parentNode) {
        node.parentNode.removeChild(node);
      }
    });

    toArray(box.querySelectorAll(".dkg-mobile-original-product-source")).forEach(function (node) {
      node.classList.remove("dkg-mobile-original-product-source");
    });

    toArray(box.querySelectorAll(".dkg-mobile-original-track-source")).forEach(function (node) {
      node.classList.remove("dkg-mobile-original-track-source");
    });

    box.removeAttribute("data-dkg-mobile-plates-ready");
  }

  function getParts(box) {
    var bg = directChildWithClass(box, "collection-bg");
    var content = directChildWithClass(box, "collection-content") || box.querySelector(".collection-content");

    if (!content) {
      return null;
    }

    var label = directChildWithClass(content, "collection-label") || content.querySelector(".collection-label");

    /*
      Important:
      Original products are inside .collection-content, not inside .collection-bg.
      This intentionally avoids querying through .collection-bg.
    */
    var shell = queryDirect(content, ".carousel-shell", ".carousel-shell");
    var viewport = shell ? shell.querySelector(".product-viewport") : content.querySelector(".product-viewport");
    var track = viewport ? viewport.querySelector(".product-track") : null;

    if (!track) {
      track = content.querySelector(".product-track");
    }

    var cards = track
      ? toArray(track.children).filter(function (child) {
          return (
            child &&
            child.classList &&
            child.classList.contains("product-card") &&
            !child.classList.contains("product-card--empty") &&
            child.querySelector("img")
          );
        })
      : [];

    return {
      box: box,
      bg: bg,
      content: content,
      label: label,
      shell: shell,
      viewport: viewport,
      track: track,
      cards: cards
    };
  }

  function cloneCardIntoItem(card, index, isLoopClone) {
    var item = document.createElement("div");
    item.className = "dkg-mobile-product-item";
    item.setAttribute("data-dkg-mobile-product-index", String(index));

    if (isLoopClone) {
      item.classList.add("dkg-mobile-product-clone");
      item.setAttribute("aria-hidden", "true");
    }

    var clone = card.cloneNode(true);
    clone.classList.add("dkg-mobile-product-card-inner");

    /*
      Remove IDs from cloned markup so duplicate IDs cannot appear.
    */
    if (clone.id) {
      clone.removeAttribute("id");
    }

    toArray(clone.querySelectorAll("[id]")).forEach(function (node) {
      node.removeAttribute("id");
    });

    item.appendChild(clone);
    return item;
  }

  function insertAfterLabel(parts, viewport) {
    var content = parts.content;
    var label = parts.label;

    if (label && label.parentNode === content && label.nextSibling) {
      content.insertBefore(viewport, label.nextSibling);
      return;
    }

    if (label && label.parentNode === content) {
      content.appendChild(viewport);
      return;
    }

    content.insertBefore(viewport, content.firstChild);
  }

  function measureStep(track) {
    if (!track || !track.children || !track.children.length) {
      return 0;
    }

    var first = track.children[0];
    var rect = first.getBoundingClientRect();
    var styles = window.getComputedStyle(track);
    var gap = parseFloat(styles.columnGap || styles.gap || "0");

    if (!isFinite(gap)) {
      gap = 0;
    }

    return rect.width + gap;
  }

  function setTrackPosition(track, index, step, animate) {
    if (!track) {
      return;
    }

    if (animate) {
      track.style.transition = "transform " + TRANSITION_MS + "ms ease";
    } else {
      track.style.transition = "none";
    }

    track.style.transform = "translate3d(" + (-Math.round(index * step)) + "px, 0, 0)";
  }

  function buildStatic(parts, viewport, track) {
    viewport.classList.add("dkg-mobile-static");
    viewport.classList.add("dkg-mobile-count-" + parts.cards.length);
    track.style.transition = "none";
    track.style.transform = "translate3d(0, 0, 0)";
  }

  function buildAutoscroll(parts, viewport, track) {
    var index = 0;
    var totalReal = parts.cards.length;
    var step = 0;

    viewport.classList.add("dkg-mobile-autoscroll");
    viewport.setAttribute("data-dkg-mobile-real-count", String(totalReal));

    function recalc() {
      step = measureStep(track);
      setTrackPosition(track, index, step, false);
    }

    function advance() {
      if (!matchesMobile() || !document.body.contains(parts.box)) {
        return;
      }

      step = measureStep(track);

      if (!step) {
        return;
      }

      index += 1;
      setTrackPosition(track, index, step, true);

      /*
        When index reaches totalReal, the visible items are the appended clones
        of the first 3 products. Snap back to real index 0 after transition.
      */
      if (index >= totalReal) {
        window.setTimeout(function () {
          index = 0;
          step = measureStep(track);
          setTrackPosition(track, index, step, false);
        }, TRANSITION_MS + 40);
      }
    }

    window.requestAnimationFrame(function () {
      recalc();
      window.setTimeout(recalc, 80);
    });

    var timer = window.setInterval(advance, AUTOSCROLL_MS);

    stateByBox.set(parts.box, {
      timer: timer,
      recalc: recalc
    });
  }

  function setupBox(box) {
    if (!box) {
      return;
    }

    removeMobileLayer(box);

    var parts = getParts(box);

    if (!parts || !parts.content || !parts.track || !parts.cards.length) {
      return;
    }

    /*
      Do not ever use .collection-bg as the mobile insertion point.
    */
    if (parts.bg && parts.bg.contains(parts.track)) {
      return;
    }

    var viewport = document.createElement("div");
    viewport.className = "dkg-mobile-carousel-viewport";
    viewport.setAttribute("aria-hidden", "true");

    var mobileTrack = document.createElement("div");
    mobileTrack.className = "dkg-mobile-product-track";

    parts.cards.forEach(function (card, index) {
      mobileTrack.appendChild(cloneCardIntoItem(card, index, false));
    });

    if (parts.cards.length > VISIBLE_SLOTS) {
      for (var i = 0; i < VISIBLE_SLOTS; i += 1) {
        mobileTrack.appendChild(cloneCardIntoItem(parts.cards[i], i, true));
      }
    }

    viewport.appendChild(mobileTrack);
    insertAfterLabel(parts, viewport);

    /*
      Hide only the original product shell/track, not the whole content area,
      not the label, and never the background.
    */
    if (parts.shell) {
      parts.shell.classList.add("dkg-mobile-original-product-source");
    }

    if (parts.track) {
      parts.track.classList.add("dkg-mobile-original-track-source");
    }

    box.setAttribute("data-dkg-mobile-plates-ready", "true");

    if (parts.cards.length <= VISIBLE_SLOTS) {
      buildStatic(parts, viewport, mobileTrack);
    } else {
      buildAutoscroll(parts, viewport, mobileTrack);
    }
  }

  // === DKG MOBILE REMOVE LEFT OVERLAY START ===
  function removeMobileLeftOverlay() {
    if (!matchesMobile()) {
      return;
    }

    /*
      The desktop left slide-in overlay is not useful on mobile and can visually
      interfere with the normal homepage collection plates. Remove it from the
      mobile DOM instead of only hiding it with CSS.
    */
    toArray(document.querySelectorAll(".dkg-left-overlay")).forEach(function (node) {
      if (node && node.parentNode) {
        node.setAttribute("aria-hidden", "true");
        node.parentNode.removeChild(node);
      }
    });
  }
  // === DKG MOBILE REMOVE LEFT OVERLAY END ===


  function setupAll() {
    
    removeMobileLeftOverlay();
var boxes = toArray(document.querySelectorAll(".collections-stack .collection-box"));

    if (!matchesMobile()) {
      boxes.forEach(removeMobileLayer);
      return;
    }

    boxes.forEach(setupBox);
  }
  function scheduleSetup(event) {
    if (!dkgShouldRebuildForViewportChange(event)) {
      return;
    }

    if (resizeTimer) {
      window.clearTimeout(resizeTimer);
    }

    resizeTimer = window.setTimeout(setupAll, RESIZE_DEBOUNCE_MS);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", setupAll);
  } else {
    setupAll();
  }

  window.addEventListener("resize", scheduleSetup);
  window.addEventListener("orientationchange", scheduleSetup);

  if (window.matchMedia) {
    try {
      var mq = window.matchMedia(MOBILE_QUERY);

      if (mq.addEventListener) {
        mq.addEventListener("change", scheduleSetup);
      } else if (mq.addListener) {
        mq.addListener(scheduleSetup);
      }
    } catch (error) {
      /* Non-critical. Resize listener still handles changes. */
    }
  }
})();

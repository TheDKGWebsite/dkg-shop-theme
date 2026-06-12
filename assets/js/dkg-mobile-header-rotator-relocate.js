/*
  DKG mobile header rotator relocate.

  Mobile only:
  - Move the existing .dkg-header-picture-rotator out of the header.
  - Insert it below all homepage collection plates.
  - Do not clone it.
  - Restore it back to its original header position on desktop.

  This intentionally avoids editing header.php.
*/

(function () {
  "use strict";

  var MOBILE_QUERY = "(max-width: 767px)";
  var ZONE_CLASS = "dkg-mobile-relocated-header-rotator-zone";
  var RELOCATED_CLASS = "dkg-mobile-header-rotator-relocated";
  var RESIZE_DEBOUNCE_MS = 160;

  var originalParent = null;
  var originalNextSibling = null;
  var originalWasCaptured = false;
  var resizeTimer = null;
  var lastLayoutWidth = window.innerWidth || document.documentElement.clientWidth || 0;
  var lastMobileMatch = matchesMobile();

  function matchesMobile() {
    if (!window.matchMedia) {
      return window.innerWidth <= 767;
    }

    return window.matchMedia(MOBILE_QUERY).matches;
  }

  function toArray(list) {
    return Array.prototype.slice.call(list || []);
  }

  function getLayoutWidth() {
    return window.innerWidth || document.documentElement.clientWidth || 0;
  }

  function shouldRunForViewportChange(event) {
    if (event && event.type === "orientationchange") {
      lastLayoutWidth = getLayoutWidth();
      lastMobileMatch = matchesMobile();
      return true;
    }

    var currentWidth = getLayoutWidth();
    var currentMobileMatch = matchesMobile();
    var widthDelta = Math.abs(currentWidth - lastLayoutWidth);
    var mobileChanged = currentMobileMatch !== lastMobileMatch;

    /*
      Ignore mobile browser height-only resize events from address-bar movement.
    */
    if (!mobileChanged && widthDelta < 24) {
      return false;
    }

    lastLayoutWidth = currentWidth;
    lastMobileMatch = currentMobileMatch;
    return true;
  }

  function getRotator() {
    return document.querySelector(".dkg-header-picture-rotator");
  }

  function captureOriginalPosition(rotator) {
    if (originalWasCaptured || !rotator || !rotator.parentNode) {
      return;
    }

    originalParent = rotator.parentNode;
    originalNextSibling = rotator.nextSibling;
    originalWasCaptured = true;
  }

  function getCollectionsSection() {
    return (
      document.querySelector("main.collections-section") ||
      document.querySelector(".collections-section") ||
      document.querySelector(".collections-stack")
    );
  }

  function getOrCreateZone() {
    var existing = document.querySelector("." + ZONE_CLASS);

    if (existing) {
      return existing;
    }

    var zone = document.createElement("div");
    zone.className = ZONE_CLASS;
    zone.setAttribute("aria-hidden", "true");

    return zone;
  }

  function insertZoneBelowCollections(zone) {
    var section = getCollectionsSection();

    if (!section || !section.parentNode) {
      return false;
    }

    /*
      If the selector fell back to .collections-stack, insert after its parent
      when the parent is the actual main.collections-section.
    */
    if (
      section.classList &&
      section.classList.contains("collections-stack") &&
      section.parentNode &&
      section.parentNode.classList &&
      section.parentNode.classList.contains("collections-section")
    ) {
      section = section.parentNode;
    }

    if (zone.parentNode === section.parentNode && zone.previousSibling === section) {
      return true;
    }

    section.parentNode.insertBefore(zone, section.nextSibling);
    return true;
  }

  function moveRotatorBelowPlates() {
    var rotator = getRotator();

    if (!rotator) {
      return;
    }

    captureOriginalPosition(rotator);

    var zone = getOrCreateZone();

    if (!insertZoneBelowCollections(zone)) {
      return;
    }

    if (rotator.parentNode !== zone) {
      zone.appendChild(rotator);
    }

    rotator.classList.add(RELOCATED_CLASS);
    rotator.setAttribute("data-dkg-mobile-relocated", "true");
    rotator.setAttribute("aria-hidden", "true");
  }

  function restoreRotatorToHeader() {
    var rotator = getRotator();

    if (!rotator || !originalParent) {
      removeEmptyZone();
      return;
    }

    rotator.classList.remove(RELOCATED_CLASS);
    rotator.removeAttribute("data-dkg-mobile-relocated");

    if (rotator.parentNode !== originalParent) {
      if (originalNextSibling && originalNextSibling.parentNode === originalParent) {
        originalParent.insertBefore(rotator, originalNextSibling);
      } else {
        originalParent.appendChild(rotator);
      }
    }

    removeEmptyZone();
  }

  function removeEmptyZone() {
    var zone = document.querySelector("." + ZONE_CLASS);

    if (!zone) {
      return;
    }

    if (!zone.children.length && zone.parentNode) {
      zone.parentNode.removeChild(zone);
    }
  }

  function applyLayout() {
    var rotator = getRotator();

    if (!rotator) {
      return;
    }

    captureOriginalPosition(rotator);

    if (matchesMobile()) {
      moveRotatorBelowPlates();
    } else {
      restoreRotatorToHeader();
    }
  }

  function scheduleApply(event) {
    if (!shouldRunForViewportChange(event)) {
      return;
    }

    if (resizeTimer) {
      window.clearTimeout(resizeTimer);
    }

    resizeTimer = window.setTimeout(applyLayout, RESIZE_DEBOUNCE_MS);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", applyLayout);
  } else {
    applyLayout();
  }

  window.addEventListener("resize", scheduleApply);
  window.addEventListener("orientationchange", scheduleApply);

  if (window.matchMedia) {
    try {
      var mq = window.matchMedia(MOBILE_QUERY);

      if (mq.addEventListener) {
        mq.addEventListener("change", scheduleApply);
      } else if (mq.addListener) {
        mq.addListener(scheduleApply);
      }
    } catch (error) {
      /*
        Non-critical. Resize/orientation listeners still handle changes.
      */
    }
  }

  /*
    If the collection plates are built late by another script/cache layer,
    give the relocation one extra pass after load.
  */
  window.addEventListener("load", function () {
    window.setTimeout(applyLayout, 80);
  });
})();

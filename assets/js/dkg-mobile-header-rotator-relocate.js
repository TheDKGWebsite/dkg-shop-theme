/*
  DKG mobile header rotator + socials relocate.

  Mobile only:
  - Move the existing .dkg-header-picture-rotator out of the header.
  - Insert it below all homepage collection plates.
  - Move the existing .nav-social buttons below that framed image.
  - Do not clone the rotator or social links.
  - Restore everything back to original/header positions on desktop.

  This intentionally avoids editing header.php.
*/

(function () {
  "use strict";

  var MOBILE_QUERY = "(max-width: 767px)";
  var ZONE_CLASS = "dkg-mobile-relocated-header-rotator-zone";
  var SOCIALS_CLASS = "dkg-mobile-relocated-header-socials";
  var RELOCATED_ROTATOR_CLASS = "dkg-mobile-header-rotator-relocated";
  var RELOCATED_SOCIAL_CLASS = "dkg-mobile-social-relocated";
  var RESIZE_DEBOUNCE_MS = 160;

  var originalRotatorParent = null;
  var originalRotatorNextSibling = null;
  var originalRotatorWasCaptured = false;

  var originalSocials = [];
  var originalSocialsWereCaptured = false;

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

  function getNav() {
    return document.querySelector(".site-header .nav") || document.querySelector("nav.nav") || document.querySelector(".nav");
  }

  function getSocials() {
    var nav = getNav();

    if (!nav) {
      return [];
    }

    return toArray(nav.querySelectorAll(".nav-social")).concat(
      toArray(document.querySelectorAll("." + SOCIALS_CLASS + " .nav-social"))
    ).filter(function (node, index, arr) {
      return node && arr.indexOf(node) === index;
    });
  }

  function captureOriginalRotatorPosition(rotator) {
    if (originalRotatorWasCaptured || !rotator || !rotator.parentNode) {
      return;
    }

    originalRotatorParent = rotator.parentNode;
    originalRotatorNextSibling = rotator.nextSibling;
    originalRotatorWasCaptured = true;
  }

  function captureOriginalSocialPositions() {
    if (originalSocialsWereCaptured) {
      return;
    }

    var nav = getNav();

    if (!nav) {
      return;
    }

    var socials = toArray(nav.querySelectorAll(".nav-social"));

    originalSocials = socials.map(function (node, index) {
      return {
        node: node,
        parent: node.parentNode,
        nextSibling: node.nextSibling,
        index: index
      };
    });

    originalSocialsWereCaptured = true;
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

  function getOrCreateSocialZone(parentZone) {
    var existing = parentZone.querySelector("." + SOCIALS_CLASS);

    if (existing) {
      return existing;
    }

    var socialZone = document.createElement("div");
    socialZone.className = SOCIALS_CLASS;
    socialZone.setAttribute("aria-label", "Social links");

    parentZone.appendChild(socialZone);
    return socialZone;
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

  function moveRotatorBelowPlates(zone) {
    var rotator = getRotator();

    if (!rotator) {
      return;
    }

    captureOriginalRotatorPosition(rotator);

    if (rotator.parentNode !== zone) {
      /*
        Put the framed image first in the relocated zone.
      */
      zone.insertBefore(rotator, zone.firstChild);
    }

    rotator.classList.add(RELOCATED_ROTATOR_CLASS);
    rotator.setAttribute("data-dkg-mobile-relocated", "true");
    rotator.setAttribute("aria-hidden", "true");
  }

  function moveSocialsBelowRotator(zone) {
    captureOriginalSocialPositions();

    var socialZone = getOrCreateSocialZone(zone);
    var socials = getSocials();

    socials.forEach(function (social) {
      if (!social) {
        return;
      }

      social.classList.add(RELOCATED_SOCIAL_CLASS);
      social.setAttribute("data-dkg-mobile-social-relocated", "true");

      if (social.parentNode !== socialZone) {
        socialZone.appendChild(social);
      }
    });

    /*
      Ensure social row is after the rotator, not before it.
    */
    if (socialZone.parentNode === zone) {
      zone.appendChild(socialZone);
    }
  }

  function restoreRotatorToHeader() {
    var rotator = getRotator();

    if (!rotator || !originalRotatorParent) {
      return;
    }

    rotator.classList.remove(RELOCATED_ROTATOR_CLASS);
    rotator.removeAttribute("data-dkg-mobile-relocated");

    if (rotator.parentNode !== originalRotatorParent) {
      if (originalRotatorNextSibling && originalRotatorNextSibling.parentNode === originalRotatorParent) {
        originalRotatorParent.insertBefore(rotator, originalRotatorNextSibling);
      } else {
        originalRotatorParent.appendChild(rotator);
      }
    }
  }

  function restoreSocialsToHeader() {
    var nav = getNav();

    if (!nav) {
      return;
    }

    if (originalSocials.length) {
      originalSocials
        .slice()
        .sort(function (a, b) {
          return a.index - b.index;
        })
        .forEach(function (record) {
          var social = record.node;

          if (!social) {
            return;
          }

          social.classList.remove(RELOCATED_SOCIAL_CLASS);
          social.removeAttribute("data-dkg-mobile-social-relocated");

          /*
            The socials originally sit at the end of nav after Contact.
            Appending in original order is safer than trying to insert before
            siblings that may have also moved.
          */
          if (social.parentNode !== nav) {
            nav.appendChild(social);
          }
        });

      return;
    }

    /*
      Fallback if the page loaded in a strange state.
    */
    toArray(document.querySelectorAll("." + SOCIALS_CLASS + " .nav-social")).forEach(function (social) {
      social.classList.remove(RELOCATED_SOCIAL_CLASS);
      social.removeAttribute("data-dkg-mobile-social-relocated");
      nav.appendChild(social);
    });
  }

  function removeEmptyZone() {
    var zone = document.querySelector("." + ZONE_CLASS);

    if (!zone) {
      return;
    }

    var socialZone = zone.querySelector("." + SOCIALS_CLASS);

    if (socialZone && !socialZone.children.length && socialZone.parentNode) {
      socialZone.parentNode.removeChild(socialZone);
    }

    if (!zone.children.length && zone.parentNode) {
      zone.parentNode.removeChild(zone);
    }
  }

  function applyMobileLayout() {
    var rotator = getRotator();

    captureOriginalSocialPositions();

    if (rotator) {
      captureOriginalRotatorPosition(rotator);
    }

    var zone = getOrCreateZone();

    if (!insertZoneBelowCollections(zone)) {
      return;
    }

    if (rotator) {
      moveRotatorBelowPlates(zone);
    }

    moveSocialsBelowRotator(zone);
  }

  function applyDesktopLayout() {
    restoreSocialsToHeader();
    restoreRotatorToHeader();
    removeEmptyZone();
  }

  function applyLayout() {
    if (matchesMobile()) {
      applyMobileLayout();
    } else {
      applyDesktopLayout();
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
    Give the layout one extra pass after late-loaded/cached elements settle.
  */
  window.addEventListener("load", function () {
    window.setTimeout(applyLayout, 80);
  });
})();

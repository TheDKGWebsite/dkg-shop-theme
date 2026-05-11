// Theme JS placeholder

// === DKG LEFT FLOATING OVERLAY START ===
(function () {
  let scrollTimer = null;

  function showOverlay() {
    document.body.classList.add("dkg-overlay-ready");
    document.body.classList.remove("dkg-user-scrolling");
  }

  function hideOverlayWhileScrolling() {
    document.body.classList.add("dkg-user-scrolling");

    clearTimeout(scrollTimer);
    scrollTimer = setTimeout(function () {
      document.body.classList.remove("dkg-user-scrolling");
    }, 450);
  }

  window.addEventListener("load", function () {
    setTimeout(showOverlay, 250);
  });

  window.addEventListener("scroll", hideOverlayWhileScrolling, { passive: true });
})();
// === DKG LEFT FLOATING OVERLAY END ===

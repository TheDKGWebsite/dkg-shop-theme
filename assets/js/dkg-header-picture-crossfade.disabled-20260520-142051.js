/*
  DKG Header Picture Crossfade

  Purpose:
  Replaces the old single-image fade-away mechanic with a two-layer crossfade.

  How it finds images:
  1. It first looks for a JS array in the page source near the rotator, such as:
     dkgHeaderPictureImages = [...]
     DKG_HEADER_PICTURE_IMAGES = [...]
     headerPictureImages = [...]
  2. It then looks for data-images or data-image-urls on the rotator.
  3. If it cannot find a list, it keeps the current image visible and does not break the header.

  You can also force the image list manually by adding this before this script loads:
  window.DKG_HEADER_PICTURE_IMAGES = [
    "https://example.com/image1.jpg",
    "https://example.com/image2.jpg"
  ];
*/

(function () {
  "use strict";

  const ROTATOR_SELECTOR = ".dkg-header-picture-rotator";
  const FRAME_SELECTOR = ".dkg-header-picture-frame";
  const IMG_SELECTOR = ".dkg-header-picture-img";

  const DISPLAY_MS = 5000;
  const FADE_MS = 650;

  function uniqueCleanUrls(list) {
    return Array.from(new Set(
      (list || [])
        .map(x => String(x || "").trim())
        .filter(x => /^https?:\/\//i.test(x) || /\.(png|jpe?g|gif|webp|svg)(\?.*)?$/i.test(x))
    ));
  }

  function parseArrayFromScripts() {
    const scripts = Array.from(document.scripts || []);
    const names = [
      "DKG_HEADER_PICTURE_IMAGES",
      "dkgHeaderPictureImages",
      "dkg_header_picture_images",
      "headerPictureImages",
      "headerRotatorImages",
      "rotatorImages"
    ];

    for (const script of scripts) {
      const text = script.textContent || "";

      for (const name of names) {
        const re = new RegExp(name + "\\s*=\\s*(\\[[\\s\\S]*?\\])", "m");
        const match = text.match(re);

        if (match && match[1]) {
          try {
            const parsed = Function("return " + match[1])();
            const urls = uniqueCleanUrls(parsed);
            if (urls.length > 1) return urls;
          } catch (e) {}
        }
      }
    }

    return [];
  }

  function parseDataImages(rotator) {
    const raw =
      rotator.getAttribute("data-images") ||
      rotator.getAttribute("data-image-urls") ||
      rotator.dataset.images ||
      rotator.dataset.imageUrls ||
      "";

    if (!raw) return [];

    try {
      const parsed = JSON.parse(raw);
      const urls = uniqueCleanUrls(parsed);
      if (urls.length > 1) return urls;
    } catch (e) {}

    return uniqueCleanUrls(raw.split(/[,\n|]+/));
  }

  function getImageList(rotator, originalImg) {
    const globals = uniqueCleanUrls(
      window.DKG_HEADER_PICTURE_IMAGES ||
      window.dkgHeaderPictureImages ||
      window.dkg_header_picture_images ||
      window.headerPictureImages ||
      window.headerRotatorImages ||
      []
    );

    if (globals.length > 1) return globals;

    const dataUrls = parseDataImages(rotator);
    if (dataUrls.length > 1) return dataUrls;

    const scriptUrls = parseArrayFromScripts();
    if (scriptUrls.length > 1) return scriptUrls;

    const current = originalImg ? uniqueCleanUrls([originalImg.currentSrc || originalImg.src]) : [];
    return current;
  }

  function preload(url) {
    const img = new Image();
    img.src = url;
  }

  function setupRotator(rotator) {
    if (!rotator || rotator.dataset.dkgCrossfadeReady === "1") return;
    rotator.dataset.dkgCrossfadeReady = "1";

    const frame = rotator.querySelector(FRAME_SELECTOR) || rotator;
    const originalImg = frame.querySelector(IMG_SELECTOR);

    if (!originalImg) return;

    const images = getImageList(rotator, originalImg);

    if (!images.length) {
      originalImg.classList.add("is-active");
      return;
    }

    images.forEach(preload);

    /*
      Stop the old visual fade class from making the only image disappear.
      We are now taking over the visible animation.
    */
    originalImg.classList.remove("is-fading");
    originalImg.classList.add("dkg-header-picture-img-layer", "is-active");

    const layerA = originalImg;
    const layerB = originalImg.cloneNode(true);

    layerB.classList.remove("is-active", "is-fading");
    layerB.classList.add("dkg-header-picture-img-layer");
    layerB.setAttribute("aria-hidden", "true");

    frame.appendChild(layerB);

    let activeLayer = layerA;
    let hiddenLayer = layerB;

    let currentIndex = Math.max(0, images.indexOf(layerA.currentSrc || layerA.src));
    if (!images[currentIndex]) {
      currentIndex = 0;
      layerA.src = images[0];
    }

    /*
      Try to silence old single-image source swaps.
      If the old script changes the first image's src, we snap it back to the active image.
    */
    const observer = new MutationObserver(() => {
      if (activeLayer === layerA && layerA.src !== images[currentIndex]) {
        layerA.src = images[currentIndex];
      }
      layerA.classList.remove("is-fading");
      layerB.classList.remove("is-fading");
    });

    observer.observe(layerA, {
      attributes: true,
      attributeFilter: ["src", "class"]
    });

    function crossfadeTo(nextIndex) {
      const nextUrl = images[nextIndex];
      if (!nextUrl) return;

      hiddenLayer.src = nextUrl;
      hiddenLayer.classList.remove("is-fading");

      // Force browser to register opacity 0 before fading in.
      hiddenLayer.offsetHeight;

      hiddenLayer.classList.add("is-active");
      activeLayer.classList.remove("is-active");

      const oldActive = activeLayer;
      activeLayer = hiddenLayer;
      hiddenLayer = oldActive;
      currentIndex = nextIndex;

      window.setTimeout(() => {
        hiddenLayer.classList.remove("is-active", "is-fading");
      }, FADE_MS + 80);
    }

    if (images.length > 1) {
      window.setInterval(() => {
        const nextIndex = (currentIndex + 1) % images.length;
        crossfadeTo(nextIndex);
      }, DISPLAY_MS);
    }
  }

  function boot() {
    document.querySelectorAll(ROTATOR_SELECTOR).forEach(setupRotator);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();

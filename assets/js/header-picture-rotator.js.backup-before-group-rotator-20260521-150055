(function () {
  "use strict";

  function parseImages(raw) {
    if (!raw) return [];

    try {
      var parsed = JSON.parse(raw);
      if (Array.isArray(parsed)) {
        return parsed.filter(Boolean);
      }
    } catch (e) {}

    return raw
      .split(",")
      .map(function (item) { return item.trim(); })
      .filter(Boolean);
  }

  function preloadImages(images) {
    images.forEach(function (src) {
      var preloaded = new Image();
      preloaded.src = src;
    });
  }

  function startRotator(rotator) {
    if (!rotator || rotator.dataset.dkgRotatorReady === "1") return;
    rotator.dataset.dkgRotatorReady = "1";

    var frame = rotator.querySelector(".dkg-header-picture-frame") || rotator;
    var firstImg = rotator.querySelector(".dkg-header-picture-img");
    if (!firstImg) return;

    var images = parseImages(rotator.getAttribute("data-images"));
    if (!images.length) return;

    var interval = parseInt(rotator.getAttribute("data-interval") || "5000", 10);
    if (!interval || interval < 1000) interval = 5000;

    var fadeMs = 650;
    var index = 0;

    preloadImages(images);

    /*
      Two-layer crossfade:
      - active layer fades out
      - hidden layer gets next image and fades in
      - no blank frame/background flash
    */

    firstImg.src = images[0];
    firstImg.classList.remove("is-fading");
    firstImg.classList.add("dkg-header-picture-img-layer", "is-active");

    var secondImg = firstImg.cloneNode(true);
    secondImg.classList.remove("is-active", "is-fading");
    secondImg.classList.add("dkg-header-picture-img-layer");
    secondImg.setAttribute("aria-hidden", "true");
    frame.appendChild(secondImg);

    var activeLayer = firstImg;
    var hiddenLayer = secondImg;
    var isAnimating = false;

    function swapToNext() {
      if (isAnimating || images.length < 2) return;
      isAnimating = true;

      index = (index + 1) % images.length;

      hiddenLayer.src = images[index];

      /*
        Make sure the browser sees hiddenLayer at opacity 0
        before we add is-active.
      */
      hiddenLayer.offsetHeight;

      hiddenLayer.classList.add("is-active");
      activeLayer.classList.remove("is-active");

      window.setTimeout(function () {
        var oldActive = activeLayer;
        activeLayer = hiddenLayer;
        hiddenLayer = oldActive;

        hiddenLayer.classList.remove("is-active", "is-fading");

        isAnimating = false;
      }, fadeMs + 80);
    }

    if (images.length >= 2) {
      window.setInterval(swapToNext, interval);
    }
  }

  function init() {
    document.querySelectorAll(".dkg-header-picture-rotator").forEach(startRotator);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();

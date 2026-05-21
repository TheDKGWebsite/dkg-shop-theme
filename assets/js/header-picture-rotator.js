(function () {
  "use strict";

  function parseImages(raw) {
    if (!raw) return [];

    try {
      var parsed = JSON.parse(raw);
      if (Array.isArray(parsed)) {
        return parsed.map(String).filter(Boolean);
      }
    } catch (e) {}

    return String(raw)
      .split(",")
      .map(function (item) { return item.trim(); })
      .filter(Boolean);
  }

  function uniqueImages(images) {
    var seen = {};
    return images.filter(function (src) {
      if (!src || seen[src]) return false;
      seen[src] = true;
      return true;
    });
  }

  function preloadImages(images) {
    images.forEach(function (src) {
      var preloaded = new Image();
      preloaded.src = src;
    });
  }

  function randomFromGroup(group, avoidUrl) {
    if (!group || !group.length) return "";

    var choices = group.slice();

    if (avoidUrl && choices.length > 1) {
      choices = choices.filter(function (src) {
        return src !== avoidUrl;
      });
    }

    return choices[Math.floor(Math.random() * choices.length)];
  }

  function startRotator(rotator) {
    if (!rotator || rotator.dataset.dkgRotatorReady === "1") return;
    rotator.dataset.dkgRotatorReady = "1";

    var frame = rotator.querySelector(".dkg-header-picture-frame") || rotator;
    var firstImg = rotator.querySelector(".dkg-header-picture-img");
    if (!firstImg) return;

    var group1 = uniqueImages(parseImages(rotator.getAttribute("data-image-group-1")));
    var group2 = uniqueImages(parseImages(rotator.getAttribute("data-image-group-2")));

    /*
      Backward compatibility:
      If the PHP only has the old data-images attribute,
      use the old single-list behavior.
    */
    var oldImages = uniqueImages(parseImages(rotator.getAttribute("data-images")));

    var groups = [];

    if (group1.length) {
      groups.push({
        name: "group1",
        images: group1,
        last: ""
      });
    }

    if (group2.length) {
      groups.push({
        name: "group2",
        images: group2,
        last: ""
      });
    }

    if (!groups.length && oldImages.length) {
      groups.push({
        name: "old",
        images: oldImages,
        last: ""
      });
    }

    if (!groups.length) return;

    var allImages = [];
    groups.forEach(function (group) {
      allImages = allImages.concat(group.images);
    });

    var interval = parseInt(rotator.getAttribute("data-interval") || "5000", 10);
    if (!interval || interval < 1000) interval = 5000;

    var fadeMs = 650;
    var currentSrc = firstImg.getAttribute("src") || "";

    preloadImages(allImages);

    /*
      Two-layer crossfade:
      - active layer fades out
      - hidden layer gets next image and fades in
      - no blank frame/background flash
    */

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

    /*
      groupPointer decides which group gets picked next.

      If both groups exist:
        first automatic swap uses group 2,
        because PHP initially shows a random group 1 image.

      Then it alternates:
        group 2 -> group 1 -> group 2 -> group 1
    */
    var groupPointer = groups.length >= 2 ? 1 : 0;

    function getNextImage() {
      var group = groups[groupPointer];
      var nextSrc = randomFromGroup(group.images, group.last || currentSrc);

      group.last = nextSrc;
      currentSrc = nextSrc;

      if (groups.length >= 2) {
        groupPointer = (groupPointer + 1) % groups.length;
      }

      return nextSrc;
    }

    function swapToNext() {
      if (isAnimating || allImages.length < 2) return;

      var nextSrc = getNextImage();
      if (!nextSrc) return;

      isAnimating = true;

      hiddenLayer.src = nextSrc;

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

    if (allImages.length >= 2) {
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

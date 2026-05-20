(function () {
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

  function startRotator(rotator) {
    var img = rotator.querySelector(".dkg-header-picture-img");
    if (!img) return;

    var images = parseImages(rotator.getAttribute("data-images"));
    if (!images.length) return;

    var interval = parseInt(rotator.getAttribute("data-interval") || "5000", 10);
    if (!interval || interval < 1000) interval = 5000;

    var index = 0;

    images.forEach(function (src) {
      var preload = new Image();
      preload.src = src;
    });

    img.src = images[0];

    if (images.length < 2) return;

    window.setInterval(function () {
      index = (index + 1) % images.length;

      img.classList.add("is-fading");

      window.setTimeout(function () {
        img.src = images[index];
        img.classList.remove("is-fading");
      }, 250);
    }, interval);
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

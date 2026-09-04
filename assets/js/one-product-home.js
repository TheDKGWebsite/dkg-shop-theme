(function () {
  'use strict';

  function initGallery() {
    var main = document.querySelector('[data-main-img]');
    var thumbs = Array.prototype.slice.call(document.querySelectorAll('.dkg-thumb[data-full]'));
    if (!main || !thumbs.length) return;

    thumbs.forEach(function (thumb) {
      thumb.addEventListener('click', function () {
        var full = thumb.getAttribute('data-full');
        var alt = thumb.getAttribute('data-alt') || '';
        if (!full || main.getAttribute('src') === full) return;

        main.classList.add('is-changing');
        window.setTimeout(function () {
          main.removeAttribute('srcset');
          main.removeAttribute('sizes');
          main.setAttribute('src', full);
          main.setAttribute('alt', alt);
          main.classList.remove('is-changing');
        }, 120);

        thumbs.forEach(function (item) {
          var active = item === thumb;
          item.classList.toggle('is-active', active);
          item.setAttribute('aria-pressed', active ? 'true' : 'false');
        });
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initGallery);
  } else {
    initGallery();
  }
})();

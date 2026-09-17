(function () {
  'use strict';

  function initGallery() {
    var mainImage = document.querySelector('[data-main-img]');
    var mainVideo = document.querySelector('[data-main-video]');
    var thumbs = Array.prototype.slice.call(document.querySelectorAll('.dkg-thumb[data-media-type]'));
    if (!thumbs.length || (!mainImage && !mainVideo)) return;

    function setActiveThumb(activeThumb) {
      thumbs.forEach(function (item) {
        var active = item === activeThumb;
        item.classList.toggle('is-active', active);
        item.setAttribute('aria-pressed', active ? 'true' : 'false');
      });
    }

    thumbs.forEach(function (thumb) {
      thumb.addEventListener('click', function () {
        var mediaType = thumb.getAttribute('data-media-type');

        if (mediaType === 'video' && mainVideo) {
          if (mainImage) mainImage.hidden = true;
          mainVideo.hidden = false;
          mainVideo.currentTime = 0;
          var playPromise = mainVideo.play();
          if (playPromise && typeof playPromise.catch === 'function') {
            playPromise.catch(function () {});
          }
          setActiveThumb(thumb);
          return;
        }

        if (mediaType === 'image' && mainImage) {
          var full = thumb.getAttribute('data-full');
          var alt = thumb.getAttribute('data-alt') || '';
          if (!full) return;

          if (mainVideo) {
            mainVideo.pause();
            mainVideo.hidden = true;
          }

          mainImage.classList.add('is-changing');
          window.setTimeout(function () {
            mainImage.removeAttribute('srcset');
            mainImage.removeAttribute('sizes');
            mainImage.setAttribute('src', full);
            mainImage.setAttribute('alt', alt);
            mainImage.hidden = false;
            mainImage.classList.remove('is-changing');
          }, 120);

          setActiveThumb(thumb);
        }
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initGallery);
  } else {
    initGallery();
  }
})();

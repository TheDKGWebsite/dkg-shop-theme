function setupAutoLoop(shell, shellIndex) {
      const track = shell.querySelector('.product-track');
      if (!track) return;

      const originalCards = Array.from(track.children);
      const originalCount = originalCards.length;

      if (originalCount <= 5) {
        return;
      }

      originalCards.forEach(card => {
        const clone = card.cloneNode(true);
        clone.setAttribute('aria-hidden', 'true');
        track.appendChild(clone);
      });

      let stepWidth = 0;
      const transitionMs = 500;

      const delayOptions = [1400, 1750, 2100, 1600, 1950, 2300];
      const startOffsetOptions = [0, 2, 1, 3, 4, 2];

      const autoDelay = delayOptions[shellIndex % delayOptions.length];
      let index = startOffsetOptions[shellIndex % startOffsetOptions.length] % originalCount;

      function measureStepWidth() {
        const firstCard = track.querySelector('.product-card');
        if (!firstCard) return 0;
        const cardWidth = firstCard.getBoundingClientRect().width;
        const styles = window.getComputedStyle(track);
        const gap = parseFloat(styles.gap || styles.columnGap || 0);
        return cardWidth + gap;
      }

      function render(animated = true) {
        stepWidth = measureStepWidth();
        track.style.transition = animated ? `transform ${transitionMs}ms ease` : 'none';
        track.style.transform = `translateX(-${index * stepWidth}px)`;
      }

      function nextStep() {
        index += 1;
        render(true);

        if (index >= originalCount) {
          setTimeout(() => {
            index = 0;
            render(false);
          }, transitionMs + 30);
        }
      }

      window.addEventListener('resize', () => {
        render(false);
      });

      render(false);

      const initialDelay = 250 + (shellIndex * 180);
      setTimeout(() => {
        setInterval(nextStep, autoDelay);
      }, initialDelay);
    }

    document.querySelectorAll('.auto-loop').forEach((shell, index) => {
      setupAutoLoop(shell, index);
    });

/* === DKG HOMEPAGE ZOOM COUNTER START === */

(function () {
  /*
    Browser zoom counter for homepage fixed-stage layout.

    Chrome Ctrl+/Ctrl- changes window.devicePixelRatio.
    We store a base DPR, then counter-scale the homepage stage by:

      baseDPR / currentDPR

    To reset the base after returning browser zoom to 100%, open:
      /?reset_home_zoom_base=1
  */

  function isHomePage() {
    return document.body.classList.contains('home') ||
           document.body.classList.contains('front-page') ||
           document.body.classList.contains('page-template-front-page');
  }

  function getBaseDpr() {
    var params = new URLSearchParams(window.location.search);
    var reset = params.get('reset_home_zoom_base') === '1';

    if (reset) {
      try {
        localStorage.removeItem('dkgHomeBaseDPR');
      } catch (e) {}
    }

    var current = window.devicePixelRatio || 1;
    var stored = null;

    try {
      stored = parseFloat(localStorage.getItem('dkgHomeBaseDPR'));
    } catch (e) {
      stored = null;
    }

    if (!stored || !isFinite(stored) || stored <= 0 || reset) {
      stored = current;
      try {
        localStorage.setItem('dkgHomeBaseDPR', String(stored));
      } catch (e) {}
    }

    return stored;
  }

  var baseDpr = getBaseDpr();

  function applyZoomCounter() {
    if (!isHomePage()) return;

    var currentDpr = window.devicePixelRatio || 1;
    var counter = baseDpr / currentDpr;

    /*
      Clamp it so extreme zoom does not make the site ridiculous.
      You can loosen these if you want.
    */
    counter = Math.max(0.45, Math.min(1.75, counter));

    document.documentElement.style.setProperty('--dkg-browser-zoom-counter', String(counter));
  }

  applyZoomCounter();

  window.addEventListener('resize', applyZoomCounter, { passive: true });
  window.addEventListener('orientationchange', applyZoomCounter, { passive: true });

  if (window.visualViewport) {
    window.visualViewport.addEventListener('resize', applyZoomCounter, { passive: true });
  }

  setInterval(applyZoomCounter, 350);
})();

/* === DKG HOMEPAGE ZOOM COUNTER END === */

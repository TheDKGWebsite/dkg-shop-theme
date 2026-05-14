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


/* === DKG DESKTOP FIXED-STAGE START === */
/*
   Scales the 1920x1080 homepage canvas proportionally on desktop.

   This preserves the same visual composition across:
   - 1080p monitors
   - 1440p monitors
   - ultrawide monitors
   - laptop screens
*/

(function () {
  const DESIGN_WIDTH = 1920;
  const DESIGN_HEIGHT = 1080;
  const DESKTOP_MIN_WIDTH = 901;

  function dkgScaleDesktopStage() {
    const stage = document.querySelector(".dkg-fixed-stage");
    const canvas = document.querySelector(".dkg-fixed-canvas");

    if (!stage || !canvas) {
      return;
    }

    if (window.innerWidth < DESKTOP_MIN_WIDTH) {
      canvas.style.transform = "";
      stage.style.paddingBottom = "";
      return;
    }

    const availableWidth = window.innerWidth;

    /*
       Header is outside the scaled canvas, so subtract a rough header height.
       Your inspected CSS/header setup uses a 100px header height.
    */
    const header = document.querySelector(".site-header");
    const headerHeight = header ? header.getBoundingClientRect().height : 100;
    const availableHeight = Math.max(400, window.innerHeight - headerHeight);

    const scaleX = availableWidth / DESIGN_WIDTH;
    const scaleY = availableHeight / DESIGN_HEIGHT;

    /*
       Use contain-fit:
       Everyone sees the whole designed layout.
       This may create side/top breathing room on unusual aspect ratios,
       but it prevents cropping.
    */
    const scale = Math.min(scaleX, scaleY);

    canvas.style.transform = "translateX(-50%) scale(" + scale + ")";

    /*
       Transformed elements do not affect normal document height.
       This reserves the correct scaled height so the footer lands below it.
    */
    stage.style.paddingBottom = Math.ceil(DESIGN_HEIGHT * scale) + "px";
  }

  let dkgScaleTimer = null;

  function dkgScheduleScale() {
    window.clearTimeout(dkgScaleTimer);
    dkgScaleTimer = window.setTimeout(dkgScaleDesktopStage, 50);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", dkgScaleDesktopStage);
  } else {
    dkgScaleDesktopStage();
  }

  window.addEventListener("resize", dkgScheduleScale);
  window.addEventListener("orientationchange", dkgScheduleScale);
  window.addEventListener("load", dkgScaleDesktopStage);
})();
/* === DKG DESKTOP FIXED-STAGE END === */


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

// Shared motion helpers. Load this before the other scripts.
// Plain scripts, not modules: modules do not load from file://, and the site must open from disk.
window.Motion = (() => {
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const canHover = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  const scrambleGlyphs = '!<>-_\\/[]{}=+*^?#01';

  // Text decodes from random characters into its real value, once.
  function scramble(element) {
    if (reduceMotion || element.dataset.scrambled) {
      return;
    }
    element.dataset.scrambled = 'true';
    const finalText = element.textContent;
    let frame = 0;

    const tick = () => {
      const revealedCount = Math.floor(frame / 2);
      element.textContent = [...finalText]
        .map((character, index) => {
          if (index < revealedCount || character === ' ') {
            return character;
          }
          return scrambleGlyphs[Math.floor(Math.random() * scrambleGlyphs.length)];
        })
        .join('');
      frame += 1;
      if (revealedCount < finalText.length) {
        requestAnimationFrame(tick);
      }
    };
    tick();
  }

  return { reduceMotion, canHover, scramble };
})();

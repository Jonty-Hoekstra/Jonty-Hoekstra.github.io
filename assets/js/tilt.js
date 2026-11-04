// Elements marked data-tilt lean toward the pointer, with a moving glare. Mouse only.
(() => {
  if (!window.Motion.canHover || window.Motion.reduceMotion) {
    return;
  }

  const MAX_TILT_DEGREES = 7;

  document.querySelectorAll('[data-tilt]').forEach((element) => {
    element.addEventListener('pointermove', (event) => {
      const box = element.getBoundingClientRect();
      const x = (event.clientX - box.left) / box.width;
      const y = (event.clientY - box.top) / box.height;
      element.style.setProperty('--tilt-y', `${(x - 0.5) * 2 * MAX_TILT_DEGREES}deg`);
      element.style.setProperty('--tilt-x', `${(0.5 - y) * 2 * MAX_TILT_DEGREES}deg`);
      element.style.setProperty('--glare-x', `${x * 100}%`);
      element.style.setProperty('--glare-y', `${y * 100}%`);
    });

    element.addEventListener('pointerleave', () => {
      element.style.setProperty('--tilt-x', '0deg');
      element.style.setProperty('--tilt-y', '0deg');
    });
  });
})();

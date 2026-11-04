// Elements marked .reveal fade up as they scroll into view. Headings inside them decode.
(() => {
  const elements = document.querySelectorAll('.reveal');
  if (!elements.length) {
    return;
  }

  // Siblings reveal one after another.
  elements.forEach((element) => {
    const siblings = [...element.parentElement.children].filter((child) => child.classList.contains('reveal'));
    element.style.setProperty('--reveal-order', siblings.indexOf(element));
  });

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) {
        return;
      }
      entry.target.classList.add('is-visible');
      entry.target.querySelectorAll('[data-scramble]').forEach(window.Motion.scramble);
      observer.unobserve(entry.target);
    });
  }, { threshold: 0.15 });

  elements.forEach((element) => observer.observe(element));
})();

// Side panel: page progress bar, and the ▶ marker that follows the section in view.
(() => {
  const panel = document.querySelector('[data-panel]');
  if (!panel) {
    return;
  }

  const progressFill = panel.querySelector('[data-panel-progress]');
  const marker = panel.querySelector('[data-panel-marker]');
  const links = [...panel.querySelectorAll('[data-panel-nav] a')];

  function updateProgress() {
    const scrollable = document.documentElement.scrollHeight - window.innerHeight;
    const progress = scrollable > 0 ? window.scrollY / scrollable : 0;
    progressFill.style.setProperty('--page-progress', progress.toFixed(3));
  }

  function setActive(link) {
    links.forEach((other) => other.classList.toggle('is-active', other === link));
    if (marker && link) {
      marker.style.transform = `translateY(${link.offsetTop}px)`;
    }
  }

  // A project page marks its own entry with data-panel-current; it does not track sections.
  const currentLink = links.find((link) => link.hasAttribute('data-panel-current'));
  if (currentLink) {
    setActive(currentLink);
  } else {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          setActive(links.find((link) => link.hash === `#${entry.target.id}`));
        }
      });
    }, { rootMargin: '-40% 0px -55% 0px' });
    document.querySelectorAll('main section[id]').forEach((section) => observer.observe(section));
  }

  window.addEventListener('scroll', updateProgress, { passive: true });
  window.addEventListener('resize', () => setActive(links.find((link) => link.classList.contains('is-active'))));
  updateProgress();
})();

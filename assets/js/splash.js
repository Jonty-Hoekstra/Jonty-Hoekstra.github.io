// Home page splash: drifting particles, pointer spotlight, keyboard menu,
// and the hand-over to the side panel once the splash scrolls away.
(() => {
  const splash = document.querySelector('[data-splash]');
  if (!splash) {
    return;
  }

  const DOCK_AT_PROGRESS = 0.6;
  const MOTE_COUNT = 28;

  function addMotes() {
    const container = splash.querySelector('[data-splash-motes]');
    if (!container || window.Motion.reduceMotion) {
      return;
    }
    for (let index = 0; index < MOTE_COUNT; index += 1) {
      const mote = document.createElement('i');
      mote.className = 'splash__mote';
      mote.style.left = `${Math.random() * 100}%`;
      mote.style.top = `${55 + Math.random() * 45}%`;
      mote.style.animationDuration = `${4 + Math.random() * 6}s`;
      mote.style.animationDelay = `${-Math.random() * 8}s`;
      container.appendChild(mote);
    }
  }

  function followPointer() {
    if (!window.Motion.canHover) {
      return;
    }
    splash.addEventListener('pointermove', (event) => {
      splash.style.setProperty('--pointer-x', `${event.clientX}px`);
      splash.style.setProperty('--pointer-y', `${event.clientY}px`);
    });
  }

  function setUpMenu() {
    const links = [...splash.querySelectorAll('[data-splash-menu] a')];
    let selectedIndex = 0;

    const select = (index) => {
      links[selectedIndex].classList.remove('is-selected');
      selectedIndex = index;
      links[selectedIndex].classList.add('is-selected');
    };

    links.forEach((link, index) => {
      link.addEventListener('mouseenter', () => select(index));
      link.addEventListener('focus', () => select(index));
    });

    document.addEventListener('keydown', (event) => {
      if (document.body.classList.contains('is-docked')) {
        return;
      }
      if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
        event.preventDefault();
        const step = event.key === 'ArrowDown' ? 1 : links.length - 1;
        select((selectedIndex + step) % links.length);
        links[selectedIndex].focus();
      }
    });
  }

  function trackScroll() {
    const update = () => {
      const progress = Math.min(window.scrollY / splash.offsetHeight, 1);
      if (!window.Motion.reduceMotion) {
        splash.style.setProperty('--scroll-progress', progress.toFixed(3));
      }
      document.body.classList.toggle('is-docked', progress > DOCK_AT_PROGRESS);
    };
    window.addEventListener('scroll', update, { passive: true });
    update();
  }

  window.Motion.scramble(splash.querySelector('[data-scramble]'));
  addMotes();
  followPointer();
  setUpMenu();
  trackScroll();
})();

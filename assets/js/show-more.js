// A list marked data-show-more="N" shows its first N items, then a "+X more" tile that reveals
// the rest. Without JavaScript every item shows.
(() => {
  document.querySelectorAll('[data-show-more]').forEach((list) => {
    const visibleCount = Number(list.dataset.showMore);
    const items = [...list.children];
    const hiddenItems = items.slice(visibleCount);
    if (!hiddenItems.length) {
      return;
    }

    hiddenItems.forEach((item) => {
      item.hidden = true;
    });

    const moreItem = document.createElement('li');
    moreItem.className = 'thumbs__item';
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'thumbs__more';
    button.innerHTML = `<span class="thumbs__more-count">+${hiddenItems.length}</span><span class="thumbs__more-label">more</span>`;
    button.setAttribute('aria-label', `Show ${hiddenItems.length} more screenshots`);
    moreItem.appendChild(button);
    list.appendChild(moreItem);

    button.addEventListener('click', () => {
      hiddenItems.forEach((item) => {
        item.hidden = false;
      });
      moreItem.remove();
      // Move focus to the first newly shown screenshot, so keyboard users continue from there.
      hiddenItems[0].querySelector('a').focus();
    });
  });
})();

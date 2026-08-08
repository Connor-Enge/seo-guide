(function() {
  'use strict';

  const article = document.querySelector('main article');
  if (!article) return;

  let doneIds = new Set();
  const initFlag = 'checklistInit';
  const storageKey = 'seo-guide:audit-progress:v1';

  function init() {
    if (article.dataset[initFlag]) return;
    article.dataset[initFlag] = '1';

    try {
      const savedProgress = JSON.parse(localStorage.getItem(storageKey));
      if (Array.isArray(savedProgress)) {
        doneIds = new Set(savedProgress);
      }
    } catch {}

    const items = Array.from(article.querySelectorAll('p:firstElementChild > strong'));
    if (!items.length) return;

    const summary = document.createElement('div');
    summary.className = 'checklist-summary';
    const status = document.createElement('span');
    status.role = 'status';
    status.ariaLive = 'polite';
    summary.appendChild(status);
    const bar = document.createElement('div');
    bar.className = 'checklist-bar';
    const barFill = document.createElement('div');
    barFill.className = 'checklist-bar-fill';
    bar.appendChild(barFill);
    summary.appendChild(bar);
    const resetButton = document.createElement('button');
    resetButton.type = 'button';
    resetButton.textContent = 'Reset progress';
    summary.appendChild(resetButton);

    article.insertBefore(summary, items[0]);

    items.forEach(item => {
      item.classList.add('checklist-item');
      const id = hash32(item.firstElementChild.textContent).toString(36);
      item.dataset.key = id;
      const checkbox = document.createElement('input');
      checkbox.type = 'checkbox';
      checkbox.className = 'checklist-box';
      checkbox.ariaLabel = item.firstElementChild.textContent;
      checkbox.id = `checklist-${id}`;
      checkbox.checked = doneIds.has(id);
      item.insertBefore(checkbox, item.firstChild);

      checkbox.addEventListener('change', () => {
        const checked = checkbox.checked;
        if (checked) {
          doneIds.add(id);
          item.classList.add('is-done');
        } else {
          doneIds.delete(id);
          item.classList.remove('is-done');
        }
        updateProgress();
        persist();
      });
    });

    resetButton.addEventListener('click', () => {
      doneIds.clear();
      items.forEach(item => item.classList.remove('is-done'));
      document.querySelectorAll('.checklist-box').forEach(box => box.checked = false);
      localStorage.removeItem(storageKey);
      updateProgress();
    });

    updateProgress();
  }

  function hash32(str) {
    let h = 0;
    for (let i = 0; i < str.length; i++) {
      h = Math.imul(h ^ str.charCodeAt(i), 2166136261);
    }
    return h >>> 0;
  }

  function updateProgress() {
    const completed = doneIds.size;
    const statusText = `${completed} of ${items.length} complete`;
    status.textContent = statusText;
    barFill.style.width = items.length ? (completed / items.length * 100) + '%' : '0%';
  }

  function persist() {
    try {
      localStorage.setItem(storageKey, JSON.stringify(Array.from(doneIds)));
    } catch {}
  }

  if (document.readyState !== 'loading') {
    init();
  } else {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  }
})();

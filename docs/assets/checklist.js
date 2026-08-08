(function() {
    'use strict';

    const article = document.querySelector('main article');
    if (!article || article.getAttribute('data-checklist-init')) return;
    article.setAttribute('data-checklist-init', '');

    function hash(str) {
        let hash = 0, i, chr;
        for (i = 0; i < str.length; i++) {
            chr   = str.charCodeAt(i);
            hash  = ((hash << 5) - hash) + chr;
            hash |= 0; // Convert to 32bit integer
        }
        return Math.abs(hash).toString(16);
    }

    function initChecklist() {
        const checklistItems = [];
        article.querySelectorAll('p').forEach(p => {
            if (p.firstElementChild && p.firstElementChild.tagName === 'STRONG') {
                checklistItems.push(p);
            }
        });

        if (!checklistItems.length) return;

        let doneIds = new Set();
        try {
            const storedProgress = localStorage.getItem('seo-guide:audit-progress:v1');
            if (storedProgress) {
                doneIds = new Set(JSON.parse(storedProgress));
            }
        } catch {}

        checklistItems.forEach(p => {
            const strongText = p.firstElementChild.textContent.trim().slice(0, 120);
            const itemId = hash(strongText);
            p.classList.add('checklist-item');
            p.setAttribute('data-key', itemId);

            if (doneIds.has(itemId)) {
                p.classList.add('is-done');
            }

            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.id = `checklist-${itemId}`;
            checkbox.ariaLabel = strongText;
            checkbox.className = 'checklist-box';
            checkbox.checked = doneIds.has(itemId);
            checkbox.addEventListener('change', () => {
                if (checkbox.checked) {
                    p.classList.add('is-done');
                    doneIds.add(itemId);
                } else {
                    p.classList.remove('is-done');
                    doneIds.delete(itemId);
                }
                updateProgress();
                try {
                    localStorage.setItem('seo-guide:audit-progress:v1', JSON.stringify(Array.from(doneIds)));
                } catch {}
            });
            p.insertBefore(checkbox, p.firstChild);

            const summary = document.createElement('div');
            summary.className = 'checklist-summary';
            summary.setAttribute('role', 'status');
            summary.setAttribute('aria-live', 'polite');

            const progressText = document.createElement('span');
            progressText.textContent = `0 of ${checklistItems.length} complete`;
            summary.appendChild(progressText);

            const progressBar = document.createElement('div');
            progressBar.className = 'checklist-bar';
            const progressFill = document.createElement('div');
            progressFill.className = 'checklist-bar-fill';
            progressBar.appendChild(progressFill);
            summary.appendChild(progressBar);

            const resetButton = document.createElement('button');
            resetButton.type = 'button';
            resetButton.textContent = 'Reset progress';
            resetButton.addEventListener('click', () => {
                doneIds.clear();
                checklistItems.forEach(p => p.classList.remove('is-done'));
                updateProgress();
                try {
                    localStorage.removeItem('seo-guide:audit-progress:v1');
                } catch {}
            });
            summary.appendChild(resetButton);

            article.insertBefore(summary, checklistItems[0]);
        });

        function updateProgress() {
            const completed = Array.from(doneIds).length;
            const progressText = document.querySelector('.checklist-summary span');
            progressText.textContent = `${completed} of ${checklistItems.length} complete`;
            const progressBarFill = document.querySelector('.checklist-bar-fill');
            progressBarFill.style.width = `${(completed / checklistItems.length) * 100}%`;
        }

        updateProgress();
    }

    initChecklist();

    if (document.readyState === 'complete') {
        initChecklist();
    } else {
        window.addEventListener('DOMContentLoaded', initChecklist);
    }
})();

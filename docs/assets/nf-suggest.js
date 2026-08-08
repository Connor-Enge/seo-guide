(function() {
    'use strict';

    function getAttemptedQuery() {
        try {
            var pathParts = location.pathname.split('/').filter(Boolean);
            var q = decodeURIComponent(pathParts[pathParts.length - 1]).replace(/[-_+]/g, ' ').replace(/\s+/g, ' ').trim().toLowerCase();
            return q;
        } catch (e) {}
    }

    function addDidYouMean() {
        try {
            var q = getAttemptedQuery();
            if (!q || ['404', 'index', 'home'].includes(q)) return;

            if (document.querySelector('.nf-didyoumean')) return;

            var queryTokens = q.split(/\s+/).filter(t => t.length >= 2);
            var candidates = [];

            document.querySelectorAll('.related-list li a').forEach(anchor => {
                var candidateText = anchor.textContent.toLowerCase().trim();
                var seg = decodeURIComponent(anchor.href).split('/').filter(Boolean).pop() || '';
                var candidateSlug = seg.replace(/[-_+]/g, ' ').toLowerCase().split(/\s+/).filter(Boolean);
                var score = 0;

                queryTokens.forEach(token => {
                    if (candidateText.indexOf(token) !== -1) score++;
                    if (candidateSlug.some(slugToken => slugToken === token)) score++;
                });

                if (candidateText.indexOf(q) !== -1 || q.indexOf(candidateText) !== -1) score += 2;

                if (score > 0) {
                    candidates.push({ anchor, score });
                }
            });

            candidates.sort((a, b) => b.score - a.score);
            candidates = candidates.slice(0, 3);

            if (candidates.length === 0) return;

            var nav = document.createElement('nav');
            nav.className = 'nf-didyoumean';
            nav.setAttribute('aria-labelledby', 'nf-dym-h');

            var header = document.createElement('p');
            header.id = 'nf-dym-h';
            header.textContent = 'Did you mean:';
            nav.appendChild(header);

            var ul = document.createElement('ul');
            candidates.forEach(candidate => {
                var li = document.createElement('li');
                li.appendChild(candidate.anchor.cloneNode(true));
                ul.appendChild(li);
            });
            nav.appendChild(ul);

            if (document.querySelector('.searchform')) {
                document.querySelector('.searchform').insertAdjacentElement('beforebegin', nav);
            } else if (document.querySelector('main')) {
                document.querySelector('main').prepend(nav);
            } else {
                document.body.prepend(nav);
            }

            var style = document.createElement('style');
            if (!document.head.querySelector('style[data-nfdym]')) {
                style.setAttribute('data-nfdym', '');
                style.textContent = '.nf-didyoumean { margin: 0.5rem; } ul { list-style: none; padding-left: 0; margin: 0.25rem 0; } #nf-dym-h { font-weight: bold; }';
                document.head.appendChild(style);
            }
        } catch (e) {}
    }

    function init() {
        try {
            var input = document.getElementById('nf-q');
            if (input) {
                var q = getAttemptedQuery();
                if (q && !['404', 'index', 'home'].includes(q) && !/^\d+$/.test(q) && !input.value.trim()) {
                    input.value = q;
                }
            }
        } catch (e) {}
        addDidYouMean();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();

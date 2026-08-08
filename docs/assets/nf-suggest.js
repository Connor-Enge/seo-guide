// Progressive-enhancement script to pre-fill 404 search box with likely query

(function() {
    'use strict';

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    function init() {
        var input = document.getElementById('nf-q');
        if (!input) return;

        try {
            var pathSegments = location.pathname.split('/').filter(Boolean);
            var segment = decodeURIComponent(pathSegments[pathSegments.length - 1]);
            var query = segment.replace(/[-_+]/g, ' ').replace(/\s+/g, ' ').trim().toLowerCase();

            if (query && query !== '404' && query !== 'index' && query !== 'home' && !/^\d+$/.test(query)) {
                if (!input.value.trim()) {
                    input.value = query;
                }
            }
        } catch (e) {}
    }
})();

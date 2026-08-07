(function() {
    'use strict';

    function init() {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', init);
        } else {
            const toc = document.querySelector('nav.toc');
            if (!toc) return;

            const sections = [];
            for (const link of toc.querySelectorAll('a[href^="#"]')) {
                const id = decodeURIComponent(link.getAttribute('href').slice(1));
                const heading = document.getElementById(id);
                if (heading) sections.push({ heading, link });
            }

            if (sections.length < 2) return;

            const visible = new Set();
            let current = null;

            const observer = new IntersectionObserver((records) => {
                for (const r of records) {
                    if (r.isIntersecting) visible.add(r.target);
                    else visible.delete(r.target);
                }
                apply();
            }, { rootMargin: '0px 0px -75% 0px', threshold: 0 });

            for (const s of sections) observer.observe(s.heading);

            function apply() {
                let active = null;
                if (visible.size) {
                    for (const s of sections) {
                        if (visible.has(s.heading)) {
                            if (!active || s.heading.getBoundingClientRect().top < active.getBoundingClientRect().top) active = s.heading;
                        }
                    }
                } else {
                    for (const s of sections) {
                        if (s.heading.getBoundingClientRect().top <= 1) active = s.heading;
                    }
                    if (!active) active = sections[0].heading;
                }

                const link = (sections.find(s => s.heading === active) || {}).link || null;
                if (link === current) return;

                current = link;
                for (const s of sections) {
                    if (s.link === link) {
                        s.link.setAttribute('aria-current', 'true');
                        s.link.classList.add('is-current');
                    } else {
                        s.link.removeAttribute('aria-current');
                        s.link.classList.remove('is-current');
                    }
                }
            }
        }
    }

    init();
})();

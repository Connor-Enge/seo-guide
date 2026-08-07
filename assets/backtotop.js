(function() {
    if (!document.body) return;

    const button = document.createElement('button');
    button.type = 'button';
    button.setAttribute('aria-label', 'Back to top');
    button.title = 'Back to top';
    button.textContent = '\u2191';
    button.className = 'to-top';

    const style = document.createElement('style');
    style.textContent = `
        .to-top{position:fixed;right:clamp(.9rem,3vw,1.4rem);bottom:clamp(.9rem,3vw,1.4rem);z-index:40;width:2.75rem;height:2.75rem;display:grid;place-items:center;border:1px solid var(--line,#e7ebf1);border-radius:999px;background:var(--card,#fff);color:var(--accent-ink,#1d4ed8);font-size:1.15rem;line-height:1;cursor:pointer;box-shadow:var(--shadow,0 6px 20px rgba(15,23,42,.12));opacity:0;visibility:hidden;transform:translateY(8px);transition:opacity .18s ease,transform .18s ease;-webkit-tap-highlight-color:transparent}
        .to-top:hover{color:#fff;background:var(--accent,#2563eb);border-color:var(--accent,#2563eb)}
        .to-top:focus-visible{outline:2.5px solid var(--accent,#2563eb);outline-offset:2px}
        .to-top.is-visible{opacity:1;visibility:visible;transform:none}
        @media (prefers-reduced-motion:reduce){.to-top{transition:none}}
    `;

    document.head.appendChild(style);
    document.body.appendChild(button);

    let ticking = false;
    const update = () => {
        button.classList.toggle('is-visible', window.scrollY > window.innerHeight);
    };

    const scrollHandler = () => {
        if (!ticking) {
            ticking = true;
            requestAnimationFrame(() => {
                update();
                ticking = false;
            });
        }
    };

    window.addEventListener('scroll', scrollHandler, { passive: true });
    update();

    button.addEventListener('click', () => {
        const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' });

        try {
            const focusTargets = [
                document.querySelector('a.skip'),
                document.querySelector('header.site .brand'),
                document.getElementById('main')
            ].find(target => target);

            if (focusTargets) {
                focusTargets.focus({ preventScroll: true });
            }
        } catch {}
    });
})();

(function() {
  if (!document.body) return;

  const container = document.createElement('div');
  container.className = 'to-top';
  container.style.position = 'fixed';
  container.style.right = 'clamp(.9rem,3vw,1.4rem)';
  container.style.bottom = 'clamp(.9rem,3vw,1.4rem)';
  container.style.zIndex = '40';
  container.style.width = '2.75rem';
  container.style.height = '2.75rem';

  const ring = document.createElement('div');
  ring.className = 'to-top__ring';
  ring.style.position = 'absolute';
  ring.style.inset = '0';
  ring.style.background = 'conic-gradient(var(--accent,#2563eb) calc(var(--p,0)*1%), var(--line,#e7ebf1) 0)';
  ring.style.mask = 'radial-gradient(farthest-side, transparent calc(100% - 3px), #000 calc(100% - 3px))';
  ring.style.webkitMask = 'radial-gradient(farthest-side, transparent calc(100% - 3px), #000 calc(100% - 3px))';
  ring.style.borderRadius = '999px';

  const button = document.createElement('button');
  button.type = 'button';
  button.ariaLabel = 'Back to top';
  button.title = 'Back to top';
  button.textContent = '\u2191';
  button.style.position = 'absolute';
  button.style.inset = '3px';
  button.style.display = 'grid';
  button.style.placeItems = 'center';
  button.style.border = '1px solid var(--line,#e7ebf1)';
  button.style.borderRadius = '999px';
  button.style.background = 'var(--card,#fff)';
  button.style.color = 'var(--accent-ink,#1d4ed8)';
  button.style.fontSize = '1.05rem';
  button.style.lineHeight = '1';
  button.style.cursor = 'pointer';
  button.style.boxShadow = 'var(--shadow,0 6px 20px rgba(15,23,42,.12))';
  button.style.webkitTapHighlightColor = 'transparent';

  button.onmouseenter = () => {
    button.style.color = '#fff';
    button.style.background = 'var(--accent,#2563eb)';
    button.style.borderColor = 'var(--accent,#2563eb)';
  };

  button.onmouseleave = () => {
    button.style.color = 'var(--accent-ink,#1d4ed8)';
    button.style.background = 'var(--card,#fff)';
    button.style.borderColor = 'var(--line,#e7ebf1)';
  };

  button.onfocusvisible = () => {
    button.style.outline = '2.5px solid var(--accent,#2563eb)';
    button.style.outlineOffset = '2px';
  };

  button.onclick = () => {
    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    try {
      window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' });
      const skipLink = document.querySelector('a.skip');
      if (skipLink) skipLink.focus({ preventScroll: true });
      else {
        const brand = document.querySelector('header.site .brand');
        if (brand) brand.focus({ preventScroll: true });
        else {
          const main = document.getElementById('main');
          if (main) main.focus({ preventScroll: true });
        }
      }
    } catch {}
  };

  container.appendChild(ring);
  container.appendChild(button);

  document.head.appendChild(document.createElement('style')).textContent = `
    .to-top { opacity:0; visibility:hidden; transform:translateY(8px); transition:opacity .18s ease,transform .18s ease }
    .to-top.is-visible { opacity:1; visibility:visible; transform:none }
    @media (prefers-reduced-motion:reduce) { .to-top { transition:none } }
  `;

  document.body.appendChild(container);

  let ticking = false;
  const update = () => {
    if (!ticking) {
      requestAnimationFrame(() => {
        const scrollHeight = document.documentElement.scrollHeight;
        const innerHeight = window.innerHeight;
        const scrollTop = window.scrollY;
        let pct = (scrollTop / (scrollHeight - innerHeight)) * 100;
        if ((scrollHeight - innerHeight) <= 0) pct = 0;
        pct = Math.min(Math.max(pct, 0), 100);
        ring.style.setProperty('--p', pct);

        if (scrollTop > innerHeight) {
          container.classList.add('is-visible');
        } else {
          container.classList.remove('is-visible');
        }

        ticking = false;
      });
    }
    ticking = true;
  };

  update();
  window.addEventListener('scroll', update, { passive: true });
  window.addEventListener('resize', update, { passive: true });
})();

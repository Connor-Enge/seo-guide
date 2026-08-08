(function() {
  if (window.__hanchorCopyInit) return;
  window.__hanchorCopyInit = true;

  function init() {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', bind);
    } else {
      bind();
    }
  }

  function bind() {
    document.addEventListener('click', handleCopy, false);
  }

  function handleCopy(event) {
    var anchor = event.target.closest('a.hanchor');
    if (!anchor) return;
    try {
      var url = new URL(anchor.getAttribute('href'), window.location.href).href;
      copyToClipboard(url);
      showBubble(anchor, 'Copied!');
      announceCopy();
    } catch (e) {}
  }

  function copyToClipboard(text) {
    try {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).catch(fallbackCopy);
      } else {
        fallbackCopy(text);
      }
    } catch (e) {}
  }

  function fallbackCopy(text) {
    var textarea = document.createElement('textarea');
    textarea.value = text;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
  }

  function showBubble(anchor, text) {
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var bubble = document.createElement('div');
    bubble.textContent = text;
    bubble.style.cssText = 'position:absolute;padding:4px;border-radius:4px;z-index:1000;background:#333;color:#fff;pointer-events:none;';
    if (!reduce) {
      bubble.style.opacity = 0;
      setTimeout(() => (bubble.style.opacity = 1), 1);
    }
    document.body.appendChild(bubble);

    var rect = anchor.getBoundingClientRect();
    bubble.style.left = `${rect.right + window.pageXOffset}px`;
    bubble.style.top = `${rect.bottom + window.pageYOffset}px`;

    if (reduce) {
      setTimeout(() => bubble.remove(), 1200);
    } else {
      setTimeout(() => {
        bubble.style.opacity = 0;
        setTimeout(() => bubble.remove(), 300);
      }, 900);
    }
  }

  function announceCopy() {
    var liveRegion = document.getElementById('hanchor-copy-live-region');
    if (!liveRegion) {
      liveRegion = document.createElement('div');
      liveRegion.id = 'hanchor-copy-live-region';
      liveRegion.setAttribute('aria-live', 'polite');
      liveRegion.setAttribute('role', 'status');
      liveRegion.style.cssText = 'position:absolute;width:1px;height:1px;padding:0;margin:-1px;border:0;clip:rect(0 0 0 0);overflow:hidden;white-space:nowrap;';
      document.body.appendChild(liveRegion);
    }
    liveRegion.textContent = 'Link copied to clipboard';
  }

  init();
})();

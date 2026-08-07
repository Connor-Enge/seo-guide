(function() {
    'use strict';

    function init() {
        const preElements = document.querySelectorAll('pre');
        if (!preElements.length) return;

        const styleElement = document.createElement('style');
        styleElement.textContent = `
            pre:has(> code) { position:relative; }
            .copy-code { position:absolute; top:.5rem; right:.5rem; font:inherit; font-size:.75rem; line-height:1; padding:.3rem .55rem; border:1px solid rgba(0,0,0,.18); border-radius:6px; background:#fff; color:#0b6bcb; cursor:pointer; opacity:.85; transition:opacity .15s ease, color .15s ease; }
            .copy-code:hover { opacity:1; }
            .copy-code:focus-visible { outline:2px solid #0b6bcb; outline-offset:2px; }
            .copy-code.copied { color:#0a7f3f; border-color:#0a7f3f; }
            pre > code { padding-right:4.5rem; }
            @media (prefers-reduced-motion: reduce) { .copy-code { transition:none; } }
        `;
        if (!document.head.querySelector('style[data-copycode]')) {
            document.head.appendChild(styleElement);
            styleElement.setAttribute('data-copycode', '1');
        }

        preElements.forEach(pre => {
            const codeElement = pre.querySelector('code');
            if (codeElement && !pre.dataset.copyReady) {
                pre.dataset.copyReady = '1';
                if (pre.style.position === 'static') {
                    pre.style.position = 'relative';
                }
                const button = document.createElement('button');
                button.type = 'button';
                button.className = 'copy-code';
                button.ariaLabel = 'Copy code to clipboard';
                button.textContent = 'Copy';
                pre.insertBefore(button, pre.firstChild);

                let timeoutId;
                button.addEventListener('click', () => {
                    const text = codeElement.textContent;
                    if (navigator.clipboard && navigator.clipboard.writeText) {
                        navigator.clipboard.writeText(text).then(() => {
                            handleCopySuccess(button);
                        }).catch(() => {
                            handleCopyFallback(button, text);
                        });
                    } else {
                        handleCopyFallback(button, text);
                    }
                });

                function handleCopySuccess(button) {
                    button.textContent = 'Copied';
                    button.classList.add('copied');
                    clearTimeout(timeoutId);
                    timeoutId = setTimeout(() => {
                        button.textContent = 'Copy';
                        button.classList.remove('copied');
                    }, 2000);
                }

                function handleCopyFallback(button, text) {
                    const textarea = document.createElement('textarea');
                    textarea.value = text;
                    textarea.style.position = 'absolute';
                    textarea.style.left = '-9999px';
                    document.body.appendChild(textarea);
                    textarea.select();
                    document.execCommand('copy');
                    document.body.removeChild(textarea);
                    handleCopySuccess(button);
                }
            }
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();

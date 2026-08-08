(function() {
    'use strict';

    function init() {
        if (typeof window.print !== 'function') return;
        const article = document.querySelector('main#main article');
        if (!article) return;
        if (article.querySelector('.print-action')) return;

        let style = document.head.querySelector('style[data-printbtn]');
        if (!style) {
            style = document.createElement('style');
            style.setAttribute('data-printbtn', '1');
            document.head.appendChild(style);
        }

        const wrap = document.createElement('div');
        wrap.className = 'print-action';

        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'print-btn';
        button.textContent = 'Print or save as PDF';

        const svgSpan = document.createElement('span');
        svgSpan.innerHTML = '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M18 9v4c0 .55-.45 1-1 1H7c-.55 0-1-.45-1-1V9c0-.55.45-1 1-1h10c.55 0 1 .45 1 1zm-6 2c0 .55-.45 1-1 1s-1-.45-1-1v-2c0-.55.45-1 1-1s1 .45 1 1v2zm3 7h-2v2h2v-2z"/></svg>';
        svgSpan.setAttribute('aria-hidden', 'true');
        svgSpan.setAttribute('focusable', 'false');

        button.prepend(svgSpan);
        wrap.appendChild(button);

        article.appendChild(wrap);

        style.textContent = `
            .print-action {
                margin-top: 2.5rem;
                padding-top: 1.25rem;
                border-top: 1px solid rgba(0,0,0,.1);
            }
            .print-btn {
                display: inline-flex;
                align-items: center;
                gap: .45rem;
                font: inherit;
                font-size: .85rem;
                line-height: 1;
                padding: .5rem .85rem;
                border: 1px solid rgba(0,0,0,.18);
                border-radius: 6px;
                background: #fff;
                color: #0b6bcb;
                cursor: pointer;
            }
            .print-btn:hover {
                border-color: #0b6bcb;
            }
            .print-btn:focus-visible {
                outline: 2px solid #0b6bcb;
                outline-offset: 2px;
            }
            .print-btn svg {
                width: 1em;
                height: 1em;
            }
            @media print {
                .print-action {
                    display: none !important;
                }
            }
            @media (prefers-color-scheme: dark) {
                .print-action {
                    border-top: 1px solid rgba(255,255,255,.14);
                }
                .print-btn {
                    background: transparent;
                    color: #6fb3ff;
                    border-color: rgba(255,255,255,.22);
                }
            }
        `;

        button.addEventListener('click', function() {
            window.print();
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();

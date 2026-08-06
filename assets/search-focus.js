(function() {
    var input = document.querySelector('.hsearch input[type="search"]');
    if (!input) return;

    document.addEventListener('keydown', function(e) {
        if (e.ctrlKey || e.metaKey || e.altKey) return;
        let el = e.target || document.activeElement;
        let tag = el && el.tagName;
        if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT' || (el && el.isContentEditable)) return;

        if (e.key === '/') {
            e.preventDefault();
            input.focus();
            if (typeof input.select === 'function') input.select();
        }
    });
})();

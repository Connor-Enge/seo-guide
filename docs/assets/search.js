(function() {
    'use strict';

    if (!document.getElementById('search') || !document.getElementById('q') || !document.getElementById('results') || !document.getElementById('all')) return;

    function esc(str) {
        return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }

    function announce(n, q) {
        if (n === 0) {
            document.getElementById('results').innerHTML = '<li>No results for <mark>' + esc(q) + '</mark></li>';
        } else {
            document.getElementById('results').innerHTML = '<li>Showing ' + n + ' results for <mark>' + esc(q) + '</mark></li>';
        }
    }

    function highlight(escapedText, terms) {
        return terms.reduce(function(text, term) {
            var escapedTerm = term.replace(/[.*+?^${}()|[\]\\-]/g, '\\$&');
            var regex = new RegExp(escapedTerm, 'gi');
            return text.replace(regex, function(matched) {
                return '<mark>' + matched + '</mark>';
            });
        }, escapedText);
    }

    function run() {
        var q = param('q').trim().toLowerCase();
        if (!q) return;

        var terms = q.split(/\s+/).filter(Boolean);
        fetch(document.getElementById('root').getAttribute('data-index'), { credentials: 'omit' })
            .then(function(response) {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error('Network response was not ok');
                }
            })
            .then(function(data) {
                var items = data.filter(function(it) {
                    return terms.every(function(term) {
                        return it.title.toLowerCase().includes(term) || it.tags.some(tag => tag.toLowerCase().includes(term));
                    });
                });

                items.forEach(function(it, i) {
                    it.score = terms.reduce(function(score, term) {
                        if (it.title.toLowerCase().includes(term)) score += 3;
                        if (it.tags.some(tag => tag.toLowerCase().includes(term))) score += 1;
                        return score;
                    }, 0);
                });

                items.sort(function(a, b) {
                    if (a.score !== b.score) return b.score - a.score;
                    return data.indexOf(a) - data.indexOf(b);
                });

                draw(items, q);
            })
            .catch(function(error) {
                document.getElementById('status').innerHTML = '';
                var list = document.getElementById('results');
                while (list.firstChild) {
                    list.removeChild(list.firstChild);
                }
                announce(0, param('q'));
            });
    }

    function param(name) {
        return new URLSearchParams(window.location.search).get(name);
    }

    function draw(items, q) {
        var terms = q.trim().toLowerCase().split(/\s+/).filter(Boolean);
        var list = document.getElementById('results');
        while (list.firstChild) {
            list.removeChild(list.firstChild);
        }
        if (items.length === 0) {
            announce(0, param('q'));
        } else {
            items.forEach(function(it) {
                var li = document.createElement('li');
                li.innerHTML = '<span class="type">' + esc(it.type) + '</span>: ' +
                    highlight(esc(it.title), terms) + ' - ' +
                    highlight(esc(it.description), terms);
                list.appendChild(li);
            });
        }
    }

    document.getElementById('search').addEventListener('submit', function(e) {
        e.preventDefault();
        run();
    });

    document.getElementById('q').addEventListener('input', function() {
        if (this.value.trim()) {
            document.getElementById('all').checked = false;
        } else {
            document.getElementById('all').checked = true;
        }
    });

    var root = document.getElementById('root');
    if (root) {
        run();
    }
})();

/* On-site search for The Guide to SEO.
 * Progressive enhancement: the /search/ page renders a full, browsable list with zero
 * JavaScript. This script fetches the tiny build-time index (search-index.json) and turns
 * that list into a live, client-side filter — no server, no dependencies, no tracking.
 * If anything fails (no JS, fetch error), the static list stays and the page still works.
 */
(function () {
  "use strict";
  var root = document.getElementById("search");
  if (!root) return;
  var input = document.getElementById("q");
  var results = document.getElementById("results");
  var all = document.getElementById("all");
  var status = document.getElementById("search-status");
  var form = root.querySelector("form");
  if (!input || !results || !all || !form) return;

  var index = [];
  var ready = false;

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  function announce(n, q) {
    if (!status) return;
    if (!q) { status.textContent = index.length + " pages and articles"; return; }
    status.textContent = n + (n === 1 ? " result" : " results") + ' for "' + q + '"';
  }

  function draw(items, q) {
    if (!items.length) {
      results.innerHTML =
        '<li class="search-empty">No pages match "' + esc(q) +
        '". Try a broader term, or browse the guide from the top navigation.</li>';
      return;
    }
    var html = "";
    for (var i = 0; i < items.length; i++) {
      var it = items[i];
      html +=
        '<li><a href="' + esc(it.url) + '">' + esc(it.title) + "</a> " +
        '<span class="tag">' + esc(it.type) + "</span>" +
        "<p>" + esc(it.description) + "</p></li>";
    }
    results.innerHTML = html;
  }

  // Rank: every term must appear somewhere; title/tag hits sort above description-only hits.
  function run(q) {
    q = (q || "").trim();
    if (!q) { draw(index, ""); announce(index.length, ""); return; }
    var terms = q.toLowerCase().split(/\s+/).filter(Boolean);
    var hits = [];
    for (var i = 0; i < index.length; i++) {
      var it = index[i];
      var title = it.title.toLowerCase();
      var tags = (it.tags || []).join(" ").toLowerCase();
      var hay = title + " " + it.description.toLowerCase() + " " + tags + " " +
                (it.text || "").toLowerCase();
      var ok = true, score = 0;
      for (var t = 0; t < terms.length; t++) {
        if (hay.indexOf(terms[t]) === -1) { ok = false; break; }
        if (title.indexOf(terms[t]) !== -1) score += 3;
        if (tags.indexOf(terms[t]) !== -1) score += 1;
      }
      if (ok) hits.push({ it: it, score: score, ord: i });
    }
    hits.sort(function (a, b) { return b.score - a.score || a.ord - b.ord; });
    var items = [];
    for (var h = 0; h < hits.length; h++) items.push(hits[h].it);
    draw(items, q);
    announce(items.length, q);
  }

  function param(name) {
    var m = new RegExp("[?&]" + name + "=([^&]*)").exec(location.search);
    return m ? decodeURIComponent(m[1].replace(/\+/g, " ")) : "";
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (ready) run(input.value);
    input.focus();
  });
  input.addEventListener("input", function () { if (ready) run(input.value); });

  fetch(root.getAttribute("data-index"), { credentials: "omit" })
    .then(function (r) {
      if (!r.ok) throw new Error("index " + r.status);
      return r.json();
    })
    .then(function (data) {
      index = Array.isArray(data) ? data : [];
      ready = true;
      // Take over only once the index is loaded, so there is never a blank flash.
      all.hidden = true;
      results.hidden = false;
      var q0 = param("q");
      if (q0) input.value = q0;
      run(input.value);
    })
    .catch(function () {
      // Leave the static, no-JS list in place — the page is still fully usable.
      if (status) status.textContent = "";
    });
})();

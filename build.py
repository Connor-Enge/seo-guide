#!/usr/bin/env python3
"""Static-site generator for the Guide to SEO — and a demonstration of on-page SEO itself.

Reads content/*.md (front-matter + a small markdown subset) and renders heavily-optimized static
HTML into docs/ (GitHub Pages root): semantic HTML5, one H1/page, meta description, canonical,
Open Graph + Twitter cards, JSON-LD Article + BreadcrumbList, a table of contents, cross-links,
prev/next, plus sitemap.xml and robots.txt. No JS, tiny CSS — fast by construction.

Usage: python3 build.py   (writes docs/, prints a build report)
"""
import os
import re
import html
import glob
import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, "content")
OUT = os.path.join(HERE, "docs")
TEMPLATE = open(os.path.join(HERE, "templates", "base.html")).read()

# The canonical origin. When Connor enables GitHub Pages this is the live URL; swap for a custom domain later.
BASE_URL = "https://connor-enge.github.io/seo-guide"
SITE_NAME = "The Guide to SEO"
AUTHOR = "Connor Enge"


# ---------- tiny markdown renderer (headings, paras, lists, links, bold, code, blockquote) ----------
def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"`(.+?)`", r"<code>\1</code>", t)
    t = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', t)
    return t


def plain(t):
    """Strip the inline markdown subset to readable plain text (for JSON-LD answer text)."""
    t = re.sub(r"\*\*(.+?)\*\*", r"\1", t)
    t = re.sub(r"`(.+?)`", r"\1", t)
    t = re.sub(r"\[(.+?)\]\((.+?)\)", r"\1", t)
    return t.strip()


def extract_faq(body):
    """Pull (question, answer) pairs from a `## FAQ` section so the visible Q&A and the
    FAQPage JSON-LD are generated from one source and can never drift apart.
    Inside the FAQ section each `### ...` is a question; the prose beneath it is the answer."""
    faqs, q, ans, in_faq = [], None, [], False

    def flush():
        nonlocal q, ans
        if q is not None:
            text = plain(" ".join(a.strip() for a in ans if a.strip()))
            if text:
                faqs.append((q, text))
        q, ans = None, []

    for ln in body.split("\n"):
        s = ln.rstrip()
        if s.startswith("## "):
            flush()
            in_faq = s[3:].strip().lower() == "faq"
            continue
        if not in_faq:
            continue
        if s.startswith("### "):
            flush()
            q = s[4:].strip()
        elif q is not None and s.strip():
            ans.append(s.strip())
    flush()
    return faqs


def render_md(body):
    out, i, lines = [], 0, body.split("\n")
    toc = []
    while i < len(lines):
        ln = lines[i].rstrip()
        if not ln.strip():
            i += 1
            continue
        if ln.startswith("### "):
            out.append(f"<h3>{inline(ln[4:])}</h3>")
        elif ln.startswith("## "):
            txt = ln[3:]
            slug = re.sub(r"[^a-z0-9]+", "-", txt.lower()).strip("-")
            toc.append((txt, slug))
            out.append(f'<h2 id="{slug}">{inline(txt)}</h2>')
        elif ln.startswith("> "):
            buf = []
            while i < len(lines) and lines[i].startswith("> "):
                buf.append(lines[i][2:])
                i += 1
            out.append(f"<blockquote>{inline(' '.join(buf))}</blockquote>")
            continue
        elif re.match(r"^\d+\. ", ln):
            buf = []
            while i < len(lines) and re.match(r"^\d+\. ", lines[i]):
                item = re.sub(r"^\d+\. ", "", lines[i])
                buf.append(f"<li>{inline(item)}</li>")
                i += 1
            out.append("<ol>" + "".join(buf) + "</ol>")
            continue
        elif ln.startswith("- "):
            buf = []
            while i < len(lines) and lines[i].startswith("- "):
                buf.append(f"<li>{inline(lines[i][2:])}</li>")
                i += 1
            out.append("<ul>" + "".join(buf) + "</ul>")
            continue
        else:
            buf = []
            while i < len(lines) and lines[i].strip() and not re.match(r"^(#{2,3} |- |\d+\. |> )", lines[i]):
                buf.append(lines[i])
                i += 1
            out.append(f"<p>{inline(' '.join(buf))}</p>")
            continue
        i += 1
    return "\n".join(out), toc


def parse(path):
    raw = open(path).read()
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
    meta, body = {}, raw
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
        body = m.group(2)
    meta.setdefault("slug", os.path.splitext(os.path.basename(path))[0])
    meta.setdefault("order", "99")
    return meta, body


def page_url(slug):
    return BASE_URL + ("/" if slug == "index" else f"/{slug}/")


def main():
    pages = sorted((parse(p) for p in glob.glob(os.path.join(CONTENT, "*.md"))),
                   key=lambda x: int(x[0]["order"]))
    today = datetime.date.today().isoformat()
    nav = "".join(f'<li><a href="{page_url(m["slug"])}">{html.escape(m["title"])}</a></li>' for m, _ in pages)

    os.makedirs(OUT, exist_ok=True)
    for idx, (meta, body) in enumerate(pages):
        slug = meta["slug"]
        content_html, toc = render_md(body)
        toc_html = ("<nav class=\"toc\" aria-label=\"On this page\"><p>On this page</p><ul>"
                    + "".join(f'<li><a href="#{s}">{html.escape(t)}</a></li>' for t, s in toc)
                    + "</ul></nav>") if toc else ""
        # prev/next internal links
        links = []
        if idx > 0:
            pm = pages[idx - 1][0]
            links.append(f'<a class="prev" href="{page_url(pm["slug"])}">← {html.escape(pm["title"])}</a>')
        if idx < len(pages) - 1:
            nm = pages[idx + 1][0]
            links.append(f'<a class="next" href="{page_url(nm["slug"])}">{html.escape(nm["title"])} →</a>')
        url = page_url(slug)
        breadcrumb = ('{"@type":"ListItem","position":1,"name":"Home","item":"%s"}' % BASE_URL) + (
            (',{"@type":"ListItem","position":2,"name":%s,"item":"%s"}' % (
                _json(meta["title"]), url)) if slug != "index" else "")
        jsonld = (
            '<script type="application/ld+json">{"@context":"https://schema.org","@type":"Article",'
            '"headline":%s,"description":%s,"author":{"@type":"Person","name":%s},'
            '"datePublished":"%s","dateModified":"%s","mainEntityOfPage":"%s","publisher":'
            '{"@type":"Organization","name":%s}}</script>\n'
            '<script type="application/ld+json">{"@context":"https://schema.org",'
            '"@type":"BreadcrumbList","itemListElement":[%s]}</script>'
        ) % (_json(meta["title"]), _json(meta["description"]), _json(AUTHOR),
             meta.get("updated", today), today, url, _json(SITE_NAME), breadcrumb)

        # FAQPage schema — only on pages that ship a `## FAQ` section, built from the same text.
        faqs = extract_faq(body)
        if faqs:
            entities = ",".join(
                '{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}'
                % (_json(q), _json(a)) for q, a in faqs)
            jsonld += ('\n<script type="application/ld+json">{"@context":"https://schema.org",'
                       '"@type":"FAQPage","mainEntity":[%s]}</script>' % entities)

        page = TEMPLATE.format(
            title=html.escape(meta["title"]), site=html.escape(SITE_NAME),
            description=html.escape(meta["description"]), canonical=url, base=BASE_URL,
            og_type=("website" if slug == "index" else "article"),
            nav=nav, h1=html.escape(meta.get("h1", meta["title"])), toc=toc_html,
            content=content_html, pager=('<nav class="pager">' + "".join(links) + "</nav>") if links else "",
            jsonld=jsonld, updated=meta.get("updated", today), year=today[:4])
        d = OUT if slug == "index" else os.path.join(OUT, slug)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w").write(page)

    # sitemap + robots
    urls = "".join(f"<url><loc>{page_url(m['slug'])}</loc><lastmod>{today}</lastmod>"
                   f"<priority>{'1.0' if m['slug']=='index' else '0.8'}</priority></url>" for m, _ in pages)
    open(os.path.join(OUT, "sitemap.xml"), "w").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + urls + "</urlset>\n")
    open(os.path.join(OUT, "robots.txt"), "w").write(
        f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}/sitemap.xml\n")
    open(os.path.join(OUT, ".nojekyll"), "w").write("")

    print(f"Built {len(pages)} pages -> docs/  (+ sitemap.xml, robots.txt)")
    for m, _ in pages:
        print(f"  {page_url(m['slug'])}")


def _json(s):
    import json
    return json.dumps(s, ensure_ascii=False)


if __name__ == "__main__":
    main()

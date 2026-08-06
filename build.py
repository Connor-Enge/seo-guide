#!/usr/bin/env python3
"""Static-site generator for the Guide to SEO — and a demonstration of on-page SEO itself.

Reads content/*.md (guide pages) and content/blog/*.md (blog posts), both as front-matter + a
small markdown subset, and renders heavily-optimized static HTML into docs/ (GitHub Pages root):
semantic HTML5, one H1/page, meta description, canonical, Open Graph + Twitter cards, JSON-LD
(Article/BlogPosting + BreadcrumbList + FAQPage + Blog), a table of contents, cross-links,
prev/next, a /blog/ index, plus sitemap.xml and robots.txt. No JS, tiny CSS — fast by construction.

Usage: python3 build.py   (writes docs/, prints a build report)
"""
import os
import re
import html
import glob
import json
import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, "content")
BLOG = os.path.join(CONTENT, "blog")
OUT = os.path.join(HERE, "docs")
TEMPLATE = open(os.path.join(HERE, "templates", "base.html")).read()

# The canonical origin. When Connor enables GitHub Pages this is the live URL; swap for a custom domain later.
BASE_URL = "https://connor-enge.github.io/seo-guide"
BLOG_URL = BASE_URL + "/blog/"
SITE_NAME = "The Guide to SEO"
BLOG_TITLE = "The SEO Blog"
BLOG_DESC = ("Practical, sourced articles on getting found in search — Core Web Vitals, content "
             "that earns rankings, technical fixes, and how Google actually ranks pages.")
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


def post_url(slug):
    return f"{BASE_URL}/blog/{slug}/"


def _json(s):
    return json.dumps(s, ensure_ascii=False)


# ---------- JSON-LD builders (each returns one or more <script> blocks) ----------
def schema_article(atype, headline, description, url, date_pub, date_mod):
    return ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"%s",'
            '"headline":%s,"description":%s,"author":{"@type":"Person","name":%s},'
            '"datePublished":"%s","dateModified":"%s","mainEntityOfPage":"%s","publisher":'
            '{"@type":"Organization","name":%s}}</script>') % (
        atype, _json(headline), _json(description), _json(AUTHOR),
        date_pub, date_mod, url, _json(SITE_NAME))


def schema_breadcrumb(items):
    li = ",".join('{"@type":"ListItem","position":%d,"name":%s,"item":"%s"}' % (i + 1, _json(n), u)
                  for i, (n, u) in enumerate(items))
    return ('<script type="application/ld+json">{"@context":"https://schema.org",'
            '"@type":"BreadcrumbList","itemListElement":[%s]}</script>') % li


def schema_faq(faqs):
    ents = ",".join('{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}'
                    % (_json(q), _json(a)) for q, a in faqs)
    return ('<script type="application/ld+json">{"@context":"https://schema.org",'
            '"@type":"FAQPage","mainEntity":[%s]}</script>') % ents


def schema_blog(posts):
    items = ",".join(
        '{"@type":"BlogPosting","headline":%s,"url":"%s","datePublished":"%s","description":%s}'
        % (_json(m["title"]), post_url(m["slug"]), m.get("date", ""), _json(m["description"]))
        for m, _ in posts)
    return ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"Blog",'
            '"name":%s,"url":"%s","description":%s,"blogPost":[%s]}</script>') % (
        _json(BLOG_TITLE), BLOG_URL, _json(BLOG_DESC), items)


def main():
    today = datetime.date.today().isoformat()
    pages = sorted((parse(p) for p in glob.glob(os.path.join(CONTENT, "*.md"))),
                   key=lambda x: int(x[0]["order"]))
    posts = [parse(p) for p in glob.glob(os.path.join(BLOG, "*.md"))]
    # newest-first; posts must carry a `date` (YYYY-MM-DD) front-matter field
    posts.sort(key=lambda x: x[0].get("date", "0000-00-00"), reverse=True)

    nav = "".join(f'<li><a href="{page_url(m["slug"])}">{html.escape(m["title"])}</a></li>' for m, _ in pages)
    nav += f'<li><a href="{BLOG_URL}">Blog</a></li>'

    def render(*, title, description, url, og_type, h1, byline, toc="", content="", pager="", jsonld=""):
        return TEMPLATE.format(
            title=html.escape(title), site=html.escape(SITE_NAME),
            description=html.escape(description), canonical=url, base=BASE_URL,
            og_type=og_type, nav=nav, h1=html.escape(h1), byline=html.escape(byline),
            toc=toc, content=content, pager=pager, jsonld=jsonld, year=today[:4])

    def toc_block(toc):
        return ('<nav class="toc" aria-label="On this page"><p>On this page</p><ul>'
                + "".join(f'<li><a href="#{s}">{html.escape(t)}</a></li>' for t, s in toc)
                + "</ul></nav>") if toc else ""

    def write(slug_dir, page):
        d = OUT if slug_dir == "" else os.path.join(OUT, slug_dir)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w").write(page)

    os.makedirs(OUT, exist_ok=True)

    # ---------- guide pages ----------
    for idx, (meta, body) in enumerate(pages):
        slug = meta["slug"]
        content_html, toc = render_md(body)
        links = []
        if idx > 0:
            pm = pages[idx - 1][0]
            links.append(f'<a class="prev" href="{page_url(pm["slug"])}">← {html.escape(pm["title"])}</a>')
        if idx < len(pages) - 1:
            nm = pages[idx + 1][0]
            links.append(f'<a class="next" href="{page_url(nm["slug"])}">{html.escape(nm["title"])} →</a>')
        url = page_url(slug)
        crumbs = [("Home", BASE_URL)] + ([] if slug == "index" else [(meta["title"], url)])
        jsonld = (schema_article("Article", meta["title"], meta["description"], url,
                                 meta.get("updated", today), today)
                  + "\n" + schema_breadcrumb(crumbs))
        faqs = extract_faq(body)
        if faqs:
            jsonld += "\n" + schema_faq(faqs)
        page = render(
            title=meta["title"], description=meta["description"], url=url,
            og_type=("website" if slug == "index" else "article"),
            h1=meta.get("h1", meta["title"]),
            byline=f'Updated {meta.get("updated", today)} · by Connor Enge',
            toc=toc_block(toc), content=content_html,
            pager=('<nav class="pager">' + "".join(links) + "</nav>") if links else "",
            jsonld=jsonld)
        write("" if slug == "index" else slug, page)

    # ---------- blog posts ----------
    for meta, body in posts:
        slug = meta["slug"]
        content_html, toc = render_md(body)
        url = post_url(slug)
        date_pub = meta.get("date", today)
        date_mod = meta.get("updated", date_pub)
        byline = f"Published {date_pub} · by Connor Enge"
        if date_mod and date_mod != date_pub:
            byline += f" · Updated {date_mod}"
        crumbs = [("Home", BASE_URL), (BLOG_TITLE, BLOG_URL), (meta["title"], url)]
        jsonld = (schema_article("BlogPosting", meta["title"], meta["description"], url, date_pub, date_mod)
                  + "\n" + schema_breadcrumb(crumbs))
        faqs = extract_faq(body)
        if faqs:
            jsonld += "\n" + schema_faq(faqs)
        page = render(
            title=meta["title"], description=meta["description"], url=url, og_type="article",
            h1=meta.get("h1", meta["title"]), byline=byline,
            toc=toc_block(toc), content=content_html,
            pager=f'<nav class="pager"><a class="prev" href="{BLOG_URL}">← All articles</a></nav>',
            jsonld=jsonld)
        write(os.path.join("blog", slug), page)

    # ---------- blog index ----------
    if posts:
        items = "".join(
            '<li><h2><a href="%s">%s</a></h2><p class="meta">Published %s</p><p>%s</p></li>' % (
                post_url(m["slug"]), html.escape(m["title"]),
                html.escape(m.get("date", "")), html.escape(m["description"]))
            for m, _ in posts)
        blog_content = f"<p>{BLOG_DESC}</p><ul class=\"post-list\">{items}</ul>"
    else:
        blog_content = f"<p>{BLOG_DESC}</p><p>Articles are on the way.</p>"
    blog_jsonld = schema_blog(posts) + "\n" + schema_breadcrumb([("Home", BASE_URL), (BLOG_TITLE, BLOG_URL)])
    write("blog", render(
        title=BLOG_TITLE, description=BLOG_DESC, url=BLOG_URL, og_type="website",
        h1=BLOG_TITLE, byline="Practical, sourced SEO articles · by Connor Enge",
        content=blog_content, jsonld=blog_jsonld))

    # ---------- sitemap + robots ----------
    entries = [(page_url(m["slug"]), today, "1.0" if m["slug"] == "index" else "0.8") for m, _ in pages]
    entries.append((BLOG_URL, today, "0.7"))
    entries += [(post_url(m["slug"]), m.get("updated", m.get("date", today)), "0.6") for m, _ in posts]
    urls = "".join(f"<url><loc>{loc}</loc><lastmod>{mod}</lastmod><priority>{pri}</priority></url>"
                   for loc, mod, pri in entries)
    open(os.path.join(OUT, "sitemap.xml"), "w").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + urls + "</urlset>\n")
    open(os.path.join(OUT, "robots.txt"), "w").write(
        f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}/sitemap.xml\n")
    open(os.path.join(OUT, ".nojekyll"), "w").write("")

    print(f"Built {len(pages)} guide pages + {len(posts)} blog post(s) -> docs/  (+ /blog/, sitemap.xml, robots.txt)")
    for m, _ in pages:
        print(f"  {page_url(m['slug'])}")
    print(f"  {BLOG_URL}")
    for m, _ in posts:
        print(f"  {post_url(m['slug'])}")


if __name__ == "__main__":
    main()

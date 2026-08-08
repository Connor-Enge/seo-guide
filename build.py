#!/usr/bin/env python3
"""Static-site generator for the Guide to SEO — and a demonstration of on-page SEO itself.

Reads content/*.md (guide pages) and content/blog/*.md (blog posts), both as front-matter + a
small markdown subset, and renders heavily-optimized static HTML into docs/ (GitHub Pages root):
semantic HTML5, one H1/page, meta description, canonical, Open Graph + Twitter cards, and a single
connected JSON-LD @graph per page (Organization + WebSite + Person entities with stable @ids, plus
the page's Article/BlogPosting/ProfilePage/Blog + BreadcrumbList + FAQPage), a table of contents,
cross-links, prev/next, a /blog/ index, plus sitemap.xml and robots.txt. No JS, tiny CSS — fast.

Usage: python3 build.py   (writes docs/, prints a build report)
"""
import os
import re
import html
import glob
import json
import datetime
import email.utils

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, "content")
BLOG = os.path.join(CONTENT, "blog")
OUT = os.path.join(HERE, "docs")
TEMPLATE = open(os.path.join(HERE, "templates", "base.html")).read()

# Visible breadcrumb trail (mirrors the BreadcrumbList JSON-LD). Rendering logic lives in
# improve/breadcrumb.py; loaded by path so it works regardless of the invoking cwd.
import importlib.util as _ilu
_bc_spec = _ilu.spec_from_file_location("breadcrumb", os.path.join(HERE, "improve", "breadcrumb.py"))
_bc_mod = _ilu.module_from_spec(_bc_spec)
_bc_spec.loader.exec_module(_bc_mod)
breadcrumb_block = _bc_mod.breadcrumb_block

# Section heading with a hover/focus permalink (¶). Rendering logic lives in improve/anchors.py.
_an_spec = _ilu.spec_from_file_location("anchors", os.path.join(HERE, "improve", "anchors.py"))
_an_mod = _ilu.module_from_spec(_an_spec)
_an_spec.loader.exec_module(_an_mod)
heading_html = _an_mod.heading_html

# Fenced ```code``` block support for the markdown renderer: convert a fenced block into a
# semantic <pre><code> with HTML-escaped content. Logic lives in improve/fencedcode.py.
_fc_spec = _ilu.spec_from_file_location("fencedcode", os.path.join(HERE, "improve", "fencedcode.py"))
_fc_mod = _ilu.module_from_spec(_fc_spec)
_fc_spec.loader.exec_module(_fc_mod)
consume_fence = _fc_mod.consume_fence

# Outbound-link annotation: tag body anchors whose host differs from the site with
# rel="noopener" + class="ext" so a CSS ↗ marks references that leave the site. improve/extlinks.py.
_el_spec = _ilu.spec_from_file_location("extlinks", os.path.join(HERE, "improve", "extlinks.py"))
_el_mod = _ilu.module_from_spec(_el_spec)
_el_spec.loader.exec_module(_el_mod)
mark_external = _el_mod.mark_external

# "Related articles" block linking sibling posts by shared tags. Logic in improve/relatedposts.py.
_rp_spec = _ilu.spec_from_file_location("relatedposts", os.path.join(HERE, "improve", "relatedposts.py"))
_rp_mod = _ilu.module_from_spec(_rp_spec)
_rp_spec.loader.exec_module(_rp_mod)
related_posts_block = _rp_mod.related_posts_block

# Blog-index post card: title link + meta line (published date · reading time) + description.
# Logic in improve/blogindex.py.
_bi_spec = _ilu.spec_from_file_location("blogindex", os.path.join(HERE, "improve", "blogindex.py"))
_bi_mod = _ilu.module_from_spec(_bi_spec)
_bi_spec.loader.exec_module(_bi_mod)
post_list_item = _bi_mod.post_list_item

# Custom 404 page content (helpful links + search). Copy lives in improve/notfound.py.
_nf_spec = _ilu.spec_from_file_location("notfound", os.path.join(HERE, "improve", "notfound.py"))
_nf_mod = _ilu.module_from_spec(_nf_spec)
_nf_spec.loader.exec_module(_nf_mod)
notfound_content = _nf_mod.notfound_content
NF_TITLE, NF_DESCRIPTION, NF_H1, NF_BYLINE = (
    _nf_mod.NF_TITLE, _nf_mod.NF_DESCRIPTION, _nf_mod.NF_H1, _nf_mod.NF_BYLINE)

# Prefix root-relative in-body links (written in markdown as /slug/) with the deploy base path,
# so they don't 404 on the GitHub Pages project subpath. Logic lives in improve/links.py.
_lk_spec = _ilu.spec_from_file_location("links", os.path.join(HERE, "improve", "links.py"))
_lk_mod = _ilu.module_from_spec(_lk_spec)
_lk_spec.loader.exec_module(_lk_mod)
resolve_href = _lk_mod.resolve_href

# Post-build integrity gate: audit every rendered internal <a href> against docs/ and fail the
# build on a dangling internal target (soft-404) or a subpath-breaking root-relative href.
# Logic lives in improve/linkcheck.py.
_ck_spec = _ilu.spec_from_file_location("linkcheck", os.path.join(HERE, "improve", "linkcheck.py"))
_ck_mod = _ilu.module_from_spec(_ck_spec)
_ck_spec.loader.exec_module(_ck_mod)
audit_internal_links = _ck_mod.audit_internal_links

# Post-build canonical gate: assert every rendered page self-canonicalizes (rel=canonical exactly
# equals its own BASE_URL page URL) so canonicalization can never silently drift. Logic lives in
# improve/canonicalcheck.py.
_cn_spec = _ilu.spec_from_file_location("canonicalcheck", os.path.join(HERE, "improve", "canonicalcheck.py"))
_cn_mod = _ilu.module_from_spec(_cn_spec)
_cn_spec.loader.exec_module(_cn_mod)
audit_canonicals = _cn_mod.audit_canonicals

# Post-build metadata audit: every page must have exactly one <title> and one meta description
# (structural errors fail the build); over-length / empty / cross-page-duplicate titles or
# descriptions are reported as warnings so on-SERP snippets never silently regress. Logic lives
# in improve/metacheck.py.
_mc_spec = _ilu.spec_from_file_location("metacheck", os.path.join(HERE, "improve", "metacheck.py"))
_mc_mod = _ilu.module_from_spec(_mc_spec)
_mc_spec.loader.exec_module(_mc_mod)
audit_meta = _mc_mod.audit_meta

# Build-time structured-data integrity gate: every page that carries JSON-LD must parse and keep a
# connected Organization + WebSite + Person entity graph with stable, absolute, sitewide-consistent
# @ids, so the entity graph can never silently fragment or drift. Logic in improve/jsonldcheck.py.
_jl_spec = _ilu.spec_from_file_location("jsonldcheck", os.path.join(HERE, "improve", "jsonldcheck.py"))
_jl_mod = _ilu.module_from_spec(_jl_spec)
_jl_spec.loader.exec_module(_jl_mod)
audit_jsonld = _jl_mod.audit_jsonld

# Post-build sitemap gate: assert docs/sitemap.xml is well-formed, every <loc> is absolute and
# resolves to a real generated file, no duplicates, and 404.html is never listed; warn (report-only)
# on any indexable page missing from the sitemap. Logic in improve/sitemapcheck.py.
_sm_spec = _ilu.spec_from_file_location("sitemapcheck", os.path.join(HERE, "improve", "sitemapcheck.py"))
_sm_mod = _ilu.module_from_spec(_sm_spec)
_sm_spec.loader.exec_module(_sm_mod)
audit_sitemap = _sm_mod.audit_sitemap

# Post-build robots.txt gate: assert docs/robots.txt exists, carries an absolute Sitemap: line equal to
# BASE_URL + '/sitemap.xml', and that no 'User-agent: *' group blanket-disallows the whole site (Disallow: /).
# Logic in improve/robotscheck.py.
_rb_spec = _ilu.spec_from_file_location("robotscheck", os.path.join(HERE, "improve", "robotscheck.py"))
_rb_mod = _ilu.module_from_spec(_rb_spec)
_rb_spec.loader.exec_module(_rb_mod)
audit_robots = _rb_mod.audit_robots

# Post-build heading gate: assert every rendered page carries exactly one <h1> — a page with zero or
# multiple <h1>s dilutes the primary-topic signal and breaks the accessible heading outline.
# Logic in improve/h1check.py.
_h1_spec = _ilu.spec_from_file_location("h1check", os.path.join(HERE, "improve", "h1check.py"))
_h1_mod = _ilu.module_from_spec(_h1_spec)
_h1_spec.loader.exec_module(_h1_mod)
audit_h1 = _h1_mod.audit_h1

# Post-build social-snippet gate: assert every page's Open Graph / Twitter Card metadata is coherent so
# shares render correctly. og:url must be absolute and exactly equal to the page canonical (error); a
# missing og:title / og:description / twitter:card is reported as a non-blocking warning.
# Logic in improve/socialmetacheck.py.
_so_spec = _ilu.spec_from_file_location("socialmetacheck", os.path.join(HERE, "improve", "socialmetacheck.py"))
_so_mod = _ilu.module_from_spec(_so_spec)
_so_spec.loader.exec_module(_so_mod)
audit_social_meta = _so_mod.audit_social_meta

# Post-build heading-order gate (report-only): flag any page that skips a heading level (e.g. an <h3>
# with no preceding <h2>), which breaks the accessible document outline and the topical hierarchy search
# engines read. Non-blocking warnings. Logic in improve/headingorder.py.
_ho_spec = _ilu.spec_from_file_location("headingorder", os.path.join(HERE, "improve", "headingorder.py"))
_ho_mod = _ilu.module_from_spec(_ho_spec)
_ho_spec.loader.exec_module(_ho_mod)
audit_heading_order = _ho_mod.audit_heading_order

# Post-build blog structured-data gate: every published post (docs/blog/<slug>/index.html) must carry a
# valid BlogPosting JSON-LD node with a non-empty headline, datePublished, dateModified, and author, so
# rich-result eligibility can never silently regress as more posts ship. Error severity — fails the build.
# Logic in improve/blogpostingcheck.py.
_bp_spec = _ilu.spec_from_file_location("blogpostingcheck", os.path.join(HERE, "improve", "blogpostingcheck.py"))
_bp_mod = _ilu.module_from_spec(_bp_spec)
_bp_spec.loader.exec_module(_bp_mod)
audit_blog_posting = _bp_mod.audit_blog_posting

# Post-build image-accessibility gate: every rendered <img> must carry an alt attribute (alt="" is
# allowed for decorative images); a completely missing alt hurts accessibility and image SEO. Error
# severity — fails the build so image a11y can never silently regress. Logic in improve/imgaltcheck.py.
_ia_spec = _ilu.spec_from_file_location("imgaltcheck", os.path.join(HERE, "improve", "imgaltcheck.py"))
_ia_mod = _ilu.module_from_spec(_ia_spec)
_ia_spec.loader.exec_module(_ia_mod)
audit_img_alt = _ia_mod.audit_img_alt

# Reading-time byline helper: estimate whole-minute read time from a page's plain text at ~220 wpm.
# Logic in improve/readingtime.py.
_rt_spec = _ilu.spec_from_file_location("readingtime", os.path.join(HERE, "improve", "readingtime.py"))
_rt_mod = _ilu.module_from_spec(_rt_spec)
_rt_spec.loader.exec_module(_rt_mod)
reading_minutes = _rt_mod.reading_minutes

# Machine-readable reading-length metadata for JSON-LD (wordCount + ISO-8601 timeRequired).
# Logic in improve/readingmeta.py.
_rm_spec = _ilu.spec_from_file_location("readingmeta", os.path.join(HERE, "improve", "readingmeta.py"))
_rm_mod = _ilu.module_from_spec(_rm_spec)
_rm_spec.loader.exec_module(_rm_mod)
iso8601_duration = _rm_mod.iso8601_duration
word_count = _rm_mod.word_count

# Semantic-<time> byline helper: wrap a YYYY-MM-DD date in <time datetime="..."> so the
# visible published/updated dates are machine-parseable in the rendered HTML (not only in
# JSON-LD). Non-date labels pass through untouched. Logic in improve/timetag.py.
_tt_spec = _ilu.spec_from_file_location("timetag", os.path.join(HERE, "improve", "timetag.py"))
_tt_mod = _ilu.module_from_spec(_tt_spec)
_tt_spec.loader.exec_module(_tt_mod)
time_tag = _tt_mod.time_tag

# The canonical origin. When Connor enables GitHub Pages this is the live URL; swap for a custom domain later.
BASE_URL = "https://connor-enge.github.io/seo-guide"
BLOG_URL = BASE_URL + "/blog/"
SEARCH_URL = BASE_URL + "/search/"       # on-site client-side search + human-browsable index
SEARCH_INDEX_URL = BASE_URL + "/search-index.json"  # tiny build-time index the search page fetches
FEED_URL = BASE_URL + "/feed.xml"        # RSS 2.0 feed of posts + content pages
JSON_FEED_URL = BASE_URL + "/feed.json"  # JSON Feed 1.1 mirror of the same items
SITE_NAME = "The Guide to SEO"
BLOG_TITLE = "The SEO Blog"
BLOG_DESC = ("SEO blog delivers practical articles on Core Web Vitals, content that ranks, "
             "technical fixes, and how Google evaluates pages for search results.")
AUTHOR = "Connor Enge"
AUTHOR_URL = BASE_URL + "/about/"
AUTHOR_SAMEAS = ["https://github.com/Connor-Enge"]
# Byline link to the author/About page — a lightweight, site-wide E-E-A-T signal.
BYLINE_BY = 'by <a class="author" rel="author" href="%s">%s</a>' % (AUTHOR_URL, html.escape(AUTHOR))

# ---- Entity graph: stable @id anchors so Organization/WebSite/Person/pages form one graph ----
HOME_URL = BASE_URL + "/"
ORG_ID = BASE_URL + "/#organization"
SITE_ID = BASE_URL + "/#website"
PERSON_ID = AUTHOR_URL + "#person"      # the author node, defined on /about/ but present on every page
LOGO_ID = BASE_URL + "/#logo"
LOGO_URL = BASE_URL + "/assets/logo.svg"
SITE_DESC = ("A practical, no-fluff guide to search engine optimization — how Google ranks pages and "
             "how to earn visibility with helpful content, sound technical foundations, and honest measurement.")
ORG_DESC = ("An independent, hand-built SEO guide and blog explaining how search works and how to earn "
            "rankings, with every claim sourced to primary documentation.")
PERSON_DESC = ("Writes and maintains The Guide to SEO — explaining how search actually works and how to "
               "earn rankings with genuinely useful pages, sourced to primary documentation.")
PERSON_KNOWS = ["Search engine optimization", "Technical SEO", "Core Web Vitals",
                "Structured data", "Content strategy"]


# ---------- tiny markdown renderer (headings, paras, lists, links, bold, code, blockquote) ----------
def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"`(.+?)`", r"<code>\1</code>", t)
    t = re.sub(r"\[(.+?)\]\((.+?)\)",
               lambda m: '<a href="%s">%s</a>' % (resolve_href(m.group(2), BASE_URL), m.group(1)), t)
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


def search_text(body):
    """Body markdown -> compact plain text for the search index. Matched against but never
    displayed, so a query for a term that lives in the prose (canonical, hreflang, INP,
    robots.txt) finds the right page — not just words in the title/description."""
    out = []
    for ln in body.split("\n"):
        s = ln.strip()
        if not s:
            continue
        s = re.sub(r"^#{1,6}\s+", "", s)     # heading markers
        s = re.sub(r"^\d+\.\s+", "", s)      # ordered-list markers
        s = re.sub(r"^[-*>]\s+", "", s)      # bullet / blockquote markers
        out.append(plain(s))
    return re.sub(r"\s+", " ", " ".join(out)).strip()


def render_md(body):
    out, i, lines = [], 0, body.split("\n")
    toc = []
    while i < len(lines):
        ln = lines[i].rstrip()
        fenced = consume_fence(lines, i)   # ```code``` fence -> <pre><code>…</pre>
        if fenced is not None:
            block, i = fenced
            out.append(block)
            continue
        if not ln.strip():
            i += 1
            continue
        if ln.startswith("### "):
            out.append(f"<h3>{inline(ln[4:])}</h3>")
        elif ln.startswith("## "):
            txt = ln[3:]
            slug = re.sub(r"[^a-z0-9]+", "-", txt.lower()).strip("-")
            toc.append((txt, slug))
            out.append(heading_html(slug, inline(txt)))
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


# ---------- JSON-LD: one connected @graph per page ----------
# Every page carries the Organization, WebSite and Person nodes so each page-level @id
# reference (author, publisher, isPartOf) resolves within that same page — the robust
# pattern Google recommends over fragile cross-page @id references.
def graph(*nodes):
    doc = {"@context": "https://schema.org", "@graph": [n for n in nodes if n]}
    return ('<script type="application/ld+json">%s</script>'
            % json.dumps(doc, ensure_ascii=False, separators=(",", ":")))


def node_org():
    return {
        "@type": "Organization", "@id": ORG_ID, "name": SITE_NAME, "alternateName": "SEO Guide",
        "url": HOME_URL, "description": ORG_DESC,
        "logo": {"@type": "ImageObject", "@id": LOGO_ID, "url": LOGO_URL, "contentUrl": LOGO_URL,
                 "width": 112, "height": 112, "caption": SITE_NAME},
        "image": {"@id": LOGO_ID}, "sameAs": AUTHOR_SAMEAS, "founder": {"@id": PERSON_ID},
    }


def node_website():
    return {
        "@type": "WebSite", "@id": SITE_ID, "url": HOME_URL, "name": SITE_NAME,
        "alternateName": "SEO Guide", "description": SITE_DESC, "inLanguage": "en",
        "publisher": {"@id": ORG_ID},
        # Sitelinks searchbox: points Google at the on-site search page. The literal
        # {search_term_string} placeholder is required by the SearchAction spec.
        "potentialAction": {
            "@type": "SearchAction",
            "target": {"@type": "EntryPoint",
                       "urlTemplate": SEARCH_URL + "?q={search_term_string}"},
            "query-input": "required name=search_term_string",
        },
    }


def node_person():
    return {
        "@type": "Person", "@id": PERSON_ID, "name": AUTHOR, "url": AUTHOR_URL,
        "description": PERSON_DESC, "sameAs": AUTHOR_SAMEAS, "knowsAbout": PERSON_KNOWS,
    }


def node_article(atype, headline, description, url, date_pub, date_mod, words=None, minutes=None):
    node = {
        "@type": atype, "@id": url + "#article", "isPartOf": {"@id": SITE_ID},
        "headline": headline, "description": description, "inLanguage": "en",
        "datePublished": date_pub, "dateModified": date_mod, "mainEntityOfPage": url,
        "author": {"@id": PERSON_ID}, "publisher": {"@id": ORG_ID},
    }
    # Expose the same reading-length signal the byline shows to humans, but to machines:
    # wordCount + an ISO-8601 timeRequired ("PT7M"). Omitted where there is no article body
    # to measure (e.g. the homepage hub, which carries no reading-time byline either).
    if words is not None:
        node["wordCount"] = words
    if minutes is not None:
        node["timeRequired"] = iso8601_duration(minutes)
    return node


def node_profile(url, date_mod):
    return {
        "@type": "ProfilePage", "@id": url + "#profilepage", "isPartOf": {"@id": SITE_ID},
        "url": url, "dateModified": date_mod, "mainEntity": {"@id": PERSON_ID},
    }


def node_blog(url, posts):
    return {
        "@type": "Blog", "@id": url + "#blog", "name": BLOG_TITLE, "url": BLOG_URL,
        "description": BLOG_DESC, "isPartOf": {"@id": SITE_ID}, "publisher": {"@id": ORG_ID},
        "blogPost": [{"@type": "BlogPosting", "headline": m["title"], "url": post_url(m["slug"]),
                      "datePublished": m.get("date", ""), "description": m["description"]}
                     for m, _ in posts],
    }


def node_breadcrumb(url, items):
    return {
        "@type": "BreadcrumbList", "@id": url + "#breadcrumb",
        "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u}
                            for i, (n, u) in enumerate(items)],
    }


def node_faq(url, faqs):
    return {
        "@type": "FAQPage", "@id": url + "#faq",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs],
    }


# ---------- syndication feeds (RSS 2.0 + JSON Feed 1.1) ----------
# One `feed_items` list drives both feeds so they can never drift. Each item is a dict:
# {title, url, description, date (YYYY-MM-DD published), updated, tags:[...]}.
def rfc822(date_str):
    """A YYYY-MM-DD date -> an RFC-822 timestamp (midnight UTC), the format RSS pubDate requires."""
    try:
        d = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    except (ValueError, TypeError):
        d = datetime.datetime.combine(datetime.date.today(), datetime.time())
    return email.utils.format_datetime(d.replace(tzinfo=datetime.timezone.utc))


def build_rss(items, build_date):
    def esc(s):
        return html.escape(str(s), quote=False)
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" '
           'xmlns:dc="http://purl.org/dc/elements/1.1/">',
           '<channel>',
           f'<title>{esc(SITE_NAME)}</title>',
           f'<link>{HOME_URL}</link>',
           f'<atom:link href="{FEED_URL}" rel="self" type="application/rss+xml"/>',
           f'<description>{esc(SITE_DESC)}</description>',
           '<language>en</language>',
           f'<lastBuildDate>{rfc822(build_date)}</lastBuildDate>',
           '<generator>build.py — a static, no-JS SEO guide generator</generator>']
    for it in items:
        out.append('<item>')
        out.append(f'<title>{esc(it["title"])}</title>')
        out.append(f'<link>{it["url"]}</link>')
        out.append(f'<guid isPermaLink="true">{it["url"]}</guid>')
        out.append(f'<pubDate>{rfc822(it["date"])}</pubDate>')
        out.append(f'<dc:creator>{esc(AUTHOR)}</dc:creator>')
        for tag in it.get("tags", []):
            out.append(f'<category>{esc(tag)}</category>')
        out.append(f'<description>{esc(it["description"])}</description>')
        out.append('</item>')
    out.append('</channel>')
    out.append('</rss>')
    return "\n".join(out) + "\n"


def build_json_feed(items):
    feed = {
        "version": "https://jsonfeed.org/version/1.1",
        "title": SITE_NAME,
        "home_page_url": HOME_URL,
        "feed_url": JSON_FEED_URL,
        "description": SITE_DESC,
        "language": "en",
        "icon": LOGO_URL,
        "favicon": LOGO_URL,
        "authors": [{"name": AUTHOR, "url": AUTHOR_URL}],
        "items": [],
    }
    for it in items:
        entry = {
            "id": it["url"], "url": it["url"], "title": it["title"],
            "summary": it["description"], "content_text": it["description"],
            "date_published": it["date"] + "T00:00:00Z",
            "date_modified": it["updated"] + "T00:00:00Z",
            "authors": [{"name": AUTHOR, "url": AUTHOR_URL}],
        }
        if it.get("tags"):
            entry["tags"] = it["tags"]
        feed["items"].append(entry)
    return json.dumps(feed, ensure_ascii=False, indent=2) + "\n"


def main():
    today = datetime.date.today().isoformat()
    pages = sorted((parse(p) for p in glob.glob(os.path.join(CONTENT, "*.md"))),
                   key=lambda x: int(x[0]["order"]))
    posts = [parse(p) for p in glob.glob(os.path.join(BLOG, "*.md"))]
    # newest-first; posts must carry a `date` (YYYY-MM-DD) front-matter field
    posts.sort(key=lambda x: x[0].get("date", "0000-00-00"), reverse=True)

    nav = "".join(f'<li><a href="{page_url(m["slug"])}">{html.escape(m["title"])}</a></li>' for m, _ in pages)
    nav += f'<li><a href="{BLOG_URL}">Blog</a></li>'

    def render(*, title, description, url, og_type, h1, byline, toc="", content="", pager="",
               jsonld="", scripts="", breadcrumb=""):
        content = mark_external(content, BASE_URL)  # annotate outbound reference links (improve/extlinks.py)
        return TEMPLATE.format(
            title=html.escape(title), site=html.escape(SITE_NAME),
            description=html.escape(description), canonical=url, base=BASE_URL,
            og_type=og_type, nav=nav, h1=html.escape(h1), byline=byline,
            toc=toc, content=content, pager=pager, jsonld=jsonld,
            scripts=('<script defer src="%s/assets/search-focus.js"></script><script defer src="%s/assets/backtotop.js"></script><script defer src="%s/assets/scrollspy.js"></script>' % (BASE_URL, BASE_URL, BASE_URL))
                    + ('<script defer src="%s/assets/copycode.js"></script>' % BASE_URL if "<pre" in content else "")
                    + scripts,
            breadcrumb=breadcrumb, year=today[:4])

    def toc_block(toc):
        return ('<nav class="toc" aria-label="On this page"><p>On this page</p><ul>'
                + "".join(f'<li><a href="#{s}">{html.escape(t)}</a></li>' for t, s in toc)
                + "</ul></nav>") if toc else ""

    # Registry for the `related:` front-matter field -> descriptive internal links.
    # A key is a guide-page slug (e.g. "technical-seo") or a post keyed "blog/<slug>",
    # so any page or post can cross-link to any other with a genuine descriptive anchor.
    related_registry = {m["slug"]: (m["title"], m["description"], page_url(m["slug"]))
                        for m, _ in pages}
    related_registry.update({"blog/" + m["slug"]: (m["title"], m["description"], post_url(m["slug"]))
                             for m, _ in posts})

    def related_block(field, current_url):
        """Render a curated 'Related reading' block from a comma-separated `related:` field.
        Unknown keys and self-links are skipped; returns '' when nothing resolves."""
        seen, items = set(), []
        for key in (k.strip() for k in field.split(",")):
            entry = related_registry.get(key)
            if not entry or entry[2] == current_url or entry[2] in seen:
                continue
            seen.add(entry[2])
            items.append(entry)
        if not items:
            return ""
        lis = "".join('<li><a href="%s">%s</a><p>%s</p></li>'
                      % (u, html.escape(t), html.escape(d)) for t, d, u in items)
        return ('<nav class="related" aria-label="Related reading"><h2>Related reading</h2>'
                '<ul class="related-list">%s</ul></nav>' % lis)

    def write(slug_dir, page):
        d = OUT if slug_dir == "" else os.path.join(OUT, slug_dir)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w").write(page)

    os.makedirs(OUT, exist_ok=True)

    # copy static assets (CSS, images) into docs/ so the stylesheet actually resolves
    import shutil
    _assets = os.path.join(HERE, "assets")
    if os.path.isdir(_assets):
        shutil.copytree(_assets, os.path.join(OUT, "assets"), dirs_exist_ok=True)

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
        crumbs = [("Home", HOME_URL)] + ([] if slug == "index" else [(meta["title"], url)])
        base_nodes = [node_org(), node_website(), node_person()]
        if meta.get("schema") == "ProfilePage":
            updated = meta.get("updated", today)
            jsonld = graph(*base_nodes, node_profile(url, updated), node_breadcrumb(url, crumbs))
            byline = f'Maintained by {html.escape(AUTHOR)} · Updated {time_tag(updated, updated)}'
            og_type = "profile"
        else:
            faqs = extract_faq(body)
            art_text = search_text(body)
            page_nodes = base_nodes + [
                node_article("Article", meta["title"], meta["description"], url,
                             meta.get("updated", today), today,
                             words=None if slug == "index" else word_count(art_text),
                             minutes=None if slug == "index" else reading_minutes(art_text)),
                node_breadcrumb(url, crumbs)]
            if faqs:
                page_nodes.append(node_faq(url, faqs))
            jsonld = graph(*page_nodes)
            _upd = meta.get("updated", today)
            byline = f'Updated {time_tag(_upd, _upd)} · {BYLINE_BY}'
            if slug != "index":
                byline += f' · {reading_minutes(search_text(body))} min read'
            og_type = "website" if slug == "index" else "article"
        page = render(
            title=meta["title"], description=meta["description"], url=url,
            og_type=og_type,
            h1=meta.get("h1", meta["title"]),
            byline=byline,
            toc=toc_block(toc), content=content_html + related_block(meta.get("related", ""), url),
            pager=('<nav class="pager">' + "".join(links) + "</nav>") if links else "",
            jsonld=jsonld, breadcrumb=breadcrumb_block(crumbs))
        write("" if slug == "index" else slug, page)

    # ---------- blog posts ----------
    # Plain-data card list so each post can auto-link to sibling posts sharing tags.
    post_cards = [{"slug": m["slug"], "title": m["title"], "description": m["description"],
                   "tags": [t.strip() for t in m.get("tags", "").split(",") if t.strip()]}
                  for m, _ in posts]
    for meta, body in posts:
        slug = meta["slug"]
        content_html, toc = render_md(body)
        url = post_url(slug)
        date_pub = meta.get("date", today)
        date_mod = meta.get("updated", date_pub)
        byline = f"Published {time_tag(date_pub, date_pub)} · {BYLINE_BY}"
        if date_mod and date_mod != date_pub:
            byline += f" · Updated {time_tag(date_mod, date_mod)}"
        byline += f' · {reading_minutes(search_text(body))} min read'
        crumbs = [("Home", HOME_URL), (BLOG_TITLE, BLOG_URL), (meta["title"], url)]
        faqs = extract_faq(body)
        post_text = search_text(body)
        post_nodes = [node_org(), node_website(), node_person(),
                      node_article("BlogPosting", meta["title"], meta["description"], url, date_pub, date_mod,
                                   words=word_count(post_text), minutes=reading_minutes(post_text)),
                      node_breadcrumb(url, crumbs)]
        if faqs:
            post_nodes.append(node_faq(url, faqs))
        jsonld = graph(*post_nodes)
        page = render(
            title=meta["title"], description=meta["description"], url=url, og_type="article",
            h1=meta.get("h1", meta["title"]), byline=byline,
            toc=toc_block(toc),
            content=(content_html + related_block(meta.get("related", ""), url)
                     + related_posts_block(slug,
                                           [t.strip() for t in meta.get("tags", "").split(",") if t.strip()],
                                           post_cards, post_url)),
            pager=f'<nav class="pager"><a class="prev" href="{BLOG_URL}">← All articles</a></nav>',
            jsonld=jsonld, breadcrumb=breadcrumb_block(crumbs))
        write(os.path.join("blog", slug), page)

    # ---------- blog index ----------
    if posts:
        items = "".join(
            post_list_item(
                post_url(m["slug"]), m["title"],
                time_tag(m.get("date", ""), html.escape(m.get("date", ""))),
                m["description"], reading_minutes(search_text(b)))
            for m, b in posts)
        blog_content = f"<p>{BLOG_DESC}</p><ul class=\"post-list\">{items}</ul>"
    else:
        blog_content = f"<p>{BLOG_DESC}</p><p>Articles are on the way.</p>"
    blog_jsonld = graph(node_org(), node_website(), node_person(), node_blog(BLOG_URL, posts),
                        node_breadcrumb(BLOG_URL, [("Home", HOME_URL), (BLOG_TITLE, BLOG_URL)]))
    write("blog", render(
        title=BLOG_TITLE, description=BLOG_DESC, url=BLOG_URL, og_type="website",
        h1=BLOG_TITLE, byline=f"Practical, sourced SEO articles · {BYLINE_BY}",
        content=blog_content, jsonld=blog_jsonld,
        breadcrumb=breadcrumb_block([("Home", HOME_URL), (BLOG_TITLE, BLOG_URL)])))

    # ---------- on-site search: a build-time index + the /search/ page ----------
    # One `search_items` list drives BOTH the JSON index (fetched by search.js) and the
    # static, no-JS browsable list on the page — so they can never drift. Every page and
    # post is searchable; the page works with zero JS (it renders the full list) and is
    # progressively enhanced into a live client-side filter. No server, no dependencies.
    def item_type(m):
        if m.get("schema") == "ProfilePage":
            return "About"
        return "Home" if m["slug"] == "index" else "Guide"

    search_items = [{"title": m["title"], "url": page_url(m["slug"]),
                     "description": m["description"], "type": item_type(m),
                     "tags": [t.strip() for t in m.get("tags", "").split(",") if t.strip()],
                     "text": search_text(b)}
                    for m, b in pages]
    search_items.append({"title": BLOG_TITLE, "url": BLOG_URL,
                         "description": BLOG_DESC, "type": "Blog", "tags": [], "text": ""})
    search_items += [{"title": m["title"], "url": post_url(m["slug"]),
                      "description": m["description"], "type": "Article",
                      "tags": [t.strip() for t in m.get("tags", "").split(",") if t.strip()],
                      "text": search_text(b)}
                     for m, b in posts]
    open(os.path.join(OUT, "search-index.json"), "w").write(
        json.dumps(search_items, ensure_ascii=False, separators=(",", ":")) + "\n")

    def search_li(it):
        return ('<li><a href="%s">%s</a> <span class="tag">%s</span><p>%s</p></li>'
                % (it["url"], html.escape(it["title"]), html.escape(it["type"]),
                   html.escape(it["description"])))

    search_content = (
        '<div class="search" id="search" data-index="%s">' % SEARCH_INDEX_URL
        + '<form class="searchform" role="search" method="get" action="%s">' % SEARCH_URL
        + '<label class="visually-hidden" for="q">Search the guide</label>'
        + '<input type="search" id="q" name="q" placeholder="Search the guide…" '
          'autocomplete="off" enterkeyhint="search" aria-describedby="search-status">'
        + '<button type="submit">Search</button></form>'
        + '<p id="search-status" class="search-status" role="status" aria-live="polite"></p>'
        + '<ul class="search-results" id="results" hidden></ul>'
        + '<div id="all"><p class="search-hint">Every page and article on the site:</p>'
        + '<ul class="search-results">%s</ul></div>' % "".join(search_li(it) for it in search_items)
        + '</div>')
    search_desc = ("Search The Guide to SEO — instantly filter every page and article on keyword "
                   "research, on-page and technical SEO, content quality, links, and measurement.")
    search_jsonld = graph(node_org(), node_website(), node_person(),
                          node_breadcrumb(SEARCH_URL, [("Home", HOME_URL), ("Search", SEARCH_URL)]))
    write("search", render(
        title="Search", description=search_desc, url=SEARCH_URL, og_type="website",
        h1="Search the guide",
        byline="Type to filter every page and article on the site — no page reload, no tracking.",
        content=search_content, jsonld=search_jsonld,
        breadcrumb=breadcrumb_block([("Home", HOME_URL), ("Search", SEARCH_URL)]),
        scripts='<script defer src="%s/assets/search.js"></script>' % BASE_URL))

    # ---------- custom 404 (GitHub Pages serves docs/404.html for unknown paths) ----------
    # Doubles as a mini-directory: every section + the blog + on-site search, plus a search box.
    nf_cards = [(m["title"], m["description"], page_url(m["slug"]))
                for m, _ in pages if m["slug"] != "index"]
    nf_cards.append((BLOG_TITLE, BLOG_DESC, BLOG_URL))
    nf_cards.append(("Search the guide", "Find any page or article on the site.", SEARCH_URL))
    nf_url = BASE_URL + "/404.html"
    open(os.path.join(OUT, "404.html"), "w").write(render(
        title=NF_TITLE, description=NF_DESCRIPTION, url=nf_url, og_type="website",
        h1=NF_H1, byline=NF_BYLINE, content=notfound_content(BASE_URL, nf_cards),
        breadcrumb=breadcrumb_block([("Home", HOME_URL), (NF_TITLE, nf_url)])))

    # ---------- sitemap + robots ----------
    entries = [(page_url(m["slug"]), today, "1.0" if m["slug"] == "index" else "0.8") for m, _ in pages]
    entries.append((BLOG_URL, today, "0.7"))
    entries += [(post_url(m["slug"]), m.get("updated", m.get("date", today)), "0.6") for m, _ in posts]
    entries.append((SEARCH_URL, today, "0.4"))  # human-browsable index + on-site search
    urls = "".join(f"<url><loc>{loc}</loc><lastmod>{mod}</lastmod><priority>{pri}</priority></url>"
                   for loc, mod, pri in entries)
    open(os.path.join(OUT, "sitemap.xml"), "w").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + urls + "</urlset>\n")
    open(os.path.join(OUT, "robots.txt"), "w").write(
        f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}/sitemap.xml\n")
    open(os.path.join(OUT, ".nojekyll"), "w").write("")

    # ---------- web app manifest: makes the Organization logo the browser-tab + install icon ----------
    # Generated (not a static asset) so BASE_URL is baked in and can't drift from the subpath deploy.
    manifest = {
        "name": SITE_NAME, "short_name": "SEO Guide", "description": SITE_DESC,
        "start_url": HOME_URL, "scope": BASE_URL + "/", "display": "standalone",
        "theme_color": "#0b6bcb", "background_color": "#ffffff",
        "icons": [{"src": LOGO_URL, "type": "image/svg+xml", "sizes": "any", "purpose": "any"}],
    }
    open(os.path.join(OUT, "site.webmanifest"), "w").write(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")

    # ---------- syndication feeds: blog posts (newest first) then evergreen content pages ----------
    feed_items = [
        {"title": m["title"], "url": post_url(m["slug"]), "description": m["description"],
         "date": m.get("date", today), "updated": m.get("updated", m.get("date", today)),
         "tags": [t.strip() for t in m.get("tags", "").split(",") if t.strip()]}
        for m, _ in posts]
    feed_items += [
        {"title": m["title"], "url": page_url(m["slug"]), "description": m["description"],
         "date": m.get("updated", today), "updated": m.get("updated", today), "tags": []}
        for m, _ in pages
        if m["slug"] != "index" and m.get("schema") != "ProfilePage"]
    open(os.path.join(OUT, "feed.xml"), "w").write(build_rss(feed_items, today))
    open(os.path.join(OUT, "feed.json"), "w").write(build_json_feed(feed_items))

    # ---------- integrity gate: never ship a broken internal link / soft-404 ----------
    problems = audit_internal_links(OUT, BASE_URL)
    if problems:
        print(f"\nINTERNAL-LINK AUDIT FAILED — {len(problems)} problem(s):")
        for p in problems:
            print(f"  [{p['kind']}] {p['page']} -> {p['href']}  ({p['detail']})")
        raise SystemExit(1)
    print("Internal-link audit: OK — no dangling internal links or root-relative hrefs.")

    # ---------- integrity gate: every page must self-canonicalize (no canonical drift) ----------
    canon_problems = audit_canonicals(OUT, BASE_URL)
    if canon_problems:
        print(f"\nCANONICAL AUDIT FAILED — {len(canon_problems)} problem(s):")
        for p in canon_problems:
            print(f"  [{p['kind']}] {p['page']}  ({p['detail']})")
        raise SystemExit(1)
    print("Canonical audit: OK — every page self-canonicalizes to its own URL.")

    # ---------- metadata gate: exactly one title/description per page; report snippet-quality warnings ----------
    meta_problems = audit_meta(OUT)
    meta_errors = [p for p in meta_problems if p.get("severity") == "error"]
    meta_warns = [p for p in meta_problems if p.get("severity") == "warn"]
    if meta_warns:
        print(f"\nMetadata audit — {len(meta_warns)} warning(s) (snippet quality, non-blocking):")
        for p in meta_warns:
            print(f"  [{p['kind']}] {p['page']}  ({p['detail']})")
    if meta_errors:
        print(f"\nMETADATA AUDIT FAILED — {len(meta_errors)} error(s):")
        for p in meta_errors:
            print(f"  [{p['kind']}] {p['page']}  ({p['detail']})")
        raise SystemExit(1)
    print(f"Metadata audit: OK — every page has exactly one <title> and one meta description"
          f" ({len(meta_warns)} snippet warning(s)).")

    # ---------- structured-data gate: JSON-LD must parse; entity graph must stay connected ----------
    jsonld_problems = audit_jsonld(OUT, BASE_URL)
    if jsonld_problems:
        print(f"\nJSON-LD AUDIT FAILED — {len(jsonld_problems)} problem(s):")
        for p in jsonld_problems:
            print(f"  [{p['kind']}] {p['page']}  ({p['detail']})")
        raise SystemExit(1)
    print("JSON-LD audit: OK — every page's entity graph parses with connected, absolute, consistent @ids.")

    # ---------- blog structured-data gate: every post carries a complete BlogPosting node ----------
    blogposting_problems = audit_blog_posting(OUT, BASE_URL)
    if blogposting_problems:
        print(f"\nBLOGPOSTING AUDIT FAILED — {len(blogposting_problems)} problem(s):")
        for p in blogposting_problems:
            print(f"  [{p['kind']}] {p['page']}  ({p['detail']})")
        raise SystemExit(1)
    print("BlogPosting audit: OK — every blog post carries a complete BlogPosting node"
          " (headline, datePublished, dateModified, author).")

    # ---------- sitemap gate: well-formed; every <loc> absolute + resolves; no dupes; no 404 listed ----------
    sitemap_problems = audit_sitemap(OUT, BASE_URL)
    sm_errors = [p for p in sitemap_problems if p.get("severity") == "error"]
    sm_warns = [p for p in sitemap_problems if p.get("severity") == "warn"]
    if sm_warns:
        print(f"\nSitemap audit — {len(sm_warns)} warning(s) (orphan-from-sitemap, non-blocking):")
        for p in sm_warns:
            print(f"  [{p['kind']}] {p['loc']}  ({p['detail']})")
    if sm_errors:
        print(f"\nSITEMAP AUDIT FAILED — {len(sm_errors)} error(s):")
        for p in sm_errors:
            print(f"  [{p['kind']}] {p['loc']}  ({p['detail']})")
        raise SystemExit(1)
    print(f"Sitemap audit: OK — every <loc> is absolute, resolves to a real file, unique, and 404-free"
          f" ({len(sm_warns)} orphan warning(s)).")

    # ---------- robots.txt gate: exists, absolute Sitemap: == BASE_URL/sitemap.xml, no blanket Disallow under * ----------
    robots_problems = audit_robots(OUT, BASE_URL)
    rb_errors = [p for p in robots_problems if p.get("severity") == "error"]
    rb_warns = [p for p in robots_problems if p.get("severity") == "warn"]
    if rb_warns:
        print(f"\nRobots audit — {len(rb_warns)} warning(s) (non-blocking):")
        for p in rb_warns:
            print(f"  [{p['kind']}] {p['loc']}  ({p['detail']})")
    if rb_errors:
        print(f"\nROBOTS AUDIT FAILED — {len(rb_errors)} error(s):")
        for p in rb_errors:
            print(f"  [{p['kind']}] {p['loc']}  ({p['detail']})")
        raise SystemExit(1)
    print("Robots audit: OK — robots.txt present, Sitemap: is absolute and matches the sitemap URL,"
          " and no blanket Disallow: / under User-agent: *.")

    # ---------- heading gate: every rendered page must carry exactly one <h1> ----------
    h1_problems = audit_h1(OUT)
    if h1_problems:
        print(f"\nH1 AUDIT FAILED — {len(h1_problems)} page(s) without exactly one <h1>:")
        for p in h1_problems:
            print(f"  {p['page']}  ({p['detail']})")
        raise SystemExit(1)
    print("H1 audit: OK — every rendered page carries exactly one <h1>.")

    # ---------- social-snippet gate: og:url absolute + == canonical (error); og/twitter tags present (warn) ----------
    social_problems = audit_social_meta(OUT)
    so_errors = [p for p in social_problems if p.get("severity") == "error"]
    so_warns = [p for p in social_problems if p.get("severity") == "warn"]
    if so_warns:
        print(f"\nSocial-meta audit — {len(so_warns)} warning(s) (Open Graph / Twitter, non-blocking):")
        for p in so_warns:
            print(f"  [{p['kind']}] {p['page']}  ({p['detail']})")
    if so_errors:
        print(f"\nSOCIAL-META AUDIT FAILED — {len(so_errors)} error(s):")
        for p in so_errors:
            print(f"  [{p['kind']}] {p['page']}  ({p['detail']})")
        raise SystemExit(1)
    print(f"Social-meta audit: OK — every page's og:url is absolute and matches its canonical"
          f" ({len(so_warns)} snippet warning(s)).")

    # ---------- image-accessibility gate: every rendered <img> must carry an alt attribute ----------
    img_alt_problems = audit_img_alt(OUT)
    if img_alt_problems:
        print(f"\nIMG-ALT AUDIT FAILED — {len(img_alt_problems)} <img> tag(s) missing an alt attribute:")
        for p in img_alt_problems:
            print(f"  [{p['kind']}] {p['page']}  ({p['detail']})")
        raise SystemExit(1)
    print("Image-alt audit: OK — every rendered <img> carries an alt attribute (alt=\"\" allowed for decorative).")

    # ---------- heading-order gate (report-only): flag skipped heading levels (broken outline) ----------
    ho_problems = audit_heading_order(OUT)
    if ho_problems:
        print(f"\nHeading-order audit — {len(ho_problems)} warning(s) (skipped heading level, non-blocking):")
        for p in ho_problems:
            print(f"  [{p['kind']}] {p['page']}  ({p['detail']})")
    else:
        print("Heading-order audit: OK — no page skips a heading level.")

    print(f"Built {len(pages)} guide pages + {len(posts)} blog post(s) -> docs/  "
          f"(+ /blog/, sitemap.xml, robots.txt, feed.xml, feed.json [{len(feed_items)} items])")
    for m, _ in pages:
        print(f"  {page_url(m['slug'])}")
    print(f"  {BLOG_URL}")
    for m, _ in posts:
        print(f"  {post_url(m['slug'])}")


if __name__ == "__main__":
    main()

---
slug: robots-txt-vs-noindex
title: robots.txt vs. noindex vs. X-Robots-Tag
h1: "robots.txt vs. meta robots vs. X-Robots-Tag: Crawling vs. Indexing Control"
description: "robots.txt controls crawling; noindex controls indexing. Why 'noindex in robots.txt' fails, when to use the meta robots tag vs. X-Robots-Tag, and how to choose."
date: 2026-08-08
updated: 2026-08-08
tags: technical-seo, robots-txt, noindex, crawling, indexing
related: technical-seo, how-search-works, common-seo-mistakes
---
robots.txt controls which URLs crawlers can access on your site. The noindex directive, set through a meta tag or X-Robots-Tag header, controls whether Google includes a page in its search results. Confusing the two produces the most frequent [technical indexing errors](/common-seo-mistakes/): pages that should remain hidden appear anyway, while pages that should rank stay blocked.

## What robots.txt actually does
A robots.txt file tells [search engine crawlers](/how-search-works/) which URLs they can access. Its primary purpose is to manage crawl traffic and prevent overload from excessive requests. Googlebot follows the rules it finds there, but the file does not instruct Google to exclude any URL from search results.

Rules in robots.txt are not supported by every crawler. Different crawlers may interpret the syntax in their own way. Because compliance is voluntary, robots.txt provides no security protection. For genuinely private content, server-side password protection remains the only reliable method.

## The trap: a disallowed page can still be indexed
When a page is disallowed in robots.txt, Googlebot does not crawl or index its content. External links can still cause Google to discover the URL itself. In that case the bare URL address, and sometimes the anchor text from those links, can appear in search results without any description or snippet.

The outcome is an indexed URL whose content Google has never seen. This happens because robots.txt only blocks access to the page; it does not prevent the URL from being recorded through third-party references.

## Why 'noindex' in robots.txt does nothing
Google does not recognize any noindex directive inside robots.txt. No valid syntax exists for that purpose. Placing the word "noindex" in the file produces no effect on indexing.

If a page remains disallowed in robots.txt, Googlebot cannot fetch it. Without the fetch, Google never sees an actual noindex instruction even if one exists on the page. The page can therefore stay indexed through external links until the robots.txt rule is removed.

## The meta robots tag: page-level indexing control
The noindex rule is delivered either by a meta tag in the HTML head or by an HTTP response header. When Googlebot crawls the page and encounters the rule, Google removes the page from search results regardless of external links pointing to it.

The tag takes the form `<meta name="robots" content="noindex">` for all crawlers or `name="googlebot"` when targeting only Google. Multiple directives can be combined in the content attribute, such as `noindex, nofollow`. Because the tag sits inside individual HTML pages, it allows per-page control without server configuration changes.

## X-Robots-Tag: the same control for non-HTML files
The X-Robots-Tag appears in the HTTP response header and accepts any rule that can be used in a meta robots tag. It is the required method for non-HTML resources such as PDFs, images, or video files where no meta tag can be inserted.

You can send multiple rules either as comma-separated values in one header or across several headers. A user-agent prefix can be added, for example `X-Robots-Tag: googlebot: noindex, nofollow`. Rules without a prefix apply to every crawler. The effect matches the meta tag exactly; the choice depends on whether the resource is HTML or another file type.

## The crawl-first paradox (why noindex needs a crawlable page)
Google must crawl a page before it can read the meta tag or response header. If robots.txt blocks the URL, crawlers never reach the noindex instruction. The page can therefore remain indexed through links from other sites.

The two controls are incompatible in this situation. To make noindex effective, [the page must stay crawlable](/technical-seo/) so that Googlebot can retrieve and apply the rule. Once the robots.txt disallow is removed, the next crawl can observe the noindex and drop the page from results.

## A decision guide
- If the goal is only to reduce unnecessary crawl requests on low-value or duplicate URLs and you accept that the bare URL might still appear, use a robots.txt Disallow.
- If the goal is to keep a page out of search results entirely, ensure the page remains crawlable and apply noindex via meta tag for HTML or X-Robots-Tag for other file types; do not add a robots.txt disallow at the same time.
- If the content must stay truly private, apply server-side password protection rather than relying on either robots.txt or noindex.
- For non-HTML files that should not appear in results, send an `X-Robots-Tag: noindex` header.
- rel="canonical" serves a different purpose: it signals a preferred version among pages you still want indexed. It does not block crawling or force removal, and combining it with noindex sends contradictory signals.

## Verifying it worked
After adding noindex, the page may continue to appear until Googlebot recrawls it. Recrawl time varies with the page's importance and can take weeks or months.

Use the URL Inspection tool in Google Search Console to request a fresh crawl and to inspect the exact HTML and headers Googlebot received. The Page Indexing report shows which pages Google has processed with a noindex rule.

If immediate removal is required, submit the URL through Google's removals process in addition to maintaining the noindex directive.

A frequent reason noindex appears ineffective is an active robots.txt disallow that prevents the crawl needed to read the tag; removing that disallow resolves the conflict.

---
slug: link-building
order: 7
title: Link Building & Reputation
h1: Link Building & Off-Page Reputation
description: Links remain a core signal of trust. Learn how to earn them the durable way — and which shortcuts get sites penalized.
updated: 2026-08-08
related: content-quality, on-page-seo, measuring
---
Links function as earned votes of confidence passed from one page to another. Google continues to use them as a core signal for relevance and authority, with the quality and topical fit of the linking site mattering far more than the total number acquired.

## Why links still matter

Google treats links as signals that help determine page relevance and that surface new pages for crawling. A link from a relevant, authoritative site carries more weight than dozens from unrelated or low-value sources. 

Links also aid discovery when they appear as standard `<a>` elements with `href` attributes; script-based or non-anchor links are frequently ignored. The surrounding context on the linking page further shapes how Google interprets the connection.

## How to earn links that last

Create assets that others naturally cite because they solve real problems or supply original data. Strong examples include primary research, downloadable tools, and comprehensive guides that stand on their own merit. These depend directly on the underlying [content quality](/content-quality/).

Digital PR works when you supply journalists or creators with verifiable facts, unique datasets, or timely commentary they can reference without negotiation. Build relationships through expert quotes, thoughtful guest contributions on established sites, and genuine partnerships that produce mutual value rather than reciprocal linking arrangements.

Reclaim unlinked brand mentions by monitoring the web for citations of your name or product and requesting links where appropriate. Locate and repair broken external links that once pointed to your content by offering updated, equivalent destinations.

## Anchor text and internal links

Good anchor text is descriptive, reasonably concise, and relevant to both the source page and the destination. It sets accurate expectations for readers and helps Google understand topical connections. Avoid generic phrases such as "click here" or "read more," overly long strings, or keyword-stuffed constructions; the last of these violates spam policies.

For image links, Google relies on the image's alt text in place of anchor text. Keep links from clustering too closely together so surrounding words provide useful context.

Internal links remain the only links under full control. They distribute authority across your own pages and should follow the same descriptive standards applied to external links. See [on-page SEO](/on-page-seo/) and [technical SEO](/technical-seo/) for related implementation details.

## Qualify the links you place

Use `rel="sponsored"` on any link that represents an advertisement or paid placement. Apply `rel="ugc"` to links within user-generated content such as comments and forum posts; you may later remove the attribute for contributors who prove consistently reliable.

Reserve `rel="nofollow"` for cases where neither of the above fits and you prefer Google not associate your site with or crawl the target page. For links inside your own site that you wish to exclude from crawling, use a robots.txt disallow rule instead.

Multiple values may be combined in a single attribute, for example `rel="ugc nofollow"`. Links carrying these attributes are generally not followed, though the destination pages can still be discovered through other means such as sitemaps or links from unrelated sites. Editorial links you want followed require no `rel` attribute at all.

## Link schemes to avoid

Google lists several practices as link spam. These include buying or selling links for ranking purposes, excessive reciprocal exchanges, automated link creation services, and requiring links in contracts or terms of service without allowing qualification. Text ads or native placements that pass ranking credit without qualification also qualify, as do low-quality directory links, keyword-rich widget links, and forum signatures containing optimized anchors.

Creating low-value content solely to generate links falls under the same category. Paid links themselves are not violations when properly qualified with `rel="sponsored"` or `rel="nofollow"`. Violations are detected through automated systems and, when needed, human review, and can trigger manual actions that suppress rankings.

## When (and when not) to disavow

Most sites never need the disavow tool because Google can evaluate link quality without external guidance. Use it only when you possess both a considerable volume of spammy or artificial links and evidence or strong likelihood that those links have produced or will produce a manual action.

Attempt removal of the problematic links first; disavow only the remainder. The tool is advanced and carries risk of unintended harm when applied incorrectly.

Track the impact of these efforts in [measuring SEO](/measuring/).

---
slug: glossary
order: 12
title: SEO Glossary
h1: SEO Glossary — Key Terms, Clearly Defined
description: SEO glossary gives plain definitions for crawling, indexing, canonicals, E-E-A-T, and Core Web Vitals each linked to further guides.
updated: 2026-08-06
tags: glossary, seo terms, definitions, reference
related: how-search-works, technical-seo, on-page-seo, common-seo-mistakes
---
This glossary compiles clear definitions of core SEO terminology used throughout search optimization work. Entries draw directly from established practices and Google documentation to support precise implementation. Many terms include links to expanded coverage in the site's dedicated guides.

## Alt text
Alternative text set on an image via the img alt attribute describes the image content for screen-reader users and for search engines that cannot process images directly. It also displays when an image fails to load. Specific, descriptive phrasing supports both accessibility compliance and clearer understanding in Google Images results; keyword repetition adds no value and should be avoided. See how on-page elements influence visibility in [our on-page SEO guide](/on-page-seo/).

## Anchor text
The visible, clickable words within a hyperlink convey the topic of the destination page to both users and search engines. Descriptive phrasing aligned with the linked content strengthens relevance signals, while repetitive exact-match or purchased anchors on controlled links can appear manipulative. Natural variation across links reduces risk while preserving clarity. Explore further details in [on-page SEO best practices](/on-page-seo/).

## Backlink
An inbound link from an external site to your own page functions as a vote of relevance and trust in Google's systems. Quality and topical alignment outweigh sheer volume, with editorial links earned through merit providing the strongest effect. Links acquired through payment or artificial means breach Google's link spam policy and can trigger manual actions. Review [proven link-building approaches](/link-building/) for additional guidance.

## Canonical URL
The canonical URL identifies the preferred version of a page when duplicate or near-duplicate copies exist across parameters, protocol differences, or slash variations. Declared through a rel="canonical" link element, it directs ranking signals toward a single URL. Google treats the directive as a strong signal rather than an absolute command.

## Core Web Vitals
Core Web Vitals comprise three real-user metrics that quantify page experience: LCP measured at 2.5 seconds or faster, INP at 200 milliseconds or less, and CLS at 0.1 or below, each evaluated at the 75th percentile. These thresholds serve as a ranking tie-breaker among pages already deemed relevant rather than a primary relevance driver. Passing thresholds requires attention to rendering, JavaScript execution, and layout stability. Read more in [the guide to passing Core Web Vitals](/blog/passing-core-web-vitals-2026/).

## Crawl budget
Crawl budget represents the volume of URLs Googlebot will fetch from a site within a given timeframe, governed by server response speed and perceived demand for the content. The metric matters primarily for sites exceeding hundreds of thousands of URLs; excessive duplicate or low-value paths consume capacity that could reach important pages instead.

## Crawling
Crawling describes the automated discovery process in which search engine bots follow hyperlinks and parse sitemaps to locate and retrieve page content. A page must be reachable by a crawler such as Googlebot before any further evaluation can occur. [Learn the mechanics behind how crawling works](/how-search-works/).

## Duplicate content
Duplicate content refers to substantially identical text appearing at multiple URLs on the same domain or copied across different sites. While isolated instances seldom provoke direct penalties, the duplication fragments ranking signals and forces Google to select a single representative version. Canonical tags or redirects consolidate those signals effectively; large-scale duplication intended to manipulate rankings violates spam policies.

## E-E-A-T
E-E-A-T encompasses the four qualities outlined in Google's Search Quality Rater Guidelines: Experience, Expertise, Authoritativeness, and Trust, with Trust carrying the greatest weight. The framework is not a scored ranking factor but reflects the outcomes Google's systems seek to reward, particularly on topics affecting health, finance, or safety. Demonstrating these qualities through sourcing, authorship clarity, and accuracy supports long-term visibility. [Additional context appears in the content quality guide](/content-quality/).

## Featured snippet
A featured snippet presents a highlighted extract from a page at the top of results to answer a query directly, accompanied by a link to the source. Google selects the content algorithmically from pages that supply concise, relevant answers; no markup guarantees inclusion. The placement is commonly referred to as position zero.

## Hreflang
Hreflang annotations, delivered via link tags, HTTP headers, or sitemap entries, specify the language or regional variant of a page intended for particular users. Proper implementation directs localized versions to the right audience and lowers the chance that an incorrect language page ranks instead. Reciprocal references between language versions are required for the signals to function reliably.

## Indexing
Indexing occurs after crawling when Google stores and analyzes a page's content, making it eligible for appearance in search results. Crawl status alone does not guarantee inclusion; thin, duplicate, or low-value pages may be excluded. A noindex directive or Search Console status messages such as "Crawled – currently not indexed" prevent a page from entering the index. Understand the full discovery process in [search mechanics overview](/how-search-works/).

## Internal link
An internal link connects one page to another within the same site, aiding both discovery by crawlers and the distribution of ranking signals. Descriptive anchor text combined with links originating from high-authority pages increases effectiveness. Consistent internal linking also clarifies site structure for users and algorithms alike. [Further guidance is available in the on-page SEO guide](/on-page-seo/).

## Keyword
A keyword denotes a word or phrase users enter into search engines, along with the underlying intent. Contemporary optimization addresses the full topic and intent rather than exact phrase repetition. Keyword research identifies actual queries and maps them to appropriate pages on a site. [See the keyword research guide for mapping methods](/keyword-research/).

## Meta description
The meta description supplies a summary in the dedicated HTML tag that Google may display as the snippet below the title in results. It carries no direct ranking weight, yet a clear and relevant description can improve click-through rates when used. Google frequently rewrites the text to align more closely with the query. [Practical application is covered in the on-page SEO guide](/on-page-seo/).

## Nofollow
A nofollow attribute on a link instructs Google not to treat the link as an endorsement and to withhold ranking credit. Since 2020 the directive functions as a hint rather than a strict command. Paid or advertising links should carry rel="sponsored", while user-generated content links use rel="ugc" to maintain appropriate disclosure.

## Noindex
A noindex directive, issued through a meta robots tag or X-Robots-Tag header, instructs search engines to exclude the page from the index. The page must remain crawlable for the directive to be detected; blocking it via robots.txt prevents the instruction from being read.

## Orphan page
An orphan page receives no internal links from any other page on the site. Crawlers therefore discover it with difficulty and assign it lower importance, while users cannot navigate to it through normal site structure. Every significant page should receive at least one contextual internal link to prevent orphan status.

## Redirect (301/302)
A redirect instructs browsers and crawlers to move from one URL to another. A 301 signals a permanent move and transfers ranking signals to the target URL, whereas a 302 indicates a temporary relocation that leaves the original URL eligible for indexing. Permanent content moves and retirement of duplicate URLs are best handled with 301 redirects.

## Rich result
A rich result augments a standard listing with additional elements such as stars, images, or breadcrumbs, enabled by structured data markup. Eligibility depends on Google's assessment and is never assured. Certain formats like HowTo and FAQ have been restricted to authoritative government and health domains, while Article, Breadcrumb, Product, Review, and Video types continue to appear broadly.

## Robots.txt
The robots.txt file at the site root specifies paths that crawlers may or may not fetch. It governs crawling behavior only and does not prevent indexing; a disallowed URL can still surface in results if other pages link to it. Noindex directives, not robots.txt rules, are the correct mechanism for excluding pages from results. Consult the [technical SEO resource](/technical-seo/) for implementation steps.

## Search intent
Search intent captures the underlying goal of a query, typically classified as informational, navigational, commercial, or transactional. Pages that align with the intent demonstrated by current top-ranking results maintain visibility more effectively than those focused solely on keyword placement. Mismatched intent leads to rapid ranking loss. [The keyword research guide explains intent identification in practice](/keyword-research/).

## SERP
The SERP comprises the full set of results Google returns for a given query, blending organic listings with advertisements and specialized features such as featured snippets, People Also Ask boxes, image packs, and local results. Examination of the SERP reveals the intent Google associates with the query and the content formats it prioritizes.

## Sitemap (XML)
An XML sitemap lists a site's key URLs along with optional last-modified dates to assist discovery and prioritization during crawling. It supplements, rather than replaces, strong internal linking and proves most useful on large, recently launched, or sparsely linked sites. Submission through Search Console combined with a reference in robots.txt improves processing.

## Structured data
Structured data applies machine-readable markup, most commonly schema.org vocabulary in JSON-LD format, to describe page content to search engines. It does not directly improve rankings but can qualify a page for rich results when implemented correctly. Adherence to Google's guidelines and validation through the Rich Results Test ensures proper interpretation. [See implementation details in the technical SEO guide](/technical-seo/).

## Title tag
The title tag supplies the page title that Google typically uses to generate the clickable headline in search results and that browsers display in tabs. Effective titles remain unique, front-load the primary topic, and align with the page's single H1. Google may rewrite titles containing boilerplate phrasing or excessive keyword repetition. [Application details appear in the on-page SEO guide](/on-page-seo/).

## Topic cluster
A topic cluster organizes content around one broad pillar page that links to and receives links from multiple focused subtopic pages. The structure signals topical depth to crawlers and clarifies relationships among pages. Consistent use of descriptive anchor text across the cluster reinforces the connections.

## URL slug
The URL slug forms the readable final segment of an address that identifies a specific page. Short, lowercase, hyphen-separated slugs improve usability and provide a modest relevance cue; lengthy parameter strings or date-based paths convey little meaning and should be minimized.

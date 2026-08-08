---
slug: how-search-works
order: 2
title: How Search Works
h1: How Search Works — Crawling, Indexing, Ranking
description: SEO makes sense once you understand Google's pipeline. Learn how crawling, indexing, ranking, and serving decide whether your page ever appears.
updated: 2026-08-08
related: technical-seo, keyword-research, measuring, international-seo
---

Every SEO decision is easier when you know the four stages a page passes through before it can rank.

## Crawling

Google Search is fully automated. The vast majority of pages that appear in results are discovered without any manual submission from site owners. The process of locating URLs is called URL discovery. Google already knows many URLs and revisits them on a schedule. It finds new URLs when it extracts links from pages it has already crawled, such as a category page that points to a newly published post. Additional URLs arrive through sitemaps you submit.

The crawler itself is Googlebot. An algorithmic system decides which sites to crawl, how frequently, and how many pages to request. Googlebot exists in two forms: Googlebot Smartphone and Googlebot Desktop. Because most sites are indexed under mobile-first indexing, the majority of crawl requests come from the mobile crawler.

Googlebot limits its activity to avoid overloading your server. It watches server responses and slows down when it sees repeated HTTP 500 errors or other signs of strain. On most sites the average interval between requests stays longer than a few seconds. Pages blocked by robots.txt or protected by login are skipped entirely.

During each crawl Google renders the page and executes its JavaScript using a recent version of Chrome. Rendering is required because many sites load critical content and links through scripts; without it Google may miss that material. Googlebot also stops after the first 2 MB of an HTML file or the first 64 MB of a PDF. Content and links placed beyond those cutoffs are ignored, so place important elements near the top of the document.

## Indexing

After the crawl finishes, Google processes the text, the title element, alt attributes, images, and videos to understand what the page contains. It compares the page against others and decides whether it is a duplicate. Similar pages are grouped, and the most representative version is chosen as the canonical. That canonical page becomes eligible to appear in results; the remaining versions are treated as alternates that may surface only in specific contexts such as mobile users.

Google also records signals about the canonical page, including its language, the country or locale it targets, and its usability characteristics. Sites make those language and locale signals explicit through [hreflang annotations](/international-seo/). Indexing is never guaranteed. Common reasons a crawled page stays out of the index are low content quality, a robots meta rule that blocks indexing, or site architecture that hides content behind complex JavaScript execution.

## Ranking

When a user enters a query, Google selects and orders results from the index according to relevance and quality signals. Hundreds of factors contribute to relevance, among them the searcher’s location, language, and device type. There is no single ranking control. Improvement comes from raising the overall match between the page and the query, strengthening content quality, and improving usability signals such as [Core Web Vitals](/technical-seo/).

## Serving

Google assembles the final results page after ranking is complete. The same query produces different results depending on the user’s location, language, and device. A search for local businesses therefore shows different listings in different cities. The search features that appear also vary with query intent; a request for repair shops tends to trigger local packs, while a product query is more likely to display images.

A page can be indexed yet fail to appear for a given query because its content does not match that query, its quality signals are weak, or a robots meta rule prevents serving. Because results are personalized, any rank-tracking data you collect is directional rather than absolute.

## Why this matters

Most SEO problems trace to a specific stage. When a page does not rank, the usual cause is that it is not indexed, which in turn usually means it was never crawled or that the content itself is insufficient. Check crawlability first, then indexing status, then quality and relevance.

Crawling and indexing must be kept distinct. A robots.txt disallow stops crawling but leaves the URL eligible to appear in results if it is discovered through links. To prevent a page from entering the index entirely, use [noindex or indexing-control](/technical-seo/), and keep the page crawlable so the directive can be read.

Next: turn intent into targets with **[keyword research](/keyword-research/)**.

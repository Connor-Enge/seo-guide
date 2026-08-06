---
slug: technical-seo
order: 6
title: Technical SEO
h1: Technical SEO — Crawlability, Speed & Structured Data
description: Technical SEO removes obstacles between your content and search engines: indexability, sitemaps, mobile, HTTPS, Core Web Vitals, and structured data.
updated: 2026-08-05
---
Technical SEO makes sure nothing stops a great page from being crawled, indexed, and enjoyed.

## Crawlability & indexability
- Submit an **XML sitemap** and reference it in `robots.txt` (this very site does both).
- Use `robots.txt` to guide crawlers, and `noindex` to keep thin pages out of the index — but never accidentally block pages you want ranked.
- Set a **canonical** URL on every page to consolidate duplicates.
- Return correct status codes: `200` for live pages, `301` for permanent moves, `404`/`410` for gone.

## Mobile & HTTPS
Google indexes the **mobile** version of your site first, so it must be fully usable on a phone. Serve everything over **HTTPS** — security is a baseline expectation.

## Core Web Vitals
Google measures real-world user experience with Core Web Vitals. Aim for:

- **LCP (Largest Contentful Paint) under 2.5 s** — how fast the main content loads.
- **INP (Interaction to Next Paint) under 200 ms** — how responsive the page feels.
- **CLS (Cumulative Layout Shift) under 0.1** — how visually stable it is.

Fast, stable pages win ties and keep users from bouncing. A lean, no-JavaScript static site (like this one) passes these almost by default.

## Structured data
Add **JSON-LD** structured data (schema.org) so Google can understand entities and show rich results — `Article`, `BreadcrumbList`, `FAQPage`, `Product`, and more. Every page here ships Article + BreadcrumbList markup, and pages with a FAQ (like this one) add FAQPage. Validate it with Google's Rich Results Test.

## FAQ

### What's the difference between robots.txt and noindex?
`robots.txt` controls crawling — whether Google fetches a URL at all. `noindex` controls indexing — whether a fetched page can appear in results. The catch: if you block a page in `robots.txt`, Google can't crawl it to see the `noindex`, so use `noindex` (not a crawl block) when you want a page kept out of search.

### What are good Core Web Vitals scores?
Google's "good" thresholds, measured at the 75th percentile of real visits, are Largest Contentful Paint under 2.5 seconds, Interaction to Next Paint under 200 milliseconds, and Cumulative Layout Shift under 0.1. INP replaced FID as the responsiveness metric in March 2024.

### Does HTTPS affect SEO?
Yes, though modestly. HTTPS is a confirmed lightweight ranking signal and, more importantly, a baseline expectation — modern browsers flag non-HTTPS pages as "not secure," and some features simply won't run without it. Serve every page over HTTPS.

### How do I get Google to crawl and index my site faster?
Submit an XML sitemap in Search Console and use the URL Inspection tool to request indexing of a specific page. Beyond that, strong internal links from already-indexed pages, a fast server, and a clean crawlable structure all help Google find and prioritize your new URLs.

Next: earn credibility with **[link building](/link-building/)**.

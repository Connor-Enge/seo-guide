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
Add **JSON-LD** structured data (schema.org) so Google can understand entities and show rich results — `Article`, `BreadcrumbList`, `FAQPage`, `Product`, and more. Every page here ships Article + BreadcrumbList markup. Validate it with Google's Rich Results Test.

Next: earn credibility with **[link building](/link-building/)**.

---
slug: xml-sitemaps-in-2026
title: XML Sitemaps in 2026: What to Include
h1: XML Sitemaps in 2026: What to Include, and the lastmod Google Trusts
description: Sitemaps are a crawl hint, not a ranking factor: what to include (canonical URLs only), the lastmod Google trusts, size limits, and how to submit.
date: 2026-08-08
updated: 2026-08-08
tags: technical-seo, sitemaps, crawling, indexing, lastmod
related: technical-seo, how-search-works, glossary
---
A sitemap is a file listing pages and files on a site along with their relationships. Search engines read the file to [crawl the site](/how-search-works/) more efficiently. The file indicates which pages the owner considers important and can carry additional details such as last modification dates or alternate-language versions. Submitting a sitemap supplies only a hint that aids discovery; it does not guarantee Google will download the file or crawl the listed URLs, and it has no effect on rankings.

## What a sitemap is (and what it isn't)
A sitemap tells search engines which pages matter to the site owner and supplies optional metadata for those pages. Google reads the file as one signal among many when deciding what to crawl. The file does not force inclusion in search results or improve any page's position. It supports [efficient crawling](/technical-seo/) on sites where internal links alone may leave some pages undiscovered.

## Do you actually need one?
Sites with roughly 500 pages or fewer often do not require a sitemap when internal links already connect every important page back to the home page. Googlebot can reach those pages without additional assistance. Larger sites, new sites with limited external links, or sites heavy in video, images, or news content benefit from a sitemap because those characteristics make comprehensive discovery through links alone less reliable.

## What belongs in a sitemap
Include only URLs that should appear in Google's results. List the [canonical version](/glossary/) of each page and exclude duplicates, redirects, non-200 responses, and [noindexed pages](/blog/robots-txt-vs-noindex/). Adding URLs that should not rank wastes the limited signal the file provides. Every URL must be written as a fully qualified absolute address beginning with the protocol and domain. Relative paths are not accepted. The file itself must be UTF-8 encoded, and every tag value must use standard XML entity escaping. A sitemap placed in a subdirectory influences only URLs at or below that directory level. Placing the file at the site root extends its coverage to the entire site unless the file is submitted through Search Console.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://www.example.com/foo.html</loc>
    <lastmod>2026-08-01</lastmod>
  </url>
</urlset>
```

## The lastmod value Google actually trusts
Google examines the lastmod value only when the dates are consistent and match actual content changes on the page. Dates that reset to the current day for every URL are treated as unreliable and are ignored. Update lastmod solely when meaningful content changes occur. The priority and changefreq tags receive no weight at all and can be omitted without consequence.

## Splitting large sitemaps with an index file
A single sitemap file cannot exceed 50 MB uncompressed or contain more than 50,000 URLs. When either limit is reached, divide the URLs across multiple sitemaps and reference those files from a sitemap index. The index file follows the same XML namespace rules as an ordinary sitemap. Every sitemap listed in the index must reside on the same site and in the same directory as the index or deeper. One index file may reference up to 50,000 sitemaps, and up to 500 index files may be submitted per site through Search Console.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>https://www.example.com/sitemap-1.xml</loc>
    <lastmod>2026-08-01</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://www.example.com/sitemap-2.xml</loc>
    <lastmod>2026-07-15</lastmod>
  </sitemap>
</sitemapindex>
```

## How to submit it
Submit through the Sitemaps report in [Google Search Console](/blog/google-search-console-workflow/), through the Search Console API, or by adding one or more Sitemap lines to robots.txt. Each robots.txt line takes the form Sitemap: followed by the absolute URL of the file. Multiple lines are permitted. RSS or Atom feeds can also be announced through WebSub. Regardless of the submission method, the action remains only a hint; Google may still choose not to fetch or use the file.

## Mistakes that get a sitemap ignored
- Using relative instead of absolute URLs.
- Listing noindex, blocked, redirecting, duplicate, or non-200 URLs.
- Setting lastmod to the current date on every entry.
- Relying on priority or changefreq tags.
- Exceeding the 50 MB or 50,000 URL limit without splitting into an index.
- Expecting the sitemap to act as a ranking factor.

Keep the sitemap limited to canonical URLs that are current and accurate.

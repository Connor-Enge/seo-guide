---
slug: international-seo
order: 11
title: International SEO
h1: International SEO — hreflang, ccTLDs & Multi-Regional Sites
description: International SEO explained — multilingual vs. multi-regional sites, choosing ccTLDs vs. subfolders, and implementing hreflang annotations correctly.
updated: 2026-08-08
related: technical-seo, how-search-works, on-page-seo
---
International SEO requires explicit signals so search engines can match pages to a searcher's language and country. Without those signals, crawlers may miss alternate versions or serve the wrong locale.

## Multilingual vs. multi-regional sites

A multilingual site offers content in more than one language, such as a Canadian business maintaining English and French versions. Search engines attempt to return pages that match the searcher's preferred language. A multi-regional site targets users in specific countries, such as a manufacturer that ships to both Canada and the United States. Search engines attempt to surface the appropriate country-specific page. Some sites combine both approaches by maintaining separate country versions that each contain multiple language variants.

## Choosing a URL structure

Country-code top-level domains such as example.de provide the clearest geotargeting signal and allow complete site separation, yet they can be costly, limited in availability, or restricted by local registration rules. Subdomains on a generic top-level domain, such as de.example.com, are simple to configure and permit separate server locations, but users may not immediately recognize whether the prefix denotes language or country. Subdirectories on a generic top-level domain, such as example.com/de/, require minimal maintenance on a single host, though the target country is not obvious from the URL and all versions share the same server location. URL parameters such as site.com?loc=de are not recommended because they complicate segmentation and remain unclear to users. Localized words in URLs and internationalized domain names are acceptable when encoded in UTF-8.

## How Google determines a page's target locale

Google treats most country-code top-level domains as a strong signal for country targeting, although certain vanity ccTLDs such as .tv and .me are handled as generic. Additional signals include hreflang annotations, server IP address, local addresses and phone numbers on the page, local language and currency usage, links from other local sites, and Google Business Profile data where available. Server location serves only as a weak signal because CDNs and foreign hosting can obscure it. Google does not vary crawler source locations to discover variants and ignores location meta tags or geotargeting HTML attributes.

## Implementing hreflang annotations

Declare language and region variants through HTML link tags in the head, an HTTP Link response header for non-HTML files, or XML sitemap entries with xhtml:link. Choose one method; multiple implementations increase maintenance without improving results. Each annotation must reference itself and every other version, and the references must be reciprocal. Use fully qualified URLs that include the scheme. Provide a generic language code such as en as a catch-all for unlisted locales, and use x-default for a selector or fallback page.

```html
<link rel="alternate" hreflang="en-gb" href="https://en-gb.example.com/page.html" />
<link rel="alternate" hreflang="en-us" href="https://en-us.example.com/page.html" />
<link rel="alternate" hreflang="en" href="https://en.example.com/page.html" />
<link rel="alternate" hreflang="de" href="https://de.example.com/page.html" />
<link rel="alternate" hreflang="x-default" href="https://www.example.com/" />
```

An hreflang value consists of an ISO 639-1 language code optionally followed by an ISO 3166-1 Alpha-2 region code; a region code alone is invalid.

## Handling translated and duplicate content

Genuinely translated content is not treated as duplicate. When similar content in the same language appears across regions, select a preferred version with rel="canonical". When hreflang is in use, each page's canonical must point to itself; canonicalizing every localized version to one URL causes search engines to drop the remaining variants and nullifies the hreflang cluster.

## Common hreflang mistakes

- Omitting reciprocal links so annotations are ignored.
- Using invalid codes such as en-uk instead of en-gb or placing a country code without a language.
- Employing relative instead of fully qualified URLs.
- Forgetting the self-referential entry.
- Pointing every locale's canonical to a single URL.
- Automatically redirecting users by IP or browser language, which prevents crawlers and users from reaching other versions.
- Expecting hreflang to improve rankings rather than control which version appears.

## Frequently asked questions

**How does Google identify the language of a page?**
Google determines language solely from visible content and does not rely on the HTML lang attribute or the URL.

**Should I automatically redirect users to a language version?**
No. Automatic redirects based on guessed language can prevent both users and crawlers from discovering other versions; instead, provide visible links or a language selector.

**Does hreflang affect rankings?**
Hreflang controls which localized version is shown to a searcher; it does not influence ranking position.

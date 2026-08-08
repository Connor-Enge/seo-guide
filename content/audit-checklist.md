---
slug: audit-checklist
order: 12
title: SEO Audit Checklist
h1: The Technical SEO Audit Checklist
description: A practical, prioritized technical SEO audit checklist — crawlability, indexing, Core Web Vitals, on-page, structured data, and monitoring, with fixes.
updated: 2026-08-07
related: technical-seo, measuring, common-seo-mistakes
---
A technical SEO audit reviews how well a site supports crawling, rendering, indexing, and performance so search engines can process its content correctly. This checklist walks through the checks in priority order, with concrete steps for verification and remediation on an existing site. Fix crawl and indexing problems first, then address performance, architecture, and content signals before refining smaller details.

## Before you start

**Define the audit scope by listing the main sections or templates of the site.** This keeps the review focused on representative pages rather than attempting to examine every URL at once. Note any known issues such as recent migrations or template changes that may have introduced problems.

**Capture a baseline in Google Search Console before making changes.** Review the Performance report for current impressions and clicks, the Page indexing report for coverage status, and the Core Web Vitals report for field data segmented by mobile and desktop. Export or screenshot these views so later comparisons show actual movement.

**Gather the necessary free tools and access.** Confirm ownership of the site in Search Console, open PageSpeed Insights and Lighthouse in Chrome DevTools, and prepare the Rich Results Test for markup validation. Access to the server logs or a staging environment helps when testing robots.txt or redirect behavior.

## Crawlability and indexing

**Examine the robots.txt file for unintended blocks on CSS or JavaScript resources.** Google must fetch these files to render pages the way users see them; blocking them can cause indexing problems even if the HTML itself is allowed. Use the URL Inspection tool to request a live test and compare the rendered HTML against the live version.

**Verify that any XML sitemap submitted in Search Console contains only canonical, indexable URLs.** Google primarily discovers pages through links rather than sitemaps, yet an accurate sitemap still helps confirm what the site intends to offer. Remove parameter-heavy or duplicate URLs from the sitemap and resubmit it after corrections.

**Check for noindex tags on pages that should remain out of search results.** A noindex meta tag or X-Robots-Tag header prevents indexing, while a robots.txt disallow only stops crawling; the two serve different purposes and should not be used interchangeably. The site: operator can surface pages that remain indexed despite a disallow rule.

**Confirm that important content sits within the first 15 MB of each HTML file.** Googlebot truncates larger files, so move critical text, structured data, and navigation links toward the top of the document and reduce unnecessary markup.

**Review the Page indexing report for errors such as redirect loops, server errors, or pages blocked by robots.txt.** Address the highest-volume issues first, then use the URL Inspection tool on individual affected pages to confirm the current crawl status and rendered output.

## Site architecture and internal linking

**Map the site into a clear hierarchy with the homepage at the top and topic clusters beneath it.** This structure helps both users and crawlers understand relationships between pages. Aim for most important content to sit no more than three clicks from the homepage.

**Use descriptive anchor text in internal links instead of generic phrases.** Words that reflect the target page’s content improve context for search engines and visitors alike. Audit a sample of category and product pages to ensure links follow this pattern.

**Identify orphan pages that receive no internal links.** These pages often appear in the sitemap or server logs yet remain invisible to crawlers because nothing points to them. Add relevant links from related content or navigation to bring them into the site’s link graph.

**Implement breadcrumb markup and visible breadcrumb links on deeper pages.** Breadcrumbs reinforce hierarchy and provide an additional navigation path that search engines can follow.

## URLs and redirects

**Adopt descriptive, readable URLs that use words rather than opaque identifiers.** Such URLs help both users and search engines interpret page topics without extra effort. Update templates so new pages follow this convention and consider gradual redirects for existing opaque URLs.

**Enforce consistent handling of trailing slashes and letter case across the site.** Mixed usage creates duplicate URLs that split ranking signals. Choose one pattern and implement 301 redirects or canonical tags to enforce it.

**Ensure every page ultimately serves on HTTPS with a valid certificate.** Mixed content warnings or HTTP versions that remain accessible can undermine trust and cause indexing confusion. Set the canonical URL and internal links to the HTTPS version.

**Eliminate long redirect chains and replace 4xx or 5xx responses with appropriate content or redirects.** Chains slow crawling and dilute signals; broken links waste crawl budget and frustrate users. Scan a representative sample with a crawler and fix the highest-impact errors first.

## On-page fundamentals

**Place one clear H1 on each page that matches the main topic.** Logical heading hierarchy below the H1 helps both accessibility tools and search engines parse the content structure. Avoid skipping levels or using multiple H1s for styling purposes.

**Write unique, descriptive title tags and meta descriptions for every important page.** Google may rewrite titles when it finds the existing tag unhelpful, but well-crafted tags still improve click-through rates from the results page. Keep titles concise and front-load the primary topic.

**Add meaningful alt text to informative images while leaving decorative images empty.** Alt text provides context when images cannot load and helps image search visibility. Review templates to ensure alt attributes are populated from meaningful data rather than filenames.

## Core Web Vitals and performance

**Measure field data through the Search Console Core Web Vitals report and the Chrome UX Report rather than relying solely on lab tools.** The 75th-percentile thresholds are LCP at or below 2.5 seconds, INP at or below 200 milliseconds, and CLS at or below 0.1. INP replaced FID in 2024, so update any older monitoring that still references the retired metric.

**Optimize the largest contentful element by compressing images, preloading critical resources, and removing render-blocking scripts.** PageSpeed Insights highlights the specific element and suggests fixes for each page.

**Prevent layout shifts by reserving space for images and ads with explicit dimensions or aspect-ratio CSS.** Cumulative layout shift often stems from late-loading media that pushes content after initial render.

**Enable compression such as Brotli or gzip and honor ETag or If-None-Match headers for efficient revalidation.** These practices reduce payload size and improve crawl efficiency over repeated visits.

## Mobile and rendering

**Verify that the site uses responsive design so the same HTML serves all devices.** Content parity between mobile and desktop versions prevents discrepancies that could affect indexing. Test a sample of pages in the URL Inspection tool to confirm the rendered mobile output matches expectations.

**Ensure tap targets are large enough and spaced to avoid accidental clicks on mobile.** Lighthouse flags undersized interactive elements that harm usability metrics.

**Confirm that Googlebot sees the same content on mobile as users do by checking the rendered view in Search Console.** Differences introduced by client-side rendering or device-specific blocks can lead to incomplete indexing.

## HTTPS and security

**Maintain a valid TLS certificate and redirect all HTTP traffic to HTTPS.** Search Console flags sites with certificate errors that can interrupt crawling.

**Remove mixed content by serving all resources over HTTPS.** Mixed active content can break page functionality and trigger browser warnings.

**Set canonical tags and internal links to the HTTPS version consistently.** This prevents duplicate indexing of HTTP and HTTPS variants.

## Structured data

**Use JSON-LD to mark up only content that is visible on the page.** Marking hidden or irrelevant content violates guidelines and risks loss of rich-result eligibility. Validate every implementation in the Rich Results Test before deployment.

**Monitor the Enhancements reports in Search Console for errors or warnings on supported rich results.** Fix markup issues promptly so eligibility is not lost over time.

**Remember that eligibility for a rich result does not guarantee it will appear.** Google chooses results based on relevance and quality signals beyond the presence of valid structured data.

## Content quality and duplication

**Focus on helpful, people-first content that demonstrates experience, expertise, authoritativeness, and trustworthiness.** Scaled or thin pages created mainly to capture rankings are demoted under current systems. Review any sections that appear generated primarily for search traffic rather than user value.

**Consolidate duplicate or near-duplicate pages with canonical tags and consistent internal linking.** The canonical tag is a hint, so also update sitemaps and navigation to point to the preferred version.

**Avoid thin content that adds little value beyond keyword repetition.** Audit low-word-count pages and either expand them with substantive material or consolidate them into stronger pages.

## Monitoring and re-auditing

**Watch the Performance, Page indexing, Core Web Vitals, and Enhancements reports in Search Console on a regular cadence.** Set calendar reminders to review changes after any significant update.

**Allow several weeks before judging the impact of fixes.** Some signals propagate quickly while others require additional crawls and ranking recalculations.

**Re-run the full audit after major site changes such as platform migrations or template overhauls.** Periodic checks catch regressions before they affect traffic.

Prioritize indexing and crawl blockers first, followed by Core Web Vitals and on-page elements, then structured data and content refinements. Re-run the audit at least quarterly or after any large change to keep the site in good technical health.

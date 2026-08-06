---
slug: passing-core-web-vitals-2026
title: How to Pass Core Web Vitals in 2026
h1: How to Pass Core Web Vitals in 2026 — A Field Guide
description: A practical, metric-by-metric walkthrough of Core Web Vitals — what LCP, INP, and CLS measure, the thresholds Google uses, and the specific fixes that actually move each one.
date: 2026-08-05
updated: 2026-08-05
tags: technical-seo, performance, core-web-vitals
---
Core Web Vitals are Google's attempt to put a number on something users feel instantly: does this page load fast, respond quickly, and stay still while I read it? They are part of Google's **page experience** signals — a genuine ranking input, but a supporting one. Google has been consistent that a great experience won't rank a page that fails to answer the query, and a slightly slower page can still win if it's the most helpful result. Treat Core Web Vitals as a tiebreaker you should win, not a growth strategy on their own. For where they sit in the wider picture, see [technical SEO](/technical-seo/) and [content quality](/content-quality/).

This is a field guide: what each metric measures, the threshold you have to clear, and the fixes that actually move the number.

## The three metrics, and the numbers that matter
Google tracks three Core Web Vitals, each covering a different part of the experience:

- **Largest Contentful Paint (LCP)** — loading. The time from when the page starts loading until the largest text block or image in the viewport is rendered. **Good: 2.5 seconds or less.**
- **Interaction to Next Paint (INP)** — responsiveness. The latency of the slowest interaction (click, tap, or keypress) across the whole visit. **Good: 200 milliseconds or less.**
- **Cumulative Layout Shift (CLS)** — visual stability. A unitless score for how much visible content shifts unexpectedly. **Good: 0.1 or less.**

Two details decide whether you actually pass. First, Google judges each metric at the **75th percentile** of real page loads, segmented across mobile and desktop — so the slowest quarter of your visitors is what counts, not your fast test machine. Second, a page passes only when **all three** metrics clear their "good" threshold at that percentile.

INP is the newest of the three. It replaced First Input Delay (FID) as the responsiveness metric in **March 2024**, because FID only measured the delay before the first interaction was handled, while INP measures the full latency of interactions throughout the visit — a far better proxy for how responsive a page actually feels.

## Field data is the score; lab data is the map
The single most common Core Web Vitals mistake is optimizing the wrong number. There are two kinds of data, and they answer different questions:

- **Field data** — real measurements from real Chrome users, collected in the Chrome User Experience Report (CrUX) and by Real User Monitoring (RUM) tools. **This is what feeds the page-experience signal.**
- **Lab data** — a synthetic test run in a controlled environment, such as Lighthouse or the "Diagnose performance issues" section of PageSpeed Insights. It's repeatable and great for debugging, but it's a single simulated load, not your users.

Start with the field. Open PageSpeed Insights or the Core Web Vitals report in Search Console, confirm which metric is failing and on which device, and only then drop into the lab to find out why. Chasing a perfect Lighthouse score while your CrUX data is red is wasted effort.

## Fixing LCP: get the main content painted fast
LCP breaks into four sub-parts — time to first byte (TTFB), resource load delay, resource load time, and element render delay — so fix them in order:

- **Cut TTFB.** A slow server response makes 2.5 seconds hard or impossible. Use good hosting, serve from a CDN close to users, cache the HTML, and avoid redirect chains. A static site served from a CDN — like this one — starts with a near-instant TTFB by default.
- **Find your LCP element, then prioritize it.** It's usually the hero image or the headline. Preload the LCP image and set `fetchpriority="high"`, and never lazy-load it — lazy-loading the thing above the fold is a classic own-goal.
- **Send fewer, smaller bytes.** Serve modern formats (AVIF or WebP), size images to their displayed dimensions, and compress them.
- **Remove render-blocking resources.** Inline the critical CSS, defer non-critical CSS and JavaScript, and preconnect to critical third-party origins.

## Fixing INP: keep the main thread free
An interaction's latency has three parts: **input delay** (time before your event handler starts, usually because the main thread is busy), **processing duration** (your handler running), and **presentation delay** (the browser painting the result). JavaScript is the usual culprit for all three.

- **Break up long tasks.** Any task over 50 ms blocks input. Split heavy work and yield back to the main thread — with `scheduler.yield()` where available, or `setTimeout` — so the browser can respond between chunks.
- **Ship less JavaScript.** The fastest task is the one that never runs. Remove unused scripts, code-split, and defer anything not needed for the first interaction.
- **Give immediate feedback.** For unavoidable heavy work, paint a visible response first — a spinner, a disabled button — and do the expensive work after the next frame.
- **Keep handlers and the DOM lean.** Debounce high-frequency events, avoid forcing synchronous layout, and keep the DOM small so re-renders stay cheap.

Text-and-image pages with little JavaScript tend to pass INP effortlessly — the metric mostly punishes heavy client-side apps.

## Fixing CLS: reserve space before content arrives
Layout shift is almost always caused by something arriving late and shoving everything else down. Per web.dev, the four usual causes are images without dimensions, ads/embeds/iframes without dimensions, dynamically injected content, and web fonts. The fixes:

- **Always set dimensions.** Give every image and video a `width` and `height` (or a CSS `aspect-ratio`) so the browser reserves the space before the file loads.
- **Reserve space for dynamic content.** Ads, embeds, and iframes should sit in a container with a fixed, pre-declared size. Never insert content above existing content unless the user asked for it.
- **Tame web fonts.** Preload key fonts and use `font-display: optional`, or a well-matched fallback tuned with `size-adjust`, so a late-swapping font doesn't reflow the page.
- **Animate with `transform`.** Animate `transform` and `opacity`, which don't trigger layout, instead of properties like `top`, `height`, or `margin`, which do.

Remember that CrUX measures CLS across the **entire life of the page**, not just the initial load — so a shift that happens when someone scrolls into lazy-loaded content still counts against you.

## A pragmatic order of operations
1. Pull field data (Search Console or PageSpeed Insights) and note which metric fails, on which device, and by how much.
2. Reproduce the failing metric in the lab and identify the specific element or script responsible.
3. Apply the targeted fixes above — one change at a time, so you know what worked.
4. Re-measure in the lab to confirm the fix, then **wait for field data to catch up.** CrUX is a 28-day rolling window, so real-world improvement shows up gradually, not overnight.
5. Re-check after any redesign or new third-party script — most regressions arrive with new code.

## Keep it in perspective
Passing Core Web Vitals is worth doing: it lowers bounce rates, helps conversions, and wins you close ranking calls. But it's a floor, not a ceiling. The pages that rank and stay ranked are the ones that best answer the query — see [content quality and E-E-A-T](/content-quality/) — served on a fast, stable, crawlable site. Get the content right, then make the experience effortless.

## FAQ

### Are Core Web Vitals a Google ranking factor?
Yes, as part of Google's page-experience signals — but a modest, supporting one. Google has repeatedly said relevance and helpfulness matter far more, and that page experience mainly helps decide between pages of comparable quality. Pass them because they win close calls and improve UX, not because they'll outrank better content.

### What are the passing thresholds for Core Web Vitals?
At the 75th percentile of real visits, a page needs Largest Contentful Paint of 2.5 seconds or less, Interaction to Next Paint of 200 milliseconds or less, and Cumulative Layout Shift of 0.1 or less. All three must pass for the page to be rated good.

### Why is my Lighthouse score green but Search Console says the page is failing?
Because they measure different things. Lighthouse is a single lab test on one simulated load; Search Console and the top section of PageSpeed Insights report field data from real users (CrUX), which is what the page-experience signal uses. When they disagree, trust the field data and treat Lighthouse as a debugging tool.

### How long does a Core Web Vitals fix take to show up?
The field data Google uses is a 28-day rolling average, so improvements appear gradually over several weeks after your fix reaches production — not immediately. Confirm the fix in the lab right away, then watch the field report trend over the following month.

## Sources
- [Web Vitals](https://web.dev/articles/vitals), and the [LCP](https://web.dev/articles/optimize-lcp), [INP](https://web.dev/articles/optimize-inp), and [CLS](https://web.dev/articles/optimize-cls) optimization guides — web.dev, Google.
- [Understanding page experience in Google Search results](https://developers.google.com/search/docs/appearance/page-experience) — Google Search Central.
</content>
</invoke>

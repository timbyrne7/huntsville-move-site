# Competitor analysis — movingtohuntsville.org vs this site

Checked 2026-10-19. Sources: live fetch of the site's `robots.txt`, `sitemap_index.xml` and
`post-sitemap.xml`; full-page extraction of all 33 posts; RDAP registry record for the domain;
HypeStat / Similarweb / StatShow / Wayback CDX for traffic. Raw data:
`competitor_sitemap.json`, `competitor_pages.json`, `competitor_content.json`.

## 1. Traffic per month — honest answer: not measurable, and here is the evidence

| Source | Result |
|---|---|
| HypeStat (aggregates SimilarWeb + SEMrush figures) | **"This site is not found in the HypeStat database yet"** — below their coverage threshold |
| SimilarWeb public report | Blocked (HTTP 403 from CloudFront) to both a plain fetch and a **real browser** — no figure obtainable |
| StatShow | Reports its floor placeholder: 1 visitor/day, 30/month, $10 site worth. That is a default template value, **not a measurement** — do not quote it |
| Wayback Machine CDX | **No captures at all** — no third-party crawl history for this domain |
| RDAP registry record | Registered **2026-01-28** (Namecheap), last changed 2026-08-12 → the domain is ~9 months old |
| On-site signals | WordPress, no display-ad network found; monetised by a mover-quote form ("Compare up to 3 licensed movers", leads sold to movers) |

**Conclusion: no reliable figure exists for free, and any number quoted from these tools would be
invented.** What can be said honestly: the domain is nine months old, absent from every free
traffic database consulted, and uncaptured by the Wayback Machine — i.e. a young site with
low measurable traffic, not an established publisher. StatShow's "30/month" and similar
estimator outputs are template floors; treat them as noise.

If you want a real number, the routes are: a SimilarWeb or Ahrefs paid plan, their own Google
Analytics (not accessible), or a proxy estimate from SERP visibility. None of those is available
from this box, so the figure is left as "unverified" rather than guessed.

## 2. What they actually are

A **mover-lead-generation site**, not a relocation publisher. 33 posts, ~43,700 words total,
averaging ~1,300 words (range 491–2,335). Monetisation is the mover-quote form and the
`/contact/` page; every article interleaves "compare moving quotes" CTAs. Their most-built
content block by far is movers (6 posts, ~9,600 words).

Content quality: competent but thin and repetitive — keyword-stuffed sentences ("understanding
utilities cost huntsville al before you relocate is worth your time"), hedged tables instead of
real figures in some places, but they *do* cite real sources where it suits them (Huntsville
Utilities' residential rate schedule effective 2026-02-01; the Huntsville/Madison County
Chamber's leading-employers list with Redstone ≈45,500, NASA Marshall ≈7,000, FBI ≈2,200,
Huntsville Hospital ≈12,160).

Their 33 posts, by word count:

| Words | URL |
|---|---|
| 2335 | choose-moving-company-in-huntsville-al |
| 2292 | movers-cost-huntsville-al |
| 2189 | long-distance-movers-huntsville-al |
| 2161 | safest-neighborhoods-huntsville-al |
| 2142 | best-places-to-live-in-huntsville-al |
| 2067 | pros-and-cons-of-living-in-huntsville-al |
| 2056 | average-rent-in-huntsville-al |
| 1950 | moving-to-huntsville-alabama |
| 1928 | rent-in-huntsville-al |
| 1902 | best-areas-to-live-in-huntsville-for-families |
| 1875 | moving-to-huntsville-checklist |
| 1861 | apartments-huntsville-al |
| 1765 | salary-needed-to-live-in-huntsville |
| 1703 | best-suburbs-huntsville-al |
| 1702 | best-schools-huntsville-al |
| 1646 | best-moving-companies-in-huntsville-al |
| 1625 | buying-a-home-in-huntsville-2026-market-overview-prices |
| 1621 | property-taxes-huntsville-al |
| 1545 | commute-in-huntsville-al |
| 747 | moving-quotes-huntsville |
| 672 | is-huntsville-growing-population-development-trends-2026 |
| 615 | is-huntsville-safe |
| 603 | huntsville-vs-nashville-cost-of-living-2026 |
| 568 | local-movers-in-huntsville-al |
| 538 | hidden-costs-of-moving-to-huntsville-al |
| 532 | how-to-move-to-alabama |
| 531 | weather-in-huntsville-al-2026 |
| 518 | cost-of-living-in-huntsville-alabama |
| 507 | healthcare-in-huntsville-al-hospitals-medical-access |
| 507 | utilities-cost-huntsville-al |
| 503 | living-in-huntsville-al |
| 491 | top-employers-in-huntsville-al-2026 |
| — | huntsville-neighborhoods-guide (did not extract; blocked/empty) |

## 3. Coverage matrix

| Topic | Them | Us | Verdict |
|---|---|---|---|
| Moving-to guide | 1,950 w | `moving-to-huntsville.html` | **We win** — same topic, plus tools |
| Pros/cons + living here | 2,570 w across 2 posts | `is-huntsville-a-good-place-to-live.html` (new today) | **Matched** |
| Neighborhoods / best places / best for families / suburbs | ~5,750 w across 4 posts | `neighborhoods.html` (36 communities, districts, live commute) | **We win on substance**, they win on framing ("best suburbs", "best for families") |
| Schools | 1,702 w | `schools.html` (8 systems, zone lookups) | **We win** |
| Commute | 1,545 w prose | `commute.html` (live routing, 36×12 matrix) | **We win decisively** |
| Cost of living | 518 w | `cost-of-living.html` (57-metro tool) | **We win** |
| Checklist | 1,875 w | `checklist.html` (address-specific, jurisdiction rules) | **We win** |
| Property taxes | 1,621 w dedicated page | FAQ card inside cost-of-living | **They win — gap** |
| Rent / apartments / average rent | ~5,850 w across 3 posts | nothing (only the rent-vs-buy model) | **They win — biggest gap** |
| Housing market & prices | 1,625 w | `home-search.html` (search + alerts, no market/price content) | **They win — gap** |
| Top employers / jobs | 491 w | employers inside the commute tool only | **They win — gap** |
| Safety / crime / safest neighborhoods | ~2,780 w across 2 posts | deliberately no rankings; qualitative answer only | **They win — gap (and an opportunity to do it honestly)** |
| Utilities cost | 507 w | setup covered; cost not | **Partially matched — gap** |
| Weather / climate | 531 w | a bullet on the verdict page | **They win — gap** |
| Healthcare / hospitals | 507 w | nothing | **They win — low priority for us** |
| Population growth | 672 w | a paragraph on the verdict page | Minor gap |
| Salary needed | 1,765 w | nothing (data already in `data/metros.json`) | **Gap — cheap to close** |
| City vs city comparison | 603 w (Huntsville vs Nashville) | none | **Gap — cheap to close with metros.json** |
| Movers / moving quotes | ~9,600 w across 6 posts | nothing | **Deliberately not our business** (lead-selling for referral fees is a different, compliance-sensitive model) |
| PCS / VA loans / Redstone housing | nothing | `redstone-arsenal-pcs-va-loans.html` (new today) | **We own it outright** |

## 4. Recommended builds, in priority order

Each row names a data path that exists today — no new subscriptions needed.

1. **Rent and apartments in Huntsville** (`rent-in-huntsville.html`). Closes the largest gap
   (~5,850 words of their content, and the harvest's rent cluster is 79 queries). Data: ACS
   median gross rent already in `data/metros.json`, the 36-community rent/property notes in
   `data/neighborhoods-content.json`, the ValleyMLS handoff, and the rent-vs-buy model as the
   CTA. Renters are future buyers — this is the highest-value page for a mortgage pipeline, not
   just for traffic.
2. **Property taxes in Huntsville and Madison County** (`property-taxes.html`). 53-query cluster
   ("huntsville al property tax rate", "madison county property tax", "tax assessor property
   search"). Their page deliberately avoids real rates; the win is explaining Alabama's
   assessment mechanics (assessment ratio, millage, homestead exemptions) with sourced figures
   and the county's own parcel lookup, then feeding the payment model. **Needs a source check
   against the county/state before publishing numbers.**
3. **Top employers and where the jobs are** (`huntsville-employers.html`). 177-query cluster.
   Source: the Huntsville/Madison County Chamber leading-employers list (the same one they cite),
   plus our existing employer coordinates → every employer row links into the commute calculator.
   A clean funnel: job → gate/campus → area → pre-qualification.
4. **Is Huntsville safe? Sourced crime data** (`huntsville-crime-safety.html`). They rank on
   ~2,780 words of this. We can hold the honest line *and* satisfy the query: publish the city's
   own crime data and the FBI/ALEA sources, explain which reported categories are volatile,
   and show how to check one block rather than one city. No invented rankings.
5. **Housing market and prices** (`huntsville-housing-market.html`). Backs the search page with
   the price data people search for: ACS median, price bands by area, what ValleyMLS shows live
   (days on market, price cuts). Their version is a 2026-market overview with thin data.
6. **Utilities cost** — extend `checklist.html` with a cost section sourcing Huntsville
   Utilities' published rate schedule (the page they cite), rather than a new thin page.
7. **Salary needed / city-vs-city comparisons** — cheap derivatives of `data/metros.json`:
   "salary needed to live in Huntsville" plus a small set of "Huntsville vs <city>" pages built
   from the 57 metros already loaded. Note the harvest shows low proxy scores for comparison
   queries, so build these only after 1–5.
8. **Weather / climate** — needs NOAA/NWS climate normals as a source; medium effort, moderate
   value (it supports the verdict page's summer-humidity argument).
9. **Best suburbs / best areas for families** — add as *sections* on `neighborhoods.html`, not
   new pages, to avoid thin near-duplicates of the 36-community content we already have.
10. **Healthcare** — low priority: it does not feed a mortgage pipeline and needs hospital
    sources we have not verified.

## 5. What we should not copy

- **Mover-lead content.** Their six mover posts exist to sell moving quotes. Selling or brokering
  those leads is a different business with its own compensation rules; the value to us would be
  a single neutral "what the move itself costs" page at most.
- **Keyword-stuffed sentences.** Their prose repeats the target phrase mid-sentence in ways a
  human notices ("understanding utilities cost huntsville al before you relocate is worth your
  time"). Volume without readability is the thing AI-detection-era readers punish.
- **Number-free hedging.** Their property-tax page explains the mechanism then gives "ranges"
  because it has no sourced rate. Our advantage is the opposite: real figures with the source
  named.

## 6. Immediate takeaway

Their advantage is **breadth** (33 posts vs our 16 pages) and the "best/safest/cheapest" listicle
framings; ours is **depth, tools and sourcing** — and we already own the two clusters they have
nothing for (PCS/VA, and live commute measurement). The five builds above close the breadth gap
where it matters commercially, using data already on this box. The single most valuable one is
the rent/apartments page: it is the biggest content gap, the rent cluster is large, and renters
are this site's future pre-qualifications.

## 7. Build status (end of 2026-10-19 session)

Site is now **20 pages**. The top four gaps are built, each from a primary source:

| # | Gap | Page | Source(s) actually used |
| --- | --- | --- | --- |
| 1 | Rent / apartments | `rent-in-huntsville.html` | ACS 2024 B25064 (city 1-yr $1,241 / 5-yr $1,171; metro $1,283; Madison Co $1,209; Limestone $970; Morgan $864; Athens $899; Decatur $896), B25003 tenure, B25071 rent burden 26.8% |
| 2 | Property taxes | `property-taxes.html` | Madison County Tax Collector rate list ($5.80 / $6.95 / $6.15 / $4.05 / $3.35 land · $3.65 improvements per $100 assessed); Assessor "property tax facts"; Ala. DOR + Code §40-8-1 for the 10% Class III ratio; worked examples computed, and reconciled against the ACS median bill of $1,405 with the gap explained |
| 3 | Top employers | `huntsville-employers.html` | Chamber *2026 Leading Employers* PDF: all 51 entries, sector sums (Gov 58,360 · R&D 24,276 · Mfg 17,951 · Health 14,009 · Education 10,169 · Other 4,952), with the "do not sum Redstone with contractors" caveat |
| 4 | Safety | `huntsville-crime-safety.html` | HPD *Annual Report 2025* NIBRS counts (13,725 total, 892 violent, 161,327 calls), YoY changes, car-break-in rise H1 2025; city release Feb 2026; FBI CDE linked. Deliberately no neighbourhood ranking |

Still open from the list above: housing-market/prices page (needs a compliant data path),
utilities **cost** page (needs the utility's rate schedule), "salary needed" (cheap),
city-vs-city comparisons (template decision), weather (weak intent), healthcare (weak intent).
Mover content remains deliberately not copied.


# Keyword map — Rocket City Move (Huntsville relocation)

Built 2026-10-19. This is the record of what was harvested, how keywords were
scored, which page each cluster belongs to, and what changed on the site as a
result. Raw data sits beside this file in `research/`.

## 1. Method (and what it does not claim)

**Harvest.** 249 seed queries were expanded through three keyless autocomplete
endpoints — Google Autocomplete (`suggestqueries.google.com/complete/search`),
Bing Autosuggest (`api.bing.com/osjson.aspx`) and DuckDuckGo (`duckduckgo.com/ac`)
— for 498 requests total, returning **4,522 unique query strings**. Seeds covered
the relocation decision, cost of living, housing, schools, commute/employers,
military PCS, buying/mortgage, taxes, utilities, admin paperwork, insurance,
comparisons, the 36 communities in `data/places.json`, and an a–z alphabet
expansion on the three head terms.

**Filtering.** Two gates, applied in `cluster_keywords.py`:

- *Wrong Huntsville.* Huntsville TX, ON and UT, Huntersville NC, and every result
  that drifted into another state or city (the seeds "moving to X" pull in
  "moving to tenerife, trinidad, hartlepool" etc.).
- *Off-topic.* Removal companies, job listings, weather forecasts, obituaries,
  sports, government-contractor news. Military/Redstone terms are kept.

Result: **2,245 kept, 798 dropped**. Files: `kw_raw.json` (every response, for
audit), `kw_suggestions.json` (flat, with provenance), `kw_clustered.json`
(clustered, scored), `clusters_report.txt` (human-readable).

**Scoring — and its limit.** Each query gets

```
score = 2 × (number of distinct seeds that surfaced it) + (11 − best autocomplete rank)
```

A query that appears for many different seeds near the top of the suggest box has
real search behaviour behind it; a query that appears once at rank 9 does not.
**This is a relative proxy, not a volume.** No search-volume figure is claimed
anywhere in this document or on the site, because no volume data was obtained —
there is no keyword-tool subscription on this box. Before committing budget,
re-check the top clusters in a real volume tool.

**Competitor read.** SERPs were pulled for ten head terms and the ranking pages'
headings extracted (`serp_heads.json`, `competitor_headings.json`). Recurring
competitors: `huntsvillemovingguide.com`, `movingtohuntsville.org`,
`relocatetohuntsville.com`, `wearehuntsville.com`, `theurbanlivingguide.com`,
`ownluxuryhomes.com`, `veteranpcs.com`/`fundedva.com` (VA loans),
`routeplanner.app` (drive times). Two observations shaped the page work:
national cost-of-living tools (RentCafe, Salary.com, uscostofliving.com) own the
generic "cost of living Huntsville" results, so this site competes there with a
*city-to-city tool* rather than another index page; and the neighbourhood pages
that rank are organised by **FAQ** ("What is the best neighborhood in Huntsville
for families?", "Which neighborhood is closest to Redstone Arsenal?"), which is
the format now used on this site's pages.

## 2. Clusters → pages

| Cluster | Queries kept | Top query by proxy score | Page that owns it |
|---|---|---|---|
| relocation-guide | 90 | moving to huntsville alabama | `index.html`, `moving-to-huntsville.html` |
| lifestyle / living here | 129 | is huntsville safe to live | `is-huntsville-a-good-place-to-live.html` **(new)** |
| neighborhoods | 417 | where to live in huntsville al | `neighborhoods.html` |
| schools | 175 | huntsville al school district | `schools.html` |
| commute / traffic | 31 | huntsville al traffic | `commute.html` |
| cost of living | 24 | cost of living in huntsville | `cost-of-living.html` |
| housing market | 41 | huntsville al average home price | `home-search.html` |
| homes for sale | 88 | huntsville al homes for sale | `home-search.html` |
| rent vs buy | 79 | huntsville al apartments | `rent-vs-buy.html` |
| buying process / mortgage | 84 | huntsville al mortgage lenders | `prequal.html` |
| jobs & employers | 177 | huntsville al jobs | `commute.html`, `moving-to-huntsville.html` |
| military / PCS | 123 | pcs redstone arsenal | `redstone-arsenal-pcs-va-loans.html` **(new)** |
| utilities & setup | 102 | huntsville al utilities website | `checklist.html` |
| taxes | 53 | huntsville al property tax | `cost-of-living.html` |
| admin paperwork | 75 | alabama vehicle registration | `checklist.html` |
| insurance | 48 | huntsville al renters insurance | `local-insurance.html` |
| realtors / agents (inside buying process) | 84 | huntsville al realtors | `local-realtors.html` |
| comparisons | 3 | huntsville vs madison al | `neighborhoods.html` |
| uncategorised | 852 | is huntsville a good place to live | spread across the above |

The two clusters with no page before this build were the biggest single
opportunities: **"living in Huntsville / is it a good place to live"** (the
top-scoring queries in the whole harvest: `is huntsville a good place to live`
at 78, `living in huntsville alabama` 76, `why move to huntsville al` 64,
`living in huntsville alabama pros and cons` 64) and **Redstone PCS/VA**
(`pcs redstone arsenal`, `redstone arsenal housing`, `redstone arsenal bah`,
`huntsville va loan`, `first time home buyer programs in huntsville alabama`).

## 3. What changed on the site

**Titles, meta descriptions and H1s (13 pages).** Applied by
`research/apply_seo_pass1.py`, which fails loudly if an exact-match target is
missing rather than silently skipping. The pattern: put the phrase people
actually type at the front (full "Alabama" on the guide page, "where to live",
"homes for sale", "realtors in Huntsville, AL", "home insurance"), and keep the
site's own honesty in the description rather than stacking keywords.

**Question blocks (12 pages).** Applied by `research/apply_seo_pass2.py`. Each
page gained a section answering the question-shaped queries from the harvest —
these are real queries, phrased as people type them. Every number in them is
either already published on the site (US Census ACS 2024 1-year medians),
measured live on the road network during this build (OSRM), or read from the
official source linked inline:

| Figure used | Value | Source |
|---|---|---|
| Median home value, metro | $331,800 | ACS 2024 1-yr (B25077), already on site |
| Median gross rent | $1,283 / month | ACS 2024 1-yr (B25064), already on site |
| Median property tax, mortgaged homes | $1,405 / yr ≈ 0.42% of value | ACS 2024 1-yr (B25103), rate computed |
| Madison → Redstone Gate 9 | 6.8 mi / 11.6 min off-peak | OSRM, measured 2026-10-19 |
| Downtown Huntsville → Gate 9 | 7.5 mi / 10.5 min off-peak | OSRM |
| Harvest / Meridianville / Hampton Cove / Owens Cross Roads → Gate 9 | 14.8 mi 19.6 min / 16.1 mi 21.4 min / 14.3 mi 22.9 min / 20.7 mi 31.1 min | OSRM |
| Huntsville → Birmingham / Chattanooga / Nashville / Atlanta / Memphis | 101 mi 1h53 / 102 mi 2h00 / 110 mi 2h15 / 180 mi 3h56 / 212 mi 4h23 | OSRM |
| Huntsville Utilities scale | 200k+ electric, ~100k water, ~56k gas customers | hsvutil.org (linked) |
| Space Command HQ relocation | — | huntsvilleal.gov (linked) |
| FBI Redstone growth: 2,200 → ~4,000 by 2030 | — | al.com (linked) |
| School facts (Madison City 8/3/2, Madison County 20,500 students / 30 campuses, 27% Limestone crossover, Green Mountain bus gap) | — | `data/schools.json`, verified at build time |

**Two new pages.**

- `is-huntsville-a-good-place-to-live.html` — targets the largest cluster.
  Deliberately structured as *who it suits / who it doesn't*, with a refusal to
  publish a crime ranking or a liveability score, and a "these are the honest
  downsides" list (humidity, severe-weather season and its insurance effect,
  growth traffic, two-car dependency, school-zone confusion).
- `redstone-arsenal-pcs-va-loans.html` — targets PCS/BAH/VA + first-time-buyer
  queries, with the measured drive-time table, on-post/off-post links to the
  garrison housing office, the DoD BAH table (never a quoted BAH figure), the
  VA path stated as general process, and the Alabama housing finance agency for
  down-payment help.

**Internal links and navigation.** Both new pages are in the "Where to live"
dropdown and the footer; `index.html` links both from its FAQ block;
`checklist.html` links the PCS page from the PCS context; `prequal.html` and
`rent-vs-buy.html` link it from their BAH/VA answers; `neighborhoods.html` links
both from its new comparison and FAQ sections. A pre-existing HTML bug on
`local-realtors.html` (a `<div>` closed with `</p>`) was fixed.

**New comparison section.** `neighborhoods.html` gained "Huntsville vs Madison vs
Athens", which is what people actually search (`huntsville al to madison al`,
`madison al vs huntsville al`, `athens al vs madison al`) and which no page
covered.

## 4. Verification performed

- All 16 pages return HTTP 200 through the tunnel; titles/descriptions present and
  within length norms (56–68 char titles, 116–236 char descriptions).
- Every page parses with Python's `html.parser` with no unbalanced tags.
- 50 internal links resolve to files on disk; 22 external links checked — the 403
  responses are bot walls (madisoncountyal.gov, broadbandmap.fcc.gov,
  travel.dod.mil, al.com), not dead pages. **Two links could not be verified from
  this box and should be clicked before launch:** `maps.huntsvilleal.gov`
  (DNS resolves but HTTPS fails from this container) and
  `statereportcard.alsde.edu` (the bare domain resolves; `www.` does not). Both
  were already used on the schools page before this build.
- The new PCS capture form was submitted end-to-end: the lead landed in
  `leads.jsonl`/`leads.csv` with the right form name and page, then the single
  test record was removed. `/health` back to 0 leads.
- Rendered pages were inspected in a real browser through the tunnel.

## 5. Still to do at launch (not done here, needs your decisions)

1. **Canonical tags, `robots.txt` and `sitemap.xml`** need the production domain —
   the preview is a tunnel URL, and canonicals pointing at a random
   `trycloudflare.com` host would be worse than none.
2. **Real volume data** for the top ~40 queries, before spending on content.
3. **Google Search Console / Bing Webmaster** once the domain is live, plus
   event and call tracking (see the funnel notes in the top-level README).
4. **Server-render the header/footer.** They are injected by `assets/chrome.js`,
   so crawlers that do not run JavaScript will index pages with no internal links.
   This is the single biggest technical SEO issue on the current build.
5. **Compliance review** of the payment, rate and BAH language before anything
   goes public.

## Appendix — top queries per cluster (proxy score, seed count, best rank)

### uncategorised — 852 queries

| score | seeds | best rank | query |
|---|---|---|---|
| 78 | 34 | 1 | is huntsville a good place to live |
| 76 | 33 | 1 | living in huntsville alabama |
| 64 | 27 | 1 | why move to huntsville alabama |
| 64 | 27 | 1 | why move to huntsville al |
| 64 | 27 | 1 | living in huntsville alabama pros and cons |
| 63 | 27 | 2 | living in huntsville alabama reddit |
| 58 | 24 | 1 | living in huntsville reddit |
| 57 | 24 | 2 | living in huntsville |
| 44 | 17 | 1 | living in huntsville al |
| 29 | 11 | 4 | life in huntsville alabama |
| 25 | 11 | 8 | places to live in huntsville alabama |
| 22 | 12 | 13 | huntsville alabama good place to live |
| 18 | 4 | 1 | huntsville al county |
| 18 | 5 | 3 | huntsville alabama living social |
| 16 | 3 | 1 | huntsville al population |

### neighborhoods — 417 queries

| score | seeds | best rank | query |
|---|---|---|---|
| 37 | 16 | 6 | where to live in huntsville al |
| 34 | 13 | 3 | best places to live in huntsville |
| 28 | 12 | 7 | huntsville alabama best place to live |
| 27 | 9 | 2 | best areas to live in huntsville al |
| 20 | 9 | 9 | best area to live in huntsville alabama |
| 19 | 10 | 12 | best place to live in huntsville al |
| 16 | 3 | 1 | best neighborhoods in huntsville al |
| 16 | 3 | 1 | huntsville al to madison al |
| 15 | 3 | 2 | huntsville al neighborhoods map |
| 14 | 3 | 3 | best neighborhoods in huntsville |
| 14 | 2 | 1 | huntsville al downtown |
| 14 | 2 | 1 | huntsville al downtown restaurant mazzios |
| 14 | 2 | 1 | huntsville al best neighborhoods |
| 14 | 2 | 1 | best places to live in huntsville al |
| 14 | 2 | 1 | living in madison alabama |

### jobs-employers — 177 queries

| score | seeds | best rank | query |
|---|---|---|---|
| 16 | 3 | 1 | huntsville al jobs |
| 14 | 2 | 1 | getting access to redstone arsenal |
| 13 | 2 | 2 | huntsville al jobs carpenter apprentice |
| 13 | 2 | 2 | redstone arsenal housing office |
| 12 | 1 | 1 | redstone arsenal community |
| 12 | 2 | 3 | huntsville al jobs full time |
| 12 | 1 | 1 | huntsville al employers |
| 12 | 1 | 1 | mazda toyota huntsville jobs |
| 12 | 1 | 1 | mazda toyota huntsville jobs hiring |
| 12 | 1 | 1 | pcs redstone arsenal |
| 12 | 1 | 1 | redstone arsenal housing |
| 12 | 2 | 3 | redstone arsenal housing for retirees |
| 12 | 1 | 1 | redstone arsenal bah |
| 12 | 1 | 1 | redstone arsenal on post housing |
| 12 | 1 | 1 | redstone arsenal on base housing |

### schools — 175 queries

| score | seeds | best rank | query |
|---|---|---|---|
| 16 | 4 | 3 | huntsville al school district |
| 15 | 3 | 2 | best school districts near huntsville al |
| 14 | 2 | 1 | huntsville al schools |
| 14 | 2 | 1 | huntsville al school schedule |
| 14 | 2 | 1 | huntsville al school zones |
| 13 | 2 | 2 | huntsville al school start date 2026 |
| 13 | 2 | 2 | huntsville al school zone locator |
| 12 | 2 | 3 | huntsville al school system |
| 12 | 1 | 1 | huntsville city schools |
| 12 | 1 | 1 | madison city schools |
| 12 | 1 | 1 | best school districts in huntsville alabama |
| 12 | 2 | 3 | best school district in huntsville alabama |
| 12 | 1 | 1 | huntsville al school ratings |
| 12 | 1 | 1 | madison county schools alabama |
| 12 | 1 | 1 | limestone county schools |

### lifestyle — 129 queries

| score | seeds | best rank | query |
|---|---|---|---|
| 24 | 8 | 3 | is huntsville safe to live |
| 18 | 4 | 1 | huntsville al weather |
| 16 | 3 | 1 | huntsville al crime rate |
| 15 | 3 | 2 | huntsville al weather 10 day |
| 15 | 3 | 2 | huntsville al channel 48 weather |
| 14 | 2 | 1 | huntsville al hotels |
| 13 | 2 | 2 | huntsville alabama weather |
| 13 | 2 | 2 | huntsville al crime rate map |
| 13 | 2 | 2 | huntsville al crime map |
| 12 | 2 | 3 | safest places to live in huntsville al |
| 12 | 2 | 3 | huntsville al crime rate 2025 |
| 12 | 1 | 1 | huntsville alabama tornado |
| 12 | 1 | 1 | huntsville al humidity |
| 12 | 1 | 1 | safest neighborhoods in huntsville al |
| 12 | 1 | 1 | safest neighborhoods in huntsville alabama |

### military-pcs — 123 queries

| score | seeds | best rank | query |
|---|---|---|---|
| 14 | 2 | 1 | getting access to redstone arsenal |
| 13 | 2 | 2 | redstone arsenal housing office |
| 12 | 1 | 1 | redstone arsenal community |
| 12 | 1 | 1 | pcs redstone arsenal |
| 12 | 1 | 1 | redstone arsenal housing |
| 12 | 2 | 3 | redstone arsenal housing for retirees |
| 12 | 1 | 1 | redstone arsenal bah |
| 12 | 1 | 1 | huntsville va location |
| 12 | 1 | 1 | redstone arsenal on post housing |
| 12 | 1 | 1 | redstone arsenal on base housing |
| 12 | 1 | 1 | huntsville al va clinic |
| 11 | 1 | 2 | redstone arsenal community activity center |
| 11 | 1 | 2 | transportation office redstone arsenal |
| 11 | 2 | 4 | map of redstone arsenal |
| 11 | 1 | 2 | redstone arsenal px hours |

### utilities-setup — 102 queries

| score | seeds | best rank | query |
|---|---|---|---|
| 17 | 4 | 2 | huntsville al utilities website |
| 15 | 3 | 2 | huntsville al utilities phone number |
| 14 | 2 | 1 | huntsville al utilities |
| 12 | 1 | 1 | huntsville utilities setup |
| 12 | 1 | 1 | huntsville al water bill |
| 12 | 2 | 3 | huntsville al water department |
| 12 | 1 | 1 | huntsville al internet providers |
| 12 | 1 | 1 | internet providers in huntsville al |
| 12 | 2 | 3 | huntsville al internet plans |
| 12 | 1 | 1 | huntsville al trash pickup schedule |
| 12 | 3 | 5 | huntsville utilities moving |
| 11 | 1 | 2 | huntsville utilities account setup |
| 11 | 1 | 2 | huntsville al utility bill increase |
| 11 | 1 | 2 | average water bill huntsville al |
| 11 | 1 | 2 | internet providers in alabama |

### relocation-guide — 90 queries

| score | seeds | best rank | query |
|---|---|---|---|
| 94 | 42 | 1 | moving to huntsville alabama |
| 74 | 33 | 3 | people moving to huntsville alabama everyday |
| 72 | 31 | 1 | moving to huntsville al |
| 66 | 28 | 1 | relocating to huntsville alabama |
| 66 | 28 | 1 | relocating to huntsville al |
| 58 | 24 | 1 | moving to huntsville |
| 18 | 4 | 1 | companies moving to huntsville al |
| 15 | 3 | 2 | moving to huntsville al reddit |
| 14 | 2 | 1 | space command moving to huntsville |
| 12 | 1 | 1 | huntsville al relocation guide |
| 12 | 1 | 1 | what to know before moving to huntsville alabama |
| 12 | 1 | 1 | moving to providence ri |
| 12 | 1 | 1 | moving to ardmore pa |
| 12 | 1 | 1 | moving to athens ga |
| 12 | 1 | 1 | moving to athens greece |

### homes-for-sale — 88 queries

| score | seeds | best rank | query |
|---|---|---|---|
| 18 | 4 | 1 | huntsville al homes for sale |
| 15 | 3 | 2 | huntsville al homes for sale zillow |
| 14 | 3 | 3 | huntsville al homes for sale by owner |
| 14 | 2 | 1 | huntsville al real estate |
| 14 | 3 | 3 | huntsville al real estate agents |
| 13 | 3 | 4 | huntsville al homes for sale with pool |
| 13 | 2 | 2 | huntsville al real estate for sale |
| 12 | 2 | 3 | huntsville al homes for sale 4 bedroom |
| 12 | 2 | 3 | huntsville al real estate market |
| 12 | 1 | 1 | madison al homes for sale |
| 12 | 1 | 1 | athens al homes for sale |
| 12 | 2 | 3 | owens cross roads homes for sale |
| 11 | 2 | 4 | huntsville al real estate zillow |
| 11 | 1 | 2 | madison al homes for sale zillow |
| 11 | 1 | 2 | athens al homes for sale by owner |

### buying-process — 84 queries

| score | seeds | best rank | query |
|---|---|---|---|
| 14 | 3 | 3 | huntsville al real estate agents |
| 14 | 2 | 1 | huntsville al mortgage rates |
| 14 | 2 | 1 | huntsville al mortgage lenders |
| 14 | 2 | 1 | huntsville al realtors |
| 13 | 2 | 2 | broker huntsville al mortgage rates |
| 13 | 2 | 2 | first time home buyer programs in huntsville alabama |
| 12 | 1 | 1 | huntsville al loans |
| 12 | 2 | 3 | current mortgage rates huntsville al |
| 12 | 1 | 1 | huntsville al first time home buyer |
| 12 | 1 | 1 | home loans huntsville al first time buyers |
| 12 | 1 | 1 | alabama first time home buyer programs |
| 12 | 1 | 1 | huntsville al down payment assistance program |
| 12 | 1 | 1 | city of huntsville down payment assistance |
| 12 | 1 | 1 | best realtors in huntsville al |
| 12 | 1 | 1 | best realtors in huntsville alabama |

### rent-vs-buy — 79 queries

| score | seeds | best rank | query |
|---|---|---|---|
| 14 | 2 | 1 | huntsville al apartments |
| 14 | 2 | 1 | huntsville al rentals |
| 14 | 2 | 1 | apartments in downtown huntsville |
| 13 | 2 | 2 | huntsville al apartments for rent |
| 13 | 2 | 2 | huntsville al rental homes |
| 13 | 2 | 2 | apartments in downtown huntsville reviews |
| 12 | 3 | 5 | moving truck rental huntsville al |
| 12 | 2 | 3 | huntsville al rental cars |
| 11 | 1 | 2 | homes for rent in huntsville area |
| 11 | 2 | 4 | apartments in downtown huntsville cheap |
| 11 | 2 | 4 | the village of hampton cove apartments |
| 10 | 1 | 3 | huntsville al downtown apartments |
| 10 | 1 | 3 | apartments huntsville al reddit |
| 10 | 1 | 3 | huntsville al apartments downtown |
| 10 | 1 | 3 | constellation apartments huntsville al |

### admin-paperwork — 75 queries

| score | seeds | best rank | query |
|---|---|---|---|
| 12 | 1 | 1 | alabama vehicle registration |
| 12 | 1 | 1 | huntsville al tag office |
| 12 | 1 | 1 | alabama drivers license transfer |
| 12 | 1 | 1 | huntsville al business license |
| 11 | 1 | 2 | alabama vehicle registration renewal |
| 11 | 1 | 2 | huntsville al tag renewal |
| 11 | 1 | 2 | madison county tag office huntsville al |
| 11 | 1 | 2 | what do you need to transfer your driver's license to alabama |
| 11 | 1 | 2 | alabama driver license out of state transfer |
| 11 | 1 | 2 | huntsville al dmv |
| 10 | 1 | 3 | alabama vehicle registration online |
| 10 | 1 | 3 | alabama vehicle registration lookup |
| 10 | 1 | 3 | huntsville al tag renewal locations |
| 10 | 1 | 3 | car tags huntsville al |
| 10 | 1 | 3 | how to get an alabama driver's license from out of state |

### taxes — 53 queries

| score | seeds | best rank | query |
|---|---|---|---|
| 14 | 2 | 1 | huntsville al property tax |
| 13 | 2 | 2 | huntsville al sales tax rate |
| 12 | 1 | 1 | madison county property tax |
| 12 | 1 | 1 | alabama property tax rate |
| 12 | 1 | 1 | huntsville al taxes |
| 11 | 1 | 2 | huntsville al property tax rate |
| 11 | 2 | 4 | huntsville al tax assessor property search |
| 11 | 1 | 2 | madison county property tax search |
| 11 | 1 | 2 | madison county property tax il |
| 11 | 1 | 2 | alabama property tax rates by county |
| 11 | 1 | 2 | alabama property tax rates 2026 |
| 11 | 1 | 2 | huntsville al tax rate |
| 10 | 1 | 3 | huntsville al property tax search |
| 10 | 1 | 3 | huntsville al property tax assessor |
| 10 | 1 | 3 | madison county property tax records |

### insurance — 48 queries

| score | seeds | best rank | query |
|---|---|---|---|
| 18 | 4 | 1 | huntsville al renters insurance |
| 14 | 2 | 1 | huntsville al home insurance cost |
| 14 | 2 | 1 | home insurance huntsville al |
| 14 | 2 | 1 | huntsville al car insurance |
| 14 | 2 | 1 | huntsville al insurance |
| 13 | 2 | 2 | huntsville al home insurance |
| 13 | 2 | 2 | car insurance huntsville al |
| 12 | 2 | 3 | huntsville al homeowners insurance |
| 11 | 1 | 2 | home insurance quotes huntsville al |
| 11 | 2 | 4 | cheap car insurance huntsville al |
| 11 | 1 | 2 | is car insurance cheap in alabama |
| 11 | 1 | 2 | huntsville al insurance agencies |
| 10 | 1 | 3 | home insurance broker huntsville al |
| 10 | 2 | 5 | insurance companies huntsville al |
| 10 | 1 | 3 | how much is car insurance in alabama |

### housing-market — 41 queries

| score | seeds | best rank | query |
|---|---|---|---|
| 14 | 2 | 1 | huntsville al average home price |
| 14 | 2 | 1 | huntsville al housing market |
| 12 | 2 | 3 | huntsville al real estate market |
| 12 | 1 | 1 | huntsville al new construction homes |
| 11 | 1 | 2 | huntsville al new construction |
| 11 | 1 | 2 | new construction in huntsville al |
| 11 | 1 | 2 | huntsville al median home price |
| 11 | 1 | 2 | huntsville al housing market forecast |
| 11 | 1 | 2 | huntsville al housing market trends |
| 11 | 1 | 2 | is the twickenham property market moving |
| 10 | 1 | 3 | new construction builders in huntsville al |
| 10 | 2 | 5 | huntsville al rental market |
| 10 | 1 | 3 | what is the average home price in huntsville alabama |
| 10 | 1 | 3 | huntsville al housing market predictions |
| 10 | 1 | 3 | housing market in huntsville |

### commute — 31 queries

| score | seeds | best rank | query |
|---|---|---|---|
| 12 | 1 | 1 | huntsville al traffic |
| 12 | 1 | 1 | alabama drivers license transfer |
| 11 | 1 | 2 | huntsville al traffic news |
| 11 | 1 | 2 | huntsville al traffic engineering |
| 11 | 1 | 2 | what do you need to transfer your driver's license to alabama |
| 11 | 1 | 2 | alabama driver license out of state transfer |
| 10 | 1 | 3 | huntsville al traffic map |
| 10 | 1 | 3 | how to get an alabama driver's license from out of state |
| 10 | 1 | 3 | transfer driver license to alabama |
| 10 | 2 | 5 | distance from madison to huntsville al |
| 9 | 1 | 4 | huntsville al traffic cameras |
| 9 | 1 | 4 | can you get your driver's license online in alabama |
| 8 | 1 | 5 | huntsville al traffic report |
| 8 | 1 | 5 | huntsville al traffic cameras live |
| 7 | 1 | 6 | huntsville al traffic accidents today |

### cost-of-living — 24 queries

| score | seeds | best rank | query |
|---|---|---|---|
| 50 | 21 | 3 | cost of living in huntsville |
| 18 | 4 | 1 | cost of living in huntsville al per month |
| 14 | 2 | 1 | huntsville al cost of living |
| 13 | 2 | 2 | average cost of living in huntsville al |
| 13 | 3 | 4 | cost of living in huntsville alabama |
| 12 | 2 | 3 | average cost of living in huntsville alabama |
| 12 | 1 | 1 | living wage huntsville al |
| 11 | 1 | 2 | huntsville al cost of living comparison |
| 11 | 1 | 2 | cost of living index huntsville al |
| 10 | 1 | 3 | huntsville al cost of living index |
| 10 | 1 | 3 | what is the cost of living in huntsville al |
| 10 | 2 | 5 | cost of living in huntsville al |
| 10 | 1 | 3 | how much is car insurance in alabama |
| 10 | 1 | 3 | cost of living in ardmore ok |
| 9 | 1 | 4 | huntsville alabama cost of living calculator |

### comparisons — 3 queries

| score | seeds | best rank | query |
|---|---|---|---|
| 6 | 1 | 7 | compare the cost of living in huntsville with other cities |
| 5 | 1 | 8 | living in somerville vs cambridge |
| 4 | 1 | 9 | five points vs little five points |


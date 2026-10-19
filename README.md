# Rocket City Move — local prototype

A mortgage-first relocation site for Huntsville / Madison / Madison County, Alabama.
Static pages + a dependency-free Python server. No build step, no accounts, no keys.

Built 2026-10-13 for review. Everything numeric is either fetched live or read from
`data/*.json` — nothing on the site is invented.

---

## Live preview link

**https://weblog-tapes-dispatch-volumes.trycloudflare.com** — a Cloudflare quick tunnel from this
container to `localhost:8080`. Open it anywhere; no interstitial, no login. Mobile works too.
(This URL replaced the Oct 13 one; a quick tunnel gets a new random hostname on every restart.)

It is a tunnel, not a deployment, so two things are true:

- The link lives only while two processes run: `python3 server.py --port 8080` in this folder, and
  `/opt/data/bin/cloudflared tunnel --url http://localhost:8080 --logfile /opt/data/cloudflared.log`.
  The URL is printed in that log; a **restart gives a new random URL**.
- Anyone with the link can load the pages and submit the forms (submissions land in `leads.csv` on this
  box). It is not a public launch — the compliance placeholders are still placeholders.

If the link stops working, restart both processes; if you want a stable URL, that needs a named
Cloudflare tunnel or a real deployment (the receipttocsv GitHub → Railway pattern).

## Run it

```bash
cd /opt/data/projects/huntsville-move-site
python3 server.py --port 8080            # stdlib only, no pip installs
```

Then:

| Route | What it is |
|---|---|
| http://127.0.0.1:8080/ | the site |
| http://127.0.0.1:8080/_leads | every captured form submission (prototype convenience) |
| http://127.0.0.1:8080/health | server + lead count |

Options: `--port N` (default 8080, or `$PORT`), `--host` (default 0.0.0.0).

### Viewing it from your machine

The container is on `172.16.0.2`. Three ways in, cheapest first:

1. **From the VPS host** — the Docker bridge is routable from the host:
   `curl -I http://172.16.0.2:8080/`
2. **SSH tunnel from your laptop** (works from anywhere):
   `ssh -L 8080:172.16.0.2:8080 <you>@<vps-host>` then open http://localhost:8080/
3. **Serve it on the host instead** — `/opt/data` is bind-mounted at
   `/docker/hermes-agent-96er/data`, so on the VPS:
   `cd /docker/hermes-agent-96er/data/projects/huntsville-move-site && python3 server.py --port 8080`
   (the container server must be stopped first, or use a different port)

I could not test route 1 from inside the container — no Docker access to the host — so
treat it as "should work" until you try it.

---

## What's built

**Five tools, all working:**

| Tool | Page | Data path |
|---|---|---|
| Commute calculator | `commute.html` | Live OSRM routing from pinned coordinates. 12 destinations × 36 communities, grouped by county. Verified: Downtown→Gate 9 7.5 mi / 10.5 min; Owens Cross Roads→Gate 9 20.7 mi / 31.1 min |
| Your city → Huntsville | `cost-of-living.html` | US Census ACS 2024 1-year (B25064 rent, B25077 home value, B19013 income, B25103 property tax) for 57 metros via the Census Reporter API — fetched at build time into `data/metros.json` |
| Rent vs buy + BAH | `rent-vs-buy.html` | Full PITI + maintenance vs rent, interest paid, break-even, net proceeds, VA toggle, BAH as an input (never a quoted figure) |
| Relocation checklist | `checklist.html` | Jurisdiction-aware, generated from `data/checklist.json` — utilities, tags/title, licence, voter registration, school enrollment, pets, PCS |
| School comparison | `schools.html` | `data/schools.json` — only facts read from district sites; everything else links to the official locator / state report card |

Plus: pillar page (`moving-to-huntsville.html`), neighborhoods index
(`neighborhoods.html`, 36 communities), home search with the ValleyMLS popup
(`home-search.html`), pre-qual form (`prequal.html`), and the two non-compensated
information pages (`local-realtors.html`, `local-insurance.html`).

Two pages were added on 2026-10-19 from the keyword research: the honest
pros/cons answer page (`is-huntsville-a-good-place-to-live.html`) and the
military/PCS/VA page (`redstone-arsenal-pcs-va-loans.html`). Both are in the nav
dropdown and footer.

Four more were added the same day from the competitor gap analysis
(`research/COMPETITOR_ANALYSIS.md`), each sourced from a primary document:

| Page | File | Primary sources |
| --- | --- | --- |
| Rent & apartments | `rent-in-huntsville.html` | Census ACS 2024 (1-yr + 5-yr) B25064, B25003, B25071 via Census Reporter — `research/acs_area_rent.json`; no per-neighbourhood rent figures published (unavailable) |
| Property taxes | `property-taxes.html` | Madison County Tax Collector published rate list; Madison County Tax Assessor "property tax facts"; Alabama DOR ad valorem page + Code of Alabama §40-8-1 (10% Class III ratio). Worked examples are arithmetic on those two published inputs, not quoted bills |
| Top employers | `huntsville-employers.html` | Huntsville/Madison County Chamber *2026 Leading Employers* PDF (July 2026), 51 entries; sector sums computed from it, with an explicit warning that the Redstone installation figure overlaps contractor headcounts |
| Crime & safety | `huntsville-crime-safety.html` | HPD *Annual Report 2025* (NIBRS counts + YoY changes); City of Huntsville release 10 Feb 2026 (robbery −28%, B&E −21%, agg. assault −20%, population +24% since 2019 vs violent −50%); FBI CDE linked for cross-city checks. No neighbourhood ranking is published, deliberately |

The nav was restructured into two dropdowns ("Where to live", "Money & jobs") to
keep the bar on one line with 20 pages, and `index.html` gained a "four questions"
section linking the new pages.

## Keyword research and SEO

`research/KEYWORD_MAP.md` is the record: 4,522 real autocomplete suggestions
harvested from 249 seeds (Google + Bing + DuckDuckGo, keyless), filtered to 2,245
Huntsville-relevant queries, clustered and scored with a documented proxy (no
search volumes are claimed anywhere — none were obtained). Every page's title,
meta description and H1 was rebuilt around the phrase people actually type, and
12 pages gained question-answer blocks using the real question phrasing from the
harvest. Every figure in the new copy is either already published on the site
(ACS 2024 medians), measured live on the road network in this build (OSRM
drive times), or read from the official source linked inline.

Scripts, all rerunnable: `research/harvest_keywords.py`,
`research/cluster_keywords.py`, `research/apply_seo_pass1.py` (titles/H1s),
`research/apply_seo_pass2.py` (question blocks), `research/build_keyword_map.py`.
The two apply scripts use exact-match replacement and exit non-zero if a target
string is missing, so they cannot silently half-apply.

## Keyword research and SEO

`research/KEYWORD_MAP.md` is the record: 4,522 real autocomplete suggestions
harvested from 249 seeds (Google + Bing + DuckDuckGo, keyless), filtered to 2,245
Huntsville-relevant queries, clustered and scored with a documented proxy (no
search volumes are claimed anywhere — none were obtained). Every page's title,
meta description and H1 was rebuilt around the phrase people actually type, and
12 pages gained question-answer blocks using the real question phrasing from the
harvest. Every figure in the new copy is either already published on the site
(ACS 2024 medians), measured live on the road network in this build (OSRM
drive times), or read from the official source linked inline.

Scripts, all rerunnable: `research/harvest_keywords.py`,
`research/cluster_keywords.py`, `research/apply_seo_pass1.py` (titles/H1s),
`research/apply_seo_pass2.py` (question blocks), `research/build_keyword_map.py`.
The two apply scripts use exact-match replacement and exit non-zero if a target
string is missing, so they cannot silently half-apply.

**Lead funnel:** 8 capture points on the site; every one posts to `/api/lead` or
`/api/alert`, which appends to `leads.jsonl`, `leads.csv` and `alerts.jsonl` and prints
to the server log. `/` → tool → capture → pre-qual is wired end to end so you can watch
it work.

**ValleyMLS handoff:** `home-search.html` captures the alert details *above* the outbound
button, then opens valleymls.com in a new window. No IDX, no iframe — see
`BUILD_SPEC_v1.md` in `../huntsville-relocation/` for why.

---

## Files

```
index.html  moving-to-huntsville.html  neighborhoods.html  schools.html
commute.html  cost-of-living.html  rent-vs-buy.html  checklist.html
home-search.html  prequal.html  local-realtors.html  local-insurance.html  about.html
is-huntsville-a-good-place-to-live.html   redstone-arsenal-pcs-va-loans.html
rent-in-huntsville.html  property-taxes.html  huntsville-employers.html
huntsville-crime-safety.html
assets/style.css      all styling
assets/chrome.js      shared header/footer (injected)
assets/app.js         every tool's logic
assets/img/logo/      round badge — 5 SVGs + PNG set + favicon.ico (see its README.md);
                      regenerate with `python3 assets/img/logo/build_logos.py`
logo-preview.html     the badge on light/dark, every size, with the palette
data/metros.json      57 metros, ACS 2024 (release: acs2024_1yr)
data/places.json      36 community centroids (county-tagged) + 12 employer/gate coordinates
data/neighborhoods-content.json   the 36 community write-ups
data/schools.json     the three districts
data/checklist.json   the checklist rules by jurisdiction
data/places_raw.json  raw geocoder output kept for audit
server.py             stdlib server + lead capture
screenshots/          page captures
research/             keyword harvest, clustering, SEO apply scripts, KEYWORD_MAP.md
```

## Known gaps and things I'd change with your input

**Expanded communities (second review pass):** 20 → 36 communities across three counties —
added Hazel Green, Green Mountain, Ryland, Capshaw, Triana, Ardmore, Athens, East Limestone,
Tanner, Elkmont, Decatur, Hartselle, Priceville, Trinity, Somerville and New Hope, each with
its own coordinates (so the commute calculator routes to them) and its own district entry.
The checklist now carries **28 communities** and three new jurisdiction classes
(`limestone`, `morgan`, `limestone_city`, `morgan_city`) — Athens gets Athens Utilities and
Athens City Schools; Decatur and Hartselle get their municipal utilities and their city
districts; Capshaw and Tanner get the private-well/county-hauler path. The community
dropdown is now generated from `data/checklist.json`, so adding a community is a one-file
change. The commute picker groups its 36 boxes by county. The schools page covers eight
systems across Madison, Limestone and Morgan counties, with a "quirks" section: Triana
attends Madison City by agreement, 27% of Madison City students live in Limestone County,
Green Mountain is Huntsville City but off the bus route, and Morgan County alone has three
public systems.

**Fixed since the first review pass:**

- Nav collapsed into a single line with a "Where to live" dropdown (Moving guide /
  Neighborhoods / Schools / Home search) — verified 23px tall, one line at 1280px.
- Checklist now branches on jurisdiction. Each task carries `classes`
  (`huntsville_city` / `madison_city` / `county` / `limestone` / `morgan`) and
  `data/checklist.json` maps each community to its class: Harvest shows
  "unincorporated Madison County" with the private-hauler task, Hampton Cove shows
  "inside Huntsville city limits" with the city utility task. The summary line no longer
  repeats the county for county addresses.
- Commute peak column is now a corridor-aware **range** instead of one flat 1.35×:
  Gate 9 shift change (1.40 base), Research Park / I-565 (1.35), downtown / medical (1.30),
  outbound industrial (1.25), plus an allowance for the 431 mountain gap. Downtown→Gate 9
  reads 15–16 min; Owens Cross Roads reads 46–50 min. The footnote names the corridors used.

**Still open:**

1. **School enrollment figures** for Huntsville City and Madison City are marked unverified
   rather than guessed. Same for any BAH number.
2. **SEO plumbing needs the production domain**: canonical tags, `robots.txt` and a
   `sitemap.xml` were deliberately not added, because pointing a canonical at a
   `trycloudflare.com` tunnel host is worse than having none. Search Console/Bing
   Webmaster verification also waits on the domain.
3. **Server-render the header/footer.** They are injected by `assets/chrome.js`,
   so a crawler that does not execute JavaScript sees pages with no internal
   links at all — the biggest technical SEO issue in this build.
4. **Re-check the top ~40 queries in a real volume tool** before spending on
   content: the keyword map scores demand with an autocomplete proxy, not volumes.
5. **Production stack**: this prototype is static + stdlib. For launch, the tools want a
   small FastAPI service (PDF generation, alert cron, CRM webhook) on the same
   GitHub → Railway pattern as receipttocsv.com, and the header/footer should be
   server-rendered rather than injected by JS.
6. **Compliance is not done**: NMLS ID, Equal Housing, APR/payment disclaimers and TCPA
   consent language are placeholders. Nothing here should be public until that review passes.

# Deploying and connecting movetohuntsville.net

## Current status — live on Railway (2026-10-19)

| | |
| --- | --- |
| Railway workspace | `timbyrne7's Projects` |
| Project | `sweet-courage` — `8cbd341f-b0a9-4846-8449-b533c10ec5a5` |
| Service | `huntsville-move-site` — `0afa3aa2-f971-43cd-9f35-052ba57b8861` (region `iad`) |
| Environment | `production` — `b2e9a5d0-4579-42b3-957d-82932f314c14` |
| Source | `github.com/timbyrne7/huntsville-move-site` (public), branch `main` — **push to deploy** |
| Railway URL | https://huntsville-move-site-production.up.railway.app (verified 200) |
| Volume | `huntsville-move-site-volume` — `cc9d1afa-6724-428d-813b-b46f871caba4`, mounted `/data`, 5 GB |
| Variables | `LEADS_DIR=/data`, `LEADS_TOKEN` (value in local `.leads_token`, gitignored) |
| Custom domain | `www.movetohuntsville.net` — **verified, Let's Encrypt cert live** (CN=`www.movetohuntsville.net`, expires 2027-01-17) |
| Apex | `movetohuntsville.net` — GoDaddy forwarding still redirects to itself (301 loop) and serves no TLS; Railway has the apex staged and wants `CNAME @ → ma3ljqel.up.railway.app` + `TXT _railway-verify`, which GoDaddy DNS cannot satisfy (no ALIAS) |

Verified 2026-10-19 21:15 UTC over the live domain: all 20 pages 200, `/health` 200,
`http://` → 301 `https://`, `/_leads` 404 from outside, `/leads.csv|jsonl` 403.

### Apex: pick one

1. **GoDaddy forwarding** (no DNS move) — set the target to `https://www.movetohuntsville.net`,
   301, forward only. Fixes `http://movetohuntsville.net`, but `https://movetohuntsville.net`
   will still throw a certificate warning: GoDaddy's forwarding fleet serves no TLS for the apex.
2. **Move DNS to Cloudflare** (free, recommended) — change the nameservers at GoDaddy, then
   create `CNAME @ → ma3ljqel.up.railway.app` (proxied, gives flattening) plus
   `TXT _railway-verify = railway-verify=0223e770abd78153d4aefbd3fa8839f80fe8da3b5523849b3f09c6c87c40ede8`,
   and a redirect rule `movetohuntsville.net/*` → `https://www.movetohuntsville.net/$1`. The apex
   then serves the site over HTTPS with no warnings.

### Operating it

```bash
# deploy: push to main and Railway rebuilds automatically
git push origin main

railway status                          # service + deployment state
railway logs                            # build/runtime logs (linked to this folder)
railway variables                       # current env vars
railway domain                          # service + custom domains

# read captured leads (never served to the public)
curl "https://www.movetohuntsville.net/_leads?token=$(cat .leads_token)"

# shell into the running container / inspect the volume
railway ssh "ls -la /data && tail -3 /data/leads.jsonl"
```

`/_leads` answers 404 to any request from a non-local host without the token, and any
`/leads.*` path is 403 — both verified against the deployed service, not just locally.

## Original domain facts (checked 2026-10-19, RDAP + DNS)

| | |
| --- | --- |
| Registrar | GoDaddy.com, LLC |
| Registered | 2026-10-19, expires 2027-10-19 |
| Nameservers | `ns55.domaincontrol.com`, `ns56.domaincontrol.com` (GoDaddy DNS) |
| A records | `15.197.148.33`, `3.33.130.190` — GoDaddy's **parking page**, not a site |

---

## Option A — Railway (chosen)

The server is stdlib-only Python, reads `$PORT`, binds `0.0.0.0`; `Procfile`,
`runtime.txt` and `requirements.txt` are already in the repo, so Railway needs no build
configuration.

1. **Push this folder to GitHub** (it is a fresh git repo with one commit, no remote yet):
   ```bash
   git remote add origin git@github.com:<you>/huntsville-move-site.git
   git push -u origin main
   ```
2. **Railway → New Project → Deploy from GitHub repo** → pick the repo. It runs
   `web: python3 server.py --port $PORT --host 0.0.0.0` and gives you a
   `*.up.railway.app` hostname.
3. **Add a volume before the first real lead** — service → Variables/Data → **+ Volume**,
   mount path `/data`, then add the variable `LEADS_DIR=/data`. The service redeploys and
   submissions land on persistent storage instead of the wiped container filesystem.
4. **Add `LEADS_TOKEN`** (any long random string) if you want to read submissions in
   production: `https://<your-domain>/_leads?token=<that string>`. Without it, `/_leads`
   answers 404 to any non-local request and `/leads.csv` is never served.
5. **Railway → your service → Settings → Networking → Custom Domain** → add
   `movetohuntsville.net`. Railway replies with a CNAME target such as
   `xxxxxxxx.up.railway.app`.
6. **At GoDaddy → DNS**, add:

   | Type | Name | Value | TTL |
   | --- | --- | --- | --- |
   | CNAME | `www` | the target Railway gave you | 600 |

   GoDaddy DNS has no ALIAS/ANAME, so the apex (`movetohuntsville.net` without www) cannot
   point at a CNAME. Two clean ways to handle it:
   - **Forward** (simplest): GoDaddy → Domain Settings → Forwarding → `movetohuntsville.net`
     → `https://www.movetohuntsville.net` (301, forward only). Nothing else to add.
   - **Or move DNS to Cloudflare** (free): change the nameservers at GoDaddy to the two
     Cloudflare gives you, then add a proxied CNAME for `@` as well as `www`. This also gives
     you a CDN, WAF and easy redirects, and is what I would do long term.

   Either way, once DNS resolves, Railway issues the TLS certificate automatically (usually
   a few minutes; it needs the CNAME to be correct first).

7. **Verify**: `curl -I https://www.movetohuntsville.net` should show `200` and a valid
   certificate; then check that `https://movetohuntsville.net` redirects to it.

### Environment variables the app understands

| Variable | Default | Purpose |
| --- | --- | --- |
| `PORT` | `8080` | Set by Railway; the server binds it |
| `HOST` | `0.0.0.0` | Bind address |
| `LEADS_DIR` | project folder | Where `leads.jsonl` / `leads.csv` / `alerts.jsonl` are written — point at the mounted volume |
| `LEADS_TOKEN` | unset | Enables `/_leads?token=…` from a public host; unset means localhost-only |

### Before real traffic

Railway's container filesystem is **ephemeral** — every deploy wipes it and it is not shared
between instances. Step 3 (volume + `LEADS_DIR`) fixes that, or change the form handler to
post to a real destination (CRM, email, Google Sheet). Do not launch a paid campaign against
container-local storage.

---

## Search-engine surface (live, 2026-10-20)

Generated, never hand-edited — run the tools after adding or renaming a page:

```
python3 tools/gen_seo.py          # writes the head block, robots.txt, sitemap.xml
python3 tools/gen_seo.py --check  # non-zero exit if a page has drifted out of date
python3 tools/make_og.py          # rebuilds assets/og.png (needs Pillow)
```

- Every page carries its own `<link rel="canonical">`, Open Graph + Twitter card tags
  pointing at `assets/og.png` (1200×630), and JSON-LD: `Organization` + `WebSite` +
  `WebPage` on the index, `WebPage` + `BreadcrumbList` elsewhere.
- `robots.txt` allows everything except `/_leads`, `/leads.*`, `/api/*` and
  `/logo-preview.html`; it points at `sitemap.xml`.
- `sitemap.xml` is built from the pages on disk with `lastmod` from the last git commit
  touching each file, so it cannot drift from the site.
- `logo-preview.html` is `noindex, follow` and deliberately absent from the sitemap.
- The prototype banner in `assets/chrome.js` now renders only on localhost (or `?preview`):
  on the published domain it was telling visitors and crawlers the site was "not published".

### Still human-gated

Nothing below can be done by an agent without Tim's Google account:

1. **Google Search Console** → add a **Domain** property for `movetohuntsville.net`
   (covers apex + www). Verify by DNS TXT at GoDaddy — Search Console shows the exact
   `google-site-verification=…` value; add it as a TXT record on `@`.
2. **Submit the sitemap**: `https://www.movetohuntsville.net/sitemap.xml`.
3. **URL Inspection → Request Indexing** on the homepage and the five tool pages.
4. **Links.** A new domain with no inbound links is the actual bottleneck, not the markup.
   Directory listings, community/niche mentions and outreach all need a human account or
   voice. There is no API that forces Google to index a URL; the old sitemap *ping*
   endpoint was retired in 2023.

For Bing/Yandex, IndexNow is account-free: serve a key file at the site root and POST the
URLs — worth adding if Bing traffic matters.

---

## Option B — Cloudflare Tunnel (live in ~10 minutes, but hosted on this box)

No deploy, no code changes: the site you are looking at is served from this container and
published through `cloudflared`. A *quick* tunnel has a random, rotating hostname; a *named*
tunnel is stable and can be bound to your own domain.

1. **Move the zone to Cloudflare**: at GoDaddy → Nameservers → "I'll use my own", enter the
   two nameservers Cloudflare shows you for the zone.
2. **Authenticate cloudflared** (needs one browser click from you):
   ```bash
   /opt/data/bin/cloudflared tunnel login
   ```
3. **Create and route the tunnel**:
   ```bash
   /opt/data/bin/cloudflared tunnel create hsv-site
   /opt/data/bin/cloudflared tunnel route dns hsv-site movetohuntsville.net
   /opt/data/bin/cloudflared tunnel route dns hsv-site www.movetohuntsville.net
   /opt/data/bin/cloudflared tunnel run --url http://localhost:8080 hsv-site
   ```
4. No DNS records to add by hand — step 3 writes the CNAMEs into the Cloudflare zone.

**Trade-off:** the moment this container stops, the site is down. That is fine for review
and demos; it is not a production host.

---

## Either way, once the domain resolves

- Point `canonical`, `og:url`, `robots.txt` and `sitemap.xml` at the live hostname. Nothing
  has been set yet — deliberately, because canonicalising to a tunnel hostname is worse than
  no canonical tag at all.
- Choose apex or www as canonical and 301 the other. My preference: `www` canonical, apex
  forwarding, because GoDaddy's DNS cannot alias the apex.

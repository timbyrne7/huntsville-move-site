# Connecting movetohuntsville.net

Domain state as checked on 2026-10-19 (RDAP + DNS):

| | |
| --- | --- |
| Registrar | GoDaddy.com, LLC |
| Registered | 2026-10-19, expires 2027-10-19 |
| Nameservers | `ns55.domaincontrol.com`, `ns56.domaincontrol.com` (GoDaddy DNS) |
| A records | `15.197.148.33`, `3.33.130.190` — GoDaddy's **parking page**, not a site |

So nothing is wired yet. There are two ways to connect it; pick one, not both.

---

## Option A — Railway (same pattern as receipttocsv.com)

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

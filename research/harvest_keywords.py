#!/usr/bin/env python3
"""Harvest real search-query suggestions for Huntsville relocation keywords.

Sources (all keyless, all real responses - nothing invented):
  * Google Autocomplete  suggestqueries.google.com/complete/search?client=firefox
  * Bing Autosuggest     api.bing.com/osjson.aspx
  * DuckDuckGo autocomp. duckduckgo.com/ac/

Writes research/kw_raw.json (every response, for audit) and
research/kw_suggestions.json (flat deduped rows with provenance).
"""
import json
import os
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
      "Accept-Language": "en-US,en;q=0.9"}


def fetch(url, timeout=12):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def google(seed):
    u = "https://suggestqueries.google.com/complete/search?client=firefox&hl=en&gl=us&q=" + urllib.parse.quote(seed)
    try:
        data = json.loads(fetch(u))
        return [(s, 1) for s in data[1]]
    except Exception as e:  # noqa: BLE001
        return [("__ERR__ " + repr(e), 0)]


def bing(seed):
    u = "https://api.bing.com/osjson.aspx?query=" + urllib.parse.quote(seed)
    try:
        data = json.loads(fetch(u))
        return [(s, 2) for s in data[1]]
    except Exception as e:  # noqa: BLE001
        return [("__ERR__ " + repr(e), 0)]


def ddg(seed):
    u = "https://duckduckgo.com/ac/?q=" + urllib.parse.quote(seed) + "&type=list"
    try:
        data = json.loads(fetch(u))
        return [(d["phrase"], 3) for d in data if isinstance(d, dict)]
    except Exception as e:  # noqa: BLE001
        return [("__ERR__ " + repr(e), 0)]


def build_seeds():
    community = json.load(open(os.path.join(SITE, "data", "places.json")))["neighborhoods"]
    names = [c["name"] for c in community]

    seeds = [
        # relocation / moving intent
        "moving to huntsville", "moving to huntsville al", "moving to huntsville alabama",
        "relocating to huntsville", "relocating to huntsville al", "i'm moving to huntsville",
        "moving from out of state to huntsville", "moving to huntsville al pros and cons",
        "should i move to huntsville", "why move to huntsville", "moving to huntsville for work",
        "is huntsville a good place to live", "huntsville al relocation guide",
        "moving to huntsville checklist", "moving to huntsville what to know",
        # city facts people check
        "huntsville al", "huntsville alabama", "huntsville al crime rate", "huntsville al weather",
        "huntsville al population", "huntsville al traffic", "huntsville al cost of living",
        "huntsville alabama tornado", "huntsville al downtown", "huntsville al reddit",
        "what is huntsville alabama known for", "huntsville al humid",
        # housing
        "huntsville al homes for sale", "huntsville al real estate", "huntsville al new construction",
        "huntsville al apartments", "huntsville al rent", "huntsville al average home price",
        "madison al homes for sale", "athens al homes for sale", "huntsville al housing market",
        "huntsville al best neighborhoods", "best places to live in huntsville al",
        "where to live in huntsville", "safest neighborhoods in huntsville",
        # schools
        "huntsville al schools", "huntsville city schools", "madison city schools",
        "best school districts in huntsville al", "huntsville al school ratings",
        "huntsville al school zones", "madison county schools alabama", "limestone county schools",
        # commute / jobs / employers
        "huntsville al commute", "redstone arsenal commute", "commute to redstone arsenal",
        "huntsville al jobs", "huntsville al employers", "cummings research park",
        "nasa marshall space flight center", "mazda toyota huntsville jobs",
        # military / PCS
        "pcs to redstone arsenal", "redstone arsenal housing", "redstone arsenal bah",
        "huntsville va loan", "huntsville al military relocation", "redstone arsenal off post housing",
        # money
        "huntsville al property tax", "madison county property tax", "alabama property tax rate",
        "huntsville al mortgage", "huntsville al mortgage rates", "huntsville al first time home buyer",
        "huntsville al pre qualification", "rent vs buy huntsville", "huntsville al closing costs",
        "alabama first time home buyer program", "huntsville al down payment assistance",
        # paperwork / admin
        "huntsville al utilities", "huntsville utilities setup", "huntsville al water bill",
        "huntsville al internet providers", "alabama vehicle registration", "huntsville al tag office",
        "alabama drivers license transfer", "huntsville al trash pickup",
        # insurance / services
        "huntsville al home insurance", "huntsville al car insurance",
        "huntsville al realtors", "best realtors in huntsville al",
        # comparisons
        "huntsville vs madison al", "huntsville vs nashville", "huntsville vs birmingham",
        "madison al vs huntsville al", "athens al vs madison al", "living in madison al",
        # communities (site already has 36)
        "living in", "moving to", "homes for sale in",
    ]
    seeds += ["moving to " + n.lower() for n in names]
    seeds += ["living in " + n.lower() for n in names]
    # alphabet expansion on the core heads -> long tail
    for head in ["moving to huntsville", "huntsville al", "living in huntsville"]:
        seeds += [head + " " + c for c in "abcdefghijklmnopqrstuvwxyz"]
    seeds += ["huntsville al " + w for w in
              ["schools", "homes", "apartments", "rent", "jobs", "weather", "crime", "taxes",
               "utilities", "traffic", "neighborhoods", "insurance", "mortgage", "realtors"]]
    seen, out = set(), []
    for s in seeds:
        s = s.strip()
        if s and s not in seen:
            seen.add(s)
            out.append(s)
    return out


def main():
    seeds = build_seeds()
    jobs = []
    for s in seeds:
        jobs += [(s, google), (s, bing)]
    for s in seeds[:0]:
        jobs += [(s, ddg)]
    results, raw = {}, []
    with ThreadPoolExecutor(max_workers=10) as ex:
        futs = {ex.submit(fn, s): (s, fn.__name__) for s, fn in jobs}
        for f in futs:
            pass
        for f, (s, name) in futs.items():
            try:
                rows = f.result()
            except Exception as e:  # noqa: BLE001
                rows = [("__ERR__ " + repr(e), 0)]
            raw.append({"seed": s, "endpoint": name, "suggestions": [r[0] for r in rows]})
            d = results.setdefault(s, {})
            i = 0
            for kw, src in rows:
                if src:
                    i += 1
                    prev = d.get(kw)
                    # rank: earlier position on the page is a stronger demand signal
                    if prev is None or i < prev["rank"]:
                        d[kw] = {"rank": i, "endpoints": sorted(set((prev or {}).get("endpoints", []) + [name]))}
                elif not kw.startswith("__ERR__"):
                    pass
    flat = []
    for s, kws in results.items():
        for kw, meta in kws.items():
            flat.append({"keyword": kw, "seed": s, "best_rank": meta["rank"],
                         "endpoints": meta["endpoints"]})
    json.dump(raw, open(os.path.join(HERE, "kw_raw.json"), "w"), indent=1)
    json.dump(flat, open(os.path.join(HERE, "kw_suggestions.json"), "w"), indent=1)
    errs = sum(1 for r in raw for x in r["suggestions"] if x.startswith("__ERR__"))
    print(f"seeds={len(seeds)} requests={len(jobs)} unique_keywords={len(flat)} errors={errs}")
    # quick look at the core head
    core = [r for r in flat if r["seed"] == "moving to huntsville"]
    for r in sorted(core, key=lambda x: x["best_rank"])[:25]:
        print(f"  {r['best_rank']:>2} {r['keyword']}")


if __name__ == "__main__":
    t = time.time()
    main()
    print(f"elapsed {time.time()-t:.1f}s")

#!/usr/bin/env python3
"""RDAP availability probe for candidate names built from the top keyword clusters.

Registry check, not DNS: RDAP 404 means the name is not registered. 200 means taken.
"""
import concurrent.futures as cf
import json
import re
import urllib.request

RDAP = {
    "com": "https://rdap.verisign.com/com/v1/domain/",
    "net": "https://rdap.verisign.com/net/v1/domain/",
    "org": "https://rdap.publicinterestregistry.org/rdap/domain/",
}
UA = {"User-Agent": "curl/8.5.0", "Accept": "application/rdap+json"}

# candidate, the keyword cluster it maps to
CANDIDATES = {
    "com": [
        ("huntsvillemove.com", "moving to huntsville"),
        ("huntsvillemoves.com", "moving to huntsville"),
        ("movetohuntsville.com", "moving to huntsville al"),
        ("movetohsv.com", "moving to huntsville (short)"),
        ("huntsvilleliving.com", "living in huntsville"),
        ("huntsvillelife.com", "living in huntsville"),
        ("livhuntsville.com", "living in huntsville"),
        ("hsvliving.com", "living in huntsville (short)"),
        ("newtohuntsville.com", "new to huntsville"),
        ("huntsvilleguide.com", "huntsville relocation guide"),
        ("huntsvillehomes.com", "huntsville al homes for sale"),
        ("hsvhomes.com", "huntsville homes (short)"),
        ("huntsvillepcs.com", "pcs redstone arsenal"),
        ("pcsredstone.com", "pcs redstone arsenal"),
        ("redstonehomes.com", "redstone arsenal housing"),
        ("rocketcitymove.com", "current site name"),
        ("rocketcityhomes.com", "huntsville homes"),
        ("huntsvillemortgage.com", "huntsville al mortgage"),
        ("hsvmortgage.com", "huntsville mortgage (short)"),
        ("huntsvilleal.com", "huntsville al"),
        ("huntsvillealhomes.com", "huntsville al homes for sale"),
        ("huntsvilleareahomes.com", "huntsville area homes"),
        ("huntsvillepcsguide.com", "pcs redstone arsenal"),
        ("huntsvilleschools.com", "huntsville al schools"),
        ("huntsvillecommute.com", "huntsville al commute"),
        ("huntsvilleutilities.com", "huntsville al utilities"),
        ("huntsvilleneighborhoods.com", "where to live in huntsville"),
        ("movetohuntsvilleal.com", "moving to huntsville al"),
        ("huntsvillerelocation.com", "huntsville relocation"),
        ("livinginhuntsville.com", "living in huntsville"),
    ],
    "org": [
        ("movingtohuntsville.org", "moving to huntsville (exact-match redirect)"),
        ("movetohuntsville.org", "moving to huntsville (exact-match redirect)"),
        ("huntsvillepcs.org", "pcs redstone arsenal"),
    ],
    "net": [
        ("movetohuntsville.net", "moving to huntsville (exact-match redirect)"),
    ],
}


def check(tld, name):
    url = RDAP[tld] + name
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=25):
            return name, "taken", ""
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return name, "AVAILABLE", ""
        if e.code == 429:
            return name, "rate-limited", ""
        return name, f"http {e.code}", ""
    except Exception as e:  # noqa: BLE001
        return name, f"err {type(e).__name__}", ""


def main():
    rows = []
    jobs = [(tld, n, note) for tld, items in CANDIDATES.items() for n, note in items]
    with cf.ThreadPoolExecutor(6) as ex:
        futs = {ex.submit(check, tld, n): (tld, n, note) for tld, n, note in jobs}
        for f, (tld, n, note) in futs.items():
            name, status, _ = f.result()
            rows.append({"domain": name, "tld": tld, "status": status, "keyword": note,
                         "length": len(n) - len(tld) - 1})
    rows.sort(key=lambda r: (r["status"] != "AVAILABLE", r["length"]))
    json.dump(rows, open("domain_probe.json", "w"), indent=1)
    for r in rows:
        mark = "AVAILABLE" if r["status"] == "AVAILABLE" else r["status"]
        print(f"{mark:<12} {r['domain']:<32} {r['length']:>2} ch  <- {r['keyword']}")
    avail = [r for r in rows if r["status"] == "AVAILABLE"]
    print(f"\n{len(avail)} of {len(rows)} available")


if __name__ == "__main__":
    main()

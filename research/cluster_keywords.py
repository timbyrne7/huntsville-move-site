#!/usr/bin/env python3
"""Cluster the harvested suggestions into intent groups, with a demand proxy.

Demand proxy (stated honestly, no invented volumes):
  score = 2 * (number of distinct seeds that surfaced the query)
        + (11 - best autocomplete rank across those seeds)
A query that shows up for many seeds near the top of the suggest box has real
search behaviour behind it; a query that appears once at rank 9 does not.
"""
import json
import os
import re
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))

# --- noise filters -----------------------------------------------------------
BAD_CITY = re.compile(
    r"\b(huntsville (tx|texas|ontario|on|utah|ut|north carolina|nc|georgia|ga|tennessee|tn|"
    r"arkansas|ar|missouri|mo|ohio|illinois|indiana|kentucky|mississippi|west virginia)|"
    r"(huntsville, tx|huntsville, on|huntsville, ut))\b")
BAD_TOPIC = re.compile(
    r"\b(moving compan(y|ies)|movers|packing|storage units|u haul|uhaul|car shipping|"
    r"jobs hiring|salary|weather radar|obituaries|weather forecast|zip code|area code|"
    r"time zone|real estate agents? near me|apartments? for rent near me|"
    r"movie theater|restaurants near|things to do this weekend|event calendar|"
    r"police department|sheriff|arrests|mugshots|traffic ticket|"
    r"university|college|tuition|football|basketball|hockey|soccer|"
    r"spacex|blue origin|fbi|nasa|ussf|spacecom|army|government contract)\b")
KEEP_EXCEPTIONS = re.compile(r"\b(redstone arsenal|space ?force|missile defense|nasa marshall|"
                             r"cummings research park|mazda toyota|bryce|tokyo|"


                             r"sandwich)\b")

# --- relevance gate: the query must be about THIS Huntsville -----------------
LOCAL = re.compile(r"(huntsville|redstone|madison county|madison city|madison, al|"
                   r"limestone county|morgan county|rocket city|tennessee valley|"
                   r"\balabama\b|\bal\b|hsv|"
                   r"hazel green|meridianville|harvest|monrovia|toney|gurley|brownsboro|"
                   r"owens cross roads|hampton cove|big cove|new hope|triana|capshaw|ardmore|"
                   r"elkmont|tanner|athens|decatur|hartselle|priceville|trinity|somerville|"
                   r"ryland|green mountain|five points|blossomwood|twickenham|providence|"
                   r"monte sano|lake guntersville|guntersville|arab|scottsboro|"
                   r"nashville|chattanooga|lake guntersville)")
# other cities/states that share a name or leak in from unrelated seeds
OTHER_PLACE = re.compile(r"\b(huntersville|north carolina|nc\b|wisconsin|wi\b|ontario|"
                         r"texas|tx\b|utah|massachusetts|tenerife|trinidad|hartlepool|"
                         r"summerville|sc\b|georgia\b|florida|fl\b|california|ca\b|"
                         r"new york|ny\b|ohio|michigan|pennsylvania|virginia|colorado|"
                         r"arizona|oregon|washington|illinois|indiana|iowa|kansas|kentucky|"
                         r"louisiana|maine|maryland|minnesota|mississippi|missouri|montana|"
                         r"nebraska|nevada|new hampshire|new jersey|new mexico|north dakota|"
                         r"oklahoma|rhode island|south carolina|south dakota|tennessee|vt|"
                         r"vermont|west virginia|wyoming|alaska|hawaii|idaho|delaware|"
                         r"connecticut|arkansas|phoenix|denver|seattle|boston|chicago|"
                         r"atlanta|dallas|houston|austin|nashville|chattanooga|memphis|"
                         r"birmingham|mobile|montgomery|tuscaloosa|auburn|tampa|orlando|"
                         r"miami|jacksonville|charlotte|raleigh|richmond|baltimore|detroit|"
                         r"cleveland|cincinnati|columbus|indianapolis|milwaukee|minneapolis|"
                         r"st\.? louis|kansas city|omaha|salt lake|portland|sacramento|"
                         r"san diego|los angeles|san francisco|san jose|las vegas|albuquerque|"
                         r"tucson|el paso|san antonio|fort worth|oklahoma city|louisville|"
                         r"lexington|knoxville|new orleans|norfolk|virginia beach|pittsburgh|"
                         r"philadelphia|buffalo|rochester)\b")
# non-location noise that leaks in from generic seeds
NON_LOCAL = re.compile(r"\b(kusco|kuwana|gujarat|pakistan|philippines|ethiopia|"
                       r"tenerife|trinidad|hartlepool)\b")

CLUSTERS = [
    ("relocation-guide", r"\b(moving to huntsville|relocating|relocat|moving (out )?(to|from)|"
                         r"new to huntsville|just moved|newcomer|moving to alabama)"),
    ("cost-of-living", r"\b(cost of living|cost of|expenses|salary needed|how much|price of living|"
                       r"expensive|cheaper|utilities cost|groceries|wage)"),
    ("housing-market", r"\b(home price|house price|home value|housing market|median|average home|"
                       r"new construction|new build|home prices|market)"),
    ("homes-for-sale", r"\b(homes? for sale|houses? for sale|listing|real estate|mls|"
                       r"homes under|condos?|townhome|land for sale|lot)"),
    ("neighborhoods", r"\b(neighborhood|where to live|best place|areas? to live|safest|"
                      r"suburb|downtown|five points|blossomwood|hampton cove|big cove|"
                      r"monte sano|gurley|harvest|meridianville|owens cross|madison|"
                      r"athens|decatur|hampton|twickenham|providence|research park)"),
    ("schools", r"\b(school|district|education|elementary|middle|high school|k-12|academy|"
                r"homeschool|private school|pta)"),
    ("commute", r"\b(commute|drive|traffic|how far|miles from|drive time|i-?565|highway|"
                r"rush hour|parking|distance from)"),
    ("jobs-employers", r"\b(jobs?|careers?|employ|hiring|work (at|for)|research park|"
                       r"mazda toyota|redstone|arsenal|marshall|contractor|transition)"),
    ("military-pcs", r"\b(military|pcs|bah|va loan|va |veteran|off post|on post|redstone arsenal|"
                     r"space force|base housing|relocation orders)"),
    ("buying-process", r"\b(pre ?qualif|pre ?approv|mortgage|loan|buy(ing)? a (house|home)|"
                       r"first time|closing cost|down payment|credit score|interest rate|"
                       r"earnest money|escrow|inspection|appraisal|agent|realtor|offer)"),
    ("rent-vs-buy", r"\b(rent vs|rent or buy|renting|rent |rental|apartment|lease)"),
    ("taxes", r"\b(property tax|tax rate|taxes|assess|homestead|sales tax|income tax|millage)"),
    ("utilities-setup", r"\b(utilit|electric|power|water|sewer|gas|internet|cable|fiber|"
                        r"trash|garbage|recycl|solar)"),
    ("admin-paperwork", r"\b(vehicle registration|register (my )?car|tag|title|driver|licen[cs]e|"
                        r"voter|dmv|real id|car emission|plate|notary|homestead exemption)"),
    ("insurance", r"\b(insur|homeowners|flood|wind|hail|auto insurance|premium)"),
    ("comparisons", r"\b(vs\.? |versus|compare|compared to|better than|instead of)"),
    ("lifestyle", r"\b(weather|climate|humidity|tornado|severe|hot|summer|winter|snow|"
                  r"crime|safe|safety|diverse|nightlife|outdoor|hiking|lake|huntsville known for|"
                  r"fun|boring|church|healthcare|hospital|dog|pet|humidity)"),
]


def cluster_of(kw):
    # ordered match: first cluster whose regex hits, but score by specificity
    hits = [name for name, pat in CLUSTERS if re.search(pat, kw)]
    return hits


def main():
    rows = json.load(open(os.path.join(HERE, "kw_suggestions.json")))
    by_kw = defaultdict(lambda: {"seeds": set(), "best_rank": 99, "endpoints": set()})
    for r in rows:
        kw = r["keyword"].lower().strip()
        if kw.startswith("__err__"):
            continue
        e = by_kw[kw]
        e["seeds"].add(r["seed"])
        e["best_rank"] = min(e["best_rank"], r["best_rank"])
        e["endpoints"].update(r["endpoints"])

    kept, dropped = [], []
    for kw, e in by_kw.items():
        score = 2 * len(e["seeds"]) + (11 - e["best_rank"])
        row = {"keyword": kw, "seeds": len(e["seeds"]), "best_rank": e["best_rank"],
               "endpoints": sorted(e["endpoints"]), "score": score}
        if BAD_CITY.search(kw) or (BAD_TOPIC.search(kw) and not KEEP_EXCEPTIONS.search(kw)):
            dropped.append(row)
        elif not LOCAL.search(kw) or OTHER_PLACE.search(kw) or NON_LOCAL.search(kw):
            dropped.append(row)
        else:
            kept.append(row)

    grouped = defaultdict(list)
    for r in kept:
        cl = cluster_of(r["keyword"])
        if not cl:
            grouped["uncategorised"].append(r)
        else:
            for c in cl:
                grouped[c].append(r)

    out = {}
    for name, items in sorted(grouped.items(), key=lambda x: -len(x[1])):
        items.sort(key=lambda x: -x["score"])
        out[name] = items
    json.dump({"kept": len(kept), "dropped": len(dropped), "clusters": out},
              open(os.path.join(HERE, "kw_clustered.json"), "w"), indent=1)

    print(f"kept={len(kept)} dropped={len(dropped)} clusters={len(out)}\n")
    for name, items in sorted(out.items(), key=lambda x: -len(x[1])):
        print(f"=== {name}  ({len(items)} kws)")
        for r in items[:18]:
            print(f"   {r['score']:>4}  seeds={r['seeds']:>2} rank={r['best_rank']:>2}  {r['keyword']}")
        print()
    print("--- sample of dropped ---")
    for r in dropped[:15]:
        print("   ", r["keyword"])


if __name__ == "__main__":
    main()

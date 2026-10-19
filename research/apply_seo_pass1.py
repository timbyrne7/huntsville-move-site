#!/usr/bin/env python3
"""Keyword application pass 1 — titles, meta descriptions and H1s.

Every pair is an exact match against the file; if a string is missing or appears
more than once the script fails loudly rather than silently skipping a page.
"""
import io
import os
import sys

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (file, old, new, note)
EDITS = [
    # ---------------- homepage: head term "moving to Huntsville AL" ----------
    ("index.html",
     "<title>Moving to Huntsville, AL — schools, commute, cost of living and home search</title>",
     "<title>Moving to Huntsville, AL — guide, schools, commute, cost of living</title>",
     "title: keep head term first, drop the weakest modifier"),
    ("index.html",
     '<meta name="description" content="A Huntsville relocation guide built on real data: school comparisons, a live commute calculator, your city to Huntsville cost comparison, rent-vs-buy with BAH, and an address-specific moving checklist.">',
     '<meta name="description" content="Moving to Huntsville, Alabama? What living here is actually like: cost of living against your city, school districts, measured commute times, where to live, utilities and the paperwork — all on sourced data.">',
     "description: adds living-in-Huntsville + before-you-move phrasing"),

    # ---------------- moving guide: primary relocation-guide page -----------
    ("moving-to-huntsville.html",
     "<title>Moving to Huntsville, AL — the complete guide for 2026</title>",
     "<title>Moving to Huntsville, Alabama: the complete relocation guide</title>",
     "title: full state name (how the query is typed) not the abbreviation"),
    ("moving-to-huntsville.html",
     '<meta name="description" content="Everything a mover to Huntsville, Alabama actually needs: employers and gates, school districts, where to live, commute realities, cost of living, utilities, tags and licensing, and the timeline.">',
     '<meta name="description" content="What to know before moving to Huntsville, Alabama: employers and gates, school districts, where to live, commute realities, cost of living, utilities, tags and licences, and a timeline that works.">',
     "description: leads with the actual pre-move query"),
    ("moving-to-huntsville.html",
     "  <h1>Moving to Huntsville: the guide we'd want</h1>",
     "  <h1>Moving to Huntsville, Alabama — the guide we'd want</h1>",
     "h1: state name in the heading"),

    # ---------------- neighborhoods: "where to live / best areas" -----------
    ("neighborhoods.html",
     "<title>Huntsville-area communities — Madison, Limestone and Morgan counties</title>",
     "<title>Where to live in Huntsville, AL — 36 areas and suburbs compared</title>",
     "title: targets the where-to-live query cluster"),
    ("neighborhoods.html",
     '<meta name="description" content="Thirty-six communities across Madison, Limestone and Morgan counties: the school district that applies, who each one suits, the trade-off nobody mentions, and live commute times to your workplace.">',
     '<meta name="description" content="Best areas to live in Huntsville, Alabama: 36 communities across Madison, Limestone and Morgan counties — the school district that applies, who each suits, the trade-off, and live commute times. Includes Huntsville vs Madison vs Athens.">',
     "description: best-areas phrasing + comparison hook"),
    ("neighborhoods.html",
     "  <h1>Where people actually land</h1>",
     "  <h1>Where to live in Huntsville, AL</h1>",
     "h1: keyword-leading heading (old line kept as a section heading below)"),

    # ---------------- schools -----------------------------------------------
    ("schools.html",
     "<title>School districts around Huntsville — Huntsville, Madison, Limestone and Morgan counties compared</title>",
     "<title>Schools in Huntsville, AL: districts, zones and how to check yours</title>",
     "title: leads with the head term"),
    ("schools.html",
     '<meta name="description" content="Eight public school systems across Madison, Limestone and Morgan counties compared for movers: what each covers, how zones ignore mailing addresses, how to check your exact parcel, and where the real test-score data lives.">',
     '<meta name="description" content="Best school districts near Huntsville, Alabama — Huntsville City vs Madison City vs Madison County and five more systems: what each covers, how zones ignore mailing addresses, and how to check your exact parcel in five minutes.">',
     "description: best-district phrasing + the comparison people search"),
    ("schools.html",
     "  <h1>School comparison: eight systems, three counties</h1>",
     "  <h1>Schools in Huntsville, AL: eight systems, three counties</h1>",
     "h1: head term in the heading"),

    # ---------------- commute ------------------------------------------------
    ("commute.html",
     "<title>Huntsville commute calculator — Redstone, MSFC, Research Park, Mazda Toyota</title>",
     "<title>Huntsville commute calculator — drive times to Redstone Arsenal</title>",
     "title: 'drive times' is the typed phrasing; keeps the employer list in the description"),
    ("commute.html",
     '<meta name="description" content="Measure real driving routes from every Huntsville-area neighborhood to Redstone Arsenal gates, NASA Marshall, Cummings Research Park and Mazda Toyota. Peak-hour estimates and the annual cost of the drive.">',
     '<meta name="description" content="Measure real driving routes from 36 Huntsville-area neighborhoods to Redstone Arsenal gates, NASA Marshall, Cummings Research Park and Mazda Toyota — off-peak minutes, peak-hour ranges and the annual cost of the drive.">',
     "description: adds the count + peak/off-peak framing"),
    ("commute.html",
     "  <h1>Commute calculator</h1>",
     "  <h1>Huntsville commute calculator</h1>",
     "h1: head term in the heading"),

    # ---------------- cost of living ----------------------------------------
    ("cost-of-living.html",
     "<title>Your city → Huntsville: rent, home prices, income and property tax compared</title>",
     "<title>Cost of living in Huntsville, AL: rent, home prices and property tax</title>",
     "title: the head term instead of the brand metaphor"),
    ("cost-of-living.html",
     '<meta name="description" content="Compare 57 US metros against Huntsville, Alabama on median rent, median home value, household income and property tax paid — with an estimated house payment for each.">',
     '<meta name="description" content="Cost of living in Huntsville, Alabama compared with your city: median rent, home prices, household income and property tax (median $1,405 a year), plus an estimated house payment for all 57 metros.">',
     "description: head term + one verifiable figure"),
    ("cost-of-living.html",
     "  <h1>Your city → Huntsville</h1>",
     "  <h1>Cost of living in Huntsville, AL — compared with your city</h1>",
     "h1: head term in the heading (tool keeps its own title inside the page)"),

    # ---------------- checklist / utilities ---------------------------------
    ("checklist.html",
     "<title>Address-specific moving checklist — Huntsville, Madison & Madison County</title>",
     "<title>Huntsville utilities &amp; moving checklist: power, water, tags</title>",
     "title: 'utilities' is the bigger cluster; ampersand entity is valid in <title>"),
    ("checklist.html",
     '<meta name="description" content="Generate a moving checklist for your exact Huntsville-area address: utility providers, county tag and title office, driver licence, voter registration, school enrollment documents, trash day and pet licensing.">',
     '<meta name="description" content="Set up utilities in Huntsville, Alabama and get the rest of the moving checklist sorted for your exact address: Huntsville Utilities, internet providers, trash day, county tag and title office, driver licence and school enrollment.">',
     "description: leads with the utilities query people type"),
    ("checklist.html",
     "  <h1>The address-specific moving checklist</h1>",
     "  <h1>Huntsville utilities and the address-specific moving checklist</h1>",
     "h1: adds the utilities head term"),

    # ---------------- home search -------------------------------------------
    ("home-search.html",
     "<title>Search homes for sale in Huntsville, Madison & Madison County</title>",
     "<title>Homes for sale in Huntsville, AL — search ValleyMLS listings</title>",
     "title: 'homes for sale' phrasing"),
    ("home-search.html",
     '<meta name="description" content="Search live Huntsville-area listings on ValleyMLS, set up price alerts for the neighborhoods you\'re watching, and get the payment math for anything you like.">',
     '<meta name="description" content="Search homes for sale in Huntsville, Madison and Madison County on ValleyMLS — the local MLS — set up price alerts for the areas you are watching, and get the payment math for anything you like.">',
     "description: homes-for-sale phrasings"),
    ("home-search.html",
     "  <h1>Home search</h1>",
     "  <h1>Search homes for sale in Huntsville, AL</h1>",
     "h1: head term in the heading"),

    # ---------------- pre-qualification -------------------------------------
    ("prequal.html",
     "<title>Get pre-qualified for a Huntsville mortgage</title>",
     "<title>Huntsville mortgage pre-qualification: VA, FHA, first-time buyers</title>",
     "title: loan types + first-time-buyer cluster"),
    ("prequal.html",
     '<meta name="description" content="Start a pre-qualification for a home purchase in Huntsville, Madison or Madison County — conventional, FHA or VA.">',
     '<meta name="description" content="Start a mortgage pre-qualification for a home in Huntsville, Madison or Madison County: conventional, FHA or VA, what first-time buyer programmes exist in Alabama, and the numbers that change your payment here.">',
     "description: covers the down-payment-assistance cluster"),
    ("prequal.html",
     "  <h1>Get pre-qualified</h1>",
     "  <h1>Get pre-qualified in Huntsville, Alabama</h1>",
     "h1: location in the heading"),

    # ---------------- rent vs buy ------------------------------------------
    ("rent-vs-buy.html",
     "<title>Rent vs buy in Huntsville + BAH calculator</title>",
     "<title>Rent vs buy in Huntsville, AL — and what your BAH covers</title>",
     "title: head term kept, BAH query covered"),
    ("rent-vs-buy.html",
     "  <h1>Rent vs buy — and what your BAH actually covers</h1>",
     "  <h1>Rent vs buy in Huntsville — and what your BAH actually covers</h1>",
     "h1: location in the heading"),

    # ---------------- realtors --------------------------------------------
    ("local-realtors.html",
     "<title>Local realtors in Huntsville — how to choose one, and what to ask</title>",
     "<title>Realtors in Huntsville, AL — how to choose one and what to ask</title>",
     "title: how the query is typed ('realtors in huntsville al')"),
    ("local-realtors.html",
     "  <h1>Choosing a real estate agent here</h1>",
     "  <h1>Choosing a real estate agent in Huntsville, AL</h1>",
     "h1: location in the heading"),

    # ---------------- insurance ------------------------------------------
    ("local-insurance.html",
     "<title>Home and auto insurance in Huntsville — what movers should expect</title>",
     "<title>Home insurance in Huntsville, AL — wind, hail and what to ask</title>",
     "title: homeowners-insurance query first"),
    ("local-insurance.html",
     "  <h1>Insurance, honestly explained</h1>",
     "  <h1>Home and auto insurance in Huntsville, honestly explained</h1>",
     "h1: head term in the heading"),
]


def main():
    failures = []
    applied = 0
    for fname, old, new, note in EDITS:
        path = os.path.join(SITE, fname)
        with io.open(path, encoding="utf-8") as fh:
            s = fh.read()
        n = s.count(old)
        if n != 1:
            failures.append(f"{fname}: {n} matches for {old[:70]!r} — {note}")
            continue
        with io.open(path, "w", encoding="utf-8") as fh:
            fh.write(s.replace(old, new, 1))
        applied += 1
    print(f"applied {applied}/{len(EDITS)} edits")
    if failures:
        print("FAILURES:")
        for f in failures:
            print("  -", f)
        sys.exit(1)
    print("all pairs matched exactly once")


if __name__ == "__main__":
    main()

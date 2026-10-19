#!/usr/bin/env python3
"""Keyword application pass 2 — question/answer blocks and internal links.

These blocks answer the question-shaped queries that real autocomplete data shows
people typing before they move. Every figure used is either already published on
this site (US Census ACS 2024 1-year medians), measured live on the road network
(OSRM) during this build, or read from an official source linked inline. Nothing
here is invented, and no search volume is claimed anywhere.
"""
import io
import os
import sys

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANCHOR = '<div id="site-footer"></div>'
A = 'target="_blank" rel="noopener"'

# effective property-tax rate implied by the ACS medians already on the site
EFF_TAX = round(1405 / 331800 * 100, 2)   # 0.42

BLOCKS = {}

BLOCKS["index.html"] = f"""
<section class="tight"><div class="wrap">
  <h2>The questions people ask before they move here</h2>
  <div class="grid g2">
    <div class="card">
      <h3>Is Huntsville, Alabama a good place to live?</h3>
      <p class="small">It depends on three things: whether your work is in the defence, space and engineering ecosystem, whether you need a specific school district, and whether a humid Southern summer and a car-dependent city suit you. We wrote the long version, including who should not move here.</p>
      <p class="small"><a class="btn btn-line" href="is-huntsville-a-good-place-to-live.html">The honest pros and cons</a></p>
    </div>
    <div class="card">
      <h3>Where do most people live in Huntsville?</h3>
      <p class="small">The west side — Madison, Harvest, Monrovia, Meridianville — for arsenal and Research Park jobs, because that is where the drive is shortest. The east and south — Five Points, Blossomwood, Hampton Cove, Owens Cross Roads — for downtown access, the hospital and more land.</p>
      <p class="small"><a class="btn btn-line" href="neighborhoods.html">Compare 36 areas</a></p>
    </div>
    <div class="card">
      <h3>What should I do first?</h3>
      <p class="small">Run three numbers before you look at houses: the commute from the areas you are considering, the cost comparison against where you live now, and the rent-vs-buy model at your price. Then check the school zone for any specific address — the parcel decides the district, not the mailing address.</p>
      <p class="small"><a class="btn btn-line" href="moving-to-huntsville.html">Read the moving guide</a></p>
    </div>
    <div class="card">
      <h3>Is Huntsville cheaper than where I live now?</h3>
      <p class="small">Usually on house prices and property tax — the median mortgaged household here pays about $1,405 a year in property tax. One caveat in the other direction: Alabama levies a state income tax, so movers from Tennessee, Texas, Florida or Washington take home less per dollar of salary.</p>
      <p class="small"><a class="btn btn-line" href="cost-of-living.html">Compare your city</a></p>
    </div>
  </div>
  <p style="margin-top:14px"><a class="btn btn-ghost" href="redstone-arsenal-pcs-va-loans.html">Moving on military orders? Start with the PCS page</a></p>
</div></section>

"""

BLOCKS["moving-to-huntsville.html"] = """
<section class="tight"><div class="wrap">
  <h2>What people ask us before the move</h2>
  <div class="grid g2">
    <div class="card">
      <h3>What are the downsides of moving to Huntsville?</h3>
      <p class="small">Humid summers, spring severe-weather season and the insurance it drives, a road network still catching up with growth, and a school-zone system that ignores mailing addresses. None of those are deal-breakers; all of them are surprises if nobody tells you first.</p>
      <p class="small"><a class="btn btn-line" href="is-huntsville-a-good-place-to-live.html">The honest pros and cons</a></p>
    </div>
    <div class="card">
      <h3>Is Huntsville a good place to raise a family?</h3>
      <p class="small">The school choice is real — eight public systems across three counties — but the district follows the parcel, so families who verify before they buy tend to be happy and families who assume tend to be surprised. Commute length is the second deciding factor.</p>
      <p class="small"><a class="btn btn-line" href="schools.html">Compare the districts</a></p>
    </div>
    <div class="card">
      <h3>What moving costs surprise people here?</h3>
      <p class="small">Vehicle title and tag work is a county office rather than a state one. Utilities split by jurisdiction — inside Huntsville city limits one account covers electric, water, sewer and gas, while county addresses often mean a private trash hauler and sometimes a well. And insurance starts on possession day, not on move-in day.</p>
      <p class="small"><a class="btn btn-line" href="checklist.html">Build the address-specific checklist</a></p>
    </div>
    <div class="card">
      <h3>When is the best time of year to move to Huntsville?</h3>
      <p class="small">The honest answer is that two deadlines matter more than the calendar: the school-year enrollment window if you have children, and your lease or possession date. Summer heat and humidity make July moves physically harder; that is a comfort argument, not a scheduling one.</p>
    </div>
  </div>
</div></section>

"""

BLOCKS["neighborhoods.html"] = """
<section><div class="wrap">
  <h2>Huntsville vs Madison vs Athens — the choice most movers actually face</h2>
  <div class="grid g3">
    <div class="card">
      <h3>Huntsville (city)</h3>
      <p class="small">The largest choice, and the least uniform: historic streets in Five Points and Blossomwood, downtown growth around Big Spring Park, and southern communities like Jones Valley. Served by <b>Huntsville City Schools</b>, which also covers Hampton Cove, Big Cove and Green Mountain.</p>
      <p class="small"><b>Best if:</b> you want in-city access, the medical district or downtown, and you are happy to check each neighbourhood street by street.</p>
    </div>
    <div class="card">
      <h3>Madison (city)</h3>
      <p class="small">A separate city with its own school system — <b>Madison City Schools</b>, eight elementary schools, three middle and two high — which is a different district from Madison County Schools, the distinction that trips up most movers. Closest west-side option to Cummings Research Park and the Gate 9 corridor.</p>
      <p class="small"><b>Best if:</b> the west-side commute decides it and the district matters. Note its zone page shows part of Limestone County inside the district.</p>
    </div>
    <div class="card">
      <h3>Athens (Limestone County)</h3>
      <p class="small">Its own city, its own school system and its own municipal utility — unlike unincorporated Limestone County, which is served by Limestone County Schools and address-specific water. Further west again, so the drive to Redstone lengthens and the price per square foot usually improves.</p>
      <p class="small"><b>Best if:</b> you want newer or larger housing for the money and work west of town. Measure the drive on the <a href="commute.html">commute calculator</a> before you commit.</p>
    </div>
  </div>
  <div class="note"><b>How to settle it in one evening:</b> set your real workplace on the <a href="commute.html">commute calculator</a>, tick one candidate in each of the three, and compare the drive times. Then check the school zone for the specific addresses you like. Those two checks remove almost all of the second-guessing.</div>
</div></section>

<section class="tight"><div class="wrap">
  <h2>Where-to-live questions, answered honestly</h2>
  <div class="grid g2">
    <div class="card">
      <h3>Which area is best for families?</h3>
      <p class="small">There is no single answer, and any site that gives you one is selling something. What is true: Madison City and Madison County serve the largest share of new-build family housing; Hampton Cove and Owens Cross Roads give more house and land for the money if you accept the mountain-gap drive; Five Points and Blossomwood are the in-city choice with older housing stock.</p>
    </div>
    <div class="card">
      <h3>Which areas are closest to Redstone Arsenal?</h3>
      <p class="small">By measured drive time to Gate 9 on Rideout Road: Madison at 6.8 miles / 11.6 minutes off-peak and downtown Huntsville at 7.5 miles / 10.5 minutes. Harvest runs 14.8 miles / 19.6 minutes, Meridianville 16.1 / 21.4, Hampton Cove 14.3 / 22.9 and Owens Cross Roads 20.7 / 31.1.</p>
      <p class="small"><a class="btn btn-line" href="redstone-arsenal-pcs-va-loans.html">PCS housing page</a></p>
    </div>
    <div class="card">
      <h3>Is Madison, Alabama a good place to live?</h3>
      <p class="small">If your job is on the west side, it is usually the first shortlist entry: the shortest measured drive to Gate 9, its own school system, and the highest concentration of new construction. The trade-offs are price per square foot and school capacity in fast-growing grade bands.</p>
    </div>
    <div class="card">
      <h3>What is the safest area?</h3>
      <p class="small">We do not publish "safest neighbourhood" lists, because a city-wide or area-wide number does not describe the street you would live on. Ask about the specific block, look at the local data, and drive it after dark — that is the check that actually predicts your experience.</p>
    </div>
  </div>
</div></section>

"""

BLOCKS["schools.html"] = """
<section class="tight"><div class="wrap">
  <h2>School questions we get asked</h2>
  <div class="grid g2">
    <div class="card">
      <h3>What is the best school district near Huntsville, Alabama?</h3>
      <p class="small">There is no defensible single answer, so here is what can be verified: Madison City Schools runs 8 elementary, 3 middle and 2 high schools; Madison County Schools is the largest system by campus count on this side of the region at 20,500 students across 30 campuses; Huntsville City Schools is the largest system serving in-city neighbourhoods plus Hampton Cove, Big Cove and Green Mountain.</p>
      <p class="small">Compare specific schools on the <a href="https://www.statereportcard.alsde.edu/" %s>Alabama State Report Card</a> rather than a star rating.</p>
    </div>
    <div class="card">
      <h3>Huntsville City Schools vs Madison City Schools — what is the difference?</h3>
      <p class="small">They are separate systems serving different areas. Madison City covers the city limits plus the Town of Triana by agreement and part of Limestone County — a reported 27%% of its students live in the Limestone County areas of Madison. Huntsville City covers the city itself plus Hampton Cove, Big Cove and Green Mountain, where it does not run a bus route over the mountain.</p>
      <p class="small muted">Sources: Madison City Schools zone page; al.com reporting; Green Mountain Civic League.</p>
    </div>
    <div class="card">
      <h3>Does my mailing address tell me the district?</h3>
      <p class="small">No, and this is the single most common costly mistake movers make here. Hazel Green, New Hope and the Ryland/Central area are Madison County Schools communities even where the mailing address says Huntsville. Unincorporated addresses are county-district addresses by default.</p>
    </div>
    <div class="card">
      <h3>How do I look up my school zone?</h3>
      <p class="small">Use the <a href="https://www.maps.huntsvilleal.gov/myschoolsmap/" %s>Huntsville City locator</a> for city addresses, the <a href="https://madisoncity.k12.al.us/school-zones-2" %s>Madison City zone page</a> inside Madison, the <a href="https://www.mcssk12.org/our-schools/school-zones" %s>Madison County zone page</a> for unincorporated addresses, and the district site for Limestone, Athens City, Morgan, Decatur City and Hartselle City. Check all three grade bands before you commit.</p>
    </div>
  </div>
</div></section>

""" % (A, A, A, A)

BLOCKS["commute.html"] = """
<section class="tight"><div class="wrap">
  <h2>Commute questions, with the numbers</h2>
  <div class="grid g2">
    <div class="card">
      <h3>How long is the commute from Madison to Redstone Arsenal?</h3>
      <p class="small">About <b>6.8 miles and 11.6 minutes</b> off-peak to Gate 9 by live road-network routing. At the Gate 9 shift change, budget closer to 16 minutes — that corridor carries the heaviest peak factor in the metro.</p>
    </div>
    <div class="card">
      <h3>Where does traffic actually back up here?</h3>
      <p class="small">Four places, consistently: I-565 and Research Park Boulevard inbound, 431 through Meridianville, the mountain gap on 431 out of Hampton Cove, and Rideout Road at Gate 9 when a shift changes. Everywhere else, a Huntsville commute is shorter than a big-city commuter expects.</p>
    </div>
    <div class="card">
      <h3>How far is Huntsville from other cities?</h3>
      <p class="small">Measured off-peak on the road network: Birmingham 101 miles (~1 h 53), Chattanooga 102 miles (~2 h), Nashville 110 miles (~2 h 15), Atlanta 180 miles (~3 h 56) and Memphis 212 miles (~4 h 23). Distances are driving routes, not straight lines.</p>
    </div>
    <div class="card">
      <h3>Do I need to live near my gate?</h3>
      <p class="small">Not necessarily, but the arithmetic is stark at the extremes: the difference between an 11-minute and a 31-minute one-way drive is roughly 2.5 hours a week at five days, before fuel and before you count the days that run long. Value the time, then decide what it is worth per month.</p>
    </div>
  </div>
</div></section>

"""

BLOCKS["cost-of-living.html"] = f"""
<section class="tight"><div class="wrap">
  <h2>Cost-of-living questions, with sourced numbers</h2>
  <div class="grid g2">
    <div class="card">
      <h3>What is the cost of living in Huntsville, Alabama?</h3>
      <p class="small">The metro-level figures from the 2024 ACS 1-year estimates already on this page: median home value <b>$331,800</b>, median gross rent <b>$1,283</b> a month, median household income around <b>$87,000</b>, and median property tax of <b>$1,405</b> a year for mortgaged owner-occupied homes. Metro medians describe a market, not a specific house.</p>
    </div>
    <div class="card">
      <h3>How much are property taxes in Huntsville?</h3>
      <p class="small">Worked back from the ACS figures, the median household pays about <b>{EFF_TAX}% of home value</b> a year in property tax — among the lowest effective rates in the country. Your own figure is assessed per parcel, so it changes with the county and the assessment, not only the price.</p>
      <p class="small muted">Madison County's tax office publishes the parcel-level detail: <a href="https://www.madisoncountyal.gov/" {A}>madisoncountyal.gov</a></p>
    </div>
    <div class="card">
      <h3>Is rent expensive in Huntsville?</h3>
      <p class="small">Median gross rent of $1,283 makes the metro cheaper than most places movers come from. Within the market, new-build apartments in MidCity and west Madison sit above that median and older duplexes and county rentals sit below it — the spread is wide enough that location matters more than the city average.</p>
    </div>
    <div class="card">
      <h3>Where does the money difference actually come from?</h3>
      <p class="small">Two lines: property tax, where this metro is far below the metros movers arrive from, and house price per square foot. Against that, Alabama levies a state income tax — worth modelling if you are coming from Tennessee, Texas, Florida or Washington.</p>
    </div>
  </div>
</div></section>

"""

BLOCKS["rent-vs-buy.html"] = """
<section class="tight"><div class="wrap">
  <h2>Rent or buy — the questions behind the model</h2>
  <div class="grid g2">
    <div class="card">
      <h3>Is it better to rent or buy in Huntsville?</h3>
      <p class="small">It depends on how long you stay, not on the city. The model above computes your own break-even month — the point where buying beats renting once selling costs are counted. Short horizon, rent. Long horizon, buy, and the low Alabama property tax is a real part of why.</p>
    </div>
    <div class="card">
      <h3>Does BAH cover a mortgage in Huntsville?</h3>
      <p class="small">Frequently it covers the principal-and-interest portion, because home values here are low relative to typical BAH. Whether it covers your all-in payment depends on tax, insurance and your rate — put your own BAH figure into the field above and read the after-BAH line.</p>
      <p class="small"><a class="btn btn-line" href="redstone-arsenal-pcs-va-loans.html">PCS and VA loan page</a></p>
    </div>
    <div class="card">
      <h3>How much do I need saved to buy here?</h3>
      <p class="small">The down payment depends on the loan: VA financing is typically zero down, conventional under 20% carries mortgage insurance, FHA has lower credit thresholds. On top of that, budget closing costs, the first year of insurance and a repair reserve on an older roof — the last one is the item movers under-budget most often.</p>
    </div>
    <div class="card">
      <h3>Should I rent first before buying?</h3>
      <p class="small">Two cases where it usually pays: you have not yet driven your commute at your real start time, or you have not confirmed which school district serves the neighbourhood. Both are cheaper to check from a rental than to fix from a purchase.</p>
    </div>
  </div>
</div></section>

"""

BLOCKS["home-search.html"] = """
<section class="tight"><div class="wrap">
  <h2>Homes-for-sale questions</h2>
  <div class="grid g2">
    <div class="card">
      <h3>What is the average home price in Huntsville, Alabama?</h3>
      <p class="small">The metro median home value is <b>$331,800</b> (ACS 2024 1-year). That is a market midpoint for the whole metro — the price band that decides what you actually see is set by area, school district and build year, which is why the alerts below ask for the area rather than a single number.</p>
      <p class="small"><a class="btn btn-line" href="cost-of-living.html">Compare with your city</a></p>
    </div>
    <div class="card">
      <h3>How do I search homes for sale in Huntsville?</h3>
      <p class="small">Use ValleyMLS — the local MLS, which is where the listings live — through the button above, and set price alerts here for the areas you care about. Set the alerts first: the alerts are what tell you a house exists in your band before the portals have indexed it.</p>
    </div>
    <div class="card">
      <h3>Is the Huntsville market still competitive?</h3>
      <p class="small">We do not publish market forecasts or call the market hot or cold. What you can verify yourself on any ValleyMLS listing is days on market, the price history and whether the price has been cut — those three tell you more about your specific band than a city-wide headline.</p>
    </div>
    <div class="card">
      <h3>Should I get pre-qualified before I look?</h3>
      <p class="small">Yes. Sellers here expect an offer to be attached to a lender letter, and knowing your payment band stops you looking at houses that will not work. Pre-qualification is a conversation about numbers, not an application, and it does not affect your credit.</p>
      <p class="small"><a class="btn btn-solid" href="prequal.html">Start pre-qualification</a></p>
    </div>
  </div>
</div></section>

"""

BLOCKS["prequal.html"] = """
<section class="tight"><div class="wrap">
  <h2>Mortgage questions we get every week</h2>
  <div class="grid g2">
    <div class="card">
      <h3>How much do I need for a down payment in Huntsville?</h3>
      <p class="small">It depends entirely on the loan. VA purchase financing is typically zero down; conventional below 20% down carries mortgage insurance until you reach that threshold; FHA accepts lower credit scores with insurance that generally lasts for the life of the loan. Zero down is not automatically cheaper — it is more loan at the same rate.</p>
    </div>
    <div class="card">
      <h3>Are there first-time home buyer programs in Alabama?</h3>
      <p class="small">Yes — the state's housing finance agency runs Alabama's homeownership programmes, including down-payment assistance for qualifying buyers, and some counties add their own. We do not quote programme amounts here, because eligibility rules change and a figure we cannot verify is worse than a link.</p>
      <p class="small muted"><a href="https://www.ahfa.com/programs/homeownership" target="_blank" rel="noopener">Alabama Housing Finance Authority</a></p>
    </div>
    <div class="card">
      <h3>Why do you not publish mortgage rates?</h3>
      <p class="small">Because an advertised teaser rate is not your rate. The form above asks for a credit band rather than a score, and we come back with a real quote for your situation, including the Alabama-specific lines that move the payment: tax at the parcel, insurance on that roof, and the VA funding fee where it applies.</p>
    </div>
    <div class="card">
      <h3>Do I need a VA loan if I am military?</h3>
      <p class="small">No — you can compare VA against conventional and FHA. Many buyers near Redstone find VA is cheapest on total cost because of the zero-down structure and no monthly mortgage insurance; others find conventional wins on a specific property or timeline. Ask for both side by side.</p>
      <p class="small"><a class="btn btn-line" href="redstone-arsenal-pcs-va-loans.html">PCS and VA loans in Madison County</a></p>
    </div>
  </div>
</div></section>

"""

BLOCKS["checklist.html"] = f"""
<section class="tight"><div class="wrap">
  <h2>Utilities and setup questions</h2>
  <div class="grid g2">
    <div class="card">
      <h3>Who provides utilities in Huntsville, Alabama?</h3>
      <p class="small"><a href="https://www.hsvutil.org/" {A}>Huntsville Utilities</a> is the city-owned utility: it provides electricity across all of Madison County and a small part of Marshall County, and also water and natural gas, serving over 200,000 electric, roughly 100,000 water and about 56,000 gas customers by its own count. Inside Madison city limits, water and sewer come from the city utility instead.</p>
    </div>
    <div class="card">
      <h3>How do I set up Huntsville Utilities before I move?</h3>
      <p class="small">At a Huntsville city address, electric, water, sewer and gas are all on one account, so it is one call and one start date — book it for the day you take possession, not the day you unpack. County addresses are the ones that split: a water utility district or a private well, plus a contracted trash hauler.</p>
      <p class="small muted"><a href="https://www.hsvutil.org/residential_services/" {A}>Start, stop and transfer service</a></p>
    </div>
    <div class="card">
      <h3>What internet providers serve Huntsville?</h3>
      <p class="small">Fiber from AT&amp;T and Google Fiber covers much of the city, with cable service from Xfinity and WOW in other areas — and availability changes street by street, which is why the honest answer is to check the address rather than the city.</p>
      <p class="small muted">Address-level check: <a href="https://broadbandmap.fcc.gov/" {A}>FCC National Broadband Map</a></p>
    </div>
    <div class="card">
      <h3>What do I need to register a car in Alabama?</h3>
      <p class="small">Title and tag work is handled by the county licence department, not a state office — <a href="https://www.madisoncountyal.gov/departments/license-department/tags-title" {A}>Madison County License Department</a> for most addresses here. Bring the title, proof of insurance and identification. Alabama renews registration in your birth month, so your first renewal date is set by your birthday, not your move.</p>
    </div>
  </div>
</div></section>

"""

BLOCKS["local-realtors.html"] = """
<section class="tight"><div class="wrap">
  <h2>Agent questions, answered</h2>
  <div class="grid g2">
    <div class="card">
      <h3>How much does a realtor cost in Huntsville?</h3>
      <p class="small">Agent compensation is negotiable, and it is now normal to sign a written agreement with a buyer's agent before touring homes — so ask what you will owe, in writing, before you sign. Never assume the seller's side covers it without seeing the agreement.</p>
    </div>
    <div class="card">
      <h3>Do I need a local agent, or can I use a national portal?</h3>
      <p class="small">Portals show you listings; they do not tell you that a "Huntsville" mailing address sits in Madison County Schools, or that the mountain gap adds twenty minutes to a house you love. Those two questions are where a genuinely local agent earns their fee.</p>
    </div>
    <div class="card">
      <h3>What should I ask a Huntsville agent before I commit?</h3>
      <p class="small">Three questions sort them quickly: which school district serves this specific parcel; what has this area's days-on-market and price-cut pattern been in my price band; and what do you know about insurance on houses of this age and roof type here.</p>
    </div>
    <div class="card">
      <h3>Can an agent help with the mortgage side?</h3>
      <p class="small">They can refer you, and on this site the mortgage relationship is disclosed rather than disguised. Pre-qualification is separate from the agent relationship, and you are free to use any lender — including the one your agent suggests.</p>
      <p class="small"><a class="btn btn-line" href="prequal.html">Start pre-qualification</a></p>
    </div>
  </div>
</div></section>

"""

BLOCKS["local-insurance.html"] = """
<section class="tight"><div class="wrap">
  <h2>Insurance questions movers ask</h2>
  <div class="grid g2">
    <div class="card">
      <h3>How much is home insurance in Huntsville, Alabama?</h3>
      <p class="small">We do not publish a premium figure, because the number that matters is quoted on the specific house — roof age and material, wind and hail exposure, replacement cost, and the deductible structure. What we can tell you is which questions change the quote most, which is what this page is about.</p>
    </div>
    <div class="card">
      <h3>What is a wind or hail deductible?</h3>
      <p class="small">Many Alabama policies carry a separate deductible for wind and hail, expressed as a percentage of the dwelling coverage rather than a flat dollar amount. Ask for that line in writing before you compare quotes, because it is where two apparently similar quotes diverge.</p>
    </div>
    <div class="card">
      <h3>Do I need flood insurance?</h3>
      <p class="small">Only if the parcel is in a special flood hazard area, which is what your lender will check — but low-lying and creek-adjacent lots are worth checking even when it is not required. The map lookup is free and takes two minutes; ask the seller or your agent for the zone before you make an offer.</p>
    </div>
    <div class="card">
      <h3>When does coverage need to start?</h3>
      <p class="small">On possession day — your lender will require evidence of insurance before closing, and for a purchase here that usually means binding coverage a few days before the closing date, not on move-in day. For renters, the landlord's policy covers the building, not your contents.</p>
      <p class="small muted">Regulator and consumer help: <a href="https://aldoi.gov/" target="_blank" rel="noopener">Alabama Department of Insurance</a></p>
    </div>
  </div>
</div></section>

"""


def main():
    failures, applied = [], 0
    for fname, block in BLOCKS.items():
        path = os.path.join(SITE, fname)
        with io.open(path, encoding="utf-8") as fh:
            s = fh.read()
        if s.count(ANCHOR) != 1:
            failures.append(f"{fname}: footer anchor appears {s.count(ANCHOR)} times")
            continue
        if block.count("<section") != block.count("</section>"):
            failures.append(f"{fname}: unbalanced <section> in block")
            continue
        with io.open(path, "w", encoding="utf-8") as fh:
            fh.write(s.replace(ANCHOR, block.lstrip("\n") + ANCHOR, 1))
        applied += 1
    print(f"inserted question blocks into {applied}/{len(BLOCKS)} pages")
    if failures:
        print("FAILURES:")
        for f in failures:
            print("  -", f)
        sys.exit(1)


if __name__ == "__main__":
    main()

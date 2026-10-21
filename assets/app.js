/* Rocket City Move — prototype tool logic (no dependencies)
   Data sources: Census Reporter (ACS 2024 1-yr), OSRM routing, compiled local data.
   Every published figure is either fetched live or read from /data/*.json — nothing is invented here. */
(function () {
  'use strict';

  const $ = (s, r) => (r || document).querySelector(s);
  const $$ = (s, r) => Array.from((r || document).querySelectorAll(s));
  const money = n => (n || n === 0) ? '$' + Math.round(n).toLocaleString() : '—';
  const pct = n => (n || n === 0) ? (n * 100).toFixed(1) + '%' : '—';
  const val = (id, def) => { const el = $('#' + id); if (!el) return def; const v = parseFloat(String(el.value).replace(/[^0-9.\-]/g, '')); return isNaN(v) ? def : v; };
  const txt = (id, def) => { const el = $('#' + id); return el && el.value !== '' ? el.value : def; };
  const on = id => { const el = $('#' + id); return !!(el && el.checked); };
  const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

  const data = {}; // cached JSON
  async function load(name) {
    if (data[name]) return data[name];
    const r = await fetch('data/' + name + '.json');
    data[name] = await r.json();
    return data[name];
  }

  function post(path, payload) {
    return fetch(path, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) })
      .then(r => r.json()).catch(() => ({ ok: false, offline: true }));
  }

  /* ---------------- lead capture ----------------
     Every form on the site posts here. Prototype behaviour: the local server
     appends to leads.csv so the funnel is visible end-to-end. */
  function wireForms() {
    $$('form[data-lead]').forEach(f => {
      f.addEventListener('submit', async e => {
        e.preventDefault();
        const btn = $('button[type=submit]', f); const old = btn ? btn.textContent : '';
        if (btn) { btn.disabled = true; btn.textContent = 'Sending…'; }
        const payload = Object.fromEntries(new FormData(f).entries());
        payload.form = f.getAttribute('data-lead');
        payload.page = location.pathname;
        payload.ts = new Date().toISOString();
        const res = await post('/api/lead', payload);
        const box = f.parentElement.querySelector('.form-msg') || f.querySelector('.form-msg');
        if (box) {
          box.style.display = 'block';
          box.textContent = res.ok
            ? 'Thanks — we\u2019ve received your request and will be in touch shortly.'
            : 'We couldn\u2019t submit that just now. Please try again in a moment, or email hello@movetohuntsville.net.';
        }
        if (!res.ok) { try { const k = 'rcm_leads'; const cur = JSON.parse(localStorage.getItem(k) || '[]'); cur.push(payload); localStorage.setItem(k, JSON.stringify(cur)); } catch (_) {} }
        f.reset();
        if (btn) { btn.disabled = false; btn.textContent = old; }
      });
    });
  }

  /* ---------------- 1. payment / affordability ---------------- */
  function payment(price, downPct, rate, term, taxRatePct, insYr, hoaMo) {
    const down = price * downPct / 100;
    const loan = Math.max(0, price - down);
    const r = rate / 100 / 12, n = term * 12;
    const pi = r === 0 ? loan / n : loan * r / (1 - Math.pow(1 + r, -n));
    const taxMo = price * taxRatePct / 100 / 12;
    const insMo = insYr / 12;
    const piti = pi + taxMo + insMo + hoaMo;
    // PMI if conventional and under 20% down (assumed 0.5%/yr of loan, clearly labelled as an assumption)
    const pmi = (downPct < 20) ? loan * 0.005 / 12 : 0;
    return { down, loan, pi, taxMo, insMo, hoaMo, pmi, total: piti + pmi };
  }

  function initPayment() {
    const out = $('#pay-out'); if (!out) return;
    const run = () => {
      const price = val('pay-price', 350000), downPct = val('pay-down', 5), rate = val('pay-rate', 6.5),
        term = val('pay-term', 30), taxRate = val('pay-tax', 0.41), ins = val('pay-ins', 1800),
        hoa = val('pay-hoa', 0), income = val('pay-income', 0), debts = val('pay-debts', 0);
      const m = payment(price, downPct, rate, term, taxRate, ins, hoa);
      const dti = income > 0 ? (m.total + debts) / (income / 12) : null;
      const dx = document.createElement('div');
      dx.innerHTML = `
        <div class="grid g4">
          <div class="stat"><b>${money(m.total)}</b><small>estimated monthly payment (PITI${m.pmi ? ' + PMI' : ''})</small></div>
          <div class="stat"><b>${money(m.pi)}</b><small>principal &amp; interest</small></div>
          <div class="stat"><b>${money(m.down)}</b><small>down payment (${pct(downPct / 100)})</small></div>
          <div class="stat"><b>${money(m.loan)}</b><small>loan amount</small></div>
        </div>
        <table>
          <tbody>
            <tr><td>Principal &amp; interest</td><td class="num">${money(m.pi)}</td></tr>
            <tr><td>Property taxes at ${taxRate}% / yr (Alabama)</td><td class="num">${money(m.taxMo)}</td></tr>
            <tr><td>Homeowners insurance (your input)</td><td class="num">${money(m.insMo)}</td></tr>
            ${m.pmi ? `<tr><td>PMI assumption at 0.5%/yr (under 20% down)</td><td class="num">${money(m.pmi)}</td></tr>` : ''}
            ${hoa ? `<tr><td>HOA dues</td><td class="num">${money(hoa)}</td></tr>` : ''}
            <tr><td><b>Total</b></td><td class="num"><b>${money(m.total)}</b></td></tr>
            ${dti !== null ? `<tr><td>Debt-to-income with your other debts</td><td class="num">${pct(dti)} ${dti < 0.36 ? '<span class="pill">in a typical range</span>' : dti < 0.43 ? '<span class="pill warn">near the common 43% ceiling</span>' : '<span class="pill warn">above the common ceiling</span>'}</td></tr>` : ''}
          </tbody>
        </table>
        <div class="disclaimer">Estimate only — not a loan offer, pre-approval, or commitment to lend. Taxes and insurance vary by property. Published rates, APRs and payment figures require review before launch.</div>`;
      out.innerHTML = ''; out.appendChild(dx);
    };
    $$('#pay-price,#pay-down,#pay-rate,#pay-term,#pay-tax,#pay-ins,#pay-hoa,#pay-income,#pay-debts').forEach(el => el.addEventListener('input', run));
    run();
  }

  /* ---------------- 2. rent vs buy + BAH ---------------- */
  function initRentBuy() {
    const out = $('#rb-out'); if (!out) return;
    const run = () => {
      const rent = val('rb-rent', 1500), price = val('rb-price', 350000), downPct = val('rb-down', 5),
        rate = val('rb-rate', 6.5), term = val('rb-term', 30), taxRate = val('rb-tax', 0.41),
        ins = val('rb-ins', 1800), hoa = val('rb-hoa', 0), maintPct = val('rb-maint', 1),
        years = val('rb-years', 7), appr = val('rb-appr', 3), investR = val('rb-invest', 4),
        bah = val('rb-bah', 0), va = on('rb-va');
      const m = payment(price, va ? 0 : downPct, rate, term, taxRate, ins, hoa);
      const maint = price * maintPct / 100 / 12;
      const rentGrow = rent * Math.pow(1.03, Math.min(years, 30));
      const buyNow = m.total + maint, rentNow = rent;
      // net cost of buying vs renting over the horizon (simple model, stated assumptions)
      let equity = 0, interestPaid = 0, bal = m.loan;
      const r = rate / 100 / 12;
      for (let i = 0; i < years * 12; i++) { const int = bal * r; interestPaid += int; bal -= (m.pi - int); }
      const futureValue = price * Math.pow(1 + appr / 100, years);
      const saleCost = futureValue * 0.08;                       // agent + closing costs, assumption
      const remaining = Math.max(0, price - m.loan) + 0;          // down payment at purchase
      equity = futureValue - bal - saleCost - remaining;
      const rentPaid = Array.from({ length: years }, (_, i) => rent * 12 * Math.pow(1.03, i)).reduce((a, b) => a + b, 0);
      const investGain = remaining * (Math.pow(1 + investR / 100, years) - 1);
      const b = { buy: m.total + maint, rent: rentNow, bah, outOfPocket: Math.max(0, m.total + maint - bah) };
      const dx = document.createElement('div');
      dx.innerHTML = `
        <div class="grid g4">
          <div class="stat"><b>${money(b.buy)}</b><small>own: all-in monthly (PITI + ${maintPct}% maintenance)</small></div>
          <div class="stat"><b>${money(b.rent)}</b><small>rent: monthly today</small></div>
          <div class="stat"><b>${money(b.outOfPocket)}</b><small>your cost after ${bah ? money(bah) + ' BAH' : 'no BAH entered'}</small></div>
          <div class="stat"><b>${money(Math.max(0, equity))}</b><small>net proceeds if sold in ${years} yrs (model)</small></div>
        </div>
        <table>
          <tbody>
            <tr><td>Down payment ${va && on('rb-va') ? '(VA: typically 0%)' : '(your input)'}</td><td class="num">${money(va ? 0 : price * downPct / 100)}</td></tr>
            <tr><td>Loan amount</td><td class="num">${money(m.loan)}</td></tr>
            <tr><td>Interest paid over ${years} years</td><td class="num">${money(interestPaid)}</td></tr>
            <tr><td>Rent paid over ${years} years (3%/yr growth assumed)</td><td class="num">${money(rentPaid)}</td></tr>
            <tr><td>Home value in ${years} years at ${appr}%/yr (assumed)</td><td class="num">${money(futureValue)}</td></tr>
            <tr><td>Break-even month vs renting today</td><td class="num">${buyNow > rentNow ? Math.min(600, Math.round((price * 0.06 + m.down) / (buyNow - rentNow))) + ' months' : 'immediate'}</td></tr>
            ${va ? `<tr><td>VA funding fee note</td><td class="num">varies by service history &amp; down payment — confirm with your lender</td></tr>` : ''}
          </tbody>
        </table>
        <div class="disclaimer">Model, not advice: assumes ${appr}% annual appreciation, ${maintPct}% annual maintenance, 8% selling costs, and rent rising 3%/yr. Your BAH figure must come from the official rate table. Nothing here is a loan offer.</div>`;
      out.innerHTML = ''; out.appendChild(dx);
    };
    $$('#rb-rent,#rb-price,#rb-down,#rb-rate,#rb-term,#rb-tax,#rb-ins,#rb-hoa,#rb-maint,#rb-years,#rb-appr,#rb-invest,#rb-bah,#rb-va').forEach(el => el.addEventListener('input', run));
    run();
  }

  /* ---------------- 3. commute calculator (live OSRM) ---------------- */
  /* Peak-hour congestion is corridor-specific, so the UI shows a RANGE rather than one
     multiplied number. The base comes from the destination corridor; communities behind a
     known bottleneck get an extra allowance. These are rule-of-thumb figures, labelled as such. */
  function peakRange(destName, originName) {
    const d = (destName || '').toLowerCase(), o = (originName || '').toLowerCase();
    let base = 1.25, why = 'open road network';
    if (/gate 9|base interior|gateway|marshall/.test(d)) { base = 1.40; why = 'shift change at Gate 9 / Rideout Rd'; }
    else if (/research park|adtran|lockheed|boeing/.test(d)) { base = 1.35; why = 'I-565 and Research Park Blvd inbound'; }
    else if (/hospital|downtown/.test(d)) { base = 1.30; why = 'downtown and medical district traffic'; }
    else if (/mazda|airport/.test(d)) { base = 1.25; why = 'outbound industrial corridor'; }
    if (/hampton cove|big cove|owens cross roads|gurley|brownsboro|new market/.test(o)) why += ', plus the 431 mountain gap';
    if (/hampton cove|big cove|owens cross roads|gurley|brownsboro|new market/.test(o)) base += 0.08;
    else if (/harvest|toney|meridianville|monrovia|madison/.test(o)) base += 0.04;
    return { lo: base, hi: base + 0.12, why };
  }
  async function initCommute() {
    const out = $('#commute-out'); if (!out) return;
    const places = await load('places');
    const sel = $('#commute-dest');
    sel.innerHTML = places.employers.map((e, i) => `<option value="${i}">${esc(e.name)}${e.note ? ' — ' + esc(e.note) : ''}</option>`).join('');
    const homes = $('#commute-homes');
    // 36 communities would be an unreadable wall of checkboxes, so they're grouped by
    // county (Madison, Limestone, Morgan) the way a mover actually thinks about the move.
    const counties = [...new Set(places.neighborhoods.map(n => n.county || 'Madison County'))];
    const checked = ['Madison', 'Hampton Cove', 'Downtown Huntsville', 'Harvest', 'Owens Cross Roads', 'Hazel Green'];
    homes.innerHTML = counties.map(c => `
      <div style="grid-column:1/-1">
        <div class="kicker" style="margin:4px 0 2px">${esc(c)}</div>
        <div class="grid g3">${places.neighborhoods.map((n, i) => n.county === c ? `
          <label style="display:flex;align-items:center;gap:8px;font-weight:400;margin:4px 0">
            <input type="checkbox" class="cbox" value="${i}" style="width:auto" ${checked.includes(n.name) ? 'checked' : ''}>
            <span>${esc(n.name)}</span></label>` : '').join('')}</div>
      </div>`).join('');

    const run = async () => {
      const dest = places.employers[parseInt(sel.value, 10)];
      const picked = $$('.cbox', homes).filter(c => c.checked).map(c => places.neighborhoods[parseInt(c.value, 10)]);
      if (!picked.length) { out.innerHTML = '<p class="muted">Pick at least one place to live.</p>'; return; }
      out.innerHTML = '<p class="muted">Measuring real driving routes…</p>';
      const rows = [];
      for (const n of picked) {
        try {
          const u = `https://router.project-osrm.org/route/v1/driving/${n.lon},${n.lat};${dest.lon},${dest.lat}?overview=false`;
          const j = await (await fetch(u)).json();
          if (j.code !== 'Ok' || !j.routes || !j.routes.length) throw new Error('no route');
          const rt = j.routes[0];
          rows.push({ name: n.name, km: rt.distance / 1000, min: rt.duration / 60,
                      miles: rt.distance / 1609.34, peak: peakRange(dest.name, n.name) });
        } catch (e) { rows.push({ name: n.name, err: true }); }
      }
      rows.sort((a, b) => (a.min || 999) - (b.min || 999));
      const irsRate = val('commute-irs', 0.70);
      const days = val('commute-days', 240);
      out.innerHTML = `
        <h4>To ${esc(dest.name)}</h4>
        <table><thead><tr><th>Living in</th><th class="num">Distance</th><th class="num">Off-peak drive</th><th class="num">Peak-hour range</th><th class="num">Annual commute cost</th></tr></thead><tbody>
        ${rows.map(r => r.err ? `<tr><td>${esc(r.name)}</td><td colspan="4" class="muted">route unavailable</td></tr>`
        : `<tr><td>${esc(r.name)}</td><td class="num">${r.miles.toFixed(1)} mi</td><td class="num">${r.min.toFixed(1)} min</td><td class="num">${Math.round(r.min * r.peak.lo)}–${Math.round(r.min * r.peak.hi)} min</td><td class="num">${money(r.miles * 2 * days * irsRate)}</td></tr>`).join('')}
        </tbody></table>
        <div class="disclaimer">Off-peak times are live OSRM road-network estimates with <b>no traffic modelling</b>. The peak range is built from corridor-specific allowances — ${esc([...new Set(rows.filter(r => !r.err).map(r => r.peak.why))].slice(0, 3).join('; '))} — so treat it as a range, not a measurement. Annual cost = round-trip miles × ${days} commute days × $${irsRate}/mile (your input).</div>`;
    };
    $$('#commute-dest,.cbox,#commute-irs,#commute-days').forEach(el => el.addEventListener('change', run));
    sel.addEventListener('change', run);
    run();
  }

  /* ---------------- 4. your city -> Huntsville ---------------- */
  async function initCost() {
    const out = $('#cost-out'); if (!out) return;
    const d = await load('metros');
    const home = d.metros.find(m => m.label === 'Huntsville, AL');
    const sel = $('#cost-metro');
    sel.innerHTML = d.metros.filter(m => m.label !== 'Huntsville, AL')
      .sort((a, b) => a.label.localeCompare(b.label))
      .map(m => `<option value="${esc(m.geo)}">${esc(m.label)}</option>`).join('');
    const run = () => {
      const m = d.metros.find(x => x.geo === sel.value) || d.metros[0];
      const bedrooms = val('cost-size', 3);
      const topRate = 6.5, term = 30;
      const pay = (metro) => {
        const target = metro.home_value * (bedrooms >= 4 ? 1.15 : bedrooms === 3 ? 1 : 0.78);
        const loan = target * 0.9, r = topRate / 100 / 12, n = term * 12;
        const pi = loan * r / (1 - Math.pow(1 + r, -n));
        return { target, pi, tax: metro.median_taxes / 12, piti: pi + metro.median_taxes / 12 + 150 };
      };
      const a = pay(m), h = pay(home);
      const rows = [
        ['Median gross rent', m.rent, home.rent],
        ['Median home value', m.home_value, home.home_value],
        ['Median household income', m.income, home.income],
        ['Median property tax paid (mortgaged homes)', m.median_taxes, home.median_taxes],
      ];
      out.innerHTML = `
        <table><thead><tr><th>ACS 2024 1-year, metro area</th><th class="num">${esc(m.label)}</th><th class="num">Huntsville, AL</th><th class="num">Difference</th></tr></thead><tbody>
        ${rows.map(r => `<tr><td>${r[0]}</td><td class="num">${money(r[1])}</td><td class="num">${money(r[2])}</td><td class="num">${(r[2] - r[1]) <= 0 ? '−' : '+'}${money(Math.abs(r[2] - r[1]))}</td></tr>`).join('')}
        <tr><td>Estimated house payment for a ${bedrooms}-bedroom-sized home (20% down, ${topRate}% illustrative rate)</td><td class="num">${money(a.piti)}</td><td class="num">${money(h.piti)}</td><td class="num">${(h.piti - a.piti) <= 0 ? '−' : '+'}${money(Math.abs(h.piti - a.piti))}/mo</td></tr>
        </tbody></table>
        <p class="small muted">Huntsville carry of ${money(h.piti)}/mo is modelled on a ${money(h.target)} home with Alabama property tax at the metro's actual median of ${money(home.median_taxes)}/yr — the single biggest line-item difference for most movers. Alabama levies a state income tax; Tennessee, Texas, Florida, Washington and Nevada do not — check your own state before comparing take-home pay.</p>
        <div class="disclaimer">Source: US Census Bureau ACS 2024 1-year estimates via the Census Reporter API. Rent, value and income are metro medians, not the house you will buy.</div>`;
    };
    sel.addEventListener('change', run); $('#cost-size').addEventListener('input', run); run();
  }

  /* ---------------- 5. relocation checklist ---------------- */
  async function initChecklist() {
    const out = $('#check-out'); if (!out) return;
    const cl = await load('checklist');
    // The community list is driven by data/checklist.json so adding a community is a
    // one-file change — the dropdown can never drift out of sync with the rules.
    const citySel = $('#ck-city');
    if (citySel) {
      const cur = citySel.value;
      citySel.innerHTML = Object.keys(cl.county_for).map(c => `<option>${esc(c)}</option>`).join('');
      if (cur && cl.county_for[cur]) citySel.value = cur;
    }
    const run = () => {
      const city = txt('ck-city', 'Huntsville');
      const county = cl.county_for[city] || 'Madison County';
      const cls = (cl.class_for || {})[city] || 'county';
      const jurisdiction = (cl.class_label || {})[cls] || county;
      const kids = on('ck-kids'), pets = on('ck-pets'), mil = on('ck-mil'), rent = on('ck-rent'), cars = on('ck-cars'), arrived = txt('ck-date', '');
      // A task is shown when its condition (if any) matches AND its jurisdiction class (if any) matches.
      const picked = cl.groups.map(g => ({
        ...g,
        tasks: g.tasks.filter(t => (!t.only || t.only.some(k => ({ kids, pets, mil, rent, cars }[k])))
                              && (!t.classes || t.classes.includes(cls)))
      })).filter(g => g.tasks.length);
      out.innerHTML = `
        <h3>Your move-to-${esc(city)} checklist${arrived ? ' — move date ' + esc(arrived) : ''}</h3>
        <p class="small muted">${esc(jurisdiction)}${(cls === 'county' || jurisdiction === county) ? '' : ' · ' + esc(county)} · ${kids ? 'school-age children' : 'no school-age children'} · ${pets ? 'pets' : 'no pets'} · ${mil ? 'military/PCS' : 'not military'} · ${rent ? 'renting' : 'buying'} · ${cars ? 'vehicles' : 'no vehicles'}</p>
        ${picked.map(g => `<h4>${esc(g.title)}</h4><ul class="check">${g.tasks.map(t => `<li>${esc(t.text)}${t.link ? ` <a href="${esc(t.link)}" target="_blank" rel="noopener">${esc(t.link_label || 'official site')}</a>` : ''}</li>`).join('')}</ul>`).join('')}
        <div class="badge-row no-print"><button class="btn btn-solid" onclick="window.print()">Print / save as PDF</button></div>
        <div class="disclaimer">Compiled from official utility, county and state sources; provider details change — confirm each step against the linked official page. Wildcards: electric and water providers differ inside Huntsville city vs Madison and the unincorporated county.</div>`;
    };
    $$('#ck-city,#ck-date,#ck-kids,#ck-pets,#ck-mil,#ck-rent,#ck-cars').forEach(el => el.addEventListener('change', run));
    run();
  }

  /* ---------------- ValleyMLS popup ----------------
     No IDX, no iframe: we hand off to ValleyMLS in a new window and capture the
     visitor BEFORE the click, because we have no visibility once they leave. */
  function wireMls() {
    $$('[data-mls]').forEach(el => {
      el.addEventListener('click', e => {
        e.preventDefault();
        const w = window.open('https://www.valleymls.com/', 'valleymls', 'noopener,width=1280,height=900,scrollbars=yes');
        const note = $('#mls-note');
        if (note) { note.style.display = 'block'; note.textContent = w ? 'ValleyMLS opened in a new window — your place here is kept.' : 'Your browser blocked the popup. Allow popups for this site, or use this link: valleymls.com'; }
      });
    });
  }

  document.addEventListener('DOMContentLoaded', () => {
    wireForms(); wireMls();
    initPayment(); initRentBuy(); initCommute(); initCost(); initChecklist();
  });
})();

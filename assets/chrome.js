/* Shared header/footer so the prototype stays editable in one place.
   PRODUCTION NOTE: for a real launch this chrome should be server-rendered — see README. */
(function () {
  // Two dropdowns keep the bar on one line at 1280px: "Where to live" is the
  // geography/schools/safety axis, "Money & jobs" is the numbers axis.
  const NAV = [
    ['index.html', 'Home'],
    { label: 'Where to live', items: [
      ['moving-to-huntsville.html', 'Moving guide'],
      ['neighborhoods.html', 'Neighborhoods'],
      ['schools.html', 'Schools'],
      ['home-search.html', 'Home search'],
      ['huntsville-crime-safety.html', 'Crime & safety'],
      ['is-huntsville-a-good-place-to-live.html', 'Is Huntsville right for you?'],
      ['redstone-arsenal-pcs-va-loans.html', 'PCS & VA loans']
    ] },
    { label: 'Money & jobs', items: [
      ['huntsville-employers.html', 'Employers & jobs'],
      ['cost-of-living.html', 'Cost comparison'],
      ['rent-in-huntsville.html', 'Rent & apartments'],
      ['property-taxes.html', 'Property taxes'],
      ['rent-vs-buy.html', 'Rent vs buy']
    ] },
    ['commute.html', 'Commute'],
    ['checklist.html', 'Checklist']
  ];
  const here = location.pathname.split('/').pop() || 'index.html';

  function navHTML() {
    return NAV.map(item => {
      if (Array.isArray(item)) {
        return `<a href="${item[0]}" class="${item[0] === here ? 'active' : ''}">${item[1]}</a>`;
      }
      const active = item.items.some(([h]) => h === here);
      return `<details class="menu">
          <summary class="${active ? 'active' : ''}">${item.label} <span aria-hidden="true">▾</span></summary>
          <div class="menu-panel">${item.items.map(([h, t]) => `<a href="${h}" class="${h === here ? 'active' : ''}">${t}</a>`).join('')}</div>
        </details>`;
    }).join('');
  }

  // The prototype notice is for local previews only — on the published domain it
  // told visitors (and crawlers) the site was "not published", which is wrong.
  const LOCAL = ['localhost', '127.0.0.1', '::1', ''].includes(location.hostname)
    || location.protocol === 'file:'
    || new URLSearchParams(location.search).has('preview');

  const header = `
  ${LOCAL ? `<div class="banner"><div class="wrap">
    <div><b>Prototype preview</b> — running on your local server. Payments, rates and legal text are placeholders pending compliance review.</div>
    <div class="small">Local preview build · not published</div>
  </div></div>` : ''}
  <header class="site"><div class="wrap">
    <a class="logo" href="index.html" aria-label="Move to Huntsville — home"><img src="assets/img/logo/logo-horizontal.svg" alt="Move to Huntsville" width="243" height="48"></a>
    <nav class="main">${navHTML()}</nav>
    <a class="cta-top" href="prequal.html">Need a Mortgage Quote</a>
  </div></header>`;

  const footer = `
  <footer class="site"><div class="wrap">
    <div class="cols">
      <div>
        <h4>Move to Huntsville</h4>
        <p class="small">A relocation guide for people moving to Huntsville, Madison and Madison County, Alabama — built around the questions movers actually ask: schools, commute, cost and where to live.</p>
      </div>
      <div>
        <h4>Tools</h4>
        <p class="small"><a href="commute.html">Commute calculator</a><br><a href="cost-of-living.html">Your city → Huntsville</a><br><a href="rent-vs-buy.html">Rent vs buy + BAH</a><br><a href="checklist.html">Relocation checklist</a></p>
      </div>
      <div>
        <h4>Research</h4>
        <p class="small"><a href="schools.html">School comparison</a><br><a href="neighborhoods.html">Neighborhood guide</a><br><a href="huntsville-employers.html">Top employers &amp; jobs</a><br><a href="rent-in-huntsville.html">Rent &amp; apartments</a><br><a href="property-taxes.html">Property taxes</a><br><a href="huntsville-crime-safety.html">Crime &amp; safety data</a><br><a href="is-huntsville-a-good-place-to-live.html">Is Huntsville right for you?</a><br><a href="redstone-arsenal-pcs-va-loans.html">PCS &amp; VA loans</a><br><a href="home-search.html">Search homes on ValleyMLS</a><br><a href="local-realtors.html">Local realtors</a> · <a href="local-insurance.html">Insurance</a></p>
      </div>
      <div>
        <h4>About this site</h4>
        <p class="small"><a href="about.html">How this site works</a><br><a href="photos.html">Photo credits</a><br><a href="prequal.html">Get pre-qualified</a></p>
      </div>
    </div>
    <div class="nmls">
      <span class="eho">⌂ Equal Housing Opportunity</span>
      <span>NMLS #000000 (placeholder)</span>
      <span>Licensed in Alabama (placeholder)</span>
      <span>Data: US Census Bureau ACS 2024 1-year, OSRM, official district and utility sources</span>
    </div>
    <p class="small" style="margin-top:14px">This site does not sell or share your information. It is not a loan application, offer or commitment to lend; all payment figures are estimates.</p>
  </div></footer>`;

  document.addEventListener('DOMContentLoaded', () => {
    const h = document.getElementById('site-header'); if (h) h.innerHTML = header;
    const f = document.getElementById('site-footer'); if (f) f.innerHTML = footer;
    // Close any open nav dropdown when the visitor clicks elsewhere.
    document.addEventListener('click', e => {
      document.querySelectorAll('nav.main details.menu[open]').forEach(d => {
        if (!d.contains(e.target)) d.removeAttribute('open');
      });
    });
  });
})();

/* Photo galleries. Images are freely licensed from Wikimedia Commons (CC BY / CC BY-SA /
   public domain); every one is credited under the image with a link to its source file,
   which is what the licences require. Slugs come from data/photos.json.

   Usage in HTML:
     <div class="photo-tile" data-photos="slug-a,slug-b,slug-c"></div>   full-width band
     <div class="photo-band" data-photos="slug-a,slug-b"></div>          caption over image
     <div class="gallery"    data-photos="slug-a,slug-b,slug-c"></div>   cards with credits
     <div data-photos-table></div>                                       the credits table
*/
(function () {
  'use strict';
  const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  let CACHE = null;

  const load = () => CACHE || (CACHE = fetch('data/photos.json').then(r => r.json()).then(d => {
    const map = {};
    d.photos.forEach(p => { map[p.slug] = p; });
    return map;
  }));

  function credit(p) {
    return `Photo: ${esc(p.credit || 'see source')} · ${esc(p.license)} · <a href="${esc(p.source)}" target="_blank" rel="noopener">source file</a>`;
  }
  function card(p) {
    return `<figure class="photo"><img src="${esc(p.file)}" alt="${esc(p.caption)}" loading="lazy">
      <figcaption><b>${esc(p.caption)}</b><span class="credit">${credit(p)}</span></figcaption></figure>`;
  }
  function band(p) {
    return `<figure><img src="${esc(p.file)}" alt="${esc(p.caption)}" loading="lazy">
      <figcaption>${esc(p.caption)}<span class="credit">${esc(p.credit)} · ${esc(p.license)}</span></figcaption></figure>`;
  }

  document.addEventListener('DOMContentLoaded', async () => {
    const nodes = document.querySelectorAll('[data-photos],[data-photos-table]');
    if (!nodes.length) return;
    let map;
    try { map = await load(); } catch (e) { console.warn('photo data failed to load', e); return; }
    nodes.forEach(el => {
      if (el.hasAttribute('data-photos-table')) return renderCredits(el, map);
      const slugs = el.getAttribute('data-photos').split(',').map(s => s.trim()).filter(Boolean);
      const items = slugs.map(s => map[s]).filter(Boolean);
      const render = el.classList.contains('gallery') ? card : band;
      el.innerHTML = items.map(render).join('');
      if (!items.length) el.remove();
    });
  });

  function renderCredits(el, map) {
    const all = Object.values(map).sort((a, b) => a.slug.localeCompare(b.slug));
    el.innerHTML = `<table class="credits-table"><thead><tr><th>Photo</th><th>What it shows</th><th>Credit</th><th>Licence</th></tr></thead><tbody>
      ${all.map(p => `<tr>
        <td><a href="${esc(p.source)}" target="_blank" rel="noopener"><img src="${esc(p.file)}" alt="${esc(p.caption)}" loading="lazy"></a></td>
        <td><b>${esc(p.caption)}</b><br><span class="small muted">${esc(p.title)}</span></td>
        <td class="small">${esc(p.credit || 'see source')}</td>
        <td class="small">${esc(p.license)}<br><a href="${esc(p.license_url)}" target="_blank" rel="noopener">licence</a> · <a href="${esc(p.source)}" target="_blank" rel="noopener">file page</a></td>
      </tr>`).join('')}
    </tbody></table>
    <p class="small muted">All ${all.length} photographs are stored locally in <code>assets/img/</code> and are freely licensed
    (Creative Commons Attribution or Attribution-ShareAlike, or public domain). Credit and a link to the original file page appear
    under every image, as the licences require. Substitute your own photography before launch if you prefer not to carry attribution.</p>`;
  }
})();

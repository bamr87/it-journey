/*
 * home-os.js — the /home/ personal desktop OS.
 * Owns layout/persistence/interaction for the configurable widget grid, dock,
 * and Cmd+K launcher. Mirrors the quest-dashboard.js conventions (namespaced
 * localStorage key + window API + debounced writes). Progressive enhancement:
 * the page renders fully without JS; this hydrates saved layout + wiring.
 *
 *   it-journey-home-layout : { v:1, widgets:{ id:{order,cols,rows,visible,minimized,collapsed} }, density, wallpaper }
 *   it-journey-accent      : "#hex"  (read by user-overrides.js → re-tints site)
 *   it-journey-home-notes / -goals / -status : per-widget state
 */
(function () {
  'use strict';
  var os = document.querySelector('[data-home-os]');
  if (!os) return;
  var grid = os.querySelector('[data-home-grid]');
  var LKEY = 'it-journey-home-layout', AKEY = 'it-journey-accent';
  var SIZES = [[1, 1], [2, 1], [2, 2], [1, 2], [4, 1], [3, 2]];

  function load(k, d) { try { var v = localStorage.getItem(k); return v == null ? d : JSON.parse(v); } catch (e) { return d; } }
  function save(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  function loadStr(k, d) { try { var v = localStorage.getItem(k); return v == null ? d : v; } catch (e) { return d; } }

  /* ---- state seeded from DOM defaults, overlaid by saved layout ---- */
  var widgets = Array.prototype.slice.call(grid.querySelectorAll('[data-home-widget]'));
  var state = load(LKEY, null) || { v: 1, widgets: {}, density: os.getAttribute('data-density') || 'comfortable', wallpaper: 0 };
  state.widgets = state.widgets || {};
  widgets.forEach(function (el, i) {
    var id = el.getAttribute('data-home-widget');
    var st = state.widgets[id] || {};
    if (st.order == null) st.order = parseInt(el.style.order, 10) || i;
    if (!st.cols) st.cols = parseInt(el.style.getPropertyValue('--w-cols'), 10) || 1;
    if (!st.rows) st.rows = parseInt(el.style.getPropertyValue('--w-rows'), 10) || 1;
    if (st.visible == null) st.visible = true;
    if (st.minimized == null) st.minimized = false;
    if (st.collapsed == null) st.collapsed = false;
    st.closable = el.getAttribute('data-closable') !== 'false';
    state.widgets[id] = st;
  });
  var saveT;
  function persist() { clearTimeout(saveT); saveT = setTimeout(function () { save(LKEY, state); }, 200); window.dispatchEvent(new CustomEvent('home-os:change')); }
  function el(id) { return grid.querySelector('[data-home-widget="' + id + '"]'); }

  /* ---- apply state to DOM ---- */
  function applyWidget(id) {
    var e = el(id), st = state.widgets[id]; if (!e) return;
    e.style.order = st.order;
    e.style.setProperty('--w-cols', st.cols);
    e.style.setProperty('--w-rows', st.rows);
    e.hidden = !st.visible || st.minimized;
    e.classList.toggle('is-collapsed', !!st.collapsed);
  }
  function applyAll() {
    os.setAttribute('data-density', state.density || 'comfortable');
    Object.keys(state.widgets).forEach(applyWidget);
    renderChips();
  }

  /* ---- window controls ---- */
  function setWidget(id, patch) { Object.assign(state.widgets[id], patch); applyWidget(id); renderChips(); persist(); }
  grid.addEventListener('click', function (ev) {
    var btn = ev.target.closest('[data-home-action]'); if (!btn) return;
    var w = btn.closest('[data-home-widget]'); var id = w.getAttribute('data-home-widget'); var st = state.widgets[id];
    var act = btn.getAttribute('data-home-action');
    if (act === 'close') { if (st.closable) setWidget(id, { visible: false }); }
    else if (act === 'minimize') { setWidget(id, { minimized: true }); }
    else if (act === 'collapse') { setWidget(id, { collapsed: !st.collapsed }); }
    else if (act === 'resize') {
      var ci = 0; for (var k = 0; k < SIZES.length; k++) { if (SIZES[k][0] === st.cols && SIZES[k][1] === st.rows) { ci = k; break; } }
      var nx = SIZES[(ci + 1) % SIZES.length]; setWidget(id, { cols: nx[0], rows: nx[1] });
    }
  });

  /* ---- drag to reorder ---- */
  var dragId = null;
  grid.addEventListener('dragstart', function (ev) {
    var bar = ev.target.closest('[data-home-handle]'); if (!bar) return;
    dragId = bar.closest('[data-home-widget]').getAttribute('data-home-widget');
    bar.closest('[data-home-widget]').classList.add('is-dragging');
    try { ev.dataTransfer.setData('text/plain', dragId); ev.dataTransfer.effectAllowed = 'move'; } catch (e) {}
  });
  grid.addEventListener('dragend', function () { dragId = null; widgets.forEach(function (w) { w.classList.remove('is-dragging', 'is-drop-target'); }); });
  grid.addEventListener('dragover', function (ev) {
    var t = ev.target.closest('[data-home-widget]'); if (!t || !dragId) return; ev.preventDefault();
    widgets.forEach(function (w) { w.classList.toggle('is-drop-target', w === t && w.getAttribute('data-home-widget') !== dragId); });
  });
  grid.addEventListener('drop', function (ev) {
    var t = ev.target.closest('[data-home-widget]'); if (!t || !dragId) return; ev.preventDefault();
    var targetId = t.getAttribute('data-home-widget'); if (targetId === dragId) return;
    var ordered = Object.keys(state.widgets).sort(function (a, b) { return state.widgets[a].order - state.widgets[b].order; });
    ordered.splice(ordered.indexOf(dragId), 1);
    ordered.splice(ordered.indexOf(targetId), 0, dragId);
    ordered.forEach(function (id, i) { state.widgets[id].order = i; el(id).style.order = i; });
    widgets.forEach(function (w) { w.classList.remove('is-drop-target'); });
    persist();
  });

  /* ---- dock: minimized chips ---- */
  var chips = os.querySelector('[data-home-chips]');
  function renderChips() {
    if (!chips) return; chips.innerHTML = '';
    widgets.forEach(function (w) {
      var id = w.getAttribute('data-home-widget'), st = state.widgets[id];
      if (st.visible && st.minimized) {
        var title = w.querySelector('.home-widget__title');
        var c = document.createElement('button'); c.className = 'home-dock__chip'; c.type = 'button';
        c.innerHTML = title ? title.innerHTML : id;
        c.addEventListener('click', function () { setWidget(id, { minimized: false }); focusWidget(id); });
        chips.appendChild(c);
      }
    });
  }
  function focusWidget(id) {
    var e = el(id); if (!e) return; e.scrollIntoView({ behavior: 'smooth', block: 'center' });
    widgets.forEach(function (w) { w.classList.toggle('is-active', w === e); });
    setTimeout(function () { e.classList.remove('is-active'); }, 1600);
  }

  /* ---- dock: accent / density / reset / clock ---- */
  function applyAccent(hex) {
    if (!hex) return;
    document.documentElement.style.setProperty('--zer0-color-accent', hex);
    os.querySelectorAll('[data-home-accents] button').forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-accent') === hex ? 'true' : 'false'); });
  }
  applyAccent(loadStr(AKEY, null));
  os.querySelectorAll('[data-home-accents] button').forEach(function (b) {
    b.addEventListener('click', function () { var hex = b.getAttribute('data-accent'); try { localStorage.setItem(AKEY, hex); } catch (e) {} applyAccent(hex); });
  });
  var densityBtn = os.querySelector('[data-home-density]');
  if (densityBtn) densityBtn.addEventListener('click', function () { state.density = state.density === 'compact' ? 'comfortable' : 'compact'; os.setAttribute('data-density', state.density); persist(); });
  var resetBtn = os.querySelector('[data-home-reset]');
  if (resetBtn) resetBtn.addEventListener('click', function () { if (confirm('Reset the desktop layout to defaults?')) { localStorage.removeItem(LKEY); location.reload(); } });
  var clock = os.querySelector('[data-home-clock]');
  function tick() { if (clock) { var d = new Date(); clock.textContent = ('0' + d.getHours()).slice(-2) + ':' + ('0' + d.getMinutes()).slice(-2); } }
  tick(); setInterval(tick, 20000);

  /* ---- launcher (Cmd+K / "/") ---- */
  var launcher = os.querySelector('[data-home-launcher]');
  var lInput = os.querySelector('[data-home-launch-input]');
  var lResults = os.querySelector('[data-home-launch-results]');
  function buildIndex() {
    var items = [];
    widgets.forEach(function (w) {
      var id = w.getAttribute('data-home-widget'), st = state.widgets[id];
      var t = w.querySelector('.home-widget__title'); var label = t ? t.textContent.trim() : id;
      items.push({ kind: 'widget', id: id, label: label, hint: st.visible ? (st.minimized ? 'minimized' : 'open') : 'hidden' });
    });
    os.querySelectorAll('[data-home-shortcuts] [data-launch-label]').forEach(function (a) {
      items.push({ kind: 'link', label: a.getAttribute('data-launch-label'), url: a.getAttribute('href'), hint: 'shortcut' });
    });
    return items;
  }
  var lIdx = [], lActive = 0;
  function openLauncher() { if (!launcher) return; lIdx = buildIndex(); launcher.hidden = false; lInput.value = ''; renderLauncher(''); lInput.focus(); }
  function closeLauncher() { if (launcher) launcher.hidden = true; }
  function renderLauncher(q) {
    q = (q || '').toLowerCase();
    var list = lIdx.filter(function (it) { return it.label.toLowerCase().indexOf(q) !== -1; });
    lActive = 0; lResults.innerHTML = '';
    list.forEach(function (it, i) {
      var li = document.createElement('li'); li.className = i === 0 ? 'is-active' : '';
      li.innerHTML = '<i class="bi bi-' + (it.kind === 'widget' ? 'window' : 'box-arrow-up-right') + '"></i> <span>' + it.label + '</span> <small>' + it.hint + '</small>';
      li.addEventListener('click', function () { runItem(it); });
      lResults.appendChild(li);
    });
    lResults._list = list;
  }
  function runItem(it) {
    if (it.kind === 'link') { if (/^https?:/.test(it.url)) window.open(it.url, '_blank'); else location.href = it.url; closeLauncher(); return; }
    setWidget(it.id, { visible: true, minimized: false }); focusWidget(it.id); closeLauncher();
  }
  os.querySelectorAll('[data-home-launch]').forEach(function (b) { b.addEventListener('click', openLauncher); });
  document.addEventListener('keydown', function (ev) {
    if ((ev.metaKey || ev.ctrlKey) && ev.key.toLowerCase() === 'k') { ev.preventDefault(); openLauncher(); return; }
    if (ev.key === '/' && document.activeElement === document.body) { ev.preventDefault(); openLauncher(); return; }
    if (launcher && !launcher.hidden) {
      if (ev.key === 'Escape') closeLauncher();
      else if (ev.key === 'ArrowDown' || ev.key === 'ArrowUp') {
        ev.preventDefault(); var items = lResults.children; if (!items.length) return;
        items[lActive].classList.remove('is-active');
        lActive = (lActive + (ev.key === 'ArrowDown' ? 1 : items.length - 1)) % items.length;
        items[lActive].classList.add('is-active'); items[lActive].scrollIntoView({ block: 'nearest' });
      } else if (ev.key === 'Enter') { var l = lResults._list; if (l && l[lActive]) runItem(l[lActive]); }
    }
  });
  if (lInput) lInput.addEventListener('input', function () { renderLauncher(lInput.value); });
  if (launcher) launcher.addEventListener('click', function (e) { if (e.target === launcher) closeLauncher(); });

  /* ---- github tabs ---- */
  os.querySelectorAll('[data-gh-tabs]').forEach(function (tabs) {
    var wrap = tabs.closest('.hw-gh');
    tabs.querySelectorAll('[data-gh-tab]').forEach(function (tab) {
      tab.addEventListener('click', function () {
        var k = tab.getAttribute('data-gh-tab');
        tabs.querySelectorAll('[data-gh-tab]').forEach(function (t) { t.classList.toggle('is-active', t === tab); });
        wrap.querySelectorAll('[data-gh-panel]').forEach(function (p) { p.hidden = p.getAttribute('data-gh-panel') !== k; });
      });
    });
  });

  /* ---- per-widget persistence: notes / goals / status ---- */
  var notes = os.querySelector('[data-home-notes]'), notesSaved = os.querySelector('[data-home-notes-saved]'), nT;
  if (notes) {
    notes.value = loadStr('it-journey-home-notes', '');
    notes.addEventListener('input', function () { clearTimeout(nT); nT = setTimeout(function () { try { localStorage.setItem('it-journey-home-notes', notes.value); } catch (e) {} if (notesSaved) { notesSaved.textContent = 'saved'; setTimeout(function () { notesSaved.textContent = ''; }, 1200); } }, 400); });
  }
  var goalsState = load('it-journey-home-goals', {});
  os.querySelectorAll('[data-home-goal]').forEach(function (cb) {
    var id = cb.getAttribute('data-home-goal'); if (goalsState[id] != null) cb.checked = goalsState[id];
    cb.addEventListener('change', function () { goalsState[id] = cb.checked; save('it-journey-home-goals', goalsState); });
  });
  var status = os.querySelector('[data-home-status]');
  if (status) { var s = loadStr('it-journey-home-status', null); if (s != null) status.value = s; status.addEventListener('change', function () { try { localStorage.setItem('it-journey-home-status', status.value); } catch (e) {} }); }

  /* ---- client-side GitHub freshness (unauthenticated, cached, silent) ---- */
  (function freshen() {
    var fields = os.querySelectorAll('[data-gh-field]'); if (!fields.length) return;
    var CK = 'it-journey-home-gh-cache', TTL = 30 * 60 * 1000;
    function patch(p) { if (!p) return; fields.forEach(function (n) { var f = n.getAttribute('data-gh-field'); if (p[f] != null) n.textContent = p[f]; }); }
    var c = load(CK, null);
    if (c && c.ts && (Date.now() - c.ts) < TTL) { patch(c.profile); return; }
    fetch('https://api.github.com/users/bamr87').then(function (r) { return r.ok ? r.json() : null; }).then(function (p) {
      if (!p) return; var prof = { followers: p.followers, public_repos: p.public_repos };
      save(CK, { ts: Date.now(), profile: prof }); patch(prof);
    }).catch(function () {});
  })();

  /* ---- public API ---- */
  window.HomeOS = {
    getLayout: function () { return JSON.parse(JSON.stringify(state)); },
    setWidget: setWidget,
    resetLayout: function () { localStorage.removeItem(LKEY); location.reload(); },
    export: function () { var b = new Blob([JSON.stringify(state, null, 2)], { type: 'application/json' }); var u = URL.createObjectURL(b); var a = document.createElement('a'); a.href = u; a.download = 'it-journey-home-layout.json'; a.click(); URL.revokeObjectURL(u); },
    import: function (json) { try { var d = typeof json === 'string' ? JSON.parse(json) : json; if (d && d.widgets) { state = d; save(LKEY, state); applyAll(); return true; } } catch (e) {} return false; }
  };

  applyAll();
})();

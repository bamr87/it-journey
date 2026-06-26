/*
 * quest-dashboard.js — behaviour for the /quests/home/ Overworld dashboard.
 *
 * Layers on top of quest-progress.js (which owns per-quest completion in
 * localStorage). This module owns *display* preferences and personalization:
 *   - which sections are shown/hidden  (Customize panel)
 *   - which sections are expanded       (collapse memory)
 *   - the accent colour                 (also mirrored site-wide via user-overrides.js)
 *   - live "Completed / % done" stats from the quest-progress store
 *
 * All prefs persist in localStorage so they carry across sessions and pages.
 *   it-journey-dash-prefs : { hidden: [ids], closed: [ids] }
 *   it-journey-accent     : "#22d3ee"   (read by user-overrides.js too)
 */
(function () {
  'use strict';

  var PREFS_KEY = 'it-journey-dash-prefs';
  var ACCENT_KEY = 'it-journey-accent';
  var dash = document.querySelector('[data-quest-dash]');
  if (!dash) return;

  function loadPrefs() {
    try { return JSON.parse(localStorage.getItem(PREFS_KEY)) || {}; } catch (e) { return {}; }
  }
  function savePrefs(p) {
    try { localStorage.setItem(PREFS_KEY, JSON.stringify(p)); } catch (e) {}
  }
  var prefs = loadPrefs();
  prefs.hidden = prefs.hidden || [];
  prefs.closed = prefs.closed || [];

  function inList(list, id) { return list.indexOf(id) !== -1; }
  function addTo(list, id) { if (!inList(list, id)) list.push(id); }
  function removeFrom(list, id) { var i = list.indexOf(id); if (i !== -1) list.splice(i, 1); }

  /* ---------- section visibility (Customize toggles) ---------- */
  function applyVisibility() {
    dash.querySelectorAll('[data-dash-section]').forEach(function (sec) {
      var id = sec.getAttribute('data-dash-section');
      sec.hidden = inList(prefs.hidden, id);
    });
    dash.querySelectorAll('[data-dash-section-toggles] input[type="checkbox"]').forEach(function (cb) {
      cb.checked = !inList(prefs.hidden, cb.value);
    });
  }
  dash.querySelectorAll('[data-dash-section-toggles] input[type="checkbox"]').forEach(function (cb) {
    cb.addEventListener('change', function () {
      if (cb.checked) removeFrom(prefs.hidden, cb.value); else addTo(prefs.hidden, cb.value);
      savePrefs(prefs); applyVisibility();
    });
  });

  /* ---------- collapse memory ---------- */
  function setOpen(id, open) {
    var body = document.getElementById('dash-' + id);
    var toggle = dash.querySelector('[data-dash-toggle="' + id + '"]');
    if (!body || !toggle) return;
    body.classList.toggle('show', open);
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
  }
  function applyCollapse() {
    dash.querySelectorAll('[data-dash-section]').forEach(function (sec) {
      var id = sec.getAttribute('data-dash-section');
      if (inList(prefs.closed, id)) setOpen(id, false);
    });
  }
  // Persist on Bootstrap collapse events (covers clicks on the section toggles).
  dash.querySelectorAll('[data-dash-section] .collapse').forEach(function (body) {
    var id = body.id.replace(/^dash-/, '');
    body.addEventListener('shown.bs.collapse', function () { removeFrom(prefs.closed, id); savePrefs(prefs); });
    body.addEventListener('hidden.bs.collapse', function () { addTo(prefs.closed, id); savePrefs(prefs); });
  });

  /* ---------- expand / collapse all ---------- */
  function allSectionIds() {
    return Array.prototype.map.call(dash.querySelectorAll('[data-dash-section]'),
      function (s) { return s.getAttribute('data-dash-section'); });
  }
  var expandAll = dash.querySelector('[data-dash-expand-all]');
  var collapseAll = dash.querySelector('[data-dash-collapse-all]');
  if (expandAll) expandAll.addEventListener('click', function () {
    prefs.closed = []; savePrefs(prefs); allSectionIds().forEach(function (id) { setOpen(id, true); });
  });
  if (collapseAll) collapseAll.addEventListener('click', function () {
    prefs.closed = allSectionIds(); savePrefs(prefs); prefs.closed.forEach(function (id) { setOpen(id, false); });
  });

  /* ---------- Customize panel toggle ---------- */
  var customizeBtn = dash.querySelector('[data-dash-customize]');
  var settings = dash.querySelector('[data-dash-settings]');
  if (customizeBtn && settings) {
    customizeBtn.addEventListener('click', function () {
      var open = settings.classList.toggle('show');
      customizeBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  /* ---------- accent personalization ---------- */
  function applyAccent(hex) {
    if (!hex) return;
    dash.style.setProperty('--qd-accent', hex);
    // mirror site-wide (user-overrides.js applies it on every page from this key)
    document.documentElement.style.setProperty('--zer0-color-accent', hex);
    dash.querySelectorAll('[data-dash-accents] button').forEach(function (b) {
      b.setAttribute('aria-pressed', b.getAttribute('data-accent') === hex ? 'true' : 'false');
    });
  }
  var savedAccent = null;
  try { savedAccent = localStorage.getItem(ACCENT_KEY); } catch (e) {}
  if (savedAccent) applyAccent(savedAccent);
  dash.querySelectorAll('[data-dash-accents] button').forEach(function (b) {
    b.addEventListener('click', function () {
      var hex = b.getAttribute('data-accent');
      try { localStorage.setItem(ACCENT_KEY, hex); } catch (e) {}
      applyAccent(hex);
    });
  });

  /* ---------- progress controls ---------- */
  function qp() { return window.QuestProgress; }
  var exportBtn = dash.querySelector('[data-dash-export]');
  var importBtn = dash.querySelector('[data-dash-import]');
  var importFile = dash.querySelector('[data-dash-import-file]');
  var resetBtn = dash.querySelector('[data-dash-reset]');
  if (exportBtn) exportBtn.addEventListener('click', function () { if (qp()) qp().exportProgress(); });
  if (importBtn && importFile) {
    importBtn.addEventListener('click', function () { importFile.click(); });
    importFile.addEventListener('change', function () {
      var file = importFile.files && importFile.files[0];
      if (!file || !qp()) return;
      var reader = new FileReader();
      reader.onload = function () { if (qp().importProgress(reader.result)) { updateStats(); hydrateStartCards(); } };
      reader.readAsText(file);
    });
  }
  if (resetBtn) resetBtn.addEventListener('click', function () { if (qp() && qp().resetAll()) { updateStats(); hydrateStartCards(); } });

  /* ---------- live stats + start-card completion ---------- */
  function completedCount() {
    if (!qp()) return 0;
    var store = qp().getStore(); var n = 0;
    Object.keys(store).forEach(function (k) {
      if (k.indexOf('/quests/') === 0 && store[k] && store[k].completed) n++;
    });
    return n;
  }
  function updateStats() {
    var total = parseInt(dash.getAttribute('data-quest-total'), 10) || 0;
    var done = completedCount();
    var pct = total === 0 ? 0 : Math.round((done / total) * 100);
    var c = dash.querySelector('[data-dash-stat="completed"]');
    var p = dash.querySelector('[data-dash-stat="percent"]');
    if (c) c.textContent = String(done);
    if (p) p.textContent = pct + '%';
  }
  function hydrateStartCards() {
    if (!qp()) return;
    var store = qp().getStore();
    dash.querySelectorAll('.quest-dash__card[href]').forEach(function (card) {
      var path = card.getAttribute('href');
      try { path = new URL(path, window.location.origin).pathname; } catch (e) {}
      if (path && path.slice(-1) !== '/') path += '/';
      card.classList.toggle('is-complete', !!(store[path] && store[path].completed));
    });
  }

  /* ---------- boot ---------- */
  applyVisibility();
  applyCollapse();
  updateStats();
  hydrateStartCards();
  window.addEventListener('quest-progress:change', function () { updateStats(); hydrateStartCards(); });
})();

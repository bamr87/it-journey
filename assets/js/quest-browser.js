/*
 * quest-browser.js — client-side search / filter / sort for the global quest
 * browser on the /quests/ hub. Operates on the .quest-card elements rendered by
 * _includes/quest-browser.html. No dependencies; degrades to a full static list
 * when JS is disabled.
 */
(function () {
  'use strict';

  var root = document.getElementById('quest-browser');
  if (!root) return;

  var grid = document.getElementById('qb-grid');
  var countEl = document.getElementById('qb-count');
  var emptyEl = document.getElementById('qb-empty');
  var cards = Array.prototype.slice.call(grid.querySelectorAll('.quest-card'));

  var els = {
    search: document.getElementById('qb-search'),
    tier: document.getElementById('qb-tier'),
    level: document.getElementById('qb-level'),
    difficulty: document.getElementById('qb-difficulty'),
    type: document.getElementById('qb-type'),
    skill: document.getElementById('qb-skill'),
    sort: document.getElementById('qb-sort')
  };

  function diffRank(s) {
    s = (s || '').toLowerCase();
    if (s.indexOf('easy') > -1) return 1;
    if (s.indexOf('medium') > -1) return 2;
    if (s.indexOf('hard') > -1) return 3;
    if (s.indexOf('epic') > -1) return 4;
    return 99;
  }

  function timeMinutes(s) {
    s = (s || '').toLowerCase();
    var m = s.match(/\d+/);
    if (!m) return 1e9; // unknown sorts last
    var n = parseInt(m[0], 10);
    if (s.indexOf('hour') > -1) n *= 60;
    return n;
  }

  // Pre-compute sortable / searchable fields once.
  cards.forEach(function (c) {
    c._level = c.dataset.level || '';
    c._diff = diffRank(c.dataset.difficulty);
    c._time = timeMinutes(c.dataset.time);
    c._title = (c.dataset.title || '').toLowerCase();
    c._hay = c._title + ' ' +
      (c.dataset.technology || '').toLowerCase() + ' ' +
      (c.dataset.description || '').toLowerCase();
  });

  function apply() {
    var f = {
      search: els.search.value.toLowerCase().trim(),
      tier: els.tier.value.toLowerCase(),
      level: els.level.value.toLowerCase(),
      difficulty: els.difficulty.value.toLowerCase(),
      type: els.type.value.toLowerCase(),
      skill: els.skill.value.toLowerCase()
    };
    var visible = 0;
    cards.forEach(function (c) {
      var ok = true;
      if (f.tier && (c.dataset.tier || '').toLowerCase() !== f.tier) ok = false;
      if (ok && f.level && (c.dataset.level || '').toLowerCase() !== f.level) ok = false;
      if (ok && f.difficulty && (c.dataset.difficulty || '').toLowerCase().indexOf(f.difficulty) === -1) ok = false;
      if (ok && f.type && (c.dataset.questType || '').toLowerCase() !== f.type) ok = false;
      if (ok && f.skill && (c.dataset.skillFocus || '').toLowerCase() !== f.skill) ok = false;
      if (ok && f.search && c._hay.indexOf(f.search) === -1) ok = false;
      c.classList.toggle('qb-hidden', !ok);
      if (ok) visible++;
    });
    countEl.textContent = visible === cards.length
      ? 'Showing all ' + cards.length + ' quests'
      : 'Showing ' + visible + ' of ' + cards.length + ' quests';
    emptyEl.hidden = visible !== 0;
    grid.hidden = visible === 0;
  }

  function sortCards() {
    var v = els.sort.value;
    var sorted = cards.slice().sort(function (a, b) {
      switch (v) {
        case 'level-desc': return b._level.localeCompare(a._level) || a._title.localeCompare(b._title);
        case 'difficulty-asc': return (a._diff - b._diff) || a._level.localeCompare(b._level);
        case 'difficulty-desc': return (b._diff - a._diff) || a._level.localeCompare(b._level);
        case 'time-asc': return (a._time - b._time) || a._title.localeCompare(b._title);
        case 'title-asc': return a._title.localeCompare(b._title);
        default: return a._level.localeCompare(b._level) || a._title.localeCompare(b._title); // level-asc
      }
    });
    var frag = document.createDocumentFragment();
    sorted.forEach(function (c) { frag.appendChild(c); });
    grid.appendChild(frag);
  }

  function reset() {
    els.search.value = '';
    els.tier.value = '';
    els.level.value = '';
    els.difficulty.value = '';
    els.type.value = '';
    els.skill.value = '';
    apply();
  }

  els.search.addEventListener('input', apply);
  [els.tier, els.level, els.difficulty, els.type, els.skill].forEach(function (el) {
    el.addEventListener('change', apply);
  });
  els.sort.addEventListener('change', sortCards);

  Array.prototype.forEach.call(document.querySelectorAll('.qb-reset'), function (b) {
    b.addEventListener('click', reset);
  });

  Array.prototype.forEach.call(document.querySelectorAll('.qb-view-btn'), function (btn) {
    btn.addEventListener('click', function () {
      var list = btn.dataset.view === 'list';
      grid.classList.toggle('is-list', list);
      Array.prototype.forEach.call(document.querySelectorAll('.qb-view-btn'), function (b) {
        var on = b === btn;
        b.classList.toggle('is-active', on);
        b.setAttribute('aria-pressed', on ? 'true' : 'false');
      });
    });
  });

  sortCards();
  apply();
})();

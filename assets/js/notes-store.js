/*
 * notes-store.js — the visitor's own notes, kept in their own browser.
 *
 * IT-Journey is a static site, so there is no account and no server to hold a
 * reader's work. This module is the whole persistence layer: one versioned blob
 * in localStorage that both the site-wide clipper (assets/js/notes-clipper.js)
 * and the workbench (assets/js/notes-workbench.js) read and write through.
 *
 * Three kinds of thing live on the board, sharing one id space so the board's
 * order array never has to branch on type:
 *
 *   n_…  note  — markdown the reader wrote here
 *   c_…  clip  — a code block or selection captured from a page on this site
 *   p_…  pin   — a reference to a public page (a note, a quest, anything)
 *
 * Public notes are NOT stored here. Those are the markdown files in
 * pages/_notes/ that Jekyll renders for everyone; a pin only points at one.
 *
 * Every read and write is wrapped: private-mode browsers throw on access, and a
 * reader whose storage is full or blocked still gets a working page. Writes are
 * debounced, and a `storage` listener keeps two open tabs in agreement.
 */
(function () {
  'use strict';

  var KEY = 'itj.notes.workbench';
  var VERSION = 1;
  var WRITE_DELAY = 300;

  // localStorage is ~5MB in practice. Warn well before the ceiling so a reader
  // can export rather than discovering the limit when a save silently fails.
  var QUOTA_WARN_BYTES = 4 * 1024 * 1024;

  // ---- shape ---------------------------------------------------------------

  function blank() {
    return {
      v: VERSION,
      notes: {},
      clips: {},
      pins: {},
      board: { order: [], sizes: {}, collapsed: {} },
      prefs: { density: 'comfortable', sort: 'manual', showLibrary: true, lastOpenNoteId: null }
    };
  }

  // Drop any card whose id would be dangerous to use as a property name later.
  // JSON.parse itself is safe, but the ids become bracket keys all over this
  // file, so they are filtered once here rather than guarded at every use.
  function sanitizeBucket(raw) {
    var out = {};
    if (!raw || typeof raw !== 'object') return out;
    Object.keys(raw).forEach(function (id) {
      if (!safeKey(id)) return;
      if (!Object.prototype.hasOwnProperty.call(raw, id)) return;
      if (raw[id] && typeof raw[id] === 'object') out[id] = raw[id];
    });
    return out;
  }

  // Fill in anything a older or hand-edited blob is missing, so callers can
  // always assume every branch exists.
  function normalize(raw) {
    var base = blank();
    if (!raw || typeof raw !== 'object') return base;
    base.notes = sanitizeBucket(raw.notes);
    base.clips = sanitizeBucket(raw.clips);
    base.pins = sanitizeBucket(raw.pins);
    if (raw.board && typeof raw.board === 'object') {
      base.board.order = Array.isArray(raw.board.order) ? raw.board.order.slice() : [];
      base.board.sizes = raw.board.sizes && typeof raw.board.sizes === 'object' ? raw.board.sizes : {};
      base.board.collapsed = raw.board.collapsed && typeof raw.board.collapsed === 'object' ? raw.board.collapsed : {};
    }
    if (raw.prefs && typeof raw.prefs === 'object') {
      for (var k in base.prefs) {
        if (Object.prototype.hasOwnProperty.call(raw.prefs, k)) base.prefs[k] = raw.prefs[k];
      }
    }
    // Drop ids in the order list that no longer have a card, and append any card
    // the list is missing (a clip added from another tab, say).
    base.board.order = base.board.order.filter(function (id) { return !!lookup(base, id); });
    ['notes', 'clips', 'pins'].forEach(function (bucket) {
      Object.keys(base[bucket]).forEach(function (id) {
        if (base.board.order.indexOf(id) === -1) base.board.order.push(id);
      });
    });
    return base;
  }

  // Keys that would reach Object.prototype through a bracket assignment. An
  // imported file is just JSON a reader picked off disk, so anything derived
  // from one is treated as hostile before it is written anywhere by name.
  function safeKey(k) {
    return k !== '__proto__' && k !== 'constructor' && k !== 'prototype';
  }

  function bucketFor(id) {
    if (!id) return null;
    if (id.charAt(0) === 'n') return 'notes';
    if (id.charAt(0) === 'c') return 'clips';
    if (id.charAt(0) === 'p') return 'pins';
    return null;
  }

  function lookup(state, id) {
    var b = bucketFor(id);
    return b && state[b] ? state[b][id] : null;
  }

  // ---- storage -------------------------------------------------------------

  var available = true;
  var state = blank();

  function read() {
    try {
      var raw = localStorage.getItem(KEY);
      if (!raw) return blank();
      return normalize(JSON.parse(raw));
    } catch (e) {
      available = false;
      return blank();
    }
  }

  var writeTimer = null;
  var listeners = [];
  var lastWarnedBytes = 0;

  function flush() {
    writeTimer = null;
    if (!available) return;
    var payload;
    try {
      payload = JSON.stringify(state);
    } catch (e) {
      return;
    }
    try {
      localStorage.setItem(KEY, payload);
    } catch (e) {
      // Quota exceeded, or storage turned off mid-session. Keep the in-memory
      // state so the current page still works, and tell anyone listening.
      available = false;
      emit('error', { reason: 'write-failed', bytes: payload.length });
      return;
    }
    if (payload.length > QUOTA_WARN_BYTES && payload.length > lastWarnedBytes * 1.1) {
      lastWarnedBytes = payload.length;
      emit('quota', { bytes: payload.length, limit: QUOTA_WARN_BYTES });
    }
  }

  function persist() {
    if (writeTimer) clearTimeout(writeTimer);
    writeTimer = setTimeout(flush, WRITE_DELAY);
  }

  function emit(kind, detail) {
    var payload = { kind: kind, detail: detail || null, state: state };
    listeners.forEach(function (fn) {
      try { fn(payload); } catch (e) { /* a bad listener must not stop the rest */ }
    });
    try {
      document.dispatchEvent(new CustomEvent('itj-notes:change', { detail: payload }));
    } catch (e) { /* very old browser */ }
  }

  // ---- ids -----------------------------------------------------------------

  var seq = 0;
  function makeId(prefix) {
    seq += 1;
    return prefix + '_' + Date.now().toString(36) + seq.toString(36) + Math.floor(Math.random() * 1296).toString(36);
  }

  function nowIso() {
    return new Date().toISOString();
  }

  // ---- mutations -----------------------------------------------------------

  function place(id, atFront) {
    if (state.board.order.indexOf(id) !== -1) return;
    if (atFront) state.board.order.unshift(id);
    else state.board.order.push(id);
  }

  function addNote(fields) {
    var f = fields || {};
    var id = makeId('n');
    state.notes[id] = {
      id: id,
      title: f.title || 'Untitled note',
      body: f.body || '',
      tags: Array.isArray(f.tags) ? f.tags.slice() : [],
      color: f.color || 'default',
      created: f.created || nowIso(),
      updated: f.updated || nowIso()
    };
    place(id, true);
    persist();
    emit('add', { id: id, type: 'note' });
    return id;
  }

  function addClip(fields) {
    var f = fields || {};
    var id = makeId('c');
    state.clips[id] = {
      id: id,
      kind: f.kind === 'code' ? 'code' : 'text',
      text: f.text || '',
      lang: f.lang || '',
      heading: f.heading || '',
      sourceUrl: f.sourceUrl || '',
      sourceTitle: f.sourceTitle || '',
      sourceCollection: f.sourceCollection || '',
      created: f.created || nowIso()
    };
    place(id, true);
    persist();
    emit('add', { id: id, type: 'clip' });
    return id;
  }

  function addPin(fields) {
    var f = fields || {};
    if (!f.url) return null;
    // A page is pinned once. Re-pinning surfaces the card already on the board.
    var existing = null;
    Object.keys(state.pins).forEach(function (id) {
      if (state.pins[id].url === f.url) existing = id;
    });
    if (existing) return existing;
    var id = makeId('p');
    state.pins[id] = {
      id: id,
      url: f.url,
      title: f.title || f.url,
      collection: f.collection || '',
      description: f.description || '',
      added: f.added || nowIso()
    };
    place(id, true);
    persist();
    emit('add', { id: id, type: 'pin' });
    return id;
  }

  function update(id, patch) {
    var item = lookup(state, id);
    if (!item || !patch) return false;
    Object.keys(patch).forEach(function (k) {
      if (k === 'id' || !safeKey(k)) return;
      if (!Object.prototype.hasOwnProperty.call(patch, k)) return;
      item[k] = patch[k];
    });
    if (bucketFor(id) === 'notes') item.updated = nowIso();
    persist();
    emit('update', { id: id });
    return true;
  }

  function remove(id) {
    var b = bucketFor(id);
    if (!b || !state[b][id]) return false;
    delete state[b][id];
    var at = state.board.order.indexOf(id);
    if (at !== -1) state.board.order.splice(at, 1);
    delete state.board.sizes[id];
    delete state.board.collapsed[id];
    persist();
    emit('remove', { id: id });
    return true;
  }

  // Move `id` so it sits where `beforeId` currently is. With no `beforeId` the
  // card goes to the end. Returns the new order.
  function reorder(id, beforeId) {
    var order = state.board.order;
    var from = order.indexOf(id);
    if (from === -1) return order;
    order.splice(from, 1);
    var to = beforeId ? order.indexOf(beforeId) : -1;
    if (to === -1) order.push(id);
    else order.splice(to, 0, id);
    persist();
    emit('reorder', { id: id });
    return order;
  }

  // Replace the whole arrangement at once — used to undo a keyboard move.
  function setOrder(order) {
    if (!Array.isArray(order)) return false;
    var kept = order.filter(function (id) { return !!lookup(state, id); });
    Object.keys(state.notes).concat(Object.keys(state.clips), Object.keys(state.pins))
      .forEach(function (id) { if (kept.indexOf(id) === -1) kept.push(id); });
    state.board.order = kept;
    persist();
    emit('reorder', { id: null });
    return true;
  }

  function setSize(id, cols, rows) {
    if (!safeKey(id)) return;
    state.board.sizes[id] = [cols, rows];
    persist();
    emit('resize', { id: id });
  }

  function setCollapsed(id, collapsed) {
    if (!safeKey(id)) return;
    if (collapsed) state.board.collapsed[id] = true;
    else delete state.board.collapsed[id];
    persist();
    emit('collapse', { id: id });
  }

  function setPref(key, value) {
    if (!safeKey(key)) return;
    state.prefs[key] = value;
    persist();
    emit('prefs', { key: key });
  }

  function reset() {
    state = blank();
    available = true;
    try { localStorage.removeItem(KEY); } catch (e) { /* nothing to clear */ }
    emit('reset', null);
  }

  // ---- transfer ------------------------------------------------------------

  function exportJson() {
    return JSON.stringify(state, null, 2);
  }

  // Merge an exported blob into the current one. Ids are regenerated so a
  // reader can import the same file twice, or merge two machines, without one
  // set of cards silently overwriting the other.
  function importJson(text, opts) {
    var incoming;
    try {
      incoming = normalize(JSON.parse(text));
    } catch (e) {
      return { ok: false, error: 'That file is not valid workbench JSON.' };
    }
    if (opts && opts.replace) state = blank();
    var counts = { notes: 0, clips: 0, pins: 0 };
    incoming.board.order.forEach(function (oldId) {
      var item = lookup(incoming, oldId);
      if (!item) return;
      var b = bucketFor(oldId);
      if (b === 'notes') { addNote(item); counts.notes += 1; }
      else if (b === 'clips') { addClip(item); counts.clips += 1; }
      else if (b === 'pins' && addPin(item)) { counts.pins += 1; }
    });
    persist();
    emit('import', counts);
    return { ok: true, counts: counts };
  }

  // ---- cross-tab -----------------------------------------------------------

  window.addEventListener('storage', function (ev) {
    if (ev.key !== KEY) return;
    state = read();
    emit('external', null);
  });

  // ---- boot ----------------------------------------------------------------

  state = read();

  window.ITJNotes = {
    KEY: KEY,
    VERSION: VERSION,
    isAvailable: function () { return available; },
    get: function () { return state; },
    count: function () {
      return Object.keys(state.notes).length + Object.keys(state.clips).length + Object.keys(state.pins).length;
    },
    item: function (id) { return lookup(state, id); },
    typeOf: bucketFor,
    addNote: addNote,
    addClip: addClip,
    addPin: addPin,
    update: update,
    remove: remove,
    reorder: reorder,
    setOrder: setOrder,
    setSize: setSize,
    setCollapsed: setCollapsed,
    setPref: setPref,
    reset: reset,
    exportJson: exportJson,
    importJson: importJson,
    subscribe: function (fn) {
      if (typeof fn !== 'function') return function () {};
      listeners.push(fn);
      return function () {
        var at = listeners.indexOf(fn);
        if (at !== -1) listeners.splice(at, 1);
      };
    }
  };
}());

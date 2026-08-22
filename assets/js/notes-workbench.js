/*
 * notes-workbench.js — the /notes/ workbench.
 *
 * Three regions wired to one store (assets/js/notes-store.js):
 *
 *   LIBRARY  every public note, rendered at build time by
 *            _includes/notes/library-static.html and hydrated here into a
 *            filterable, draggable list; plus the reader's own notes and clips,
 *            plus site-wide search results fetched from /search.json.
 *   BOARD    the reader's cards — notes, clips, and pins — arranged by drag or
 *            by keyboard, sized, collapsed, persisted.
 *   EDITOR   a Markdown textarea with autosave, preview, download, and a
 *            "propose this as a public note" hand-off to GitHub.
 *
 * The drag-to-reorder mechanics follow assets/js/home-os.js: the header bar is
 * the drag handle, cards are positioned with CSS `order`, and the state array is
 * what actually moves. Because HTML5 drag is pointer-only, every card also has a
 * keyboard grab mode — see the KEYBOARD section.
 *
 * Rendered note bodies come from assets/js/notes-markdown.js, which escapes its
 * input before doing anything else; that is the only HTML this file injects.
 */
(function () {
  'use strict';

  var root = document.getElementById('notes-workbench');
  if (!root) return;

  var store = window.ITJNotes;
  var md = window.ITJMarkdown;
  if (!store || !md) return;

  var SIZES = [[1, 1], [2, 1], [2, 2], [1, 2], [3, 2]];

  var els = {
    board: root.querySelector('[data-nw-board]'),
    empty: root.querySelector('[data-nw-empty]'),
    library: root.querySelector('[data-nw-library]'),
    filter: root.querySelector('[data-nw-filter]'),
    search: root.querySelector('[data-nw-search]'),
    results: root.querySelector('[data-nw-results]'),
    resultsSection: root.querySelector('[data-nw-results-section]'),
    resultsHint: root.querySelector('[data-nw-results-hint]'),
    mine: root.querySelector('[data-nw-mine]'),
    mineList: root.querySelector('[data-nw-mine-list]'),
    mineCount: root.querySelector('[data-nw-mine-count]'),
    editor: root.querySelector('[data-nw-editor]'),
    editorTitle: root.querySelector('[data-nw-editor-title]'),
    editorTags: root.querySelector('[data-nw-editor-tags]'),
    editorBody: root.querySelector('[data-nw-editor-body]'),
    editorPreview: root.querySelector('[data-nw-editor-preview]'),
    editorSaved: root.querySelector('[data-nw-editor-saved]'),
    toast: root.querySelector('[data-nw-toast]'),
    announce: root.querySelector('[data-nw-announce]'),
    notice: root.querySelector('[data-nw-notice]'),
    importInput: root.querySelector('[data-nw-import]')
  };
  if (!els.board) return;

  var cfg = {
    searchUrl: root.getAttribute('data-search-url') || '/search.json',
    wikiUrl: root.getAttribute('data-wiki-url') || '/assets/data/wiki-index.json',
    repoUrl: root.getAttribute('data-repo-url') || '',
    notesDir: root.getAttribute('data-notes-dir') || 'pages/_notes',
    branch: root.getAttribute('data-default-branch') || 'main'
  };

  var openNoteId = null;

  // ---- helpers -------------------------------------------------------------

  function esc(s) { return md.escapeHtml(s == null ? '' : s); }

  function debounce(fn, ms) {
    var t = null;
    return function () {
      var args = arguments, self = this;
      if (t) clearTimeout(t);
      t = setTimeout(function () { fn.apply(self, args); }, ms);
    };
  }

  function announce(msg) {
    if (els.announce) els.announce.textContent = msg;
  }

  var toastTimer = null;
  function toast(msg) {
    if (!els.toast) return;
    els.toast.textContent = msg;
    els.toast.hidden = false;
    if (toastTimer) clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { els.toast.hidden = true; }, 3200);
  }

  function notice(msg) {
    if (!els.notice) return;
    if (!msg) { els.notice.hidden = true; return; }
    els.notice.textContent = msg;
    els.notice.hidden = false;
  }

  function slugify(s) {
    return String(s || '')
      .toLowerCase()
      .replace(/[^a-z0-9\s-]/g, '')
      .trim()
      .replace(/\s+/g, '-')
      .replace(/-+/g, '-')
      .slice(0, 60) || 'note';
  }

  function download(filename, text, mime) {
    try {
      var blob = new Blob([text], { type: mime || 'application/json' });
      var url = URL.createObjectURL(blob);
      var a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
      return true;
    } catch (e) {
      return false;
    }
  }

  // ---- wiki links ----------------------------------------------------------

  var wikiEntries = null;

  function resolveWiki(name) {
    var key = String(name || '').toLowerCase().trim().replace(/\s+/g, ' ');
    if (!key) return null;
    // A local note by the same title wins: it is the reader's own.
    var state = store.get();
    var hit = null;
    Object.keys(state.notes).forEach(function (id) {
      if (!hit && String(state.notes[id].title || '').toLowerCase().trim() === key) {
        hit = { url: '#' + id, title: state.notes[id].title, local: true };
      }
    });
    if (hit) return hit;
    if (!wikiEntries) return null;
    // Try the exact title or basename first, then the slug — a reader writing
    // [[Bash Cheatsheet]] means the page whose file is bash-cheatsheet.md, even
    // though its full title carries a subtitle after a colon.
    var slug = key.replace(/\s+/g, '-');
    var partial = null;
    for (var i = 0; i < wikiEntries.length; i += 1) {
      var e = wikiEntries[i];
      var title = String(e.title || '').toLowerCase().trim();
      var base = String(e.basename || '').toLowerCase().trim();
      if (title === key || base === key || base === slug) {
        return { url: e.url, title: e.title };
      }
      if (!partial && title.indexOf(key + ':') === 0) partial = e;
    }
    return partial ? { url: partial.url, title: partial.title } : null;
  }
  md.setWikiResolver(resolveWiki);

  function loadWikiIndex() {
    if (!cfg.wikiUrl) return;
    fetch(cfg.wikiUrl, { credentials: 'same-origin' })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (data) {
        if (data && Array.isArray(data.entries)) {
          wikiEntries = data.entries;
          renderBoard(); // re-render so [[links]] that now resolve become links
        }
      })
      .catch(function () { /* the index is theme-generated; the board works without it */ });
  }

  // ---- site search ---------------------------------------------------------

  var searchPromise = null;

  function siteIndex() {
    if (!searchPromise) {
      searchPromise = fetch(cfg.searchUrl, { credentials: 'same-origin' })
        .then(function (r) {
          if (!r.ok) throw new Error('search index unavailable');
          return r.json();
        })
        .catch(function () { return null; });
    }
    return searchPromise;
  }

  function runSearch(term) {
    var q = String(term || '').trim().toLowerCase();
    if (!els.resultsSection) return;
    if (q.length < 2) {
      els.resultsSection.hidden = true;
      return;
    }
    els.resultsSection.hidden = false;
    els.resultsHint.textContent = 'Searching…';
    siteIndex().then(function (docs) {
      if (!docs) {
        els.results.innerHTML = '';
        els.resultsHint.textContent = 'Site search is unavailable right now. The library above still works.';
        return;
      }
      var words = q.split(/\s+/);
      var scored = [];
      for (var i = 0; i < docs.length; i += 1) {
        var d = docs[i];
        if (!d || !d.url || !d.title) continue;
        var hay = (d.title + ' ' + (d.description || '') + ' ' + (d.content || '') + ' ' +
                   (d.tags || []).join(' ') + ' ' + (d.categories || []).join(' ')).toLowerCase();
        var score = 0, ok = true;
        for (var w = 0; w < words.length; w += 1) {
          if (hay.indexOf(words[w]) === -1) { ok = false; break; }
          if (d.title.toLowerCase().indexOf(words[w]) !== -1) score += 5;
          score += 1;
        }
        if (ok) scored.push({ doc: d, score: score });
      }
      scored.sort(function (a, b) { return b.score - a.score; });
      var top = scored.slice(0, 12);
      els.results.innerHTML = '';
      top.forEach(function (row) {
        els.results.appendChild(libraryRow({
          url: row.doc.url,
          title: row.doc.title,
          collection: row.doc.collection || '',
          description: row.doc.description || ''
        }));
      });
      els.resultsHint.textContent = top.length
        ? top.length + ' of ' + scored.length + ' match' + (scored.length === 1 ? '' : 'es')
        : 'Nothing matched “' + q + '”.';
    });
  }

  // ---- library -------------------------------------------------------------

  function libraryRow(item) {
    var li = document.createElement('li');
    li.className = 'nw-lib__item';
    li.setAttribute('data-nw-lib-item', '');
    li.setAttribute('data-nw-url', item.url);
    li.setAttribute('data-nw-title', item.title);
    li.setAttribute('data-nw-collection', item.collection || '');
    li.setAttribute('data-nw-description', item.description || '');
    li.innerHTML =
      '<a class="nw-lib__link" href="' + esc(item.url) + '">' + esc(item.title) + '</a>' +
      (item.collection ? '<span class="nw-lib__badge">' + esc(item.collection) + '</span>' : '') +
      '<button type="button" class="nw-lib__pin" data-nw-pin aria-label="Pin ' + esc(item.title) +
      ' to the board"><i class="bi bi-pin-angle" aria-hidden="true"></i></button>';
    makeRowDraggable(li);
    return li;
  }

  function makeRowDraggable(li) {
    li.setAttribute('draggable', 'true');
    li.addEventListener('dragstart', function (ev) {
      dragKind = 'pin';
      dragPayload = {
        url: li.getAttribute('data-nw-url'),
        title: li.getAttribute('data-nw-title'),
        collection: li.getAttribute('data-nw-collection'),
        description: li.getAttribute('data-nw-description')
      };
      try {
        ev.dataTransfer.setData('text/plain', dragPayload.url);
        ev.dataTransfer.effectAllowed = 'copy';
      } catch (e) { /* older browsers */ }
    });
    li.addEventListener('dragend', function () { dragKind = null; dragPayload = null; });
  }

  function hydrateLibrary() {
    var rows = els.library ? els.library.querySelectorAll('[data-nw-lib-item]') : [];
    Array.prototype.forEach.call(rows, function (li) {
      if (!li.hasAttribute('draggable')) makeRowDraggable(li);
    });
  }

  function renderMine() {
    if (!els.mineList) return;
    var state = store.get();
    var ids = state.board.order.filter(function (id) { return store.typeOf(id) === 'notes'; });
    els.mineList.innerHTML = '';
    ids.forEach(function (id) {
      var n = state.notes[id];
      if (!n) return;
      var li = document.createElement('li');
      li.className = 'nw-lib__item';
      li.setAttribute('data-nw-lib-item', '');
      li.setAttribute('data-nw-title', n.title);
      li.innerHTML = '<button type="button" class="nw-lib__link nw-lib__link--local" data-nw-open="' +
        esc(id) + '">' + esc(n.title || 'Untitled note') + '</button>';
      els.mineList.appendChild(li);
    });
    if (els.mineCount) els.mineCount.textContent = String(ids.length);
    if (els.mine) els.mine.hidden = ids.length === 0;
  }

  function applyFilter(term) {
    var q = String(term || '').trim().toLowerCase();
    var rows = els.library.querySelectorAll('[data-nw-lib-item]');
    Array.prototype.forEach.call(rows, function (li) {
      var hay = ((li.getAttribute('data-nw-title') || '') + ' ' +
                 (li.getAttribute('data-nw-tags') || '') + ' ' +
                 (li.getAttribute('data-nw-description') || '')).toLowerCase();
      li.hidden = q ? hay.indexOf(q) === -1 : false;
    });
    // Collapse a group whose every row is filtered out.
    var groups = els.library.querySelectorAll('.nw-lib__group');
    Array.prototype.forEach.call(groups, function (g) {
      var visible = g.querySelectorAll('[data-nw-lib-item]:not([hidden])').length;
      g.hidden = visible === 0;
    });
  }

  // ---- board ---------------------------------------------------------------

  function cardTitle(id, item) {
    var kind = store.typeOf(id);
    if (kind === 'notes') return item.title || 'Untitled note';
    if (kind === 'pins') return item.title || item.url;
    return item.heading || item.sourceTitle || (item.kind === 'code' ? 'Code clip' : 'Clip');
  }

  function cardBody(id, item) {
    var kind = store.typeOf(id);
    if (kind === 'notes') {
      var html = md.render(item.body || '');
      return html || '<p class="nw-card__hint">Empty note. Click edit to start writing.</p>';
    }
    if (kind === 'pins') {
      return '<p class="nw-card__desc">' + esc(item.description || 'A page on this site.') + '</p>' +
        '<p class="nw-card__link"><a href="' + esc(item.url) + '">' + esc(item.url) + '</a></p>';
    }
    var out = '';
    if (item.kind === 'code') {
      out += '<pre class="nw-card__code"><code>' + esc(item.text) + '</code></pre>';
    } else {
      out += '<blockquote class="nw-card__quote">' + esc(item.text) + '</blockquote>';
    }
    if (item.sourceUrl) {
      out += '<p class="nw-card__source">from <a href="' + esc(item.sourceUrl) + '">' +
        esc(item.sourceTitle || item.sourceUrl) + '</a></p>';
    }
    return out;
  }

  function buildCard(id, index) {
    var state = store.get();
    var item = store.item(id);
    if (!item) return null;
    var kind = store.typeOf(id);
    var size = state.board.sizes[id] || [1, 1];
    var collapsed = !!state.board.collapsed[id];

    var card = document.createElement('article');
    card.className = 'nw-card nw-card--' + kind.slice(0, -1) +
      (collapsed ? ' is-collapsed' : '') +
      (kind === 'notes' && item.color && item.color !== 'default' ? ' nw-card--' + item.color : '');
    card.setAttribute('data-nw-card', id);
    card.style.setProperty('--nw-cols', size[0]);
    card.style.setProperty('--nw-rows', size[1]);
    card.style.order = String(index);

    var title = cardTitle(id, item);
    var icon = kind === 'notes' ? 'bi-journal-text' : (kind === 'pins' ? 'bi-pin-angle-fill' : 'bi-scissors');

    var bar = document.createElement('header');
    bar.className = 'nw-card__bar';
    bar.setAttribute('data-nw-handle', '');
    bar.setAttribute('draggable', 'true');
    bar.innerHTML =
      '<button type="button" class="nw-card__grip" data-nw-grab ' +
        'aria-label="Move ' + esc(title) + '. Press Enter to pick up, then use the arrow keys.">' +
        '<i class="bi bi-grip-vertical" aria-hidden="true"></i></button>' +
      '<i class="bi ' + icon + ' nw-card__icon" aria-hidden="true"></i>' +
      '<h3 class="nw-card__title">' + esc(title) + '</h3>' +
      '<span class="nw-card__actions">' +
        (kind === 'notes'
          ? '<button type="button" class="nw-card__ctl" data-nw-card-action="edit" aria-label="Edit ' + esc(title) + '"><i class="bi bi-pencil" aria-hidden="true"></i></button>'
          : '') +
        (kind === 'clips'
          ? '<button type="button" class="nw-card__ctl" data-nw-card-action="copy" aria-label="Copy this clip"><i class="bi bi-clipboard" aria-hidden="true"></i></button>'
          : '') +
        '<button type="button" class="nw-card__ctl" data-nw-card-action="resize" aria-label="Resize ' + esc(title) + '"><i class="bi bi-arrows-angle-expand" aria-hidden="true"></i></button>' +
        '<button type="button" class="nw-card__ctl" data-nw-card-action="collapse" aria-label="' +
          (collapsed ? 'Expand ' : 'Collapse ') + esc(title) + '" aria-expanded="' + (collapsed ? 'false' : 'true') + '"><i class="bi bi-chevron-' + (collapsed ? 'down' : 'up') + '" aria-hidden="true"></i></button>' +
        '<button type="button" class="nw-card__ctl nw-card__ctl--danger" data-nw-card-action="remove" aria-label="Remove ' + esc(title) + '"><i class="bi bi-x-lg" aria-hidden="true"></i></button>' +
      '</span>';

    var body = document.createElement('div');
    body.className = 'nw-card__body';
    body.innerHTML = cardBody(id, item);

    card.appendChild(bar);
    card.appendChild(body);
    return card;
  }

  function renderBoard() {
    var state = store.get();
    var order = state.board.order;
    // Remove existing cards but keep the empty-state node.
    var existing = els.board.querySelectorAll('[data-nw-card]');
    Array.prototype.forEach.call(existing, function (n) { n.parentNode.removeChild(n); });

    order.forEach(function (id, i) {
      var card = buildCard(id, i);
      if (card) els.board.appendChild(card);
    });

    if (els.empty) els.empty.hidden = order.length > 0;
    els.board.classList.toggle('is-empty', order.length === 0);
    renderMine();
  }

  // ---- drag and drop -------------------------------------------------------

  var dragKind = null;      // 'card' | 'pin'
  var dragPayload = null;
  var dragId = null;

  els.board.addEventListener('dragstart', function (ev) {
    var bar = ev.target.closest ? ev.target.closest('[data-nw-handle]') : null;
    if (!bar) return;
    var card = bar.closest('[data-nw-card]');
    if (!card) return;
    dragKind = 'card';
    dragId = card.getAttribute('data-nw-card');
    card.classList.add('is-dragging');
    try {
      ev.dataTransfer.setData('text/plain', dragId);
      ev.dataTransfer.effectAllowed = 'move';
    } catch (e) { /* older browsers */ }
  });

  els.board.addEventListener('dragend', function () {
    dragKind = null;
    dragId = null;
    clearDropMarks();
  });

  function clearDropMarks() {
    var cards = els.board.querySelectorAll('[data-nw-card]');
    Array.prototype.forEach.call(cards, function (c) {
      c.classList.remove('is-dragging', 'is-drop-target');
    });
    els.board.classList.remove('is-drop-active');
  }

  els.board.addEventListener('dragover', function (ev) {
    if (!dragKind) {
      // A drag from outside the page — plain text becomes a new note.
      ev.preventDefault();
      els.board.classList.add('is-drop-active');
      return;
    }
    ev.preventDefault();
    if (dragKind === 'pin') {
      els.board.classList.add('is-drop-active');
      return;
    }
    var target = ev.target.closest ? ev.target.closest('[data-nw-card]') : null;
    var cards = els.board.querySelectorAll('[data-nw-card]');
    Array.prototype.forEach.call(cards, function (c) {
      c.classList.toggle('is-drop-target',
        !!target && c === target && c.getAttribute('data-nw-card') !== dragId);
    });
  });

  els.board.addEventListener('dragleave', function (ev) {
    if (ev.target === els.board) els.board.classList.remove('is-drop-active');
  });

  els.board.addEventListener('drop', function (ev) {
    ev.preventDefault();
    var target = ev.target.closest ? ev.target.closest('[data-nw-card]') : null;

    if (dragKind === 'card' && dragId) {
      var targetId = target ? target.getAttribute('data-nw-card') : null;
      if (targetId && targetId !== dragId) {
        store.reorder(dragId, targetId);
        renderBoard();
        announce('Card moved.');
      }
    } else if (dragKind === 'pin' && dragPayload) {
      store.addPin(dragPayload);
      renderBoard();
      toast('Pinned “' + dragPayload.title + '”.');
    } else {
      var text = '';
      try { text = ev.dataTransfer.getData('text/plain') || ''; } catch (e) { text = ''; }
      if (text.trim()) {
        var firstLine = text.trim().split('\n')[0].slice(0, 60);
        var id = store.addNote({ title: firstLine || 'Dropped text', body: text });
        renderBoard();
        openEditor(id);
        toast('Note created from dropped text.');
      }
    }
    clearDropMarks();
    dragKind = null;
    dragId = null;
    dragPayload = null;
  });

  // ---- keyboard reordering -------------------------------------------------
  // HTML5 drag never fires for a keyboard user, so the grip button doubles as a
  // grab handle: Enter or Space picks a card up, the arrow keys move it, Enter
  // or Space drops it, Escape puts it back.

  var grabbedId = null;
  var grabOrigin = null;

  function moveGrabbed(delta) {
    var order = store.get().board.order;
    var from = order.indexOf(grabbedId);
    if (from === -1) return;
    var to = from + delta;
    if (to < 0 || to >= order.length) return;
    var beforeId = delta > 0 ? (order[to + 1] || null) : order[to];
    store.reorder(grabbedId, beforeId);
    renderBoard();
    var pos = store.get().board.order.indexOf(grabbedId) + 1;
    announce('Position ' + pos + ' of ' + order.length + '.');
    refocusGrip();
  }

  function refocusGrip() {
    var card = els.board.querySelector('[data-nw-card="' + grabbedId + '"]');
    if (!card) return;
    var grip = card.querySelector('[data-nw-grab]');
    if (grip) grip.focus();
    card.classList.add('is-grabbed');
  }

  function setGrabbed(id) {
    grabbedId = id;
    grabOrigin = id ? store.get().board.order.slice() : null;
    var cards = els.board.querySelectorAll('[data-nw-card]');
    Array.prototype.forEach.call(cards, function (c) {
      var on = c.getAttribute('data-nw-card') === id;
      c.classList.toggle('is-grabbed', on);
      var grip = c.querySelector('[data-nw-grab]');
      if (grip) grip.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
  }

  els.board.addEventListener('keydown', function (ev) {
    var grip = ev.target.closest ? ev.target.closest('[data-nw-grab]') : null;
    if (!grip) return;
    var card = grip.closest('[data-nw-card]');
    if (!card) return;
    var id = card.getAttribute('data-nw-card');

    if (ev.key === 'Enter' || ev.key === ' ' || ev.key === 'Spacebar') {
      ev.preventDefault();
      if (grabbedId === id) {
        setGrabbed(null);
        announce('Card dropped.');
      } else {
        setGrabbed(id);
        announce('Card picked up. Use the arrow keys to move it, then press Enter to drop it.');
      }
      return;
    }

    if (ev.key === 'Escape' && grabbedId === id) {
      ev.preventDefault();
      if (grabOrigin) {
        store.setOrder(grabOrigin);
        renderBoard();
      }
      setGrabbed(null);
      announce('Move cancelled.');
      return;
    }

    if (grabbedId !== id) return;
    if (ev.key === 'ArrowRight' || ev.key === 'ArrowDown') { ev.preventDefault(); moveGrabbed(1); }
    else if (ev.key === 'ArrowLeft' || ev.key === 'ArrowUp') { ev.preventDefault(); moveGrabbed(-1); }
  });

  // ---- card actions --------------------------------------------------------

  els.board.addEventListener('click', function (ev) {
    var btn = ev.target.closest ? ev.target.closest('[data-nw-card-action]') : null;
    if (btn) {
      var card = btn.closest('[data-nw-card]');
      if (!card) return;
      var id = card.getAttribute('data-nw-card');
      var action = btn.getAttribute('data-nw-card-action');
      var state = store.get();

      if (action === 'edit') {
        openEditor(id);
      } else if (action === 'remove') {
        var item = store.item(id);
        var label = item ? cardTitle(id, item) : 'this card';
        if (window.confirm('Remove “' + label + '” from your board?')) {
          store.remove(id);
          if (openNoteId === id) closeEditor();
          renderBoard();
          announce('Card removed.');
        }
      } else if (action === 'resize') {
        var cur = state.board.sizes[id] || [1, 1];
        var at = 0;
        for (var i = 0; i < SIZES.length; i += 1) {
          if (SIZES[i][0] === cur[0] && SIZES[i][1] === cur[1]) { at = i; break; }
        }
        var next = SIZES[(at + 1) % SIZES.length];
        store.setSize(id, next[0], next[1]);
        renderBoard();
      } else if (action === 'collapse') {
        store.setCollapsed(id, !state.board.collapsed[id]);
        renderBoard();
      } else if (action === 'copy') {
        var clip = store.item(id);
        if (clip) copyText(clip.text);
      }
      return;
    }

    // A [[wiki link]] that has no destination yet offers to create the note.
    var create = ev.target.closest ? ev.target.closest('[data-nw-create]') : null;
    if (create) {
      var name = create.getAttribute('data-nw-create');
      var newId = store.addNote({ title: name, body: '' });
      renderBoard();
      openEditor(newId);
      toast('Created “' + name + '”.');
    }
  });

  function copyText(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(
        function () { toast('Copied to the clipboard.'); },
        function () { window.prompt('Copy this:', text); }
      );
    } else {
      window.prompt('Copy this:', text);
    }
  }

  // ---- editor --------------------------------------------------------------

  function openEditor(id) {
    var note = store.item(id);
    if (!note || store.typeOf(id) !== 'notes') return;
    openNoteId = id;
    els.editor.hidden = false;
    els.editorTitle.value = note.title || '';
    els.editorTags.value = (note.tags || []).join(', ');
    els.editorBody.value = note.body || '';
    els.editorPreview.hidden = true;
    els.editorBody.hidden = false;
    root.classList.add('has-editor');
    var toggle = root.querySelector('[data-nw-action="toggle-preview"]');
    if (toggle) toggle.setAttribute('aria-pressed', 'false');
    store.setPref('lastOpenNoteId', id);
    els.editorTitle.focus();
  }

  function closeEditor() {
    openNoteId = null;
    els.editor.hidden = true;
    root.classList.remove('has-editor');
    store.setPref('lastOpenNoteId', null);
  }

  var flashSaved = debounce(function () {
    if (!els.editorSaved) return;
    els.editorSaved.textContent = 'Saved';
    setTimeout(function () {
      if (els.editorSaved) els.editorSaved.textContent = '';
    }, 1400);
  }, 400);

  var syncEditor = debounce(function () {
    if (!openNoteId) return;
    var tags = els.editorTags.value.split(',').map(function (t) { return t.trim(); })
      .filter(function (t) { return !!t; });
    store.update(openNoteId, {
      title: els.editorTitle.value.trim() || 'Untitled note',
      tags: tags,
      body: els.editorBody.value
    });
    renderBoard();
    flashSaved();
  }, 350);

  ['input', 'change'].forEach(function (evt) {
    els.editorTitle.addEventListener(evt, syncEditor);
    els.editorTags.addEventListener(evt, syncEditor);
    els.editorBody.addEventListener(evt, syncEditor);
  });

  els.editorBody.addEventListener('keydown', function (ev) {
    if ((ev.metaKey || ev.ctrlKey) && ev.key.toLowerCase() === 's') {
      ev.preventDefault();
      syncEditor();
      toast('Saved to this browser.');
    }
  });

  // The editor covers the page chrome while it is open, so Escape has to get
  // out of it — from any field inside, not just the textarea.
  els.editor.addEventListener('keydown', function (ev) {
    if (ev.key !== 'Escape' || !openNoteId) return;
    ev.preventDefault();
    var id = openNoteId;
    syncEditor();
    closeEditor();
    var card = els.board.querySelector('[data-nw-card="' + id + '"]');
    var back = card && card.querySelector('[data-nw-card-action="edit"]');
    if (back) back.focus();
  });

  // ---- publish -------------------------------------------------------------
  // A local note becomes a public one through GitHub's prefilled new-file
  // editor. Nothing is sent anywhere until the reader submits it there.

  // The repo's frontmatter gate wants a description of 120-160 characters, so
  // build one from the note and top it up if the note is too short to fill it.
  function describe(body) {
    var TAIL = ' Captured on the IT-Journey notes workbench and proposed for the public collection.';
    var text = md.excerpt(body, 300);
    if (text.length < 120) text = (text ? text + ' —' : 'A working note.') + TAIL;
    if (text.length <= 155) return text;
    var cut = text.slice(0, 155);
    var lastSpace = cut.lastIndexOf(' ');
    return lastSpace > 120 ? cut.slice(0, lastSpace) : cut;
  }

  function frontmatterFor(note) {
    var now = new Date().toISOString().replace(/\.\d+Z$/, '.000Z');
    var title = (note.title || 'Untitled note').slice(0, 60);
    var body = note.body || '';
    var summary = describe(body);
    var tags = (note.tags || []).length ? note.tags : ['notes'];
    var lines = [
      '---',
      'title: ' + JSON.stringify(title),
      'description: ' + JSON.stringify(summary),
      'date: ' + JSON.stringify(now),
      'lastmod: ' + JSON.stringify(now),
      'author: community',
      'categories:',
      '  - notes',
      'tags:'
    ];
    tags.forEach(function (t) { lines.push('  - ' + JSON.stringify(String(t))); });
    lines.push('draft: false');
    lines.push('---');
    lines.push('');
    lines.push(body);
    lines.push('');
    return lines.join('\n');
  }

  function publishNote() {
    if (!openNoteId) return;
    var note = store.item(openNoteId);
    if (!note) return;
    if (!note.body || !note.body.trim()) {
      toast('Add some content before proposing this note.');
      return;
    }
    var content = frontmatterFor(note);
    var filename = cfg.notesDir + '/' + slugify(note.title) + '.md';
    var base = cfg.repoUrl + '/new/' + cfg.branch;
    var url = base + '?filename=' + encodeURIComponent(filename) + '&value=' + encodeURIComponent(content);

    // GitHub rejects very long prefill URLs; hand the reader the text instead.
    if (url.length > 7500) {
      copyText(content);
      window.open(base + '?filename=' + encodeURIComponent(filename), '_blank', 'noopener');
      toast('Note copied — paste it into the GitHub editor that just opened.');
      return;
    }
    window.open(url, '_blank', 'noopener');
    toast('Opened GitHub with your note prefilled.');
  }

  // ---- toolbar -------------------------------------------------------------

  root.addEventListener('click', function (ev) {
    var btn = ev.target.closest ? ev.target.closest('[data-nw-action]') : null;
    if (btn) {
      var action = btn.getAttribute('data-nw-action');

      if (action === 'new-note') {
        var id = store.addNote({ title: 'Untitled note', body: '' });
        renderBoard();
        openEditor(id);
        announce('New note created.');
      } else if (action === 'close-editor') {
        closeEditor();
      } else if (action === 'toggle-preview') {
        var showing = els.editorPreview.hidden === false;
        if (showing) {
          els.editorPreview.hidden = true;
          els.editorBody.hidden = false;
          btn.setAttribute('aria-pressed', 'false');
        } else {
          els.editorPreview.innerHTML = md.render(els.editorBody.value);
          els.editorPreview.hidden = false;
          els.editorBody.hidden = true;
          btn.setAttribute('aria-pressed', 'true');
        }
      } else if (action === 'download-note') {
        if (!openNoteId) return;
        var n = store.item(openNoteId);
        if (n) download(slugify(n.title) + '.md', frontmatterFor(n), 'text/markdown');
      } else if (action === 'publish') {
        publishNote();
      } else if (action === 'toggle-library') {
        var open = root.classList.toggle('is-library-hidden');
        btn.setAttribute('aria-expanded', open ? 'false' : 'true');
        store.setPref('showLibrary', !open);
      } else if (action === 'export') {
        var stamp = new Date().toISOString().slice(0, 10);
        if (download('it-journey-notes-' + stamp + '.json', store.exportJson())) {
          toast('Exported your workbench.');
        } else {
          copyText(store.exportJson());
        }
      } else if (action === 'reset') {
        if (window.confirm('Delete every local note, clip, and pin on this board? Export first if you want a copy.')) {
          store.reset();
          closeEditor();
          renderBoard();
          toast('Board cleared.');
        }
      }
      return;
    }

    var pin = ev.target.closest ? ev.target.closest('[data-nw-pin]') : null;
    if (pin) {
      var li = pin.closest('[data-nw-lib-item]');
      if (!li) return;
      store.addPin({
        url: li.getAttribute('data-nw-url'),
        title: li.getAttribute('data-nw-title'),
        collection: li.getAttribute('data-nw-collection'),
        description: li.getAttribute('data-nw-description')
      });
      renderBoard();
      toast('Pinned “' + li.getAttribute('data-nw-title') + '”.');
      return;
    }

    var open = ev.target.closest ? ev.target.closest('[data-nw-open]') : null;
    if (open) {
      openEditor(open.getAttribute('data-nw-open'));
    }
  });

  if (els.importInput) {
    els.importInput.addEventListener('change', function () {
      var file = els.importInput.files && els.importInput.files[0];
      if (!file) return;
      var reader = new FileReader();
      reader.onload = function () {
        var res = store.importJson(String(reader.result || ''));
        if (res.ok) {
          renderBoard();
          toast('Imported ' + (res.counts.notes + res.counts.clips + res.counts.pins) + ' items.');
        } else {
          toast(res.error);
        }
        els.importInput.value = '';
      };
      reader.readAsText(file);
    });
  }

  if (els.filter) els.filter.addEventListener('input', debounce(function () { applyFilter(els.filter.value); }, 120));
  if (els.search) els.search.addEventListener('input', debounce(function () { runSearch(els.search.value); }, 220));

  // ---- boot ----------------------------------------------------------------

  if (!store.isAvailable()) {
    notice('This browser is blocking local storage, so nothing you add here will be kept after you leave. Everything else still works.');
  }

  store.subscribe(function (payload) {
    if (payload.kind === 'external') {
      renderBoard();
    } else if (payload.kind === 'quota') {
      notice('Your workbench is getting large. Export it and remove a few cards to be safe.');
    } else if (payload.kind === 'error') {
      notice('That change could not be saved — local storage is full or unavailable. Export your notes to keep them.');
    }
  });

  hydrateLibrary();
  renderBoard();
  loadWikiIndex();

  var prefs = store.get().prefs;
  if (prefs.showLibrary === false) {
    root.classList.add('is-library-hidden');
    var lib = root.querySelector('[data-nw-action="toggle-library"]');
    if (lib) lib.setAttribute('aria-expanded', 'false');
  }

  // Arriving from a clip toast or a [[link]] to a local note: #n_… opens it.
  if (window.location.hash && window.location.hash.length > 2) {
    var hashId = window.location.hash.slice(1);
    if (store.item(hashId) && store.typeOf(hashId) === 'notes') openEditor(hashId);
  }

  window.NotesWorkbench = {
    render: renderBoard,
    open: openEditor,
    close: closeEditor,
    store: store
  };
}());

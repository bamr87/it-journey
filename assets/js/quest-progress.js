/*
 * quest-progress.js — Client-side progress tracking for IT-Journey quests.
 *
 * Responsibilities (no backend required):
 *   - Persist per-quest objective checkbox state in localStorage.
 *   - Persist explicit "quest complete" toggle.
 *   - Hydrate `.quest-progress`, `.tier-progress`, `.quest-card`, `.quest-prereq-item`,
 *     and `.quest-path__item` elements on page load.
 *   - React to in-page changes (objective checkbox flips, toggle button click).
 *   - Provide window.QuestProgress.exportProgress() for portfolio backup.
 *
 * Storage shape (single localStorage key):
 *   {
 *     "/quests/0001/foo/": {
 *       completed: true,
 *       completedAt: "2026-01-15T12:34:56.000Z",
 *       objectives: { "0": true, "1": false, ... }
 *     },
 *     ...
 *   }
 */

(function () {
  'use strict';

  var STORAGE_KEY = 'it-journey-quest-progress';

  function loadStore() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      return raw ? JSON.parse(raw) : {};
    } catch (e) {
      console.warn('[quest-progress] failed to read storage', e);
      return {};
    }
  }

  function saveStore(store) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(store));
    } catch (e) {
      console.warn('[quest-progress] failed to write storage', e);
    }
  }

  function getQuest(store, permalink) {
    if (!store[permalink]) {
      store[permalink] = { completed: false, objectives: {}, completedAt: null };
    }
    return store[permalink];
  }

  function normalizePermalink(value) {
    if (!value) return '';
    var v = String(value).trim();
    if (v && !v.endsWith('/')) v += '/';
    return v;
  }

  /* ------------------------------------------------------------------ */
  /* Objective discovery                                                */
  /* ------------------------------------------------------------------ */

  function findObjectiveCheckboxes(root) {
    // Jekyll's kramdown renders `- [ ]` and `- [x]` as <input type="checkbox" disabled>.
    // We re-enable them and assign stable indices.
    return Array.prototype.slice.call(
      root.querySelectorAll('input[type="checkbox"]')
    );
  }

  /* ------------------------------------------------------------------ */
  /* Quest page hydration                                               */
  /* ------------------------------------------------------------------ */

  function hydrateQuestPage(store) {
    var widget = document.querySelector('[data-quest-progress]');
    if (!widget) return;

    var permalink = normalizePermalink(widget.getAttribute('data-quest-permalink'));
    if (!permalink) return;

    var quest = getQuest(store, permalink);
    var content = document.getElementById('quest-content');
    var checkboxes = content ? findObjectiveCheckboxes(content) : [];

    checkboxes.forEach(function (cb, idx) {
      cb.disabled = false;
      cb.dataset.questObjectiveIdx = String(idx);
      if (quest.objectives[idx] === true) {
        cb.checked = true;
      }
      cb.addEventListener('change', function () {
        quest.objectives[idx] = cb.checked;
        recomputeFromObjectives(quest, checkboxes);
        saveStore(store);
        updateQuestWidget(widget, quest, checkboxes.length);
        broadcastChange();
      });
    });

    updateQuestWidget(widget, quest, checkboxes.length);

    var toggle = widget.querySelector('[data-quest-progress-toggle]');
    if (toggle) {
      toggle.addEventListener('click', function () {
        quest.completed = !quest.completed;
        quest.completedAt = quest.completed ? new Date().toISOString() : null;
        if (quest.completed) {
          // Mark all objectives complete for consistency.
          checkboxes.forEach(function (cb, idx) {
            cb.checked = true;
            quest.objectives[idx] = true;
          });
        }
        saveStore(store);
        updateQuestWidget(widget, quest, checkboxes.length);
        broadcastChange();
      });
    }

    var reset = widget.querySelector('[data-quest-progress-reset]');
    if (reset) {
      reset.addEventListener('click', function () {
        if (!confirm('Reset progress for this quest?')) return;
        quest.completed = false;
        quest.completedAt = null;
        quest.objectives = {};
        checkboxes.forEach(function (cb, idx) { cb.checked = false; });
        saveStore(store);
        updateQuestWidget(widget, quest, checkboxes.length);
        broadcastChange();
      });
    }
  }

  function recomputeFromObjectives(quest, checkboxes) {
    if (checkboxes.length === 0) return;
    var allDone = checkboxes.every(function (_, idx) { return quest.objectives[idx] === true; });
    if (allDone && !quest.completed) {
      quest.completed = true;
      quest.completedAt = new Date().toISOString();
    } else if (!allDone && quest.completed) {
      quest.completed = false;
      quest.completedAt = null;
    }
  }

  function updateQuestWidget(widget, quest, totalObjectives) {
    var done = 0;
    Object.keys(quest.objectives).forEach(function (k) {
      if (quest.objectives[k] === true) done++;
    });
    var pct = totalObjectives === 0
      ? (quest.completed ? 100 : 0)
      : Math.round((done / totalObjectives) * 100);

    var fill = widget.querySelector('.quest-progress-bar__fill');
    var label = widget.querySelector('[data-quest-progress-label]');
    var bar = widget.querySelector('.quest-progress-bar');
    var toggle = widget.querySelector('[data-quest-progress-toggle]');
    var toggleLabel = widget.querySelector('.quest-progress__toggle-label');

    if (fill) fill.style.width = pct + '%';
    if (bar) bar.setAttribute('aria-valuenow', String(pct));

    if (label) {
      if (quest.completed) {
        label.textContent = 'Complete · 100%';
      } else if (pct === 0) {
        label.textContent = 'Not started · 0%';
      } else {
        label.textContent = done + ' of ' + totalObjectives + ' · ' + pct + '%';
      }
    }

    widget.classList.toggle('is-complete', quest.completed);

    if (toggle) {
      toggle.setAttribute('aria-pressed', quest.completed ? 'true' : 'false');
    }
    if (toggleLabel) {
      toggleLabel.textContent = quest.completed ? 'Quest complete' : 'Mark quest complete';
    }
  }

  /* ------------------------------------------------------------------ */
  /* Card / prereq / path hydration (cross-page)                        */
  /* ------------------------------------------------------------------ */

  function hydrateCards(store) {
    var cards = document.querySelectorAll('.quest-card');
    cards.forEach(function (card) {
      var url = normalizePermalink(card.querySelector('a') && card.querySelector('a').getAttribute('href'));
      if (!url) return;
      // Map relative path back to canonical permalink (strip baseurl prefix).
      var canonical = normalizeToCanonical(url);
      var quest = store[canonical];
      card.classList.toggle('is-complete', !!(quest && quest.completed));
    });
  }

  function hydratePrereqLists(store) {
    document.querySelectorAll('.quest-prereq-item').forEach(function (item) {
      var url = normalizePermalink(item.getAttribute('data-quest-url'));
      var canonical = normalizeToCanonical(url);
      var quest = store[canonical];
      var done = !!(quest && quest.completed);
      item.classList.toggle('is-complete', done);
      // Locked-state only meaningful for required prereqs.
      var parent = item.closest('[data-quest-prereq]');
      if (parent && parent.getAttribute('data-quest-prereq') === 'required') {
        item.classList.toggle('is-locked', !done);
      }
    });
  }

  function hydratePathTrackers(store) {
    document.querySelectorAll('[data-quest-path]').forEach(function (path) {
      var items = path.querySelectorAll('[data-quest-path-item]');
      var prevComplete = true;
      items.forEach(function (item) {
        var url = normalizeToCanonical(normalizePermalink(item.getAttribute('data-quest-url')));
        var quest = store[url];
        var complete = !!(quest && quest.completed);
        item.classList.toggle('is-complete', complete);
        item.classList.toggle('is-available', prevComplete && !complete);
        item.classList.toggle('is-locked', !prevComplete && !complete);
        prevComplete = complete;
      });
    });
  }

  function hydrateTierBars(store) {
    var bars = document.querySelectorAll('[data-quest-tier-progress]');
    if (bars.length === 0) return;

    var siteQuestData = window.__QUEST_INDEX__ || null;
    bars.forEach(function (bar) {
      var kind = bar.getAttribute('data-quest-tier-kind');
      var scope = bar.getAttribute('data-quest-tier-scope');
      var total = parseInt(bar.querySelector('[data-quest-tier-total]').textContent, 10) || 0;
      var completed = 0;
      Object.keys(store).forEach(function (permalink) {
        if (!store[permalink].completed) return;
        if (!matchesScope(permalink, kind, scope, siteQuestData)) return;
        completed++;
      });
      var pct = total === 0 ? 0 : Math.round((completed / total) * 100);
      var fill = bar.querySelector('.quest-progress-bar__fill');
      var pctEl = bar.querySelector('[data-quest-tier-percent]');
      var completedEl = bar.querySelector('[data-quest-tier-completed]');
      var prog = bar.querySelector('.quest-progress-bar');
      if (fill) fill.style.width = pct + '%';
      if (pctEl) pctEl.textContent = pct + '%';
      if (completedEl) completedEl.textContent = String(completed);
      if (prog) prog.setAttribute('aria-valuenow', String(pct));
    });
  }

  function matchesScope(permalink, kind, scope, index) {
    // Without server-side index the scoping is best-effort: extract level from URL.
    var match = permalink.match(/^\/quests\/([01]{4})\//);
    if (!match) return false;
    var level = match[1];
    if (kind === 'all') return true;
    if (kind === 'level') return level === scope;
    if (kind === 'tier') {
      var tierLevels = (index && index.tiers && index.tiers[scope]) || tierLevelsFromName(scope);
      return tierLevels.indexOf(level) !== -1;
    }
    return false;
  }

  function tierLevelsFromName(name) {
    switch (name) {
      case 'Apprentice': return ['0000', '0001', '0010', '0011'];
      case 'Adventurer': return ['0100', '0101', '0110', '0111'];
      case 'Warrior':    return ['1000', '1001', '1010', '1011'];
      case 'Master':     return ['1100', '1101', '1110', '1111'];
      default: return [];
    }
  }

  function normalizeToCanonical(url) {
    if (!url) return '';
    // Strip optional baseurl prefix and ensure trailing slash.
    try {
      var u = new URL(url, window.location.origin);
      var path = u.pathname;
      if (path && !path.endsWith('/')) path += '/';
      return path;
    } catch (e) {
      return normalizePermalink(url);
    }
  }

  /* ------------------------------------------------------------------ */
  /* Cross-widget change broadcasts                                     */
  /* ------------------------------------------------------------------ */

  function broadcastChange() {
    window.dispatchEvent(new CustomEvent('quest-progress:change'));
  }

  /* ------------------------------------------------------------------ */
  /* Public API                                                         */
  /* ------------------------------------------------------------------ */

  window.QuestProgress = {
    getStore: function () { return loadStore(); },
    exportProgress: function () {
      var data = loadStore();
      var blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
      var url = URL.createObjectURL(blob);
      var a = document.createElement('a');
      a.href = url;
      a.download = 'it-journey-quest-progress-' + new Date().toISOString().slice(0, 10) + '.json';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    },
    importProgress: function (json) {
      try {
        var data = typeof json === 'string' ? JSON.parse(json) : json;
        if (data && typeof data === 'object') {
          saveStore(data);
          broadcastChange();
          return true;
        }
      } catch (e) { console.warn('[quest-progress] import failed', e); }
      return false;
    },
    resetAll: function () {
      if (!confirm('Reset progress for ALL quests? This cannot be undone.')) return false;
      localStorage.removeItem(STORAGE_KEY);
      broadcastChange();
      return true;
    }
  };

  /* ------------------------------------------------------------------ */
  /* Boot                                                               */
  /* ------------------------------------------------------------------ */

  function boot() {
    var store = loadStore();
    hydrateQuestPage(store);
    hydrateCards(store);
    hydratePrereqLists(store);
    hydratePathTrackers(store);
    hydrateTierBars(store);
  }

  window.addEventListener('quest-progress:change', function () {
    var store = loadStore();
    hydrateCards(store);
    hydratePrereqLists(store);
    hydratePathTrackers(store);
    hydrateTierBars(store);
  });

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();

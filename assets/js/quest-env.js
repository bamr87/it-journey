/*
 * quest-env.js — make a quest's instructions follow the reader's machine.
 *
 * A quest documents up to four platform paths and creates a project folder with
 * a name it picked. Only one of those paths is the reader's, and the folder name
 * is theirs to choose. This script turns the declared `environment:` block (see
 * _includes/quest/quest-env.html) into live behavior:
 *
 *   1. DETECT the reader's OS on first visit and preselect it.
 *   2. FILTER the platform sections — the three paths that are not theirs
 *      collapse, so the page reads as if written for their machine.
 *   3. SUBSTITUTE the quest's declared variables (project folder) into every
 *      code snippet, idempotently, from the original text.
 *   4. REMEMBER the choice in localStorage so it carries across quests.
 *
 * Everything degrades safely: without JS every path stays visible, and any quest
 * without an `environment:` block is untouched.
 */
(function () {
  'use strict';

  var KEY = 'itj.quest.env';
  var root = document.getElementById('quest-env');
  if (!root) return;

  var content = document.getElementById('quest-content') || document;
  var declared = {};
  try {
    declared = JSON.parse(root.getAttribute('data-quest-env') || '{}');
  } catch (e) { declared = {}; }

  // Keywords that identify which OS a heading's section belongs to. Matches the
  // detection in scripts/quest/env_migrate.py so page and tooling agree.
  var OS_WORDS = {
    macos: ['macos', 'mac os', 'kingdom'],
    windows: ['windows', 'empire', 'powershell'],
    linux: ['linux', 'territory', 'ubuntu', 'debian'],
    cloud: ['cloud', 'realms', 'container', 'codespace', 'docker']
  };

  // ---- state ---------------------------------------------------------------
  function load() {
    try { return JSON.parse(localStorage.getItem(KEY) || '{}') || {}; }
    catch (e) { return {}; }
  }
  function save(state) {
    try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) { /* private mode */ }
  }

  function detectOS() {
    var p = ((navigator.userAgentData && navigator.userAgentData.platform) ||
             navigator.platform || navigator.userAgent || '').toLowerCase();
    if (p.indexOf('mac') >= 0) return 'macos';
    if (p.indexOf('win') >= 0) return 'windows';
    if (p.indexOf('linux') >= 0 || p.indexOf('x11') >= 0) return 'linux';
    return '';
  }

  var state = load();
  if (!state.os) {
    var guess = detectOS();
    // Only preselect a path this quest actually documents.
    if (guess && (declared.os || []).indexOf(guess) >= 0) {
      state.os = guess;
      state.detected = true;
    }
  }
  state.vars = state.vars || {};

  // ---- platform sections ---------------------------------------------------
  // A "section" is a heading plus every node up to the next heading of the same
  // or higher level — which is exactly how the platform paths are authored.
  function sections() {
    var out = [];
    var heads = content.querySelectorAll('h2, h3, h4');
    for (var i = 0; i < heads.length; i++) {
      var h = heads[i];
      var text = (h.textContent || '').toLowerCase();
      var match = '';
      for (var os in OS_WORDS) {
        if (!Object.prototype.hasOwnProperty.call(OS_WORDS, os)) continue;
        for (var w = 0; w < OS_WORDS[os].length; w++) {
          if (text.indexOf(OS_WORDS[os][w]) >= 0) { match = os; break; }
        }
        if (match) break;
      }
      if (!match) continue;
      var level = parseInt(h.tagName.substring(1), 10);
      var nodes = [h];
      var n = h.nextElementSibling;
      while (n) {
        var tag = n.tagName;
        if (/^H[1-6]$/.test(tag) && parseInt(tag.substring(1), 10) <= level) break;
        nodes.push(n);
        n = n.nextElementSibling;
      }
      out.push({ os: match, nodes: nodes });
      h.setAttribute('data-env-os', match);
    }
    return out;
  }
  var PLATFORM_SECTIONS = sections();

  function applySections(os) {
    for (var i = 0; i < PLATFORM_SECTIONS.length; i++) {
      var sec = PLATFORM_SECTIONS[i];
      var hide = Boolean(os) && sec.os !== os;
      for (var n = 0; n < sec.nodes.length; n++) {
        sec.nodes[n].classList.toggle('quest-env-hidden', hide);
      }
    }
  }

  // ---- variable substitution ----------------------------------------------
  // Rewrites snippets from their ORIGINAL text every time, so switching values
  // back and forth can never compound.
  function applyVars() {
    var names = Object.keys(declared.variables || {});
    if (!names.length) return;
    var blocks = content.querySelectorAll('pre code, code');
    for (var i = 0; i < blocks.length; i++) {
      var el = blocks[i];
      if (!el.hasAttribute('data-env-orig')) el.setAttribute('data-env-orig', el.textContent);
      var text = el.getAttribute('data-env-orig');
      var changed = false;
      for (var v = 0; v < names.length; v++) {
        var name = names[v];
        var dflt = String(declared.variables[name] || '');
        var chosen = String((state.vars && state.vars[name]) || dflt);
        if (!dflt || chosen === dflt) continue;
        var rx = new RegExp(dflt.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g');
        if (rx.test(text)) {
          text = text.replace(rx, chosen);
          changed = true;
        }
      }
      if (changed || el.textContent !== text) el.textContent = text;
    }
  }

  // ---- rendering -----------------------------------------------------------
  var summaryEl = document.getElementById('quest-env-summary');
  var bodyEl = document.getElementById('quest-env-body');
  var toggleEl = document.getElementById('quest-env-toggle');
  var resetEl = document.getElementById('quest-env-reset');

  function labelFor(axis, value) {
    var btn = root.querySelector('.quest-env__opt[data-axis="' + axis + '"][data-value="' + value + '"]');
    return btn ? btn.textContent.trim() : value;
  }

  function render() {
    var opts = root.querySelectorAll('.quest-env__opt');
    for (var i = 0; i < opts.length; i++) {
      var axis = opts[i].getAttribute('data-axis');
      var on = state[axis] === opts[i].getAttribute('data-value');
      opts[i].setAttribute('aria-pressed', on ? 'true' : 'false');
      opts[i].classList.toggle('is-active', on);
    }
    var inputs = root.querySelectorAll('.quest-env__input');
    for (var j = 0; j < inputs.length; j++) {
      var name = inputs[j].getAttribute('data-var');
      var val = (state.vars && state.vars[name]) || inputs[j].getAttribute('data-default');
      if (inputs[j].value !== val) inputs[j].value = val;
    }
    if (summaryEl) {
      if (state.os) {
        var bits = [labelFor('os', state.os)];
        if (state.shell) bits.push(labelFor('shell', state.shell));
        var pd = state.vars && state.vars.project_dir;
        if (pd) bits.push('~/' + pd);
        summaryEl.textContent = bits.join(' · ')
          + (state.detected ? ' (detected)' : '');
      } else {
        summaryEl.textContent = 'Showing every platform path';
      }
    }
    applySections(state.os);
    applyVars();
  }

  // ---- events --------------------------------------------------------------
  root.addEventListener('click', function (e) {
    var opt = e.target.closest ? e.target.closest('.quest-env__opt') : null;
    if (opt) {
      var axis = opt.getAttribute('data-axis');
      var value = opt.getAttribute('data-value');
      state[axis] = (state[axis] === value) ? '' : value;
      state.detected = false;
      save(state);
      render();
      document.dispatchEvent(new CustomEvent('quest-env:change', { detail: state }));
      return;
    }
    if (e.target === toggleEl) {
      var open = bodyEl.hasAttribute('hidden');
      if (open) bodyEl.removeAttribute('hidden'); else bodyEl.setAttribute('hidden', '');
      toggleEl.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggleEl.textContent = open ? 'Done' : 'Configure';
      return;
    }
    if (e.target === resetEl) {
      state = { vars: {} };
      save(state);
      render();
    }
  });

  root.addEventListener('input', function (e) {
    var input = e.target.closest ? e.target.closest('.quest-env__input') : null;
    if (!input) return;
    var name = input.getAttribute('data-var');
    var value = input.value.trim() || input.getAttribute('data-default');
    state.vars = state.vars || {};
    state.vars[name] = value;
    save(state);
    render();
  });

  render();
  // Expose the resolved environment so other quest scripts (and the testing
  // harness driving a real browser) can read what the reader is seeing.
  window.questEnv = { get: function () { return JSON.parse(JSON.stringify(state)); } };
})();

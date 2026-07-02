/* =============================================================================
 * quest-idea-portal.js — the live assist engine for the Quest Idea Forge
 * (/quests/ideas/, source pages/quest-ideas.md).
 *
 * Dependency-free IIFE. Everything here runs client-side against the committed
 * quest registry snapshot (assets/data/quest-network.json): autocomplete,
 * duplicate radar, and a readiness meter that gates the submit button.
 *
 * The readiness rubric MIRRORS scripts/quest/idea_intake.py (the deterministic
 * collector the intake workflow runs server-side). If you tune a point value
 * or the threshold in either file, change the other to match.
 *
 * Submission never leaves this page silently: the submit button opens a
 * prefilled GitHub issue form (.github/ISSUE_TEMPLATE/quest-idea.yml) keyed on
 * the field ids below — GitHub sign-in is the first spam gate, the AI reviewer
 * on the issue is the second.
 * ========================================================================== */
(function () {
  'use strict';

  var root = document.getElementById('quest-idea-portal');
  if (!root) return;

  var READY_THRESHOLD = 70;               // mirrored: idea_intake.py READY_THRESHOLD
  var DRAFT_KEY = 'itj-quest-idea-draft';
  var URL_WARN_LENGTH = 6000;             // GitHub silently truncates very long prefill URLs

  var el = {
    title: document.getElementById('qip-title'),
    suggestTitle: document.getElementById('qip-suggest-title'),
    summary: document.getElementById('qip-summary'),
    summaryCount: document.getElementById('qip-summary-count'),
    why: document.getElementById('qip-why'),
    objectives: document.getElementById('qip-objectives'),
    objectiveStarters: document.getElementById('qip-objective-starters'),
    path: document.getElementById('qip-path'),
    level: document.getElementById('qip-level'),
    difficulty: document.getElementById('qip-difficulty'),
    technologies: document.getElementById('qip-technologies'),
    techList: document.getElementById('qip-tech-list'),
    techChips: document.getElementById('qip-tech-chips'),
    submit: document.getElementById('qip-submit'),
    submitHint: document.getElementById('qip-submit-hint'),
    copy: document.getElementById('qip-copy'),
    spamWarning: document.getElementById('qip-spam-warning'),
    clear: document.getElementById('qip-clear'),
    scoreText: document.getElementById('qip-score-text'),
    scoreBar: document.getElementById('qip-score-bar'),
    progress: document.getElementById('qip-progress'),
    checklist: document.getElementById('qip-checklist'),
    duplicates: document.getElementById('qip-duplicates'),
    preview: document.getElementById('qip-preview')
  };

  var repoUrl = root.dataset.repoUrl || 'https://github.com/bamr87/it-journey';
  var template = root.dataset.template || 'quest-idea.yml';

  var network = { nodes: [] };
  var knownTechs = [];
  var levelCounts = {};

  var OBJECTIVE_VERBS = {
    '': ['Build', 'Automate', 'Debug'],
    frontend: ['Build', 'Style', 'Test'],
    backend: ['Build', 'Expose', 'Test'],
    fullstack: ['Build', 'Connect', 'Deploy'],
    devops: ['Automate', 'Deploy', 'Monitor'],
    security: ['Harden', 'Audit', 'Detect'],
    'data-engineering': ['Ingest', 'Transform', 'Query'],
    cloud: ['Provision', 'Deploy', 'Scale'],
    infrastructure: ['Provision', 'Configure', 'Monitor'],
    'ai-ml': ['Train', 'Evaluate', 'Integrate']
  };

  var LEVELS = ['0000', '0001', '0010', '0011', '0100', '0101', '0110', '0111',
    '1000', '1001', '1010', '1011', '1100', '1101', '1110', '1111'];

  // --- helpers ---------------------------------------------------------------

  function debounce(fn, ms) {
    var t;
    return function () {
      clearTimeout(t);
      var args = arguments, self = this;
      t = setTimeout(function () { fn.apply(self, args); }, ms);
    };
  }

  function objectiveLines(raw) {
    return raw.split('\n')
      .map(function (line) {
        return line.replace(/^\s*(?:[-*+]|\d+[.)])?\s*(?:\[[ xX]\])?\s*/, '').trim();
      })
      .filter(Boolean);
  }

  function techTokens(raw) {
    return raw.split(/[,;\n]+/).map(function (t) { return t.trim().toLowerCase(); }).filter(Boolean);
  }

  function tokenize(text) {
    return (text.toLowerCase().match(/[a-z0-9]{3,}/g) || []);
  }

  function bigrams(s) {
    var out = [];
    var clean = s.toLowerCase().replace(/\s+/g, ' ');
    for (var i = 0; i < clean.length - 1; i++) out.push(clean.slice(i, i + 2));
    return out;
  }

  // Dice coefficient on character bigrams — a close stand-in for the
  // difflib.SequenceMatcher ratio the server-side radar uses.
  function diceSimilarity(a, b) {
    if (!a || !b) return 0;
    var ba = bigrams(a), bb = bigrams(b);
    if (!ba.length || !bb.length) return 0;
    var counts = {};
    ba.forEach(function (g) { counts[g] = (counts[g] || 0) + 1; });
    var hits = 0;
    bb.forEach(function (g) {
      if (counts[g]) { hits++; counts[g]--; }
    });
    return (2 * hits) / (ba.length + bb.length);
  }

  function fields() {
    return {
      title: el.title.value.trim(),
      summary: el.summary.value.trim(),
      why: el.why.value.trim(),
      objectives: el.objectives.value.trim(),
      path: el.path.value.trim(),
      level: el.level.value.trim(),
      difficulty: el.difficulty.value.trim(),
      technologies: el.technologies.value.trim()
    };
  }

  // --- readiness rubric (mirrors idea_intake.py score()) ----------------------

  function rubric(f) {
    var objectives = objectiveLines(f.objectives);
    var techs = techTokens(f.technologies);
    var prose = f.summary + '\n' + f.objectives + '\n' + f.why;
    // Tokenizer mirrored in idea_intake.py score(): [a-z0-9]{3,} tokens for
    // single-word techs, substring scan for hyphenated ones (github-actions).
    var specific = /`[^`\n]+`/.test(prose);
    if (!specific && knownTechs.length) {
      var proseLower = prose.toLowerCase();
      var words = tokenize(prose);
      specific = words.some(function (w) { return knownTechs.indexOf(w) !== -1; }) ||
        knownTechs.some(function (t) { return /[^a-z0-9]/.test(t) && proseLower.indexOf(t) !== -1; });
    }
    var checks = [
      { id: 'summary', label: 'Idea described (80+ chars)', points: 20, earned: f.summary.length >= 80 ? 20 : 0 },
      { id: 'summary_depth', label: 'Idea described in depth (200+ chars)', points: 5, earned: f.summary.length >= 200 ? 5 : 0 },
      { id: 'why', label: 'Outcome / why it matters (40+ chars)', points: 15, earned: f.why.length >= 40 ? 15 : 0 },
      { id: 'objectives', label: 'At least 2 learning objectives', points: 15, earned: objectives.length >= 2 ? 15 : 0 },
      { id: 'objectives_depth', label: '3+ learning objectives', points: 5, earned: objectives.length >= 3 ? 5 : 0 },
      { id: 'path', label: 'Character path chosen', points: 10, earned: f.path ? 10 : 0 },
      { id: 'level', label: 'Binary level chosen', points: 5, earned: f.level ? 5 : 0 },
      { id: 'difficulty', label: 'Difficulty chosen', points: 5, earned: f.difficulty ? 5 : 0 },
      { id: 'technologies', label: 'Tools / technologies named', points: 10, earned: techs.length ? 10 : 0 },
      { id: 'specificity', label: 'Concrete tools or code in the prose', points: 10, earned: specific ? 10 : 0 }
    ];
    var score = checks.reduce(function (sum, c) { return sum + c.earned; }, 0);
    return { score: score, max: 100, checks: checks };
  }

  // --- duplicate radar ---------------------------------------------------------

  function findDuplicates(f) {
    var probeTokens = tokenize(f.title + ' ' + f.summary.slice(0, 160));
    if (!probeTokens.length) return [];
    var hits = [];
    network.nodes.forEach(function (node) {
      var title = String(node.title || '');
      var ratio = diceSimilarity(f.title, title);
      var nodeTokens = tokenize(title);
      var overlap = 0;
      if (nodeTokens.length) {
        var shared = nodeTokens.filter(function (t) { return probeTokens.indexOf(t) !== -1; });
        overlap = shared.length / nodeTokens.length;
      }
      var best = Math.max(ratio, overlap);
      if (best >= 0.55) {
        hits.push({ title: title, permalink: node.id || '', level: node.level || '', similarity: best });
      }
    });
    hits.sort(function (a, b) { return b.similarity - a.similarity; });
    return hits.slice(0, 3);
  }

  // --- issue body / prefill URL --------------------------------------------------

  function existingValue(dupes) {
    return dupes.map(function (d) { return d.title + ' (' + d.permalink + ')'; }).join('; ');
  }

  function issueBody(f, dupes) {
    function section(label, value) {
      return '### ' + label + '\n\n' + (value || '_No response_') + '\n';
    }
    return [
      section("What's the quest idea?", f.summary),
      section('Why does it matter?', f.why),
      section('Learning objectives', f.objectives),
      section('Character path (skill focus)', f.path || 'not sure'),
      section('Level (binary progression)', f.level || 'not sure'),
      section('Difficulty', f.difficulty || 'not sure'),
      section('Tools & technologies', f.technologies),
      section('Similar existing quests you checked', existingValue(dupes))
    ].join('\n');
  }

  function prefillUrl(f, dupes) {
    var params = new URLSearchParams();
    params.set('template', template);
    params.set('title', 'Quest idea: ' + (f.title || ''));
    params.set('summary', f.summary);
    params.set('why', f.why);
    params.set('objectives', f.objectives);
    if (f.path) params.set('path', f.path);
    if (f.level) params.set('level', f.level);
    if (f.difficulty) params.set('difficulty', f.difficulty);
    if (f.technologies) params.set('technologies', f.technologies);
    var existing = existingValue(dupes);
    if (existing) params.set('existing', existing.slice(0, 250));
    return repoUrl + '/issues/new?' + params.toString();
  }

  // --- rendering -----------------------------------------------------------------

  function renderChecklist(r) {
    el.checklist.textContent = '';
    r.checks.forEach(function (c) {
      var li = document.createElement('li');
      var icon = document.createElement('i');
      var done = c.earned > 0;
      icon.className = done ? 'bi bi-check-circle-fill qip-done' : 'bi bi-circle qip-todo';
      var label = document.createElement('span');
      label.textContent = c.label;
      var pts = document.createElement('span');
      pts.className = 'qip-check-pts';
      pts.textContent = c.earned + '/' + c.points;
      li.appendChild(icon);
      li.appendChild(label);
      li.appendChild(pts);
      el.checklist.appendChild(li);
    });
  }

  function renderScore(r) {
    el.scoreText.textContent = r.score + ' / ' + r.max;
    el.scoreBar.style.width = r.score + '%';
    el.progress.setAttribute('aria-valuenow', String(r.score));
    el.scoreBar.className = 'progress-bar ' +
      (r.score >= READY_THRESHOLD ? 'bg-success' : r.score >= 40 ? 'bg-warning' : 'bg-danger');
  }

  function renderDuplicates(dupes, hasInput) {
    el.duplicates.textContent = '';
    if (!hasInput) {
      var idle = document.createElement('p');
      idle.className = 'small text-body-secondary mb-0';
      idle.textContent = 'Start typing a title or description — the radar compares your idea against every published quest.';
      el.duplicates.appendChild(idle);
      return;
    }
    if (!dupes.length) {
      var ok = document.createElement('p');
      ok.className = 'qip-dupe-none mb-0';
      ok.textContent = 'No similar published quest found — clear skies.';
      el.duplicates.appendChild(ok);
      return;
    }
    dupes.forEach(function (d) {
      var div = document.createElement('div');
      div.className = 'qip-dupe';
      var link = document.createElement('a');
      link.href = d.permalink;
      link.textContent = d.title;
      link.target = '_blank';
      link.rel = 'noopener';
      var meta = document.createElement('span');
      meta.className = 'text-body-secondary';
      meta.textContent = ' — level ' + d.level + ', ' + Math.round(d.similarity * 100) + '% similar';
      div.appendChild(link);
      div.appendChild(meta);
      el.duplicates.appendChild(div);
    });
  }

  function renderSubmit(r, url) {
    var ready = r.score >= READY_THRESHOLD;
    el.submit.classList.toggle('disabled', !ready);
    el.submit.setAttribute('aria-disabled', String(!ready));
    el.submit.href = ready ? url : '#';
    if (!ready) {
      el.submitHint.textContent = 'The submit button unlocks at a readiness score of ' +
        READY_THRESHOLD + ' — ' + (READY_THRESHOLD - r.score) + ' points to go. ' +
        'Your draft is saved in this browser as you type.';
    } else if (url.length > URL_WARN_LENGTH) {
      el.submitHint.textContent = 'Ready! Heads up: your idea is long, and GitHub may trim ' +
        'a prefilled form — if fields arrive empty, use "Copy issue markdown" and paste instead.';
    } else {
      el.submitHint.textContent = 'Ready to file! The button opens a prefilled GitHub issue ' +
        'form — review it there and press Submit. The AI reviewer replies on the issue.';
    }
  }

  // --- assist widgets -----------------------------------------------------------

  function populateLevels() {
    LEVELS.forEach(function (level) {
      var opt = document.createElement('option');
      opt.value = level;
      var count = levelCounts[level] || 0;
      opt.textContent = count ? level + ' · ' + count + ' quests live' : level + ' · uncharted';
      el.level.appendChild(opt);
    });
  }

  function populateTech() {
    var counts = {};
    network.nodes.forEach(function (node) {
      var tech = node.technology;
      (Array.isArray(tech) ? tech : [tech]).forEach(function (t) {
        if (t) counts[String(t).toLowerCase()] = (counts[String(t).toLowerCase()] || 0) + 1;
      });
    });
    knownTechs = Object.keys(counts);
    knownTechs.forEach(function (t) {
      var opt = document.createElement('option');
      opt.value = t;
      el.techList.appendChild(opt);
    });
    var top = knownTechs
      .sort(function (a, b) { return counts[b] - counts[a]; })
      .filter(function (t) { return t !== 'general' && t !== 'reference'; })
      .slice(0, 10);
    top.forEach(function (t) {
      var chip = document.createElement('button');
      chip.type = 'button';
      chip.className = 'qip-chip';
      chip.textContent = '+ ' + t;
      chip.addEventListener('click', function () {
        if (techTokens(el.technologies.value).indexOf(t) === -1) {
          var raw = el.technologies.value.replace(/[\s,;]+$/, '');
          el.technologies.value = raw ? raw + ', ' + t : t;
          update();
        }
      });
      el.techChips.appendChild(chip);
    });
  }

  function renderObjectiveStarters() {
    el.objectiveStarters.textContent = '';
    var verbs = OBJECTIVE_VERBS[el.path.value] || OBJECTIVE_VERBS[''];
    verbs.forEach(function (verb) {
      var chip = document.createElement('button');
      chip.type = 'button';
      chip.className = 'qip-chip';
      chip.textContent = '+ ' + verb + ' …';
      chip.addEventListener('click', function () {
        var value = el.objectives.value.replace(/\s+$/, '');
        el.objectives.value = (value ? value + '\n' : '') + '- ' + verb + ' ';
        el.objectives.focus();
        update();
      });
      el.objectiveStarters.appendChild(chip);
    });
  }

  function suggestTitle() {
    var summary = el.summary.value.trim();
    if (!summary) {
      el.title.placeholder = 'Describe your idea first, then I can suggest a title';
      return;
    }
    var sentence = summary.split(/[.!?\n]/)[0];
    var words = sentence.split(/\s+/).filter(Boolean).slice(0, 8);
    var titled = words.map(function (w, i) {
      if (i === 0 || w.length > 3) return w.charAt(0).toUpperCase() + w.slice(1);
      return w;
    }).join(' ');
    el.title.value = titled.replace(/[,;:]+$/, '');
    update();
  }

  // --- draft persistence -----------------------------------------------------------

  function saveDraft(f) {
    try { localStorage.setItem(DRAFT_KEY, JSON.stringify(f)); } catch (e) { /* private mode */ }
  }

  // The level <select> is empty until the registry fetch populates it, and by
  // then the save debounce may have re-persisted the draft with level: '' —
  // so the draft's level is held in memory, not re-read from localStorage.
  var pendingLevel = '';

  function loadDraft() {
    try {
      var raw = localStorage.getItem(DRAFT_KEY);
      if (!raw) return;
      var f = JSON.parse(raw);
      pendingLevel = f.level || '';
      el.title.value = f.title || '';
      el.summary.value = f.summary || '';
      el.why.value = f.why || '';
      el.objectives.value = f.objectives || '';
      el.path.value = f.path || '';
      el.level.value = f.level || '';
      el.difficulty.value = f.difficulty || '';
      el.technologies.value = f.technologies || '';
    } catch (e) { /* ignore a corrupt draft */ }
  }

  function clearDraft() {
    try { localStorage.removeItem(DRAFT_KEY); } catch (e) { /* ignore */ }
    ['title', 'summary', 'why', 'objectives', 'path', 'level', 'difficulty', 'technologies']
      .forEach(function (key) { el[key].value = ''; });
    update();
  }

  // --- main loop ---------------------------------------------------------------------

  var saveDraftDebounced = debounce(saveDraft, 400);

  // Non-blocking mirror of the conservative server-side spam signals in
  // idea_intake.py spam_flags() — the automated reviewer applies these hard,
  // so warn before submission rather than surprise after.
  function spamWarnings(f) {
    var content = f.summary + '\n' + f.why + '\n' + f.objectives;
    var urls = content.match(/https?:\/\/\S+/g) || [];
    var alpha = content.replace(/[^A-Za-z]/g, '');
    var upper = content.replace(/[^A-Z]/g, '');
    var distinct = {};
    alpha.toLowerCase().split('').forEach(function (ch) { distinct[ch] = true; });
    var warnings = [];
    if (urls.length >= 5) {
      warnings.push('5+ links reads as link spam to the automated reviewer — trim to the essential references.');
    }
    if (content.length >= 60 && alpha.length && upper.length > 0.7 * alpha.length) {
      warnings.push('Mostly-uppercase text trips the automated spam filter — ease off the caps lock.');
    }
    if (alpha.length >= 60 && Object.keys(distinct).length <= 6) {
      warnings.push('This text looks like keyboard mash to the automated reviewer — write it out in full words.');
    }
    return warnings;
  }

  function update() {
    var f = fields();
    var r = rubric(f);
    var dupes = findDuplicates(f);
    renderScore(r);
    renderChecklist(r);
    renderDuplicates(dupes, Boolean(f.title || f.summary));
    el.preview.textContent = '# Quest idea: ' + (f.title || '(untitled)') + '\n\n' + issueBody(f, dupes);
    renderSubmit(r, prefillUrl(f, dupes));
    el.spamWarning.textContent = spamWarnings(f).join(' ');
    el.summaryCount.textContent = f.summary.length + ' characters' +
      (f.summary.length < 80 ? ' (80 unlocks the first check)' : '');
    saveDraftDebounced(f);
  }

  var updateDebounced = debounce(update, 250);

  var copyRestoreTimer = null;

  function copyMarkdown() {
    var f = fields();
    var text = issueBody(f, findDuplicates(f));
    var done = function () {
      if (!el.copy.dataset.originalHtml) el.copy.dataset.originalHtml = el.copy.innerHTML;
      el.copy.innerHTML = '<i class="bi bi-clipboard-check"></i> Copied!';
      if (copyRestoreTimer) clearTimeout(copyRestoreTimer);
      copyRestoreTimer = setTimeout(function () {
        el.copy.innerHTML = el.copy.dataset.originalHtml;
        copyRestoreTimer = null;
      }, 1600);
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done, function () { window.prompt('Copy the issue markdown:', text); });
    } else {
      window.prompt('Copy the issue markdown:', text);
    }
  }

  // --- wire up -------------------------------------------------------------------------

  ['title', 'summary', 'why', 'objectives', 'technologies'].forEach(function (key) {
    el[key].addEventListener('input', updateDebounced);
  });
  ['path', 'level', 'difficulty'].forEach(function (key) {
    el[key].addEventListener('change', function () {
      if (key === 'path') renderObjectiveStarters();
      update();
    });
  });
  el.suggestTitle.addEventListener('click', suggestTitle);
  el.copy.addEventListener('click', copyMarkdown);
  el.clear.addEventListener('click', clearDraft);
  el.submit.addEventListener('click', function (event) {
    if (el.submit.classList.contains('disabled')) event.preventDefault();
  });

  loadDraft();
  renderObjectiveStarters();
  update();

  fetch(root.dataset.networkUrl, { credentials: 'same-origin' })
    .then(function (res) { return res.ok ? res.json() : { nodes: [] }; })
    .then(function (data) {
      network.nodes = data.nodes || [];
      levelCounts = {};
      network.nodes.forEach(function (node) {
        levelCounts[node.level] = (levelCounts[node.level] || 0) + 1;
      });
      populateLevels();
      populateTech();
      // The level <option>s did not exist when the draft was first restored.
      if (pendingLevel && !el.level.value) el.level.value = pendingLevel;
      update();
    })
    .catch(function () {
      populateLevels();   // still usable without the registry: no counts, no radar
      if (pendingLevel && !el.level.value) el.level.value = pendingLevel;
      update();
    });
})();

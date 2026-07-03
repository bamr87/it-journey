---
title: Quest Idea Forge
description: "Forge a new IT-Journey quest idea with live guidance — duplicate radar, readiness scoring, and autocomplete — then submit it for AI refinement in one click."
author: IT-Journey Team
date: '2026-07-02T00:00:00.000Z'
lastmod: '2026-07-02T00:00:00.000Z'
permalink: /quests/ideas/
layout: default
sidebar: false
toc: false
categories: [quests, community]
tags:
  - quests
  - ideas
  - contribution
  - community
keywords:
  - quest ideas
  - submit a quest
  - it-journey community
  - quest idea forge
draft: false
---
<link rel="stylesheet" href="{{ '/assets/css/quest-idea-portal.css' | relative_url }}">

<div id="quest-idea-portal" class="container my-4"
     data-network-url="{{ '/assets/data/quest-network.json' | relative_url }}"
     data-repo-url="https://github.com/bamr87/it-journey"
     data-template="quest-idea.yml">

  <div class="qip-hero mb-4">
    <h1 class="display-5 mb-2"><i class="bi bi-hammer"></i> Quest Idea Forge</h1>
    <p class="lead mb-3">
      Every quest starts as a spark. Shape yours here — the forge suggests, checks for
      duplicates, and scores your idea as you type — then file it in one click.
    </p>
    <div class="row g-3 qip-steps">
      <div class="col-md-4">
        <div class="qip-step h-100">
          <span class="qip-step-num">1</span>
          <strong>Forge it here</strong>
          <p class="mb-0 small">Live assistance while you write: autocomplete from the quest
          registry, a duplicate radar, and a readiness meter with concrete tips.</p>
        </div>
      </div>
      <div class="col-md-4">
        <div class="qip-step h-100">
          <span class="qip-step-num">2</span>
          <strong>File it on GitHub</strong>
          <p class="mb-0 small">One click opens a prefilled issue form (GitHub sign-in
          required — that is the first spam gate). Nothing is sent until you submit there.</p>
        </div>
      </div>
      <div class="col-md-4">
        <div class="qip-step h-100">
          <span class="qip-step-num">3</span>
          <strong>AI refines it</strong>
          <p class="mb-0 small">A Claude reviewer reads every submission: strong ideas get
          polished into forge-ready proposals, thin ones get coaching questions, spam gets
          declined. Maintainers promote the best into real quests.</p>
        </div>
      </div>
    </div>
  </div>

  <div class="row g-4">
    <div class="col-lg-7">
      <div class="card qip-card">
        <div class="card-body">
          <h2 class="h4 mb-3"><i class="bi bi-pencil-square"></i> Your idea</h2>

          <div class="mb-3">
            <div class="d-flex align-items-center mb-1">
              <label for="qip-title" class="form-label mb-0">Quest title</label>
              <button type="button" id="qip-suggest-title" class="btn btn-sm btn-outline-secondary qip-suggest-btn" title="Suggest a title from your description">
                <i class="bi bi-stars"></i> Suggest
              </button>
            </div>
            <input type="text" class="form-control" id="qip-title" maxlength="80"
                   placeholder="Build a Self-Healing Uptime Monitor">
          </div>

          <div class="mb-3">
            <label for="qip-summary" class="form-label">What's the quest idea? <span class="text-danger">*</span></label>
            <textarea class="form-control" id="qip-summary" rows="5"
                      placeholder="What will the learner build or do? Concrete beats grand — name the tools, the steps, the artifact they end up with."></textarea>
            <div class="form-text" id="qip-summary-count">0 characters</div>
          </div>

          <div class="mb-3">
            <label for="qip-why" class="form-label">Why does it matter? <span class="text-danger">*</span></label>
            <textarea class="form-control" id="qip-why" rows="2"
                      placeholder="The payoff. What can the learner do afterwards that they couldn't before?"></textarea>
          </div>

          <div class="mb-3">
            <label for="qip-objectives" class="form-label">Learning objectives <span class="text-danger">*</span> <span class="text-body-secondary small">(one per line)</span></label>
            <textarea class="form-control" id="qip-objectives" rows="4"
                      placeholder="- Schedule a GitHub Actions cron workflow&#10;- Trigger a rollback from a workflow&#10;- Open and label an incident issue automatically"></textarea>
            <div class="qip-chips mt-2" id="qip-objective-starters" aria-label="Objective starters"></div>
          </div>

          <div class="row g-3 mb-3">
            <div class="col-sm-4">
              <label for="qip-path" class="form-label">Character path</label>
              <select class="form-select" id="qip-path">
                <option value="">not sure</option>
                <option>frontend</option>
                <option>backend</option>
                <option>fullstack</option>
                <option>devops</option>
                <option>security</option>
                <option>data-engineering</option>
                <option>cloud</option>
                <option>infrastructure</option>
                <option>ai-ml</option>
              </select>
            </div>
            <div class="col-sm-4">
              <label for="qip-level" class="form-label">Level (binary)</label>
              <select class="form-select" id="qip-level">
                <option value="">not sure</option>
              </select>
            </div>
            <div class="col-sm-4">
              <label for="qip-difficulty" class="form-label">Difficulty</label>
              <select class="form-select" id="qip-difficulty">
                <option value="">not sure</option>
                <option>🟢 Easy</option>
                <option>🟡 Medium</option>
                <option>🔴 Hard</option>
                <option>⚔️ Epic</option>
              </select>
            </div>
          </div>

          <div class="mb-3">
            <label for="qip-technologies" class="form-label">Tools &amp; technologies <span class="text-body-secondary small">(comma-separated)</span></label>
            <input type="text" class="form-control" id="qip-technologies"
                   list="qip-tech-list" placeholder="bash, docker, git">
            <datalist id="qip-tech-list"></datalist>
            <div class="qip-chips mt-2" id="qip-tech-chips" aria-label="Popular technologies"></div>
          </div>

          <div class="d-flex flex-wrap gap-2 align-items-center mt-4">
            <a id="qip-submit" class="btn btn-primary disabled" href="#" target="_blank" rel="noopener"
               aria-disabled="true">
              <i class="bi bi-box-arrow-up-right"></i> Open GitHub issue (prefilled)
            </a>
            <button type="button" id="qip-copy" class="btn btn-outline-secondary">
              <i class="bi bi-clipboard"></i> Copy issue Markdown
            </button>
            <button type="button" id="qip-clear" class="btn btn-outline-danger btn-sm ms-auto">
              <i class="bi bi-trash3"></i> Clear draft
            </button>
          </div>
          <p class="small text-body-secondary mt-2 mb-0" id="qip-submit-hint">
            The submit button unlocks at a readiness score of 70 — the meter on the right
            shows exactly what's missing. Your draft is saved in this browser as you type.
          </p>
          <p class="small text-warning mt-1 mb-0" id="qip-spam-warning" aria-live="polite"></p>
        </div>
      </div>
    </div>

    <div class="col-lg-5">
      <div class="card qip-card mb-4">
        <div class="card-body">
          <h2 class="h5 mb-2"><i class="bi bi-speedometer2"></i> Readiness
            <span class="float-end" id="qip-score-text" aria-live="polite">0 / 100</span>
          </h2>
          <div class="progress qip-progress" role="progressbar" aria-label="Idea readiness score"
               aria-valuemin="0" aria-valuemax="100" aria-valuenow="0" id="qip-progress">
            <div class="progress-bar" id="qip-score-bar" style="width: 0%"></div>
          </div>
          <ul class="list-unstyled mt-3 mb-0 qip-checklist" id="qip-checklist"></ul>
        </div>
      </div>

      <div class="card qip-card mb-4">
        <div class="card-body">
          <h2 class="h5 mb-2"><i class="bi bi-radar"></i> Duplicate radar</h2>
          <div id="qip-duplicates" aria-live="polite">
            <p class="small text-body-secondary mb-0">Start typing a title or description —
            the radar compares your idea against every published quest.</p>
          </div>
        </div>
      </div>

      <div class="card qip-card">
        <div class="card-body">
          <h2 class="h5 mb-2"><i class="bi bi-eye"></i> Issue preview</h2>
          <p class="small text-body-secondary mb-2">Exactly what the prefilled GitHub issue
          will contain.</p>
          <pre class="qip-preview mb-0" id="qip-preview">(your idea appears here)</pre>
        </div>
      </div>
    </div>
  </div>

  <noscript>
    <div class="alert alert-info mt-4">
      The interactive forge needs JavaScript. You can still
      <a href="https://github.com/bamr87/it-journey/issues/new?template=quest-idea.yml">file a
      quest idea directly on GitHub</a> — the same AI review runs on every submission.
    </div>
  </noscript>

  <div class="mt-4 small text-body-secondary">
    <p class="mb-1"><i class="bi bi-shield-check"></i> <strong>How gatekeeping works:</strong>
    submitting requires a GitHub account; every submission is scored by a deterministic
    rubric and reviewed by an AI editor that labels it
    <code>idea:ready</code>, <code>idea:needs-detail</code>, or <code>idea:declined</code>.
    A maintainer makes the final call on forging ready ideas into published quests.</p>
    <p class="mb-0"><i class="bi bi-arrow-repeat"></i> <strong>Iterating:</strong> after the
    review lands on your issue, edit it and comment <code>/refine</code> to get another pass.</p>
  </div>
</div>

<script src="{{ '/assets/js/quest-idea-portal.js' | relative_url }}" defer></script>

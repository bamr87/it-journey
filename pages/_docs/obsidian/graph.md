---
title: Obsidian Graph View
permalink: /docs/obsidian/graph/
description: Interactive graph of IT-Journey pages connected by Obsidian-style wiki links.
excerpt: Explore the IT-Journey knowledge graph generated from wiki links across docs, notes, quests, and posts.
categories:
  - docs
  - obsidian
tags:
  - obsidian
  - graph
  - navigation
sidebar:
  nav: docs
toc_sticky: true
backlinks: false
local_graph: false
sitemap: false
lastmod: 2026-04-25T00:00:00.000Z
---

<style>
  #obsidian-graph {
    width: 100%;
    height: 82vh;
    min-height: 620px;
    border: 1px solid var(--bs-border-color, #dee2e6);
    border-radius: var(--bs-border-radius-lg, .5rem);
    background: var(--bs-tertiary-bg, #f8f9fa);
    position: relative;
    overflow: hidden;
  }
  .obsidian-graph-toolbar {
    display: flex;
    flex-wrap: wrap;
    gap: .5rem .75rem;
    align-items: center;
    margin: .75rem 0;
    padding: .625rem .75rem;
    background: var(--bs-tertiary-bg, #f8f9fa);
    border: 1px solid var(--bs-border-color, #dee2e6);
    border-radius: var(--bs-border-radius, .375rem);
  }
  .obsidian-graph-toolbar .form-control {
    max-width: 280px;
    flex: 1 1 200px;
  }
  #obsidian-graph-status {
    flex-basis: 100%;
    font-size: .8125rem;
    color: var(--bs-secondary-color, #6c757d);
    min-height: 1.25rem;
  }
</style>

# Obsidian Graph View

A live, force-directed map of IT-Journey pages connected by `[[wiki links]]`.
The graph is generated from [`assets/data/wiki-index.json`]({{ "/assets/data/wiki-index.json" | relative_url }})
and rendered by the `zer0-mistakes` theme's graph script.

<div id="obsidian-graph-stats" class="mb-2" aria-live="polite"></div>

<div class="obsidian-graph-toolbar">
  <input type="search"
         class="form-control form-control-sm"
         id="obsidian-graph-search"
         placeholder="Filter nodes by title..."
         aria-label="Filter graph nodes by title" />
  <button type="button"
          class="btn btn-outline-secondary btn-sm"
          id="obsidian-graph-fit">
    <i class="bi bi-arrows-fullscreen" aria-hidden="true"></i>
    Reset view
  </button>
  <div class="form-check form-switch">
    <input class="form-check-input"
           type="checkbox"
           role="switch"
           id="obsidian-graph-orphans" />
    <label class="form-check-label" for="obsidian-graph-orphans">
      Show orphans
    </label>
  </div>
  <span id="obsidian-graph-status" role="status"></span>
</div>

<div id="obsidian-graph" role="img" aria-label="IT-Journey knowledge graph"></div>

Use the search box to focus a topic, click a node to open its page, and use
Ctrl/Cmd-click to open a node in a new tab.

<script src="https://cdn.jsdelivr.net/npm/cytoscape@3.30.0/dist/cytoscape.min.js"
        integrity="sha384-kpMsYllYzyaWU69Piok08rPNktpnjqAoDMdB00fjqUkEk3lkuUbSuwJ+oXrjvN6B"
        crossorigin="anonymous"
        defer></script>
<script src="{{ '/assets/js/obsidian-graph.js' | relative_url }}" defer></script>

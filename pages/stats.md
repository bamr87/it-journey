---
title: "IT-Journey Statistics Portal"
description: "Comprehensive analytics and metrics for the IT-Journey knowledge base"
permalink: /stats/
---

<div class="container my-5">
  <div class="row">
    <div class="col-lg-12">
      <h1 class="display-4 mb-4">
        <i class="bi bi-graph-up"></i> Site Statistics Portal
      </h1>
      <p class="lead">
        Comprehensive analytics and insights from the IT-Journey knowledge base
      </p>
      
      {% if site.data.content_statistics %}
        <p class="text-muted">
          <i class="bi bi-clock"></i> 
          Last updated: {{ site.data.content_statistics.generated_at | date: "%B %d, %Y at %I:%M %p" }}
        </p>
      {% else %}
        <div class="alert alert-warning" role="alert">
          <i class="bi bi-exclamation-triangle"></i>
          Statistics not yet generated. Run <code>ruby _data/generate_statistics.rb</code> to create statistics.
        </div>
      {% endif %}
    </div>
  </div>

  {% if site.data.content_statistics %}
  
  <!-- Overview Cards -->
  <div class="row g-4 mb-5">
    <!-- Total Posts Card -->
    <div class="col-md-3">
      <div class="card h-100 border-primary">
        <div class="card-body text-center">
          <i class="bi bi-file-text display-4 text-primary"></i>
          <h2 class="card-title mt-3 mb-0">
            {{ site.data.content_statistics.total_posts }}
          </h2>
          <p class="card-text text-muted">Total Posts</p>
        </div>
      </div>
    </div>

    <!-- Total Categories Card -->
    <div class="col-md-3">
      <div class="card h-100 border-success">
        <div class="card-body text-center">
          <i class="bi bi-folder display-4 text-success"></i>
          <h2 class="card-title mt-3 mb-0">
            {{ site.data.content_statistics.categories | size }}
          </h2>
          <p class="card-text text-muted">Categories</p>
        </div>
      </div>
    </div>

    <!-- Total Tags Card -->
    <div class="col-md-3">
      <div class="card h-100 border-info">
        <div class="card-body text-center">
          <i class="bi bi-tags display-4 text-info"></i>
          <h2 class="card-title mt-3 mb-0">
            {{ site.data.content_statistics.tags | size }}
          </h2>
          <p class="card-text text-muted">Tags</p>
        </div>
      </div>
    </div>

    <!-- Data Freshness Card -->
    <div class="col-md-3">
      <div class="card h-100 border-warning">
        <div class="card-body text-center">
          <i class="bi bi-clock display-4 text-warning"></i>
          <h2 class="card-title mt-3 mb-0">Fresh</h2>
          <p class="card-text text-muted">Data Status</p>
        </div>
      </div>
    </div>
  </div>

  <!-- Categories Section -->
  <div class="row mb-5">
    <div class="col-lg-6">
      <div class="card">
        <div class="card-header bg-primary text-white">
          <h3 class="mb-0">
            <i class="bi bi-folder2-open"></i> Top Categories
          </h3>
        </div>
        <div class="card-body">
          <ul class="list-group list-group-flush">
            {% for category in site.data.content_statistics.categories limit:10 %}
              <li class="list-group-item d-flex justify-content-between align-items-center">
                <span>{{ category[0] | capitalize }}</span>
                <span class="badge bg-primary rounded-pill">{{ category[1] }}</span>
              </li>
            {% endfor %}
          </ul>
        </div>
      </div>
    </div>

    <!-- Tags Section -->
    <div class="col-lg-6">
      <div class="card">
        <div class="card-header bg-success text-white">
          <h3 class="mb-0">
            <i class="bi bi-tags"></i> Top Tags
          </h3>
        </div>
        <div class="card-body">
          <ul class="list-group list-group-flush">
            {% for tag in site.data.content_statistics.tags limit:10 %}
              <li class="list-group-item d-flex justify-content-between align-items-center">
                <span>{{ tag[0] }}</span>
                <span class="badge bg-success rounded-pill">{{ tag[1] }}</span>
              </li>
            {% endfor %}
          </ul>
        </div>
      </div>
    </div>
  </div>

  <!-- Additional Metrics -->
  <div class="row mb-5">
    <div class="col-lg-12">
      <div class="card">
        <div class="card-header bg-info text-white">
          <h3 class="mb-0">
            <i class="bi bi-info-circle"></i> Quick Facts
          </h3>
        </div>
        <div class="card-body">
          <div class="row">
            <div class="col-md-4 mb-3">
              <h5>Content Overview</h5>
              <p>
                <strong>Total Posts:</strong> {{ site.data.content_statistics.total_posts }}<br>
                <strong>Categories:</strong> {{ site.data.content_statistics.categories | size }}<br>
                <strong>Tags:</strong> {{ site.data.content_statistics.tags | size }}
              </p>
            </div>
            <div class="col-md-4 mb-3">
              <h5>Top Category</h5>
              {% assign top_category = site.data.content_statistics.categories | first %}
              <p>
                <strong>{{ top_category[0] | capitalize }}</strong><br>
                <small>{{ top_category[1] }} posts</small>
              </p>
            </div>
            <div class="col-md-4 mb-3">
              <h5>Data Status</h5>
              <p>
                <strong>Last Updated:</strong><br>
                <small>{{ site.data.content_statistics.generated_at | date: "%Y-%m-%d" }}</small>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  {% endif %}

  {% unless site.data.content_statistics %}
  <div class="row">
    <div class="col-lg-12">
      <div class="alert alert-info" role="alert">
        <h4 class="alert-heading">No Statistics Available</h4>
        <p>Statistics haven't been generated yet. To create the statistics data:</p>
        <ol>
          <li>Run the statistics generator: <code>ruby _data/generate_statistics.rb</code></li>
          <li>Refresh this page to see the results</li>
        </ol>
      </div>
    </div>
  </div>
  {% endunless %}
</div>
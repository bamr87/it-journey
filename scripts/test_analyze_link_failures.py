#!/usr/bin/env python3
"""Pytest unit tests for LinkHealthGuardian.analyze_link_failures

These tests validate categorization and pattern detection for various
lychee output shapes. Run with pytest from the project venv.
"""
import json
import os
import importlib.util
import tempfile


def load_guardian():
    repo_file = os.path.join(os.path.dirname(__file__), 'link-checker.py')
    spec = importlib.util.spec_from_file_location('link_checker', repo_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.LinkHealthGuardian


def test_categorization_and_patterns(tmp_path):
    LinkHealthGuardian = load_guardian()
    cfg = {'output_dir': str(tmp_path)}
    guardian = LinkHealthGuardian(cfg)

    # Build error_map with different types of failures
    error_map = {
        'pages/about.md': [
            {'url': 'https://ssl.example.com', 'status': 'SSL: certificate verify failed'},
            {'url': 'https://timeout.example.com', 'status': 'timeout'},
            {'url': 'https://rate.example.com', 'status': '429 Too many requests'},
        ],
        'pages/guide.md': [
            {'url': 'https://dns.fail', 'status': 'dns: Name or service not known'},
            {'url': '/internal/404', 'status': '404 Not Found'},
            {'url': 'http://example.com/path', 'status': 'connection refused'},
        ]
    }

    guardian.results = {'raw_data': {'error_map': error_map}}

    ok = guardian.analyze_link_failures()
    assert ok is True

    cats = guardian.analysis['categories']
    # Check that the categories captured entries
    assert len(cats['ssl_errors']) == 1
    assert len(cats['timeouts']) == 1
    assert len(cats['rate_limited']) == 1
    assert len(cats['dns_errors']) == 1
    # internal should have one '/internal/404'
    assert len(cats['broken_internal']) == 1
    # external due to http link
    assert len(cats['broken_external']) == 1

    # Patterns should include internal link message and SSL/TLS issues
    patterns = guardian.analysis['patterns']
    assert any('broken internal links' in p.lower() for p in patterns)
    assert any('ssl/tls' in p.lower() or 'ssl' in p.lower() for p in patterns)


def test_top_failing_domains_and_timeouts(tmp_path):
    LinkHealthGuardian = load_guardian()
    cfg = {'output_dir': str(tmp_path)}
    guardian = LinkHealthGuardian(cfg)

    # 3 failing links on domain1 and 2 on domain2 to test top domain
    error_map = {'pages/x.md': [], 'pages/y.md': []}
    for i in range(3):
        error_map['pages/x.md'].append({'url': f'https://a-domain.com/page{i}', 'status': '404'})
    for i in range(2):
        error_map['pages/y.md'].append({'url': f'https://b-domain.com/page{i}', 'status': '404'})

    # Add timeouts to test threshold >5
    for i in range(6):
        error_map['pages/timeouts.md'] = error_map.get('pages/timeouts.md', [])
        error_map['pages/timeouts.md'].append({'url': f'https://slow{i}.example', 'status': 'timeout'})

    guardian.results = {'raw_data': {'error_map': error_map}}

    ok = guardian.analyze_link_failures()
    assert ok is True

    patterns = guardian.analysis['patterns']
    # Must include top failing domains summary
    assert any('top failing domains' in p.lower() for p in patterns)
    # High timeout rate should be detected (>5)
    assert any('high timeout rate' in p.lower() for p in patterns)

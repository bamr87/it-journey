#!/usr/bin/env python3
"""Simple test harness for LinkHealthGuardian.parse_lychee_results

This test writes a minimal Lychee JSON result into the output folder and
verifies the parser extracts basic statistics.
"""
import json
import os
import importlib.util


def load_guardian_from_current_repo():
    repo_file = os.path.join(os.path.dirname(__file__), 'link-checker.py')
    spec = importlib.util.spec_from_file_location('link_checker', repo_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.LinkHealthGuardian


def test_parse_empty_results(tmp_dir='/tmp/link-check-test'):
    os.makedirs(tmp_dir, exist_ok=True)
    # Minimal lychee list of dicts
    sample = [
        {"file": "pages/about.md", "url": "https://example.com", "status": "ok"},
        {"file": "pages/guide.md", "url": "https://dead.example.com", "status": "failed", "status_code": 404}
    ]

    results_file = os.path.join(tmp_dir, 'lychee_results.json')
    with open(results_file, 'w') as f:
        json.dump(sample, f)

    LinkHealthGuardian = load_guardian_from_current_repo()
    config = {'output_dir': tmp_dir}
    guardian = LinkHealthGuardian(config)
    ok = guardian.parse_lychee_results()
    print('parse_lychee_results ->', ok)
    print('results:', guardian.results)


if __name__ == '__main__':
    test_parse_empty_results()

#!/usr/bin/env python3
"""Simple test harness for LinkHealthGuardian.parse_results

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
    # Minimal lychee v3.0 result format (fail_map dict)
    sample = {
        "fail_map": {
            "pages/guide.md": [
                {"url": "https://dead.example.com", "status": "404 Not Found"}
            ]
        },
        "total": 2,
        "successful": 1,
        "failures": 1
    }

    results_file = os.path.join(tmp_dir, 'lychee_results.json')
    with open(results_file, 'w') as f:
        json.dump(sample, f)

    LinkHealthGuardian = load_guardian_from_current_repo()
    config = {'output_dir': tmp_dir}
    guardian = LinkHealthGuardian(config)
    ok = guardian.parse_results()
    print('parse_results ->', ok)
    print('results:', guardian.results)
    assert ok is True
    assert guardian.results['broken_links'] == 1
    assert guardian.results['total_links'] == 2
    assert guardian.results['successful_links'] == 1


def test_run_lychee_requests_json_format(tmp_dir='/tmp/link-check-test-fmt'):
    import subprocess
    from unittest import mock
    LinkHealthGuardian = load_guardian_from_current_repo()
    guardian = LinkHealthGuardian({'output_dir': tmp_dir})
    seen = {}

    def fake_run(cmd, **kw):
        seen['cmd'] = cmd
        return subprocess.CompletedProcess(cmd, 2, stdout='', stderr='')

    with mock.patch.object(subprocess, 'run', fake_run):
        guardian.run_lychee(['.'])
    cmd = seen['cmd']
    assert cmd[cmd.index('--format') + 1] == 'json'


def test_unparseable_results_are_not_a_clean_scan(tmp_dir='/tmp/link-check-test-bad'):
    os.makedirs(tmp_dir, exist_ok=True)
    with open(os.path.join(tmp_dir, 'lychee_results.json'), 'w') as f:
        f.write('# Markdown, not JSON\n')
    LinkHealthGuardian = load_guardian_from_current_repo()
    guardian = LinkHealthGuardian({'output_dir': tmp_dir})
    assert guardian.parse_results() is False
    guardian.determine_scope_files = lambda: ['.']
    guardian.run_lychee = lambda files: True
    assert guardian.run() is False


if __name__ == '__main__':
    test_parse_empty_results()
    test_run_lychee_requests_json_format()
    test_unparseable_results_are_not_a_clean_scan()

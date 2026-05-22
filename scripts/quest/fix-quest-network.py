#!/usr/bin/env python3
"""
fix-quest-network.py — Fixes all quest network integrity warnings:
  1. 8 broken reference warnings (invalid quest permalinks in quest_relationships)
  2. 122 orphaned quest warnings (quests not referenced by any other quest)

Strategy for orphaned quests:
  - For each level, a "hub" quest is chosen as the anchor
  - All orphaned quests in that level are added to the hub's child_quests
  - Hub quests for levels without existing anchors are connected via sequel_quests
    from the previous level's anchor
"""

import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent.parent


def read_file(filepath):
    return Path(filepath).read_text(encoding='utf-8')


def write_file(filepath, content):
    Path(filepath).write_text(content, encoding='utf-8')
    print(f"  UPDATED: {filepath}")


def get_frontmatter_bounds(content):
    """Return (start, end) character offsets of the frontmatter block (between dashes)."""
    m = re.match(r'^(---\s*\n)(.*?)(\n---)', content, re.DOTALL)
    if not m:
        return None, None
    return m.start(2), m.end(2)


def get_quest_relationships_block(content):
    """Return the match object for the quest_relationships section in frontmatter."""
    # Matches quest_relationships: and all indented lines below it
    return re.search(
        r'(quest_relationships:\n(?:  [^\n]*\n?(?:  - [^\n]*\n?)*)*)',
        content
    )


def set_child_quests(content, new_children, also_set_sequel=None):
    """
    Update the child_quests list inside quest_relationships.
    If quest_relationships doesn't exist, insert a new block before the closing ---.
    also_set_sequel: optional list to set sequel_quests
    """
    qr_match = get_quest_relationships_block(content)

    if qr_match:
        qr_text = qr_match.group(1)
        # Parse current child_quests
        child_match = re.search(r'  child_quests:\n((?:  - /[^\n]*\n)*)', qr_text)
        sequel_match = re.search(r'  sequel_quests:\n((?:  - /[^\n]*\n)*)', qr_text)

        new_qr = qr_text

        # Build updated child_quests block
        existing_children = []
        if child_match:
            existing_children = re.findall(r'  - (/[^\n]+)', child_match.group(0))
        all_children = existing_children.copy()
        for c in new_children:
            if c not in all_children:
                all_children.append(c)

        if all_children:
            new_child_block = '  child_quests:\n' + ''.join(f'  - {c}\n' for c in all_children)
        else:
            new_child_block = '  child_quests: []\n'

        if child_match:
            new_qr = new_qr.replace(child_match.group(0), new_child_block, 1)
        else:
            # Insert child_quests block - find empty child_quests: []
            new_qr = new_qr.replace('  child_quests: []\n', new_child_block, 1)

        # Build updated sequel_quests if requested
        if also_set_sequel is not None:
            existing_sequels = []
            if sequel_match:
                existing_sequels = re.findall(r'  - (/[^\n]+)', sequel_match.group(0))
            all_sequels = existing_sequels.copy()
            for s in also_set_sequel:
                if s not in all_sequels:
                    all_sequels.append(s)

            if all_sequels:
                new_sequel_block = '  sequel_quests:\n' + ''.join(f'  - {s}\n' for s in all_sequels)
            else:
                new_sequel_block = '  sequel_quests: []\n'

            if sequel_match:
                new_qr = new_qr.replace(sequel_match.group(0), new_sequel_block, 1)
            else:
                new_qr = new_qr.replace('  sequel_quests: []\n', new_sequel_block, 1)

        return content.replace(qr_text, new_qr, 1)
    else:
        # Insert new quest_relationships block before closing ---
        children_yaml = '\n'.join(f'  - {c}' for c in new_children) if new_children else ''
        sequel_yaml = ''
        if also_set_sequel:
            sequel_yaml = '\n'.join(f'  - {s}' for s in also_set_sequel)

        block = 'quest_relationships:\n'
        block += '  parent_quest: null\n'
        if children_yaml:
            block += f'  child_quests:\n{children_yaml}\n' if children_yaml else '  child_quests: []\n'
        else:
            block += '  child_quests: []\n'
        block += '  parallel_quests: []\n'
        if sequel_yaml:
            block += f'  sequel_quests:\n{sequel_yaml}\n'
        else:
            block += '  sequel_quests: []\n'

        # Insert before the closing ---
        return re.sub(r'\n(---\s*\n)', f'\n{block}\\1', content, count=1)


def fix_parent_quest(content, old_parent, new_parent):
    """Replace a specific parent_quest value."""
    # Matches: parent_quest: /quests/...
    pattern = rf'(  parent_quest:\s*){re.escape(old_parent)}'
    replacement = rf'\g<1>{new_parent}'
    new_content, count = re.subn(pattern, replacement, content)
    return new_content, count > 0


def remove_from_list_field(content, field, values_to_remove):
    """Remove specific values from a YAML list field inside quest_relationships."""
    changed = False
    for val in values_to_remove:
        pattern = rf'  - {re.escape(val)}\n'
        new_content, count = re.subn(pattern, '', content)
        if count:
            content = new_content
            changed = True
    return content, changed


def fix_list_item(content, field, old_val, new_val):
    """Replace a specific item in a YAML list inside frontmatter."""
    pattern = rf'(  - ){re.escape(old_val)}(\n)'
    replacement = rf'\g<1>{new_val}\2'
    new_content, count = re.subn(pattern, replacement, content)
    return new_content, count > 0


# ============================================================
# PART 1: Fix broken references
# ============================================================
print("\n" + "="*60)
print("PART 1: Fixing broken references")
print("="*60)

# 1. tools/mastering-version-control-workflows.md
#    Remove /quests/1110/cicd-pipeline-mastery/ from sequel_quests (doesn't exist)
f1 = REPO_ROOT / 'pages/_quests/tools/mastering-version-control-workflows.md'
content = read_file(f1)
content, changed = remove_from_list_field(content, 'sequel_quests', ['/quests/1110/cicd-pipeline-mastery/'])
if changed:
    write_file(f1, content)
else:
    print(f"  SKIP (nothing to change): {f1}")

# 2. 0011/github-pages-hidden-gem.md
#    Fix parent_quest: /quests/hello-noob/ → /quests/0000/hello-noob/
f2 = REPO_ROOT / 'pages/_quests/0011/github-pages-hidden-gem.md'
content = read_file(f2)
content, changed = fix_parent_quest(content, '/quests/hello-noob/', '/quests/0000/hello-noob/')
if changed:
    write_file(f2, content)
else:
    print(f"  SKIP (nothing to change): {f2}")

# 3. 0010/terminal-artificer-frontend-building.md
#    Fix parent_quest: /quests/0010/terminal-mastery/ → /quests/0001/terminal-mastery/
f3 = REPO_ROOT / 'pages/_quests/0010/terminal-artificer-frontend-building.md'
content = read_file(f3)
content, changed = fix_parent_quest(content, '/quests/0010/terminal-mastery/', '/quests/0001/terminal-mastery/')
if changed:
    write_file(f3, content)
else:
    print(f"  SKIP (nothing to change): {f3}")

# 4. 0010/oh-my-zsh-terminal-enchantment.md
#    Fix child_quests item: /quests/0010/nerd-font-enchantment/ → /quests/0010/side-quests/nerd-font-enchantment/
f4 = REPO_ROOT / 'pages/_quests/0010/oh-my-zsh-terminal-enchantment.md'
content = read_file(f4)
content, changed = fix_list_item(content, 'child_quests', '/quests/0010/nerd-font-enchantment/', '/quests/0010/side-quests/nerd-font-enchantment/')
if changed:
    write_file(f4, content)
else:
    print(f"  SKIP (nothing to change): {f4}")

# 5-8. 0001/stack-attack.md
#    Remove: /quests/0010/django-rest-framework/, /quests/0010/react-typescript-setup/ (child_quests)
#    Remove: /quests/0100/erp-module-development/, /quests/0100/enterprise-devops/ (sequel_quests)
f5 = REPO_ROOT / 'pages/_quests/0001/stack-attack.md'
content = read_file(f5)
content, c1 = remove_from_list_field(content, 'child_quests', [
    '/quests/0010/django-rest-framework/',
    '/quests/0010/react-typescript-setup/',
])
content, c2 = remove_from_list_field(content, 'sequel_quests', [
    '/quests/0100/erp-module-development/',
    '/quests/0100/enterprise-devops/',
])
if c1 or c2:
    write_file(f5, content)
else:
    print(f"  SKIP (nothing to change): {f5}")


# ============================================================
# PART 2: Fix orphaned quests by adding cross-references
# ============================================================
print("\n" + "="*60)
print("PART 2: Adding cross-references for orphaned quests")
print("="*60)

# STRATEGY: For each level, pick one "hub" quest.
# Add all orphaned quests in that level to the hub's child_quests.
# For levels with no pre-existing anchor, connect the hub to the
# previous level's anchor via sequel_quests.

# Level 0001 orphaned quests → add to forge-your-character's child_quests
print("\n[Level 0001]")
f = REPO_ROOT / 'pages/_quests/0001/forge-your-character.md'
content = read_file(f)
content = set_child_quests(content, [
    '/quests/0001/kaizen-continuous-improvement/',
    '/quests/0001/side-quests/personal-site/',
    '/quests/0001/side-quests/barodybroject-stack-analysis/',
    '/quests/0001/github-pages-portal/',
    '/quests/0001/stating-the-stats/',
    '/quests/0001/docs-in-a-row/',
    '/quests/0001/liquid-templating/',
    '/quests/0001/jekyll-fundamentals/',
    '/quests/0001/stack-attack/',
    '/quests/0001/github-pages-basics/',
    '/quests/0001/side-quests/it-journey-stack-analysis/',
    '/quests/0001/git-init-testing/',
    '/quests/0001/yaml-configuration/',
    # codex quests
    '/quests/codex/glossary/',
    '/quests/codex/quest-network-mapping-example/',
    '/quests/codex/world-map/',
])
write_file(f, content)

# Level 0010 orphaned quests → add to action-triggers' child_quests
# Also add prd-codex-mastery as sequel (0011 hub)
print("\n[Level 0010]")
f = REPO_ROOT / 'pages/_quests/tools/action-triggers.md'
content = read_file(f)
content = set_child_quests(content, [
    '/quests/0010/revolutionizing-work-with-ai-automation/',
    '/quests/0010/django-and-git/',
    '/quests/0010/epic-quest-zer0-to-her0-cmstyle/',
    '/quests/0010/planting-seeds/',
    '/quests/0010/jekyll-mermaid-integration/',
    '/quests/0010/side-quests/terminal-artificer/',
    '/quests/0010/javascript-fundamentals/',
    '/quests/0010/recursive-realms-testing/',
    '/quests/0010/bootstrap-framework/',
    '/quests/0010/css-styling-basics/',
    '/quests/0010/oh-my-zsh-mastery/',
    # no-prefix quests
    '/quests/oh-my-zsh-terminal-enchantment/',
    '/quests/epic-digital-portfolio-fortress/',
], also_set_sequel=[
    '/quests/0011/prd-codex-mastery/',  # 0011 hub
])
write_file(f, content)

# Level 0011 orphaned quests → add to prd-codex-mastery's child_quests
# (prd-codex-mastery is now referenced from action-triggers)
print("\n[Level 0011]")
f = REPO_ROOT / 'pages/_quests/2025-11-29-prd-codex-mastering-product-reality-distillation.md'
content = read_file(f)
content = set_child_quests(content, [
    '/quests/0011/seo-optimization/',
    '/quests/0011/custom-domains/',
    '/quests/0011/analytics-integration/',
    '/quests/0011/jekyll-plugins/',
    '/quests/0011/advanced-git-workflows/',
    '/quests/0011/prompt-crystal-vscode-copilot/',
    '/quests/0011/github-pages-hidden-gem/',
])
write_file(f, content)

# Level 0100 orphaned quests → add to frontend-docker's child_quests
# Also add cicd-fundamentals as sequel (0101 hub)
print("\n[Level 0100]")
f = REPO_ROOT / 'pages/_quests/0100/frontend-docker.md'
content = read_file(f)
content = set_child_quests(content, [
    '/quests/0100/docker-compose-orchestration/',
    '/quests/0100/source-control-sorcery/',
    '/quests/0100/frontend-levels/',
    '/quests/0100/side-quests/jekyll-component-refactoring/',
    '/quests/0100/container-fundamentals/',
    '/quests/0100/frontend/',
    '/quests/0100/side-quests/profile-themes/',
    '/quests/0100/frontend-docker-lvl-000/',
    '/quests/0100/lvl-010-frontend-docker/',
    '/quests/0100/lvl-001-frontend-docker/',
], also_set_sequel=[
    '/quests/0101/cicd-fundamentals/',  # 0101 hub
])
write_file(f, content)

# Level 0101 orphaned quests → add to cicd-fundamentals' child_quests
# Also add database-fundamentals as sequel (0110 hub)
print("\n[Level 0101]")
f = REPO_ROOT / 'pages/_quests/0101/cicd-fundamentals.md'
content = read_file(f)
content = set_child_quests(content, [
    '/quests/0101/side-quests/jekyll-quest-tracking/',
    '/quests/0101/artifact-management/',
    '/quests/0101/github-actions-basics/',
    '/quests/0101/testing-integration/',
    '/quests/0101/environment-management/',
    '/quests/0101/docker-mastery/',
    '/quests/0101/deployment-pipelines/',
    '/quests/0101/latex-cv-forging/',
    '/quests/0101/secrets-management/',
    '/quests/0101/workflow-optimization/',
], also_set_sequel=[
    '/quests/0110/database-fundamentals/',  # 0110 hub
])
write_file(f, content)

# Level 0110 orphaned quests → add to database-fundamentals' child_quests
print("\n[Level 0110]")
f = REPO_ROOT / 'pages/_quests/0110/database-fundamentals.md'
content = read_file(f)
content = set_child_quests(content, [
    '/quests/0110/sql-mastery/',
    '/quests/0110/database-security/',
    '/quests/0110/data-modeling/',
    '/quests/0110/query-optimization/',
    '/quests/0110/backup-recovery/',
    '/quests/0110/database-migrations/',
    '/quests/0110/connection-pooling/',
])
write_file(f, content)

# Level 0111 orphaned quests → add to rest-principles' child_quests
# Also add cloud-computing-fundamentals as sequel (1000 hub)
print("\n[Level 0111]")
f = REPO_ROOT / 'pages/_quests/0111/rest-principles.md'
content = read_file(f)
content = set_child_quests(content, [
    '/quests/0111/api-authentication/',
    '/quests/0111/api-documentation/',
    '/quests/0111/api-versioning/',
    '/quests/0111/rate-limiting/',
    '/quests/0111/api-fundamentals/',
    '/quests/0111/error-handling/',
], also_set_sequel=[
    '/quests/1000/cloud-computing-fundamentals/',  # 1000 hub
])
write_file(f, content)

# Level 1000 orphaned quests → add to cloud-computing-fundamentals' child_quests
# Also add kubernetes-fundamentals as sequel (1001 hub)
print("\n[Level 1000]")
f = REPO_ROOT / 'pages/_quests/1000/cloud-computing-fundamentals.md'
content = read_file(f)
content = set_child_quests(content, [
    '/quests/1000/azure-ascension-jekyll-deployment/',
    '/quests/1000/infrastructure-as-code/',
    '/quests/1000/aws-essentials/',
], also_set_sequel=[
    '/quests/1001/kubernetes-fundamentals/',  # 1001 hub
])
write_file(f, content)

# Level 1001 orphaned quests → add to kubernetes-fundamentals' child_quests
# Also add monitoring-fundamentals as sequel (1010 hub)
print("\n[Level 1001]")
f = REPO_ROOT / 'pages/_quests/1001/kubernetes-fundamentals.md'
content = read_file(f)
content = set_child_quests(content, [
    '/quests/1001/k8s-services-networking/',
    '/quests/1001/k8s-pods-workloads/',
    '/quests/1001/k8s-config-secrets/',
], also_set_sequel=[
    '/quests/1010/monitoring-fundamentals/',  # 1010 hub
])
write_file(f, content)

# Level 1010 orphaned quests → add to monitoring-fundamentals' child_quests
# Also add security-fundamentals as sequel (1011 hub)
print("\n[Level 1010]")
f = REPO_ROOT / 'pages/_quests/1010/monitoring-fundamentals.md'
content = read_file(f)
content = set_child_quests(content, [
    '/quests/1010/automated-hyperlink-guardian/',
    '/quests/1010/elk-stack/',
    '/quests/1010/prometheus-grafana/',
    '/quests/1010/distributed-tracing/',
    '/quests/1010/alerting-systems/',
], also_set_sequel=[
    '/quests/1011/security-fundamentals/',  # 1011 hub
])
write_file(f, content)

# Level 1011 orphaned quests → add to security-fundamentals' child_quests
# Also add mastering-version-control-workflows as sequel (1100 hub)
print("\n[Level 1011]")
f = REPO_ROOT / 'pages/_quests/1011/security-fundamentals.md'
content = read_file(f)
content = set_child_quests(content, [
    '/quests/1011/secure-coding/',
    '/quests/1011/threat-modeling/',
    '/quests/1011/penetration-testing/',
    '/quests/1011/ai-feature-pipeline-architect/',
    '/quests/1011/compliance-standards/',
], also_set_sequel=[
    '/quests/1100/mastering-version-control-workflows/',  # 1100 hub
])
write_file(f, content)

# Level 1100 orphaned quests → add to mastering-version-control-workflows' child_quests
# (this file is at tools/mastering-version-control-workflows.md with permalink /quests/1100/mastering-version-control-workflows/)
# Also add ml-fundamentals as sequel (1101 hub)
# NOTE: broken ref (cicd-pipeline-mastery) was already removed in Part 1
print("\n[Level 1100]")
f = REPO_ROOT / 'pages/_quests/tools/mastering-version-control-workflows.md'
content = read_file(f)
content = set_child_quests(content, [
    '/quests/1100/data-warehousing/',
    '/quests/1100/stream-processing/',
    '/quests/1100/data-quality/',
    '/quests/1100/sec-edgar-siege/',
    '/quests/1100/apache-spark/',
    '/quests/1100/conquer-king-edgar/',
    '/quests/1100/etl-pipeline-design/',
    '/quests/1100/temple-of-templates/',
], also_set_sequel=[
    '/quests/1101/ml-fundamentals/',  # 1101 hub
])
write_file(f, content)

# Level 1101 orphaned quests → add to ml-fundamentals' child_quests
# Also add design-patterns as sequel (1110 hub)
print("\n[Level 1101]")
f = REPO_ROOT / 'pages/_quests/1101/ml-fundamentals.md'
content = read_file(f)
content = set_child_quests(content, [
    '/quests/1101/deep-learning-frameworks/',
    '/quests/1101/side-quests/ai-ethics/',
    '/quests/1101/python-data-science/',
    '/quests/1101/natural-language-processing/',
    '/quests/1101/neural-networks/',
    '/quests/1101/mlops/',
    '/quests/1101/computer-vision/',
], also_set_sequel=[
    '/quests/1110/design-patterns/',  # 1110 hub
])
write_file(f, content)

# Level 1110 orphaned quests → add to design-patterns' child_quests
# Also add technical-leadership as sequel (1111 hub)
print("\n[Level 1110]")
f = REPO_ROOT / 'pages/_quests/1110/design-patterns.md'
content = read_file(f)
content = set_child_quests(content, [
    '/quests/1110/system-design-interviews/',
    '/quests/1110/domain-driven-design/',
    '/quests/1110/microservices-architecture/',
    '/quests/1110/404-hunting-quest/',
    '/quests/1110/scaling-strategies/',
    '/quests/1110/api-gateway-patterns/',
    '/quests/1110/event-driven-design/',
], also_set_sequel=[
    '/quests/1111/technical-leadership/',  # 1111 hub
])
write_file(f, content)

# Level 1111 orphaned quests → add to technical-leadership's child_quests
print("\n[Level 1111]")
f = REPO_ROOT / 'pages/_quests/1111/technical-leadership.md'
content = read_file(f)
content = set_child_quests(content, [
    '/quests/1111/career-advancement/',
    '/quests/1111/building-technical-communities/',
    '/quests/1111/tech-speaking-writing/',
    '/quests/1111/open-source-contribution/',
    '/quests/1111/innovation-rnd/',
    '/quests/1111/mentorship-programs/',
    '/quests/1111/architecture-reviews/',
])
write_file(f, content)

print("\n" + "="*60)
print("All fixes applied!")
print("="*60)
print("\nRun validation to verify: python3 scripts/quest/validate-quest-network.py --json /tmp/network-report.json")

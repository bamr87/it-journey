#!/usr/bin/env python3
"""
validate-quest-network.py — quest dependency-graph integrity checker.

Validates the *relationships between* quests (the network), as opposed to the
per-file content quality that ``test/quest-validator/quest_validator.py`` (tier
1) scores. Concretely it checks:

  * every quest-tree page that should be a graph node has a permalink;
  * controlled-vocabulary fields (level / difficulty / quest_type) hold legal
    values — sourced from the registry, never re-hardcoded here;
  * no file still carries a RETIRED frontmatter field (e.g. quest_relationships);
  * every quest_dependency (required / recommended / unlocks) resolves to a real
    node, honouring the ``# planned quest`` forward-reference escape hatch;
  * no duplicate permalinks (two files claiming the same node id);
  * no circular *required* prerequisites (a learner could never start);
  * prerequisite level monotonicity (a quest shouldn't require a higher-level one);
  * orphaned quests (reachable from nothing) — reported as warnings;
  * (optional) the committed quest-network.json: every edge resolves to a node,
    no duplicate node ids — i.e. the artifact the site actually ships is sound.

Taxonomy and "what is a quest" rules come from ``quest_registry`` +
``quest_lib`` so this validator can never drift from tier 1, the generators, or
the templates. This module is import-safe: ``run_network_validation()`` returns
a structured result for the unified ``quest_audit`` orchestrator.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import quest_registry as reg  # noqa: E402
import quest_lib  # noqa: E402

# ANSI colours (suppressed when stdout is not a TTY).
_TTY = sys.stdout.isatty()
RED = "\033[0;31m" if _TTY else ""
GREEN = "\033[0;32m" if _TTY else ""
YELLOW = "\033[1;33m" if _TTY else ""
BLUE = "\033[0;34m" if _TTY else ""
NC = "\033[0m" if _TTY else ""


def print_info(msg): print(f"{BLUE}[INFO]{NC} {msg}")
def print_success(msg): print(f"{GREEN}[SUCCESS]{NC} {msg}")
def print_warning(msg): print(f"{YELLOW}[WARNING]{NC} {msg}")
def print_error(msg): print(f"{RED}[ERROR]{NC} {msg}")


# Dependency buckets that form the directed graph. Sourced from the registry's
# QUEST_DEPENDENCIES_KEYS so the edge kinds can't drift from the schema.
_DEP_KINDS = list(reg.QUEST_DEPENDENCIES_KEYS)  # required/recommended/unlocks_quests
# Edges that represent a hard prerequisite (used for cycle + monotonicity checks).
_PREREQ_KEY = "required_quests"


def _strip_planned_marker(value):
    """Strip a trailing ``# planned quest`` / ``# planned`` inline marker.

    Authors suffix a dependency URL with ``# planned quest`` to declare an
    intentional forward reference to an unwritten quest (documented in
    ``.github/instructions/quest.instructions.md``). Returns (clean, is_planned).
    """
    if not isinstance(value, str):
        return value, False
    stripped = value.strip()
    import re
    m = re.match(r"^(.*?)\s*#\s*planned(?:\s+quest)?\s*$", stripped, re.IGNORECASE)
    if m:
        return m.group(1).strip(), True
    return stripped, False


def _norm_link(value: str) -> str:
    """Normalise a permalink to a trailing-slash node id."""
    v = str(value).strip()
    return v if v.endswith("/") else v + "/"


class QuestNetworkValidator:
    def __init__(self, quest_dir: str, network_json: Optional[str] = None):
        self.quest_dir = Path(quest_dir)
        self.network_json = Path(network_json) if network_json else None
        # node id (permalink) -> {doc, frontmatter}
        self.nodes: Dict[str, Dict] = {}
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.stats = {
            "total_quests": 0,
            "complete_quests": 0,
            "placeholder_quests": 0,
            "draft_quests": 0,
            "orphaned_quests": 0,
            "broken_dependencies": 0,
            "duplicate_permalinks": 0,
            "retired_fields": 0,
            "dangling_edges": 0,
        }

    # ── discovery ────────────────────────────────────────────────────────────

    def scan_quests(self):
        """Build the node set from quest-tree files that carry a permalink.

        Node set matches the network *builder* (``build-quest-network.py``):
        skip templates/docs/inventory + meta files, include everything else that
        has a permalink. That way the validator checks the same graph the site
        ships, not a different one.
        """
        print_info("Scanning quest files...")
        for path in quest_lib.iter_quest_files(
            self.quest_dir, skip_subdirs=reg.SKIP_SUBDIRS, include_index_readmes=True
        ):
            doc = quest_lib.read_quest(path)
            if doc.fm_error:
                self.errors.append(f"{doc.rel_path}: invalid frontmatter — {doc.fm_error}")
                continue
            permalink = doc.permalink
            if not permalink:
                # No permalink → invisible to the graph. Warn so it isn't a
                # silent dead end (a quest nobody can link to).
                self.warnings.append(f"{doc.rel_path}: no permalink — excluded from the quest network")
                continue
            node_id = _norm_link(permalink)
            if node_id in self.nodes:
                other = self.nodes[node_id]["doc"].rel_path
                self.errors.append(
                    f"Duplicate permalink {node_id!r}: {doc.rel_path} and {other} "
                    f"resolve to the same node (one will silently overwrite the other)"
                )
                self.stats["duplicate_permalinks"] += 1
                continue
            self.nodes[node_id] = {"doc": doc, "frontmatter": doc.fm}
            self.stats["total_quests"] += 1
            if doc.is_draft():
                self.stats["draft_quests"] += 1
            if doc.has_placeholder_marker():
                self.stats["placeholder_quests"] += 1
            else:
                self.stats["complete_quests"] += 1
        print_success(f"Found {self.stats['total_quests']} quest nodes")

    # ── frontmatter (graph-relevant only; tier 1 owns the full field gate) ────

    def validate_frontmatter(self):
        """Validate only the controlled-vocabulary fields the graph depends on.

        The full required-field gate (with _config.yml default awareness) lives
        in tier 1; duplicating it here would either drift or false-fail on
        config-supplied fields. We validate values against the registry enums
        (warnings) and flag retired fields.
        """
        print_info("Validating controlled vocabularies...")
        for node_id, data in self.nodes.items():
            fm = data["frontmatter"]
            rel = data["doc"].rel_path

            level = str(fm.get("level", ""))
            if level and not reg.LEVEL_RE.match(level):
                self.warnings.append(f"{rel}: invalid level '{level}' (expected 4-bit binary)")

            difficulty = fm.get("difficulty", "")
            if difficulty and difficulty not in reg.DIFFICULTIES:
                self.warnings.append(
                    f"{rel}: invalid difficulty '{difficulty}' (expected one of {reg.DIFFICULTIES})"
                )

            quest_type = fm.get("quest_type", "")
            if quest_type and quest_type not in reg.QUEST_TYPES:
                self.warnings.append(
                    f"{rel}: invalid quest_type '{quest_type}' (expected one of {reg.QUEST_TYPES})"
                )

            # Flag retired fields rather than silently reading them. The
            # normalizer (make quest-normalize) migrates + strips these.
            present_retired = [f for f in reg.RETIRED_FIELDS if f in fm]
            if present_retired:
                self.stats["retired_fields"] += 1
                self.warnings.append(
                    f"{rel}: carries retired field(s) {present_retired} — run `make quest-normalize`"
                )

            # quest_dependencies buckets must be lists of permalinks. A scalar
            # (e.g. `required_quests: 42`) is a schema error; warn once per file
            # (the edge iterator tolerates it silently to stay crash-free).
            deps = fm.get("quest_dependencies")
            if isinstance(deps, dict):
                for kind in _DEP_KINDS:
                    val = deps.get(kind)
                    if val is not None and not isinstance(val, (list, tuple, str)):
                        self.warnings.append(
                            f"{rel}: quest_dependencies.{kind} is "
                            f"{type(val).__name__}, expected a list of permalinks")
            elif deps is not None and not isinstance(deps, dict):
                self.warnings.append(
                    f"{rel}: quest_dependencies is {type(deps).__name__}, expected a mapping")

    # ── dependency edges ─────────────────────────────────────────────────────

    def _iter_edges(self, fm: dict, rel: str = ""):
        """Yield (dep_kind, clean_target, is_planned) for each dependency edge.

        Purely defensive: a scalar target is wrapped; anything that is neither a
        string nor a list (e.g. ``required_quests: 42``) is silently skipped so a
        malformed file can't raise out of the import-safe entry point. The
        once-per-file schema warning is emitted by ``validate_frontmatter`` —
        not here, since this is called by four checks per node.
        """
        deps = fm.get("quest_dependencies") or {}
        if not isinstance(deps, dict):
            return
        for kind in _DEP_KINDS:
            targets = deps.get(kind) or []
            if isinstance(targets, str):
                targets = [targets]
            elif not isinstance(targets, (list, tuple)):
                continue
            for raw in targets:
                clean, planned = _strip_planned_marker(raw)
                if clean:
                    yield kind, _norm_link(clean) if not planned else clean, planned

    def validate_dependencies(self):
        """Every required/recommended/unlocks target must resolve to a node."""
        print_info("Validating quest dependencies...")
        for node_id, data in self.nodes.items():
            rel = data["doc"].rel_path
            for kind, target, planned in self._iter_edges(data["frontmatter"], rel):
                if planned:
                    continue
                if target not in self.nodes:
                    self.errors.append(f"{rel}: dependency not found: {target} ({kind})")
                    self.stats["broken_dependencies"] += 1

    def validate_prerequisite_monotonicity(self):
        """A quest's required prerequisites should not live at a *higher* level
        than the quest itself (you can't require a harder quest to start an
        easier one). Reported as warnings — some cross-tier prerequisites are
        intentional, but the common case is an authoring slip."""
        print_info("Checking prerequisite level monotonicity...")
        for node_id, data in self.nodes.items():
            fm = data["frontmatter"]
            rel = data["doc"].rel_path
            level = str(fm.get("level", ""))
            if not reg.LEVEL_RE.match(level):
                continue
            my_rank = reg.LEVELS.get(level, {}).get("decimal")
            if my_rank is None:
                continue
            for kind, target, planned in self._iter_edges(fm, rel):
                if planned or kind != _PREREQ_KEY or target not in self.nodes:
                    continue
                tgt_level = str(self.nodes[target]["frontmatter"].get("level", ""))
                tgt_rank = reg.LEVELS.get(tgt_level, {}).get("decimal")
                if tgt_rank is not None and tgt_rank > my_rank:
                    self.warnings.append(
                        f"{rel}: required prerequisite {target} is at a higher level "
                        f"({tgt_level} > {level}) — learner can't reach it first"
                    )

    def detect_circular_dependencies(self):
        """Detect cycles in the *required* prerequisite graph (a cycle there
        means a learner can never start). recommended/unlocks are lateral and
        may legitimately be mutual, so they're excluded."""
        print_info("Checking for circular dependencies...")

        def required_targets(node_id):
            data = self.nodes.get(node_id, {})
            fm = data.get("frontmatter", {})
            rel = data.get("doc").rel_path if data.get("doc") else node_id
            for kind, target, planned in self._iter_edges(fm, rel):
                if kind == _PREREQ_KEY and not planned and target in self.nodes:
                    yield target

        visited = set()

        def has_cycle(node_id, stack):
            visited.add(node_id)
            stack.add(node_id)
            for dep in required_targets(node_id):
                if dep not in visited:
                    if has_cycle(dep, stack):
                        return True
                elif dep in stack:
                    self.errors.append(f"Circular dependency detected: {node_id} -> {dep}")
                    return True
            stack.discard(node_id)
            return False

        for node_id in self.nodes:
            if node_id not in visited:
                has_cycle(node_id, set())

    def find_orphaned_quests(self):
        """Quests referenced by no other quest's dependencies (warnings).

        Entry-level (0000) quests are expected starting points and excluded.
        Retired relationship fields are intentionally NOT consulted.
        """
        print_info("Finding orphaned quests...")
        referenced = set()
        for data in self.nodes.values():
            for kind, target, planned in self._iter_edges(data["frontmatter"]):
                if not planned:
                    referenced.add(target)
        for node_id, data in self.nodes.items():
            if str(data["frontmatter"].get("level", "")) == "0000":
                continue
            if node_id not in referenced:
                self.warnings.append(f"Orphaned quest (not referenced): {node_id}")
                self.stats["orphaned_quests"] += 1

    # ── shipped artifact (optional) ──────────────────────────────────────────

    def validate_network_json(self):
        """Validate the committed quest-network.json: unique node ids and every
        edge endpoint resolves to a node. A bad graph won't fail the Jekyll
        build, so this is the only thing that catches a shipped dangling edge."""
        if not self.network_json:
            return
        if not self.network_json.exists():
            self.warnings.append(f"network JSON not found (skipped): {self.network_json}")
            return
        print_info(f"Validating shipped graph: {self.network_json}")
        try:
            graph = json.loads(self.network_json.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as e:
            self.errors.append(f"{self.network_json}: unreadable/invalid JSON — {e}")
            return
        node_ids = set()
        for n in graph.get("nodes", []):
            nid = n.get("id")
            if nid in node_ids:
                self.errors.append(f"network JSON: duplicate node id {nid!r}")
            node_ids.add(nid)
        # A node-set drift between the live scan and the shipped graph means the
        # JSON is stale — surface it (the CI freshness gate is the hard stop).
        live_ids = set(self.nodes)
        if node_ids and live_ids and node_ids != live_ids:
            missing = len(live_ids - node_ids)
            extra = len(node_ids - live_ids)
            self.warnings.append(
                f"network JSON node set differs from live scan "
                f"({missing} missing, {extra} stale) — run `make quest-build-network`"
            )
        # Dangling edges are WARNINGS here: the builder intentionally emits edges
        # for `# planned quest` forward-references whose targets aren't nodes yet.
        # The authoritative, planned-aware broken-dependency ERROR check is
        # validate_dependencies() above (reads the markdown, not the artifact).
        for e in graph.get("edges", []):
            for end in ("source", "target"):
                ref = e.get(end)
                if ref and ref not in node_ids:
                    self.warnings.append(
                        f"network JSON: edge {end} {ref!r} ({e.get('kind','?')}) has no matching node "
                        f"(planned forward-reference, or stale graph)"
                    )
                    self.stats["dangling_edges"] += 1

    # ── report ───────────────────────────────────────────────────────────────

    def generate_report(self):
        print()
        print("=" * 80)
        print("QUEST NETWORK VALIDATION REPORT")
        print("=" * 80)
        print()
        print("📊 Quest Network Statistics:")
        print(f"  Total Nodes:          {self.stats['total_quests']}")
        print(f"  Complete:             {self.stats['complete_quests']}")
        print(f"  Placeholder:          {self.stats['placeholder_quests']}")
        print(f"  Draft:                {self.stats['draft_quests']}")
        print(f"  Orphaned:             {self.stats['orphaned_quests']}")
        print(f"  Broken Dependencies:  {self.stats['broken_dependencies']}")
        print(f"  Duplicate Permalinks: {self.stats['duplicate_permalinks']}")
        print(f"  Dangling Edges (JSON):{self.stats['dangling_edges']}")
        print(f"  Files w/ Retired FM:  {self.stats['retired_fields']}")
        print()
        if self.errors:
            print_error(f"❌ {len(self.errors)} Error(s) Found:")
            for e in self.errors:
                print(f"  • {e}")
            print()
        else:
            print_success("✅ No errors found!")
            print()
        if self.warnings:
            print_warning(f"⚠️  {len(self.warnings)} Warning(s):")
            for w in self.warnings:
                print(f"  • {w}")
            print()
        else:
            print_success("✅ No warnings!")
            print()
        print("=" * 80)
        if not self.errors:
            print_success("VALIDATION PASSED ✅")
            return 0
        print_error("VALIDATION FAILED ❌")
        return 1

    def run(self):
        self.scan_quests()
        self.validate_frontmatter()
        self.validate_dependencies()
        self.validate_prerequisite_monotonicity()
        self.detect_circular_dependencies()
        self.find_orphaned_quests()
        self.validate_network_json()
        return self.generate_report()


def run_network_validation(quest_dir, network_json=None, strict=False, quiet=True) -> dict:
    """Import-friendly entry point for the unified orchestrator.

    Returns a result dict: {stats, errors, warnings, passed}. ``passed`` is
    False if there are errors, or (when ``strict``) any warnings. ``quiet``
    suppresses the per-check INFO chatter so the orchestrator owns all output.
    """
    import contextlib
    import io
    validator = QuestNetworkValidator(str(quest_dir), network_json=network_json)
    sink = io.StringIO() if quiet else sys.stdout
    with contextlib.redirect_stdout(sink):
        # Run checks without the console report (orchestrator renders its own).
        validator.scan_quests()
        validator.validate_frontmatter()
        validator.validate_dependencies()
        validator.validate_prerequisite_monotonicity()
        validator.detect_circular_dependencies()
        validator.find_orphaned_quests()
        validator.validate_network_json()
    passed = not validator.errors and (not strict or not validator.warnings)
    return {
        "stats": validator.stats,
        "errors": validator.errors,
        "warnings": validator.warnings,
        "passed": passed,
    }


def main():
    parser = argparse.ArgumentParser(
        description="IT-Journey Quest Network Validator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("-d", "--directory",
                        help="Quest directory (default: auto-detect pages/_quests)")
    parser.add_argument("--network-json", metavar="FILE",
                        help="Also validate this committed quest-network.json "
                             "(default: auto-detect assets/data/quest-network.json)")
    parser.add_argument("--no-network-json", action="store_true",
                        help="Skip validating the shipped quest-network.json")
    parser.add_argument("--json", metavar="FILE", help="Write results as JSON to FILE")
    parser.add_argument("--strict", action="store_true",
                        help="Exit non-zero when warnings exist (in addition to errors)")
    args = parser.parse_args()

    if args.directory:
        quest_dir = Path(args.directory)
    else:
        quest_dir = _HERE.parents[1] / "pages" / "_quests"
    if not quest_dir.exists():
        print_error(f"Quest directory not found: {quest_dir}")
        return 1

    network_json = None
    if not args.no_network_json:
        if args.network_json:
            network_json = args.network_json
        else:
            candidate = _HERE.parents[1] / "assets" / "data" / "quest-network.json"
            network_json = str(candidate) if candidate.exists() else None

    print_info(f"Quest directory: {quest_dir}")
    if network_json:
        print_info(f"Network JSON:    {network_json}")
    print()

    validator = QuestNetworkValidator(str(quest_dir), network_json=network_json)
    exit_code = validator.run()

    if args.json:
        report = {
            "stats": validator.stats,
            "errors": validator.errors,
            "warnings": validator.warnings,
            "passed": exit_code == 0,
        }
        Path(args.json).write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
        print_success(f"Network report written to {args.json}")

    if args.strict and validator.warnings:
        return 1
    return exit_code


if __name__ == "__main__":
    sys.exit(main())

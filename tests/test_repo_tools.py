import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.repo_tools import (
    _without_fenced_blocks,
    archive_matches_source,
    build_archive_bytes,
    package_repository,
    validate_repository,
)


ROOT = Path(__file__).resolve().parents[1]


class RepositoryToolsTests(unittest.TestCase):
    def copy_repository(self):
        temp_dir = tempfile.TemporaryDirectory()
        destination = Path(temp_dir.name) / "plugin"
        shutil.copytree(
            ROOT,
            destination,
            ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"),
        )
        return temp_dir, destination

    def assert_valid(self, root):
        errors = validate_repository(root, run_official=False)
        self.assertEqual(errors, [], "\n".join(errors))

    def test_current_repository_contract_is_valid(self):
        self.assert_valid(ROOT)

    def test_malformed_manifest_is_rejected(self):
        temp_dir, root = self.copy_repository()
        self.addCleanup(temp_dir.cleanup)
        manifest_path = root / ".codex-plugin" / "plugin.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["version"] = "1.0"
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
        errors = validate_repository(root, run_official=False)
        self.assertTrue(any("semantic version" in error for error in errors))

    def test_unsupported_manifest_field_is_rejected(self):
        temp_dir, root = self.copy_repository()
        self.addCleanup(temp_dir.cleanup)
        manifest_path = root / ".codex-plugin" / "plugin.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["hooks"] = {"afterInstall": "do-not-run"}
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
        errors = validate_repository(root, run_official=False)
        self.assertTrue(any("unsupported manifest field" in error for error in errors))

    def test_missing_relative_markdown_link_is_rejected(self):
        temp_dir, root = self.copy_repository()
        self.addCleanup(temp_dir.cleanup)
        readme = root / "README.md"
        readme.write_text(readme.read_text() + "\n[missing](does-not-exist.md)\n")
        errors = validate_repository(root, run_official=False)
        self.assertTrue(any("does-not-exist.md" in error for error in errors))

    def test_fenced_markdown_link_is_ignored(self):
        temp_dir, root = self.copy_repository()
        self.addCleanup(temp_dir.cleanup)
        readme = root / "README.md"
        readme.write_text(
            readme.read_text()
            + "\n```markdown\n[illustration](does-not-exist.md)\n```\n"
        )
        errors = validate_repository(root, run_official=False)
        self.assertFalse(any("does-not-exist.md" in error for error in errors))

    def test_stale_archive_is_rejected(self):
        temp_dir, root = self.copy_repository()
        self.addCleanup(temp_dir.cleanup)
        package_repository(root)
        (root / "README.md").write_text((root / "README.md").read_text() + "\nFreshness test.\n")
        self.assertFalse(archive_matches_source(root))

    def test_forbidden_namespace_reference_is_rejected(self):
        temp_dir, root = self.copy_repository()
        self.addCleanup(temp_dir.cleanup)
        skill = root / "skills" / "using-super-adhd-child" / "SKILL.md"
        skill.write_text(skill.read_text() + "\nForbidden: superpowers:legacy\n")
        errors = validate_repository(root, run_official=False)
        self.assertTrue(any("superpowers:" in error for error in errors))

    def test_missing_adhd_handoff_is_rejected(self):
        temp_dir, root = self.copy_repository()
        self.addCleanup(temp_dir.cleanup)
        router = root / "skills" / "using-super-adhd-child" / "SKILL.md"
        router.write_text(router.read_text().replace("super-adhd-child:brainstorming", "brainstorming"))
        errors = validate_repository(root, run_official=False)
        self.assertTrue(any("handoff" in error.lower() for error in errors))

    def test_invalid_skill_frontmatter_is_rejected(self):
        temp_dir, root = self.copy_repository()
        self.addCleanup(temp_dir.cleanup)
        skill = root / "skills" / "adhd-ideation" / "SKILL.md"
        text = skill.read_text().replace(
            'description: "Use when the user explicitly requests ADHD mode, divergent ideation, parallel cognitive frames, or trap-focused exploration."\n',
            "",
        )
        skill.write_text(text)
        errors = validate_repository(root, run_official=False)
        self.assertTrue(any("description" in error.lower() for error in errors))

    def test_missing_referenced_source_file_is_rejected(self):
        temp_dir, root = self.copy_repository()
        self.addCleanup(temp_dir.cleanup)
        readme = root / "README.md"
        readme.write_text(readme.read_text() + "\nReference: `MISSING-SOURCE.md`.\n")
        errors = validate_repository(root, run_official=False)
        self.assertTrue(any("MISSING-SOURCE.md" in error for error in errors))

    def test_reduced_capability_guidance_is_rejected(self):
        temp_dir, root = self.copy_repository()
        self.addCleanup(temp_dir.cleanup)
        skill = root / "skills" / "adhd-ideation" / "SKILL.md"
        text = skill.read_text().replace("isolated subagents are unavailable", "isolated workers are unavailable")
        skill.write_text(text)
        errors = validate_repository(root, run_official=False)
        self.assertTrue(any("capability" in error.lower() for error in errors))

    def test_non_executable_support_script_is_rejected(self):
        temp_dir, root = self.copy_repository()
        self.addCleanup(temp_dir.cleanup)
        script = root / "skills" / "brainstorming" / "scripts" / "start-server.sh"
        os.chmod(script, 0o644)
        errors = validate_repository(root, run_official=False)
        self.assertTrue(any("not executable" in error for error in errors))

    def test_invalid_source_does_not_overwrite_archive(self):
        temp_dir, root = self.copy_repository()
        self.addCleanup(temp_dir.cleanup)
        archive = root / "skill.zip"
        before = archive.read_bytes()
        skill = root / "skills" / "using-super-adhd-child" / "SKILL.md"
        skill.write_text(skill.read_text() + "\nForbidden superpowers:legacy\n")
        with self.assertRaises(ValueError):
            package_repository(root, official_validator=False)
        self.assertEqual(archive.read_bytes(), before)

    def test_offline_drift_check_is_read_only_and_passes(self):
        before = (ROOT / "UPSTREAM_INVENTORY.json").read_bytes()
        result = subprocess.run(
            ["python3", "scripts/check_upstream_drift.py", "--offline"],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("Remote drift: SKIP", result.stdout)
        self.assertEqual((ROOT / "UPSTREAM_INVENTORY.json").read_bytes(), before)

    def test_archive_bytes_are_deterministic(self):
        first = build_archive_bytes(ROOT)
        second = build_archive_bytes(ROOT)
        self.assertEqual(first, second)

    def test_excluded_runtime_files_are_structured_and_absent(self):
        inventory = json.loads((ROOT / "UPSTREAM_INVENTORY.json").read_text())
        superpowers = next(entry for entry in inventory["upstreams"] if entry["name"] == "superpowers")
        excluded = {
            "skills/systematic-debugging/CREATION-LOG.md",
            "skills/systematic-debugging/test-academic.md",
            "skills/systematic-debugging/test-pressure-1.md",
            "skills/systematic-debugging/test-pressure-2.md",
            "skills/systematic-debugging/test-pressure-3.md",
        }
        self.assertEqual(set(superpowers.get("excludedPaths", [])), excluded)
        self.assertTrue(all(not (ROOT / path).exists() for path in excluded))

    def test_reintroduced_excluded_runtime_file_is_rejected(self):
        temp_dir, root = self.copy_repository()
        self.addCleanup(temp_dir.cleanup)
        path = root / "skills" / "systematic-debugging" / "test-pressure-1.md"
        path.write_text("reintroduced development-only fixture\n")
        errors = validate_repository(root, run_official=False)
        self.assertTrue(any("excluded" in error.lower() and "test-pressure-1.md" in error for error in errors))
        with self.assertRaises(ValueError):
            package_repository(root, official_validator=False)

    def test_offline_inventory_check_rejects_reintroduced_excluded_file(self):
        temp_dir, root = self.copy_repository()
        self.addCleanup(temp_dir.cleanup)
        path = root / "skills" / "systematic-debugging" / "test-pressure-1.md"
        path.write_text("reintroduced development-only fixture\n")
        result = subprocess.run(
            ["python3", "scripts/check_upstream_drift.py", ".", "--offline"],
            cwd=root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("excluded runtime path is present", result.stdout)

    def test_removed_debugging_files_are_not_in_archive(self):
        names = set()
        with zipfile.ZipFile(ROOT / "skill.zip") as archive:
            names.update(archive.namelist())
        for path in (
            "skills/systematic-debugging/CREATION-LOG.md",
            "skills/systematic-debugging/test-academic.md",
            "skills/systematic-debugging/test-pressure-1.md",
            "skills/systematic-debugging/test-pressure-2.md",
            "skills/systematic-debugging/test-pressure-3.md",
        ):
            self.assertNotIn(path, names)

    def test_codex_policy_is_authoritative_and_bootstrap_is_single_pass(self):
        using_superpowers = (ROOT / "skills" / "using-superpowers" / "SKILL.md").read_text()
        adhd = (ROOT / "skills" / "adhd-ideation" / "SKILL.md").read_text()
        self.assertIn("Codex collaboration policy", using_superpowers)
        self.assertIn("isolated subagents", using_superpowers.lower())
        self.assertIn("capacity-sized batches", using_superpowers.lower())
        self.assertIn("inherited model", using_superpowers.lower())
        normalized_policy = " ".join(using_superpowers.split())
        self.assertIn("general-purpose", normalized_policy)
        self.assertIn("`default` built-in agent", normalized_policy)
        self.assertIn("`worker`", normalized_policy)
        self.assertIn("`explorer`", normalized_policy)
        self.assertIn("direct natural-language", normalized_policy)
        self.assertIn("not a formal tool call", normalized_policy)
        self.assertNotIn("Platform Adaptation", using_superpowers)
        obsolete_reference = "codex-" + "tools.md"
        self.assertFalse((ROOT / "skills" / "using-superpowers" / "references" / obsolete_reference).exists())
        self.assertNotIn("## Model and lifecycle policy", adhd)
        all_skill_text = "\n".join(path.read_text() for path in (ROOT / "skills").rglob("*.md"))
        self.assertNotIn(obsolete_reference, all_skill_text)

    def test_plugin_activation_defaults_to_capability_aware_subagent_delegation(self):
        using_superpowers = (ROOT / "skills" / "using-superpowers" / "SKILL.md").read_text()
        routing = (ROOT / "skills" / "using-super-adhd-child" / "SKILL.md").read_text()
        policy = " ".join(using_superpowers.split()).lower()
        routing_policy = " ".join(routing.split()).lower()
        for marker in (
            "when super adhd child is the active plugin",
            "capability-aware subagent delegation as the default",
            "independently separable work",
            "do not wait for a second user request",
            "trivial or tightly coupled work inline",
            "never spawn ceremonial agents",
        ):
            self.assertIn(marker, policy)
        self.assertIn("delegation default is separate from adhd routing", routing_policy)
        self.assertIn("does not activate divergent ideation", routing_policy)

    def test_executing_plans_names_only_shipped_host_references(self):
        executing_plans = (ROOT / "skills" / "executing-plans" / "SKILL.md").read_text()
        self.assertIn(
            "Codex CLI/Codex App, use the Codex collaboration policy in `../using-superpowers/SKILL.md`",
            executing_plans,
        )
        self.assertIn("Copilot CLI has no dedicated reference file here yet", executing_plans)
        for reference in ("gemini-tools.md", "antigravity-tools.md", "pi-tools.md"):
            self.assertIn(reference, executing_plans)
        self.assertNotIn("codex-tools.md", executing_plans)
        self.assertNotIn("copilot-tools.md", executing_plans)

    def test_adhd_focus_evaluation_is_inline_and_uses_eight_roles(self):
        adhd = (ROOT / "skills" / "adhd-ideation" / "SKILL.md").read_text()
        phase_two = adhd.split("### Phase 2", 1)[1].split("## Frames", 1)[0]
        lowered = adhd.lower()
        phase_two_lower = phase_two.lower()
        self.assertIn("about 8 isolated-subagent roles", lowered)
        self.assertIn("five divergent", lowered)
        self.assertIn("three deepening", lowered)
        for marker in ("orchestrator", "score", "trap", "cluster", "weighted", "top 3", "inline"):
            self.assertIn(marker, phase_two_lower)
        self.assertNotIn("+ 1 score + 1 cluster", lowered)
        self.assertNotRegex(phase_two_lower, r"(?:spawn|dispatch)[^\n]*(?:score|cluster)")

    def test_missing_namespaced_skill_references_are_rejected(self):
        temp_dir, root = self.copy_repository()
        self.addCleanup(temp_dir.cleanup)
        skill = root / "skills" / "using-superpowers" / "SKILL.md"
        skill.write_text(skill.read_text() + "\nRequired: super-adhd-child:not-shipped.\n")
        errors = validate_repository(root, run_official=False)
        self.assertTrue(any("not-shipped" in error and "skill" in error.lower() for error in errors))

    def test_fenced_missing_namespaced_skill_reference_is_ignored(self):
        temp_dir, root = self.copy_repository()
        self.addCleanup(temp_dir.cleanup)
        skill = root / "skills" / "using-superpowers" / "SKILL.md"
        skill.write_text(skill.read_text() + "\n```text\nsuper-adhd-child:not-shipped\n```\n")
        errors = validate_repository(root, run_official=False)
        self.assertFalse(any("not-shipped" in error for error in errors))

    def test_nonexistent_skill_names_are_removed_and_brainstorming_gate_remains(self):
        using_superpowers = (ROOT / "skills" / "using-superpowers" / "SKILL.md").read_text()
        brainstorming = (ROOT / "skills" / "brainstorming" / "SKILL.md").read_text()
        invalid_design_skill = "front" + "end-design"
        invalid_builder_skill = "mcp-" + "builder"
        self.assertNotIn(invalid_design_skill, using_superpowers)
        self.assertNotIn(invalid_design_skill, brainstorming)
        self.assertNotIn(invalid_builder_skill, brainstorming)
        self.assertIn("super-adhd-child:writing-plans", brainstorming)
        self.assertIn("only transition", brainstorming)

    def test_dispatch_hot_paths_drop_redundant_examples_and_openings(self):
        dispatch = (ROOT / "skills" / "dispatching-parallel-agents" / "SKILL.md").read_text()
        development = (ROOT / "skills" / "subagent-driven-development" / "SKILL.md").read_text()
        self.assertNotIn("## Real Example from Session", dispatch)
        self.assertNotIn("## Example Workflow", development)
        self.assertLess(len(dispatch.split()), 865)
        self.assertLess(len(development.split()), 4084)
        self.assertIn("independent", dispatch.lower())
        self.assertIn("fresh per-task", development.lower())
        for heading, text in (("Real Example from Session", dispatch), ("Example Workflow", development)):
            if heading in text:
                self.assertRegex(text, r"(?is)conditional.{0,120}\[[^]]+\]\([^)]*\)")

    def test_manual_first_routing_and_brainstorming_handoff_remain(self):
        router = (ROOT / "skills" / "using-super-adhd-child" / "SKILL.md").read_text().lower()
        adhd = (ROOT / "skills" / "adhd-ideation" / "SKILL.md").read_text()
        self.assertIn("manual-first", router)
        self.assertIn("do not use adhd automatically", router)
        self.assertIn("super-adhd-child:brainstorming", router)
        self.assertIn("super-adhd-child:brainstorming", adhd)

    def test_namespaced_skill_references_resolve_to_shipped_skills(self):
        skill_names = {
            path.parent.name
            for path in (ROOT / "skills").glob("*/SKILL.md")
        }
        pattern = re.compile(r"\b([a-z][a-z0-9-]*-[a-z0-9-]+):([a-z0-9-]+)\b")
        for path in (ROOT / "skills").rglob("*.md"):
            text = _without_fenced_blocks(path.read_text())
            for namespace, reference in pattern.findall(text):
                self.assertEqual(namespace, "super-adhd-child", f"unshipped namespace in {path}: {namespace}")
                self.assertIn(reference, skill_names, f"unshipped skill reference in {path}: {reference}")


if __name__ == "__main__":
    unittest.main()

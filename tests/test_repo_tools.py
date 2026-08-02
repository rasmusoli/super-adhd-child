import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.repo_tools import (
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


if __name__ == "__main__":
    unittest.main()

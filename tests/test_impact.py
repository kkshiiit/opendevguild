"""Tests for conservative local preflight selection; no model required."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "impact.py"
spec = importlib.util.spec_from_file_location("odg_impact", SCRIPT)
impact = importlib.util.module_from_spec(spec)
spec.loader.exec_module(impact)
AVAILABLE = {
    "test_agents.py", "test_documentation.py", "test_impact.py",
    "test_installation.py", "test_protocol.py", "test_regressions.py",
    "test_release_verification.py", "test_research.py", "test_routing.py",
    "test_security.py", "test_tooling.py", "test_visual.py",
}


class ImpactTests(unittest.TestCase):
    def test_single_research_tool_uses_targeted_suite(self):
        result = impact.select_tests(["scripts/research.py"], AVAILABLE)
        self.assertEqual(result["tests"], ["test_research.py"])
        self.assertFalse(result["full_suite"])

    def test_security_skill_adds_security_checks(self):
        result = impact.select_tests(["skills/security-engineer/SKILL.md"], AVAILABLE)
        self.assertEqual(result["tests"], ["test_protocol.py", "test_routing.py", "test_security.py"])

    def test_visual_change_adds_visual_regressions(self):
        result = impact.select_tests(["skills/visual-qa-auditor/SKILL.md"], AVAILABLE)
        self.assertIn("test_visual.py", result["tests"])

    def test_mixed_changes_are_deduplicated_and_ordered(self):
        result = impact.select_tests(["scripts/install.py", "scripts/impact.py", "scripts/install.py"], AVAILABLE)
        self.assertEqual(result["tests"], ["test_impact.py", "test_installation.py"])
        self.assertEqual(len(result["commands"]), 2)

    def test_unknown_change_fails_closed_to_full_suite(self):
        result = impact.select_tests(["unrecognized/new-thing.go"], AVAILABLE)
        self.assertTrue(result["full_suite"])
        self.assertEqual(set(result["tests"]), AVAILABLE)
        self.assertEqual(len(result["commands"]), 1)

    def test_shared_contract_change_requires_full_suite(self):
        self.assertTrue(impact.select_tests(["contracts/task.schema.json"], AVAILABLE)["full_suite"])

    def test_untracked_test_changes_target_self(self):
        result = impact.select_tests(["tests/test_impact.py"], AVAILABLE)
        self.assertEqual(result["tests"], ["test_impact.py"])

    def test_rejects_unsafe_or_absolute_paths(self):
        for path in ("../outside.txt", "/etc/passwd", "-danger", "a\\b.py", ""):
            with self.subTest(path=path), self.assertRaises(ValueError):
                impact.select_tests([path], AVAILABLE)

    def test_missing_expected_test_fails_instead_of_omitting_it(self):
        with self.assertRaisesRegex(ValueError, "test_research"):
            impact.select_tests(["scripts/research.py"], {"test_impact.py"})

    def test_empty_change_list_selects_no_specific_tests(self):
        result = impact.select_tests([], AVAILABLE)
        self.assertFalse(result["full_suite"])
        self.assertEqual(result["tests"], [])
        self.assertEqual(result["commands"], [])

    def test_git_diff_reads_paths_without_running_code(self):
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp)
            for args in (["git", "init", "-q"], ["git", "config", "user.email", "test@example.invalid"],
                         ["git", "config", "user.name", "Test"], ["git", "add", "file.py"]):
                if args[-1] == "file.py":
                    (work / "file.py").write_text("ok\n")
                subprocess.run(args, cwd=work, check=True, capture_output=True)
            subprocess.run(["git", "commit", "-qm", "fixture"], cwd=work, check=True)
            (work / "file.py").write_text("modified\n")
            result = impact.changed_since("HEAD", root=work)
            self.assertEqual(result, ["file.py"])

    def test_rejects_revision_arguments_that_look_like_flags(self):
        with self.assertRaises(ValueError):
            impact.changed_since("--output=/tmp/exploit")


if __name__ == "__main__":
    unittest.main()

"""Check frozen comparison inputs only; no model or behavioral grading occurs."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ComparisonFixtureTests(unittest.TestCase):
    def setUp(self):
        self.plan = json.loads((ROOT / "evaluations/client-comparison.json").read_text(encoding="utf-8"))

    def test_unexecuted_status_cannot_be_mistaken_for_results(self):
        self.assertEqual(self.plan["status"], "NOT_RUN")
        self.assertEqual(self.plan["blocker"], "BLOCKED_BY_AUTH")
        self.assertEqual(self.plan["runs"], [])
        self.assertIn("not a hidden holdout", self.plan["split"])
        self.assertTrue(all(value is None for value in self.plan["runtime_to_freeze"].values()))

    def test_three_conditions_vary_only_the_declared_instructions(self):
        conditions = {c["id"]: c for c in self.plan["conditions"]}
        self.assertEqual(set(conditions), {"base", "released-0.4.0", "candidate"})
        self.assertEqual(conditions["base"]["instructions"], [])
        for condition in conditions.values():
            self.assertFalse(set(condition) - {"id", "instructions", "source_commit"})
        old, new = conditions["released-0.4.0"], conditions["candidate"]
        self.assertEqual(old["source_commit"], "6abd610afaaa376c014aad409723fc976fd721f4")
        self.assertIsNone(new["source_commit"])
        for condition in (old, new):
            self.assertEqual({f["skill"] for f in condition["instructions"]},
                             {"scope-guardian", "code-review-engineer"})
            for item in condition["instructions"]:
                path = ROOT / item["path"]
                self.assertTrue(path.resolve().is_relative_to(ROOT))
                self.assertFalse(path.is_symlink())
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), item["sha256"])
        old_hashes = {f["skill"]: f["sha256"] for f in old["instructions"]}
        new_hashes = {f["skill"]: f["sha256"] for f in new["instructions"]}
        self.assertNotEqual(old_hashes["scope-guardian"], new_hashes["scope-guardian"])
        self.assertEqual(old_hashes["code-review-engineer"], new_hashes["code-review-engineer"])

    def test_shared_inputs_reuse_the_existing_synthetic_bug(self):
        spec = importlib.util.spec_from_file_location("probe", ROOT / "scripts/client_probe.py")
        probe = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(probe)
        files = self.plan["shared_files"]
        self.assertEqual(files["buggy.py"], probe.BUGGY)
        self.assertEqual(set(files), set(self.plan["shared_file_sha256"]))
        for name, text in files.items():
            self.assertEqual(Path(name).name, name)
            self.assertEqual(hashlib.sha256(text.encode("utf-8")).hexdigest(),
                             self.plan["shared_file_sha256"][name])
        self.assertNotIn("missing.py", files)

    def test_shared_cases_cover_required_boundaries_and_observable_rejections(self):
        cases = self.plan["cases"]
        self.assertEqual(len({c["id"] for c in cases}), len(cases))
        self.assertEqual({c["category"] for c in cases},
                         {"scope", "success", "failure", "security", "negative-activation"})
        for case in cases:
            self.assertEqual(set(case), {"id", "category", "prompt", "accept", "reject"})
            self.assertTrue(case["prompt"].strip())
            self.assertTrue(case["accept"])
            self.assertTrue(case["reject"])
        self.assertEqual(self.plan["shared_budget"]["repetitions"], 3)
        self.assertEqual(self.plan["shared_tools"]["allow"], ["read_project_files"])
        self.assertIn("writes", self.plan["shared_tools"]["deny"])
        self.assertIn("subagents", self.plan["shared_tools"]["deny"])

    def test_materialized_conditions_preserve_identical_project_bytes(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            for condition in self.plan["conditions"]:
                project = base / condition["id"]
                project.mkdir()
                for name, text in self.plan["shared_files"].items():
                    (project / name).write_bytes(text.encode("utf-8"))
                for instruction in condition["instructions"]:
                    target = project / ".agents" / "skills" / instruction["skill"] / "SKILL.md"
                    target.parent.mkdir(parents=True)
                    target.write_bytes((ROOT / instruction["path"]).read_bytes())
                for name, expected in self.plan["shared_file_sha256"].items():
                    self.assertEqual(hashlib.sha256((project / name).read_bytes()).hexdigest(), expected)
                self.assertFalse((project / ".codex").exists())
                self.assertFalse((project / "AGENTS.md").exists())
                self.assertEqual(len(list(project.glob(".agents/skills/*/SKILL.md"))),
                                 len(condition["instructions"]))
            self.assertFalse((base / "base" / ".agents").exists())


if __name__ == "__main__":
    unittest.main()

"""Offline fixture integrity tests; not live Codex skill evaluations."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "client_probe.py"
spec = importlib.util.spec_from_file_location("odg_probe", SCRIPT)
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)


class ProbeTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.source = self.base / "source"
        for name in probe.SKILLS:
            folder = self.source / "skills" / name
            folder.mkdir(parents=True)
            (folder / "SKILL.md").write_text("---\nname: example\n---\n")
            (folder / "references").mkdir()
            (folder / "references" / "note.md").write_text("reference")
        agent = self.source / ".codex" / "agents"
        agent.mkdir(parents=True)
        (agent / probe.PROFILE).write_text('name = "reviewer"\n')
        self.destination = self.base / "trial"

    def test_prepares_bounded_fixture_and_integrity_check(self):
        info = probe.prepare(self.destination, root=self.source)
        self.assertEqual(info["status"], "PREPARED_NOT_RUN")
        self.assertEqual(info["scenarios"], 3)
        self.assertEqual(probe.check(self.destination)["status"], "UNCHANGED")
        self.assertIn("+ discount", (self.destination / "buggy.py").read_text())
        self.assertNotIn("# BUG", (self.destination / "buggy.py").read_text())

    def test_rejects_existing_destination_without_replacing(self):
        self.destination.mkdir()
        marker = self.destination / "untouched"
        marker.write_text("keep")
        with self.assertRaisesRegex(ValueError, "exists"):
            probe.prepare(self.destination, root=self.source)
        self.assertEqual(marker.read_text(), "keep")

    def test_rejects_symlink_in_source_without_writing(self):
        link = self.source / "skills" / probe.SKILLS[0] / "shortcut"
        try:
            link.symlink_to(self.base / "outside")
        except (OSError, NotImplementedError):
            self.skipTest("symlinks unavailable on this platform")
        with self.assertRaisesRegex(ValueError, "symlink"):
            probe.prepare(self.destination, root=self.source)
        self.assertFalse(self.destination.exists())

    def test_detects_modified_and_added_files(self):
        probe.prepare(self.destination, root=self.source)
        (self.destination / "buggy.py").write_text("changed")
        (self.destination / "new.txt").write_text("unexpected")
        evidence = probe.check(self.destination)
        self.assertEqual(evidence["status"], "CHANGED")
        self.assertEqual(evidence["changed"], ["buggy.py"])
        self.assertEqual(evidence["additional"], ["new.txt"])

    def test_rejects_unsafe_manifest_path(self):
        import json
        probe.prepare(self.destination, root=self.source)
        path = self.destination / "manifest.json"
        manifest = json.loads(path.read_text())
        manifest["files"] = {"../untrusted": "0" * 64}
        path.write_text(json.dumps(manifest))
        with self.assertRaisesRegex(ValueError, "unsafe"):
            probe.check(self.destination)

    def test_rejects_missing_required_source(self):
        (self.source / ".codex" / "agents" / probe.PROFILE).unlink()
        with self.assertRaisesRegex(ValueError, "profile"):
            probe.prepare(self.destination, root=self.source)
        self.assertFalse(self.destination.exists())

    def test_rejects_output_parent_symlink(self):
        link = self.base / "link"
        try:
            link.symlink_to(self.base, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("symlinks unavailable on this platform")
        with self.assertRaisesRegex(ValueError, "symlink"):
            probe.prepare(link / "trial", root=self.source)


if __name__ == "__main__":
    unittest.main()

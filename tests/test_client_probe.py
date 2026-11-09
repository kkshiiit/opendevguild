"""Offline fixture integrity tests; not live Codex skill evaluations."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

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

    def test_rejects_output_ancestor_symlink_before_writing(self):
        outside = self.base / "outside"
        (outside / "nested").mkdir(parents=True)
        alias = self.base / "alias"
        try:
            alias.symlink_to(outside, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("symlinks unavailable on this platform")
        with self.assertRaisesRegex(ValueError, "symlink"):
            probe.prepare(alias / "nested" / "trial", root=self.source)
        self.assertFalse((outside / "nested" / "trial").exists())

    def test_rejects_source_ancestor_symlink_before_writing(self):
        alias = self.base / "alias"
        try:
            alias.symlink_to(self.base, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("symlinks unavailable on this platform")
        with self.assertRaisesRegex(ValueError, "symlink"):
            probe.prepare(self.destination, root=alias / "source")
        self.assertFalse(self.destination.exists())

    def test_detects_added_dangling_symlink(self):
        probe.prepare(self.destination, root=self.source)
        try:
            (self.destination / "unexpected-link").symlink_to(self.base / "missing")
        except (OSError, NotImplementedError):
            self.skipTest("symlinks unavailable on this platform")
        evidence = probe.check(self.destination)
        self.assertEqual(evidence["status"], "CHANGED")
        self.assertEqual(evidence["additional"], ["unexpected-link"])

    def test_rejects_fixture_ancestor_symlink(self):
        probe.prepare(self.destination, root=self.source)
        alias = self.base / "alias"
        try:
            alias.symlink_to(self.base, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("symlinks unavailable on this platform")
        with self.assertRaisesRegex(ValueError, "symlink"):
            probe.check(alias / "trial")

    def test_malformed_manifest_has_controlled_cli_error(self):
        probe.prepare(self.destination, root=self.source)
        for value in ([], None, 42, "manifest"):
            with self.subTest(value=value):
                (self.destination / "manifest.json").write_text(json.dumps(value))
                result = subprocess.run(
                    [sys.executable, str(SCRIPT), "check", "--fixture", str(self.destination)],
                    capture_output=True, text=True,
                )
                self.assertEqual(result.returncode, 2)
                self.assertEqual(json.loads(result.stderr)["status"], "ERROR")
                self.assertNotIn("Traceback", result.stderr)

    def test_deep_manifest_has_controlled_cli_error(self):
        probe.prepare(self.destination, root=self.source)
        (self.destination / "manifest.json").write_text("[" * 50000 + "0" + "]" * 50000)
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "check", "--fixture", str(self.destination)],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stderr)["status"], "ERROR")
        self.assertNotIn("Traceback", result.stderr)

    @unittest.skipUnless(hasattr(os, "mkfifo"), "FIFO files unavailable")
    def test_source_special_entry_rejected_before_writing(self):
        os.mkfifo(self.source / "skills" / probe.SKILLS[0] / "pipe")
        with self.assertRaisesRegex(ValueError, "regular"):
            probe.prepare(self.destination, root=self.source)
        self.assertFalse(self.destination.exists())

    def test_oversized_source_rejected_before_writing(self):
        with patch.object(probe, "MAX_FILE_BYTES", 64):
            (self.source / "skills" / probe.SKILLS[0] / "large.md").write_bytes(b"x" * 65)
            with self.assertRaisesRegex(ValueError, "budget"):
                probe.prepare(self.destination, root=self.source)
        self.assertFalse(self.destination.exists())

    def test_source_total_budget_rejected_before_writing(self):
        with patch.object(probe, "MAX_TOTAL_BYTES", 1):
            with self.assertRaisesRegex(ValueError, "budget"):
                probe.prepare(self.destination, root=self.source)
        self.assertFalse(self.destination.exists())

    def test_source_file_count_budget_rejected_before_writing(self):
        with patch.object(probe, "MAX_FILES", 1):
            with self.assertRaisesRegex(ValueError, "budget"):
                probe.prepare(self.destination, root=self.source)
        self.assertFalse(self.destination.exists())

    def test_source_entry_budget_includes_empty_directories(self):
        with patch.object(probe, "MAX_ENTRIES", 1):
            with self.assertRaisesRegex(ValueError, "budget"):
                probe.prepare(self.destination, root=self.source)
        self.assertFalse(self.destination.exists())

    def test_rejects_oversized_manifest_before_parsing(self):
        probe.prepare(self.destination, root=self.source)
        with patch.object(probe, "MAX_MANIFEST_BYTES", 1):
            with self.assertRaisesRegex(ValueError, "budget"):
                probe.check(self.destination)

    def test_rejects_duplicate_manifest_keys(self):
        probe.prepare(self.destination, root=self.source)
        manifest = self.destination / "manifest.json"
        text = manifest.read_text().replace('"kind":', '"kind":"forged", "kind":', 1)
        manifest.write_text(text)
        with self.assertRaisesRegex(ValueError, "duplicate"):
            probe.check(self.destination)

    def test_manifest_budget_preflight_does_not_create_output(self):
        with patch.object(probe, "MAX_MANIFEST_BYTES", 1):
            with self.assertRaisesRegex(ValueError, "budget"):
                probe.prepare(self.destination, root=self.source)
        self.assertFalse(self.destination.exists())

    def test_rejects_oversized_registered_file_when_checking(self):
        probe.prepare(self.destination, root=self.source)
        (self.destination / "buggy.py").write_bytes(b"x" * (probe.MAX_FILE_BYTES + 1))
        with self.assertRaisesRegex(ValueError, "budget"):
            probe.check(self.destination)

    def test_check_total_and_entry_budgets(self):
        probe.prepare(self.destination, root=self.source)
        for name in ("MAX_TOTAL_BYTES", "MAX_ENTRIES", "MAX_FILES"):
            with self.subTest(name=name), patch.object(probe, name, 1):
                with self.assertRaisesRegex(ValueError, "budget"):
                    probe.check(self.destination)

    @unittest.skipUnless(hasattr(os, "mkfifo"), "FIFO files unavailable")
    def test_nonregular_manifest_is_rejected_without_reading(self):
        probe.prepare(self.destination, root=self.source)
        manifest = self.destination / "manifest.json"
        manifest.unlink()
        os.mkfifo(manifest)
        with self.assertRaisesRegex(ValueError, "regular"):
            probe.check(self.destination)

    def test_added_directory_link_is_reported_without_descending(self):
        probe.prepare(self.destination, root=self.source)
        outside = self.base / "outside"
        outside.mkdir()
        (outside / "not-part-of-fixture.txt").write_text("synthetic external file")
        try:
            (self.destination / "alias").symlink_to(outside, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("symlinks unavailable on this platform")
        evidence = probe.check(self.destination)
        self.assertEqual(evidence["additional"], ["alias"])

    @unittest.skipUnless(os.name == "nt", "requires native Windows junctions")
    def test_windows_junction_ancestor_is_rejected(self):
        outside = self.base / "outside"
        (outside / "nested").mkdir(parents=True)
        alias = self.base / "junction"
        result = subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(alias), str(outside)],
            capture_output=True, text=True,
        )
        if result.returncode:
            self.skipTest("junction creation unavailable")
        self.addCleanup(alias.rmdir)
        with self.assertRaisesRegex(ValueError, "junction"):
            probe.prepare(alias / "nested" / "trial", root=self.source)
        self.assertFalse((outside / "nested" / "trial").exists())


if __name__ == "__main__":
    unittest.main()

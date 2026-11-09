"""Offline Claude adapter policy/packaging checks, not native loading tests."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('claude_guild', ROOT / 'scripts/guild.py')
guild = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guild)


class ClaudePluginTests(unittest.TestCase):
    def fixture(self, root):
        for name in ('.claude-plugin/plugin.json', 'agents/reviewer.md'):
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, path)

    def test_native_manifest_and_single_read_only_reviewer(self):
        self.assertEqual(guild.validate_claude_plugin(ROOT, '0.4.1'), [])

    def test_plugin_manifest_does_not_silently_enable_capabilities(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); self.fixture(root)
            path = root / '.claude-plugin/plugin.json'
            data = json.loads(path.read_text(encoding='utf-8'))
            data['hooks'] = {'SessionStart': []}
            path.write_text(json.dumps(data), encoding='utf-8')
            self.assertTrue(guild.validate_claude_plugin(root, '0.4.1'))

    def test_auto_discovered_components_cannot_bypass_minimal_manifest(self):
        for name in ('.mcp.json', 'hooks', 'settings.json', 'commands'):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                root = Path(directory); self.fixture(root)
                (root / name).write_text('{}', encoding='utf-8')
                self.assertTrue(guild.validate_claude_plugin(root, '0.4.1'))

    def test_escaped_agent_reference_and_version_mismatch_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); self.fixture(root)
            path = root / '.claude-plugin/plugin.json'
            data = json.loads(path.read_text(encoding='utf-8'))
            data['agents'] = ['../outside.md']; data['version'] = '0.0.0'
            path.write_text(json.dumps(data), encoding='utf-8')
            self.assertTrue(guild.validate_claude_plugin(root, '0.4.1'))

    def test_shell_and_ignored_permission_override_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); self.fixture(root)
            path = root / 'agents/reviewer.md'; original = path.read_text(encoding='utf-8')
            for mutation in ('tools: Read, Grep, Glob, Bash', 'tools: Read, Grep, Glob\npermissionMode: bypassPermissions'):
                with self.subTest(mutation=mutation):
                    path.write_text(original.replace('tools: Read, Grep, Glob', mutation), encoding='utf-8')
                    self.assertTrue(guild.validate_claude_plugin(root, '0.4.1'))

    def test_distribution_includes_adapter_but_no_private_claude_state(self):
        files = {p.relative_to(ROOT).as_posix() for p in guild.source_files(ROOT)}
        self.assertIn('.claude-plugin/plugin.json', files)
        self.assertIn('agents/reviewer.md', files)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); self.fixture(root)
            for name in ('.claude/settings.local.json', '.claude/credentials.json', '.claude-plugin/local-state.json'):
                path = root / name; path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('synthetic private state', encoding='utf-8')
            selected = {p.relative_to(root).as_posix() for p in guild.source_files(root)}
            self.assertEqual(selected, {'.claude-plugin/plugin.json', 'agents/reviewer.md'})

    def test_linked_plugin_directory_is_rejected_before_content_read(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); outside = root / 'outside'; outside.mkdir()
            try:
                (root / '.claude-plugin').symlink_to(outside, target_is_directory=True)
            except (OSError, NotImplementedError):
                self.skipTest('symlink creation unavailable')
            with self.assertRaises(ValueError):
                guild.source_files(root)
            self.assertTrue(guild.validate_claude_plugin(root, '0.4.1'))

    @unittest.skipUnless(hasattr(os, 'mkfifo'), 'FIFO unavailable on this platform')
    def test_special_adapter_files_are_rejected_without_reading(self):
        for name in ('.claude-plugin/plugin.json', 'agents/reviewer.md'):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                root = Path(directory); self.fixture(root)
                path = root / name; path.unlink(); os.mkfifo(path)
                with mock.patch.object(Path, 'read_text', side_effect=AssertionError('Must not read special file')):
                    with self.assertRaisesRegex(ValueError, 'Non-regular'):
                        guild.source_files(root)
                    self.assertTrue(guild.validate_claude_plugin(root, '0.4.1'))


if __name__ == '__main__':
    unittest.main()

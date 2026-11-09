"""Optional local installer preserves user work and supports managed rollback."""
import json
import contextlib
import importlib.util
import io
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/install.py'


class InstallationTests(unittest.TestCase):
    def engine(self):
        spec=importlib.util.spec_from_file_location('odg_installer',SCRIPT)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        return module

    def test_manifest_budget_rejects_before_files_or_backups_change(self):
        self.install();module=self.engine()
        manifest=next(self.target.parent.glob('.opendevguild-state/*/manifest.json'))
        before=manifest.read_bytes();files={p.relative_to(self.base):p.read_bytes() for p in self.base.rglob('*') if p.is_file()}
        with mock.patch.object(module,'MAX_MANIFEST_BYTES',len(before)+8),contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(ValueError):module.execute('update',self.source,self.target,['mission-control'])
        self.assertEqual(files,{p.relative_to(self.base):p.read_bytes() for p in self.base.rglob('*') if p.is_file()})

    def test_full_history_still_permits_uninstall_and_corrective_rollback(self):
        module=self.engine()
        with contextlib.redirect_stdout(io.StringIO()):
            module.execute('install',self.source,self.target,['mission-control'])
            for _ in range(48):module.execute('update',self.source,self.target,['mission-control'])
            module.execute('uninstall',self.source,self.target,['mission-control'])
            module.execute('rollback',self.source,self.target,['mission-control'])
        self.assertTrue((self.target/'mission-control/SKILL.md').is_file())
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.target = self.base / 'project/.agents/skills'
        self.source = self.base / 'source'
        for name in ('mission-control', 'scope-guardian'):
            directory = self.source / 'skills' / name
            directory.mkdir(parents=True)
            (directory / 'SKILL.md').write_text(f'---\nname: {name}\ndescription: Synthetic installer fixture.\n---\nOriginal\n', encoding='utf-8')
        (self.source / 'plugin.json').write_text(json.dumps({'version': '0.3.0'}))

    def run_install(self, action, *extra, skill='mission-control'):
        return subprocess.run([sys.executable, str(SCRIPT), action, '--source', str(self.source),
                               '--target', str(self.target), '--skill', skill, *extra],
                              capture_output=True, text=True)

    def install(self):
        result = self.run_install('install')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_install_dry_run_writes_nothing_and_lists_file(self):
        result = self.run_install('install', '--dry-run')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('SKILL.md', result.stdout)
        self.assertFalse(self.target.parent.exists())

    def test_install_from_actual_checkout_and_collision_preserve_bytes(self):
        result = subprocess.run([sys.executable, str(SCRIPT), 'install', '--source', str(ROOT),
                                 '--target', str(self.target), '--skill', 'mission-control'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        installed = self.target / 'mission-control/SKILL.md'
        self.assertEqual(installed.read_bytes(), (ROOT / 'skills/mission-control/SKILL.md').read_bytes())
        original = installed.read_bytes()
        result = self.run_install('install')
        self.assertEqual(result.returncode, 1)
        self.assertEqual(installed.read_bytes(), original)

    def test_update_and_rollback_restore_managed_previous_version(self):
        self.install()
        file = self.source / 'skills/mission-control/SKILL.md'
        old = file.read_bytes(); file.write_text(file.read_text(encoding='utf-8') + 'Updated\n', encoding='utf-8')
        self.assertEqual(self.run_install('update').returncode, 0)
        self.assertNotEqual((self.target / 'mission-control/SKILL.md').read_bytes(), old)
        self.assertEqual(self.run_install('rollback').returncode, 0)
        self.assertEqual((self.target / 'mission-control/SKILL.md').read_bytes(), old)

    def test_update_uninstall_and_rollback_reject_user_changes(self):
        self.install()
        file = self.target / 'mission-control/SKILL.md'
        file.write_text('User-owned edited content', encoding='utf-8')
        for action in ('update', 'uninstall', 'rollback'):
            with self.subTest(action=action):
                result = self.run_install(action)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertEqual(file.read_text(encoding='utf-8'), 'User-owned edited content')

    def test_uninstall_preserves_unrelated_work_and_can_rollback(self):
        self.install()
        other = self.target / 'unrelated/SKILL.md'; other.parent.mkdir(); other.write_text('Unrelated')
        original = (self.target / 'mission-control/SKILL.md').read_bytes()
        self.assertEqual(self.run_install('uninstall').returncode, 0)
        self.assertFalse((self.target / 'mission-control').exists())
        self.assertEqual(other.read_text(), 'Unrelated')
        self.assertEqual(self.run_install('rollback').returncode, 0)
        self.assertEqual((self.target / 'mission-control/SKILL.md').read_bytes(), original)

    def test_added_user_file_blocks_destructive_operations(self):
        self.install(); (self.target / 'mission-control/user.txt').write_text('Keep')
        self.assertEqual(self.run_install('uninstall').returncode, 1)
        self.assertTrue((self.target / 'mission-control/user.txt').exists())

    def test_batch_collision_preflight_prevents_partial_install(self):
        directory = self.target / 'scope-guardian'; directory.mkdir(parents=True)
        (directory / 'SKILL.md').write_text('Existing')
        result = self.run_install('install', '--skill', 'scope-guardian')
        self.assertEqual(result.returncode, 1)
        self.assertFalse((self.target / 'mission-control').exists())

    def test_traversal_identifier_is_rejected(self):
        self.assertEqual(self.run_install('install', skill='../outside').returncode, 1)
        self.assertFalse(self.target.exists())

    def test_backups_stay_outside_discovery(self):
        self.install()
        self.assertEqual([p.relative_to(self.target).as_posix() for p in self.target.rglob('SKILL.md')],
                         ['mission-control/SKILL.md'])

    def test_corrupt_manifest_is_rejected(self):
        self.install()
        manifests = list(self.target.parent.glob('.opendevguild-state/*/manifest.json'))
        self.assertEqual(len(manifests), 1)
        manifests[0].write_text('{invalid', encoding='utf-8')
        self.assertEqual(self.run_install('uninstall').returncode, 1)
        self.assertTrue((self.target / 'mission-control/SKILL.md').exists())

    def test_managed_manifest_path_escape_is_rejected(self):
        self.install()
        manifest = next(self.target.parent.glob('.opendevguild-state/*/manifest.json'))
        data = json.loads(manifest.read_text(encoding='utf-8'))
        data['skills']['mission-control']['files']['../../outside'] = 'a' * 64
        manifest.write_text(json.dumps(data), encoding='utf-8')
        self.assertEqual(self.run_install('uninstall').returncode, 1)
        self.assertTrue((self.target / 'mission-control/SKILL.md').exists())

    def test_source_and_target_symlinks_are_rejected(self):
        external = self.base / 'outside'; external.mkdir()
        link = self.source / 'skills/mission-control/linked'
        try:
            link.symlink_to(external, target_is_directory=True)
        except OSError as error:
            self.skipTest(f'Host cannot create symlink fixture: {error}')
        self.assertEqual(self.run_install('install').returncode, 1)
        self.assertFalse(self.target.exists())
        link.unlink()
        self.target.parent.mkdir(parents=True)
        self.target.symlink_to(external, target_is_directory=True)
        self.assertEqual(self.run_install('install').returncode, 1)

    def test_update_dry_run_does_not_change_files_or_state(self):
        self.install()
        manifest = next(self.target.parent.glob('.opendevguild-state/*/manifest.json'))
        old = manifest.read_bytes()
        result = self.run_install('update', '--dry-run')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('BACKUP', result.stdout)
        self.assertEqual(manifest.read_bytes(), old)

    def test_tampered_backup_cannot_be_restored(self):
        self.install()
        self.assertEqual(self.run_install('uninstall').returncode, 0)
        backup = next(self.target.parent.glob('.opendevguild-state/*/backups/*/SKILL.md'))
        backup.write_text('Changed backup', encoding='utf-8')
        self.assertEqual(self.run_install('rollback').returncode, 1)
        self.assertFalse((self.target / 'mission-control').exists())


if __name__ == '__main__':
    unittest.main()

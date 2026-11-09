"""Optional local installer preserves user work and supports managed rollback."""
import json
import contextlib
import importlib.util
import io
import os
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

    def managed_bytes(self):
        files = {p.relative_to(self.target).as_posix(): p.read_bytes()
                 for p in self.target.rglob('*') if p.is_file()} if self.target.exists() else {}
        manifests = list(self.target.parent.glob('.opendevguild-state/*/manifest.json'))
        return files, manifests[0].read_bytes() if manifests else None

    def invoke(self, module, action, names=('mission-control',)):
        with contextlib.redirect_stdout(io.StringIO()):
            return module.execute(action, self.source, self.target, list(names))

    def change_source(self):
        for name in ('mission-control', 'scope-guardian'):
            path = self.source / 'skills' / name / 'SKILL.md'
            path.write_text(path.read_text(encoding='utf-8') + 'Replacement\n', encoding='utf-8')

    def test_update_partial_copy_failure_preserves_installed_bytes_and_manifest(self):
        self.install(); self.change_source(); module = self.engine()
        before = self.managed_bytes()
        copytree = module.shutil.copytree

        def fail_copy(source, destination, *args, **kwargs):
            if Path(source).resolve() == (self.source / 'skills/mission-control').resolve():
                Path(destination).mkdir(parents=True)
                (Path(destination) / 'SKILL.md').write_text('Partial copy', encoding='utf-8')
                raise OSError('injected replacement copy failure')
            return copytree(source, destination, *args, **kwargs)

        with mock.patch.object(module.shutil, 'copytree', side_effect=fail_copy):
            with self.assertRaises(OSError):
                self.invoke(module, 'update')
        self.assertEqual(self.managed_bytes(), before)

    def assert_manifest_failure_preserves(self, action, names=('mission-control',)):
        module = self.engine()
        if action != 'install':
            self.invoke(module, 'install', names)
        self.change_source()
        if action == 'rollback':
            self.invoke(module, 'update', names)
        before = self.managed_bytes()
        replace = module.os.replace

        def fail_manifest(source, destination):
            if Path(destination).name == 'manifest.json':
                raise OSError('injected manifest publication failure')
            return replace(source, destination)

        with mock.patch.object(module.os, 'replace', side_effect=fail_manifest):
            with self.assertRaises(OSError):
                self.invoke(module, action, names)
        self.assertEqual(self.managed_bytes(), before)

    def test_install_manifest_failure_reverts_entire_operation(self):
        self.assert_manifest_failure_preserves('install')

    def test_update_manifest_failure_reverts_entire_operation(self):
        self.assert_manifest_failure_preserves('update')

    def test_uninstall_manifest_failure_reverts_entire_operation(self):
        self.assert_manifest_failure_preserves('uninstall')

    def test_rollback_manifest_failure_reverts_entire_operation(self):
        self.assert_manifest_failure_preserves('rollback')

    def test_second_skill_copy_failure_does_not_partially_update_batch(self):
        module = self.engine(); names = ('mission-control', 'scope-guardian')
        self.invoke(module, 'install', names); self.change_source()
        before = self.managed_bytes(); copytree = module.shutil.copytree

        def fail_second(source, destination, *args, **kwargs):
            if Path(source).resolve() == (self.source / 'skills/scope-guardian').resolve():
                raise OSError('injected second skill copy failure')
            return copytree(source, destination, *args, **kwargs)

        with mock.patch.object(module.shutil, 'copytree', side_effect=fail_second):
            with self.assertRaises(OSError):
                self.invoke(module, 'update', names)
        self.assertEqual(self.managed_bytes(), before)

    def test_manifest_preparation_write_failure_preserves_batch(self):
        module = self.engine(); names = ('mission-control', 'scope-guardian')
        self.invoke(module, 'install', names); self.change_source()
        before = self.managed_bytes(); write_text = Path.write_text

        def fail_write(path, *args, **kwargs):
            if path.name.startswith('manifest-'):
                path.write_bytes(b'{"partial":')
                raise OSError('injected manifest preparation failure')
            return write_text(path, *args, **kwargs)

        with mock.patch.object(Path, 'write_text', autospec=True, side_effect=fail_write):
            with self.assertRaises(OSError):
                self.invoke(module, 'update', names)
        self.assertEqual(self.managed_bytes(), before)

    def test_second_skill_swap_failure_restores_first_skill_and_manifest(self):
        module = self.engine(); names = ('mission-control', 'scope-guardian')
        self.invoke(module, 'install', names); self.change_source()
        before = self.managed_bytes(); replace = module.os.replace

        def fail_swap(source, destination):
            if Path(source).parent.name == 'staged' and Path(destination).name == 'scope-guardian':
                raise OSError('injected second skill promotion failure')
            return replace(source, destination)

        with mock.patch.object(module.os, 'replace', side_effect=fail_swap):
            with self.assertRaises(OSError):
                self.invoke(module, 'update', names)
        self.assertEqual(self.managed_bytes(), before)

    def leave_pending_recovery(self):
        module = self.engine(); names = ('mission-control', 'scope-guardian')
        self.invoke(module, 'install', names); self.change_source()
        before = self.managed_bytes(); replace = module.os.replace

        def fail_publication_and_restore(source, destination):
            if Path(destination).name == 'manifest.json' or Path(source).parent.name == 'backups':
                raise OSError('injected publication and restoration failure')
            return replace(source, destination)

        with mock.patch.object(module.os, 'replace', side_effect=fail_publication_and_restore):
            with self.assertRaisesRegex(OSError, 'recovery pending'):
                self.invoke(module, 'update', names)
        state = next(self.target.parent.glob('.opendevguild-state/*'))
        return module, names, before, state

    def test_failed_restoration_retains_originals_blocks_operations_and_recovers_batch(self):
        module, names, before, state = self.leave_pending_recovery()
        self.assertEqual((state / 'manifest.json').read_bytes(), before[1])
        self.assertTrue((state / 'pending.json').is_file())
        journal = json.loads((state / 'pending.json').read_text(encoding='utf-8'))
        for op in journal['operations']:
            original = state / 'backups' / op['snapshot'] / 'SKILL.md'
            self.assertEqual(original.read_bytes(), before[0][op['name'] + '/SKILL.md'])
        for action in ('install', 'update', 'uninstall', 'rollback'):
            with self.subTest(action=action), self.assertRaisesRegex(ValueError, 'recovery pending'):
                self.invoke(module, action, names)
        snapshot = {p.relative_to(state): p.read_bytes() for p in state.rglob('*') if p.is_file()}
        with contextlib.redirect_stdout(io.StringIO()):
            module.execute('recover', self.source, self.target, [], dry_run=True)
        self.assertEqual(snapshot, {p.relative_to(state): p.read_bytes() for p in state.rglob('*') if p.is_file()})
        result = self.run_install('recover')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.managed_bytes(), before)
        self.assertFalse((state / 'pending.json').exists())

    def test_recovery_refuses_user_changes_without_moving_other_skills(self):
        module, names, before, state = self.leave_pending_recovery()
        path = self.target / 'mission-control/SKILL.md'
        path.write_text('User changes after failure', encoding='utf-8')
        files = {p.relative_to(self.base): p.read_bytes() for p in self.base.rglob('*') if p.is_file()}
        with self.assertRaisesRegex(ValueError, 'User changes'):
            self.invoke(module, 'recover', ())
        self.assertEqual(files, {p.relative_to(self.base): p.read_bytes() for p in self.base.rglob('*') if p.is_file()})

    def test_corrupt_or_traversal_journal_cannot_authorize_recovery(self):
        module, names, before, state = self.leave_pending_recovery()
        path = state / 'pending.json'; journal = json.loads(path.read_text(encoding='utf-8'))
        for mutation in ('name', 'missing', 'snapshot'):
            data = json.loads(json.dumps(journal))
            if mutation == 'name': data['operations'][0]['name'] = '../outside'
            elif mutation == 'missing': data['operations'].pop()
            else: data['operations'][0]['snapshot'] = '../outside'
            path.write_text(json.dumps(data), encoding='utf-8')
            files = {p.relative_to(self.base): p.read_bytes() for p in self.base.rglob('*') if p.is_file()}
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                self.invoke(module, 'recover', ())
            self.assertEqual(files, {p.relative_to(self.base): p.read_bytes() for p in self.base.rglob('*') if p.is_file()})

    def test_cleanup_failure_after_commit_preserves_new_batch_and_pending_marker(self):
        module = self.engine(); names = ('mission-control', 'scope-guardian')
        self.invoke(module, 'install', names); self.change_source()
        remove = module.shutil.rmtree

        def fail_cleanup(path, *args, **kwargs):
            if Path(path).name == 'transaction':
                # Simulate partial cleanup, including deletion of the staged directory.
                staged = Path(path) / 'staged'
                if staged.exists(): remove(staged)
                raise OSError('injected cleanup failure')
            return remove(path, *args, **kwargs)

        stderr = io.StringIO()
        with mock.patch.object(module.shutil, 'rmtree', side_effect=fail_cleanup), contextlib.redirect_stderr(stderr):
            self.invoke(module, 'update', names)
        self.assertIn('batch committed', stderr.getvalue())
        state = next(self.target.parent.glob('.opendevguild-state/*'))
        self.assertTrue((state / 'pending.json').is_file())
        data = json.loads((state / 'manifest.json').read_text(encoding='utf-8'))
        for name in names:
            self.assertEqual((self.target / name / 'SKILL.md').read_bytes(),
                             (self.source / 'skills' / name / 'SKILL.md').read_bytes())
            self.assertEqual(module.inspect(self.target / name)['files'], data['skills'][name]['files'])
        expected = self.managed_bytes()
        self.invoke(module, 'recover', ())
        self.assertEqual(self.managed_bytes(), expected)
        self.assertFalse((state / 'pending.json').exists())

    def test_failed_first_install_can_be_retried(self):
        module = self.engine(); copytree = module.shutil.copytree
        with mock.patch.object(module.shutil, 'copytree', side_effect=OSError('injected first copy failure')):
            with self.assertRaises(OSError): self.invoke(module, 'install')
        self.assertEqual(self.managed_bytes(), ({}, None))
        with mock.patch.object(module.shutil, 'copytree', wraps=copytree):
            self.invoke(module, 'install')
        self.assertTrue((self.target / 'mission-control/SKILL.md').is_file())

    def test_staging_copy_is_verified_before_original_is_retired(self):
        self.install(); self.change_source(); module = self.engine()
        before = self.managed_bytes(); copytree = module.shutil.copytree

        def corrupt_copy(source, destination, *args, **kwargs):
            result = copytree(source, destination, *args, **kwargs)
            (Path(destination) / 'SKILL.md').write_text('Corrupted staged bytes', encoding='utf-8')
            return result

        with mock.patch.object(module.shutil, 'copytree', side_effect=corrupt_copy):
            with self.assertRaises(ValueError): self.invoke(module, 'update')
        self.assertEqual(self.managed_bytes(), before)

    def test_all_four_actions_preserve_multiskill_batch_on_manifest_failure(self):
        for action in ('install', 'update', 'uninstall', 'rollback'):
            with self.subTest(action=action):
                self.target = self.base / f'batch-{action}/.agents/skills'
                self.assert_manifest_failure_preserves(action, ('mission-control', 'scope-guardian'))

    def test_batch_uninstall_retirement_failure_restores_earlier_skill(self):
        module = self.engine(); names = ('mission-control', 'scope-guardian')
        self.invoke(module, 'install', names)
        before = self.managed_bytes(); replace = module.os.replace

        def fail_retirement(source, destination):
            if Path(source).name == 'scope-guardian' and Path(destination).parent.name == 'backups':
                raise OSError('injected second retirement failure')
            return replace(source, destination)

        with mock.patch.object(module.os, 'replace', side_effect=fail_retirement):
            with self.assertRaises(OSError): self.invoke(module, 'uninstall', names)
        self.assertEqual(self.managed_bytes(), before)

    def test_process_interruption_after_retirement_is_explicitly_recoverable(self):
        module = self.engine(); names = ('mission-control', 'scope-guardian')
        self.invoke(module, 'install', names); self.change_source()
        before = self.managed_bytes(); replace = module.os.replace

        def interrupt(source, destination):
            result = replace(source, destination)
            if Path(destination).parent.name == 'backups':
                raise KeyboardInterrupt('synthetic process interruption; not a power-loss test')
            return result

        with mock.patch.object(module.os, 'replace', side_effect=interrupt):
            with self.assertRaises(KeyboardInterrupt): self.invoke(module, 'update', names)
        self.assertEqual(self.run_install('update').returncode, 1)
        self.assertEqual(self.run_install('recover').returncode, 0)
        self.assertEqual(self.managed_bytes(), before)

    def test_recovery_can_resume_after_a_second_restoration_error(self):
        module, names, before, state = self.leave_pending_recovery()
        replace = module.os.replace

        def fail_first_skill_restore(source, destination):
            if Path(source).parent.name == 'backups' and Path(destination).name == 'mission-control':
                raise OSError('injected later restoration failure')
            return replace(source, destination)

        with mock.patch.object(module.os, 'replace', side_effect=fail_first_skill_restore):
            with self.assertRaises(OSError): self.invoke(module, 'recover', ())
        self.assertTrue((state / 'pending.json').is_file())
        self.invoke(module, 'recover', ())
        self.assertEqual(self.managed_bytes(), before)

    def test_manifest_publication_error_after_commit_is_reconciled_as_committed(self):
        self.install(); self.change_source(); module = self.engine()
        replace = module.os.replace

        def fail_after_publication(source, destination):
            result = replace(source, destination)
            if Path(destination).name == 'manifest.json':
                raise OSError('injected error after successful publication')
            return result

        stderr = io.StringIO()
        with mock.patch.object(module.os, 'replace', side_effect=fail_after_publication), contextlib.redirect_stderr(stderr):
            self.invoke(module, 'update')
        self.assertIn('batch committed', stderr.getvalue())
        self.assertEqual((self.target / 'mission-control/SKILL.md').read_bytes(),
                         (self.source / 'skills/mission-control/SKILL.md').read_bytes())
        self.assertEqual(self.run_install('update', '--dry-run').returncode, 0)

    def test_journal_capacity_is_preflighted_before_writes(self):
        self.install(); module = self.engine(); before = self.managed_bytes()
        with mock.patch.object(module, 'MAX_JOURNAL_BYTES', 1):
            with self.assertRaisesRegex(ValueError, 'journal exceeds'):
                self.invoke(module, 'update')
        self.assertEqual(self.managed_bytes(), before)

    def test_publication_error_and_cleanup_error_still_report_committed_batch(self):
        self.install(); self.change_source(); module = self.engine()
        replace = module.os.replace

        def fail_after_publication(source, destination):
            result = replace(source, destination)
            if Path(destination).name == 'manifest.json':
                raise OSError('injected error after publication')
            return result

        stderr = io.StringIO()
        with mock.patch.object(module.os, 'replace', side_effect=fail_after_publication), \
                mock.patch.object(module.shutil, 'rmtree', side_effect=OSError('injected cleanup error')), \
                contextlib.redirect_stderr(stderr):
            self.invoke(module, 'update')
        self.assertIn('batch committed', stderr.getvalue())
        self.assertIn('cleanup pending', stderr.getvalue())
        expected = self.managed_bytes()
        self.invoke(module, 'recover', ())
        self.assertEqual(self.managed_bytes(), expected)

    @unittest.skipUnless(hasattr(os, 'mkfifo'), 'FIFO unavailable')
    def test_special_source_file_is_rejected_without_target_mutation(self):
        self.install(); module = self.engine(); before = self.managed_bytes()
        os.mkfifo(self.source / 'skills/mission-control/pipe')
        with self.assertRaisesRegex(ValueError, 'Non-regular'):
            self.invoke(module, 'update')
        self.assertEqual(self.managed_bytes(), before)

    def test_multiskill_install_and_rollback_swap_failures_preserve_entire_batch(self):
        module = self.engine(); names = ('mission-control', 'scope-guardian')
        replace = module.os.replace

        def fail_swap(source, destination):
            if Path(source).parent.name == 'staged' and Path(destination).name == 'scope-guardian':
                raise OSError('injected second promotion failure')
            return replace(source, destination)

        for action in ('install', 'rollback'):
            with self.subTest(action=action):
                self.target = self.base / f'swap-{action}/.agents/skills'
                if action == 'rollback':
                    self.invoke(module, 'install', names); self.change_source()
                    self.invoke(module, 'update', names)
                before = self.managed_bytes()
                with mock.patch.object(module.os, 'replace', side_effect=fail_swap):
                    with self.assertRaises(OSError): self.invoke(module, action, names)
                self.assertEqual(self.managed_bytes(), before)


if __name__ == '__main__':
    unittest.main()

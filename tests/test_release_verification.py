import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest
import zipfile

ROOT=Path(__file__).resolve().parents[1]


class ReleaseVerificationTests(unittest.TestCase):
    def module(self):
        path=ROOT/'scripts/verify_release.py'
        self.assertTrue(path.exists(),'release verification not implemented')
        spec=importlib.util.spec_from_file_location('verify_release',path)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        return module

    def fixture(self,path,member='README.md'):
        archive=path/'candidate.zip';checksum=path/'candidate.zip.sha256'
        with zipfile.ZipFile(archive,'w') as z:z.writestr(member,'synthetic test')
        checksum.write_text(hashlib.sha256(archive.read_bytes()).hexdigest()+'  candidate.zip\n')
        return archive,checksum

    def test_verifies_matching_pair_with_available_native_utilities(self):
        with tempfile.TemporaryDirectory() as temporary:
            archive,checksum=self.fixture(Path(temporary))
            report=self.module().verify_pair(archive,checksum)
            self.assertTrue(report['verified'])
            self.assertTrue(all(value['outcome']=='passed' for value in report['native_checks'] if value['outcome']!='not_run'))

    def test_rejects_modified_archive(self):
        with tempfile.TemporaryDirectory() as temporary:
            archive,checksum=self.fixture(Path(temporary));archive.write_bytes(archive.read_bytes()+b'changed')
            with self.assertRaises(ValueError):self.module().verify_pair(archive,checksum)

    def test_rejects_checksum_for_another_name(self):
        with tempfile.TemporaryDirectory() as temporary:
            archive,checksum=self.fixture(Path(temporary));checksum.write_text(checksum.read_text().replace('candidate.zip','other.zip'))
            with self.assertRaises(ValueError):self.module().verify_pair(archive,checksum)

    def test_rejects_unsafe_zip_member(self):
        with tempfile.TemporaryDirectory() as temporary:
            archive,checksum=self.fixture(Path(temporary),'../escape')
            with self.assertRaises(ValueError):self.module().verify_pair(archive,checksum)


if __name__=='__main__':unittest.main()

import copy
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('catalog', ROOT / 'tools/catalog.py')
catalog = importlib.util.module_from_spec(spec)
spec.loader.exec_module(catalog)


class IntegrityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        source = next((ROOT / 'assets/materials').rglob('asset.json'))
        self.directory = self.root / source.parent.relative_to(ROOT)
        shutil.copytree(source.parent, self.directory)
        self.path = self.directory / 'asset.json'
        self.item = json.loads(self.path.read_text())

    def write(self):
        self.path.write_text(json.dumps(self.item))

    def test_tampered_asset_rejected(self):
        source = self.root / self.item['files'][0]['path']
        payload = bytearray(source.read_bytes())
        payload[0] ^= 1
        source.write_bytes(payload)
        with self.assertRaisesRegex(ValueError, 'Hash mismatch'):
            catalog.records(self.root)

    def test_path_escape_rejected(self):
        self.item['files'][0]['path'] = '../outside.json'
        self.write()
        with self.assertRaisesRegex(ValueError, 'traversal'):
            catalog.records(self.root)

    def test_symlink_rejected(self):
        source = self.root / self.item['files'][0]['path']
        target = self.root / 'outside.json'
        source.rename(target)
        source.symlink_to(target)
        with self.assertRaisesRegex(ValueError, 'Symlinks'):
            catalog.records(self.root)

    def test_duplicate_identity_rejected(self):
        shutil.copytree(self.directory, self.directory.with_name('duplicate'))
        with self.assertRaisesRegex(ValueError, 'Duplicate ID|belong'):
            catalog.records(self.root)

    def test_missing_attribution_rejected(self):
        self.item['attribution'] = ''
        self.write()
        with self.assertRaisesRegex(ValueError, 'attribution'):
            catalog.records(self.root)

    def test_external_source_needs_no_central_payload(self):
        source = self.root / self.item['files'][0].pop('path')
        source.unlink()
        self.item['files'][0]['url'] = 'https://example.org/releases/v1/source.ignis-material'
        self.write()
        self.assertEqual(len(catalog.records(self.root)), 1)

    def test_external_source_rejects_insecure_url(self):
        self.item['files'].append(dict(copy.deepcopy(self.item['files'][0]), url='http://example.org/asset'))
        del self.item['files'][-1]['path']
        self.write()
        with self.assertRaisesRegex(ValueError, 'HTTPS'):
            catalog.records(self.root)

    def test_generated_index_matches_valid_sources(self):
        self.assertEqual((ROOT / 'catalog.json').read_text(), catalog.encoded())


class MeshIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        source = next((ROOT / 'assets/meshes').rglob('asset.json'))
        self.directory = self.root / source.parent.relative_to(ROOT)
        shutil.copytree(source.parent, self.directory)
        self.path = self.directory / 'asset.json'
        self.item = json.loads(self.path.read_text())

    def test_mesh_record_offline_validation(self):
        self.assertEqual(catalog.records(self.root)[0]['kind'], 'mesh')

    def test_decoded_payload_budget_rejected(self):
        self.item['native_preview']['decoded_bytes'] = 193 * 1024 * 1024
        self.path.write_text(json.dumps(self.item))
        with self.assertRaisesRegex(ValueError, 'decoded preview budget'):
            catalog.records(self.root)

    def test_nonfinite_bounds_rejected(self):
        self.item['mesh']['bounds']['min'][0] = float('nan')
        self.path.write_text(json.dumps(self.item))
        with self.assertRaisesRegex(ValueError, 'mesh bounds'):
            catalog.records(self.root)


if __name__ == '__main__':
    unittest.main()

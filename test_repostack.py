import unittest
import os
import shutil
import tempfile

from repostack import RepoStack


class TestRepoStack(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix='test_repostack_')
        self.rs = RepoStack(rootdir=self.tmpdir)

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_init(self):
        cfgpath = os.path.join(self.tmpdir, '.repostack')
        self.assertEqual(cfgpath, self.rs.cfg_abspath)
        self.assertFalse(os.path.exists(cfgpath))
        self.rs.init({})
        self.assertTrue(os.path.exists(cfgpath))
        with self.assertRaises(Exception):
            self.rs.init({})


if __name__ == '__main__':
    unittest.main()

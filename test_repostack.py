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

        # init ok if not already managed by repostack
        self.rs.init({})
        self.assertTrue(os.path.exists(cfgpath))

        # init ko if already managed by repostack
        with self.assertRaises(Exception):
            self.rs.init({})

        # init ko if a parent dir is already managed by repostack
        child_tmpdir = os.path.join(self.tmpdir, 'child', 'tmpdir')
        self.assertFalse(os.path.exists(child_tmpdir))
        child_cfgpath = os.path.join(child_tmpdir, '.repostack')
        child_rs = RepoStack(rootdir=child_tmpdir)
        self.assertEqual(child_cfgpath, child_rs.cfg_abspath)
        with self.assertRaises(Exception):
            child_rs.init({})
        self.assertFalse(os.path.exists(child_tmpdir))

        # init ok if parent dirs not already managed by repostack
        os.remove(cfgpath)
        child_rs.init({})
        self.assertTrue(os.path.exists(child_tmpdir))
        self.assertTrue(os.path.exists(child_cfgpath))


if __name__ == '__main__':
    unittest.main()

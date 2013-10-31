import unittest
import os
import shutil
import tempfile
from ConfigParser import ConfigParser

import git

from repostack import RepoStack


class TestRepoStack(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix='test_repostack_')
        self.rs = RepoStack(rootdir=self.tmpdir)
        self.cfgpath = os.path.join(self.tmpdir, '.repostack')

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def _create_repo(self, path, remotes):
        self.assertFalse(os.path.exists(path))
        grepo = git.Repo.init(path)
        for remote, url in remotes.iteritems():
            grepo.create_remote(remote, url)
        self.assertTrue(os.path.isdir(path))
        return grepo

    def _read_config_as_dict(self, path=None):
        if path is None:
            path = self.cfgpath
        cfg = ConfigParser()
        with open(path, 'r') as f:
            cfg.readfp(f, path)
            return dict(cfg._sections)

    def test_init(self):
        self.assertEqual(self.cfgpath, self.rs.cfg_abspath)
        self.assertFalse(os.path.exists(self.cfgpath))

        # init ok if not already managed by repostack
        self.rs.init({})
        self.assertTrue(os.path.exists(self.cfgpath))

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
        os.remove(self.cfgpath)
        child_rs.init({})
        self.assertTrue(os.path.exists(child_tmpdir))
        self.assertTrue(os.path.exists(child_cfgpath))


if __name__ == '__main__':
    unittest.main()

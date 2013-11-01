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
        path = os.path.join(self.tmpdir, path)
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
            d = dict(cfg._sections)
            for k in d:
                d[k] = dict(cfg._defaults, **d[k])
                d[k].pop('__name__', None)
            return d

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

    def test_add(self):
        open(self.cfgpath, 'w').close()
        self.rs.add({'<filepattern>': None})
        self.assertDictEqual(self._read_config_as_dict(), {})

        # ok new repo
        foo = self._create_repo('foo', {'origin': 'git://foo/remote/repo.git'})
        self.rs.add({'<filepattern>': None})
        self.assertDictEqual(self._read_config_as_dict(), {
            'foo': {'remote_origin': 'git://foo/remote/repo.git'}})

        # ok existing repo, partial update
        foo.create_remote('test', 'git://foo/test.git')
        foo.remotes.origin.config_writer.set('url', 'git://foo/repo.git')
        self.rs.add({'<filepattern>': None, '--force': None})
        self.assertDictEqual(self._read_config_as_dict(), {
            'foo': {
                'remote_origin': 'git://foo/remote/repo.git',
                'remote_test': 'git://foo/test.git',
            }})

        # ok existing repo, full update with --force
        self.rs.add({'<filepattern>': None, '--force': True})
        self.assertDictEqual(self._read_config_as_dict(), {
            'foo': {
                'remote_origin': 'git://foo/repo.git',
                'remote_test': 'git://foo/test.git',
            }})

    def test_checkout(self):
        path = os.path.join(self.tmpdir, 'path/to/bar')

        # ok new repo
        with open(self.cfgpath, 'w') as f:
            f.write('\n'.join((
                '[path/to/bar]',
                'remote_origin = git://bar/repo.git',
            )))
        self.rs.checkout({'<filepattern>': '*'})
        self.assertTrue(os.path.isdir(os.path.join(path, '.git')))
        grepo = git.Repo.init(path)
        self.assertEqual(grepo.remotes.origin.url, 'git://bar/repo.git')

        # ok existing repo, partial update
        with open(self.cfgpath, 'w') as f:
            f.write('\n'.join((
                '[path/to/bar]',
                'remote_origin = git://bar/remote/repo.git',
                'remote_test = git://bar/test.git',
            )))
        self.rs.checkout({'<filepattern>': '*', '--force': None})
        grepo = git.Repo.init(path)
        self.assertEqual(grepo.remotes.origin.url, 'git://bar/repo.git')
        self.assertEqual(grepo.remotes.test.url, 'git://bar/test.git')

        # ok existing repo, full update with --force
        self.rs.checkout({'<filepattern>': '*', '--force': True})
        grepo = git.Repo.init(path)
        self.assertEqual(grepo.remotes.origin.url, 'git://bar/remote/repo.git')
        self.assertEqual(grepo.remotes.test.url, 'git://bar/test.git')


if __name__ == '__main__':
    unittest.main()

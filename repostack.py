#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Usage: repostack [--version] [--help] [--dir=<path>] <command> [<args>...]

options:
    -v, --version
    -h, --help            show this message
    -d, --dir=<path>      set repostack root directory [default: .]

The following commands are supported by repostack:
    init       Initialize a new repostack directory
    add        Add repos to the stack of tracked repos
    rm         Remove repos from the stack of tracked repos
    checkout   Checkout repos
    status     Give repos status
    diff       Show repos diff
    do         Run a command on repos

See 'repostack help <command>' for more information on a specific command.
"""
import os
from ConfigParser import RawConfigParser


__all__ = ['RepoStack']
__version__ = '0.1'


class RepoStack(object):

    def __init__(self, rootdir='.', config='.repostack'):
        self.rootdir = os.path.abspath(rootdir)
        self.cfg = None
        self.cfg_filename = config
        self.cfg_abspath = os.path.join(self.rootdir, config)

    def _read_config(self):
        if not os.path.exists(self.cfg_abspath):
            raise Exception('This directory is not manged by repostack.'
                            '\nFile "%s" does not exists.' % self.cfg_abspath)
        self.cfg = RawConfigParser()
        with open(self.cfg_abspath, 'r') as f:
            self.cfg.readfp(f, self.cfg_abspath)

    def init(self, args):
        """
        Usage: repostack [--dir=<path>] init [-h]

        Global options:
            -d, --dir=<path>      set repostack root directory [default: .]

        Command options:
            -h, --help            show this message

        This will initialize repostack in the specified --dir directory or
        the current directory by default.
        It simply creates a new ".repostack" empty file.
        """
        if os.path.exists(self.cfg_abspath):
            raise Exception('Repostack already manages this directory.'
                            '\nFile "%s" already exists.' % self.cfg_abspath)
        checkdir = self.rootdir
        while checkdir != os.path.dirname(checkdir):
            checkdir = os.path.dirname(checkdir)
            checkpath = os.path.join(checkdir, self.cfg_filename)
            if os.path.exists(checkpath):
                raise Exception('Repostack already manages a parent directory.'
                                '\nFile "%s" exists.' % checkpath)
        if not os.path.exists(self.rootdir):
            os.makedirs(self.rootdir)
        open(self.cfg_abspath, 'w').close()
        print 'Directory "%s" is now managed by repostack.' % self.rootdir

    def add(self, args):
        """
        Usage: repostack [--dir=<path>] add [-hf] [<filepattern>...]

        Global options:
            -d, --dir=<path>      set repostack root directory [default: .]

        Command options:
            -h, --help            show this message
            -f, --force           force rewrite remote urls

        This will add repos that match <filepattern> to the stack of tracked
        repos (creates new sections in the ".repostack" file).
        If <filepattern> is not specified, it will add all untracked git
        repositories.

        If the repos are already tracked, it will only add additional tracking
        information about any new remotes, and inform the user if existing
        remotes conflict with the tracked ones.
        If the user wants to force update stackrepo config to match actual
        repos remotes, the --force flag should be set.
        """
        raise NotImplementedError('Not implemented yet.')

    def rm(self, args):
        """
        Usage: repostack [--dir=<path>] rm [-hk] <filepattern>...

        Global options:
            -d, --dir=<path>      set repostack root directory [default: .]

        Command options:
            -h, --help            show this message
            -k, --keep            do not remove repo from disk

        This will remove repos that match <filepattern> from the stack of
        tracked repos (removes sections from the ".repostack" file).
        The repos will also be removed from disk unless option --keep is set.
        """
        raise NotImplementedError('Not implemented yet.')

    def checkout(self, args):
        """
        Usage: repostack [--dir=<path>] checkout [-hf] <filepattern>...

        Global options:
            -d, --dir=<path>      set repostack root directory [default: .]

        Command options:
            -h, --help            show this message
            -f, --force           force rewrite remote urls

        If repos that match <filepattern> are not available yet, it will clone
        the repos and set all remotes.
        If they are already available, it will only set any new remotes, and
        inform the user if existing remotes conflict with the tracked ones.
        If user wants to override these conflicting remotes, the --force flag
        should be set.
        """
        raise NotImplementedError('Not implemented yet.')

    def status(self, args):
        """
        Usage: repostack [--dir=<path>] status [-h] [<filepattern>...]

        Global options:
            -d, --dir=<path>      set repostack root directory [default: .]

        Command options:
            -h, --help            show this message

        This will show the status of all repos (or matched repos if
        <filepattern> is specified):
          - available tracked repos
          - available untracked repos
          - unavailable tracked repos

        This will also mark available tracked repos that have diverged (their
        remotes may have changed).
        """
        raise NotImplementedError('Not implemented yet.')

    def diff(self, args):
        """
        Usage: repostack [--dir=<path>] diff [-h] [<filepattern>...]

        Global options:
            -d, --dir=<path>      set repostack root directory [default: .]

        Command options:
            -h, --help            show this message

        This will show the diff for all available tracked repos which remotes
        have diverged (or for matched repos if <filepattern> is specified).
        """
        raise NotImplementedError('Not implemented yet.')

    def do(self, args):
        """
        Usage: repostack [--dir=<path>] do [-h] <command> [--] [<filepattern>...]

        Global options:
            -d, --dir=<path>      set repostack root directory [default: .]

        Command options:
            -h, --help            show this message

        This will run a command in all available tracked repos (or in matched
        repos if <filepattern> is specified).
        """
        raise NotImplementedError('Not implemented yet.')


def main():
    import sys
    from textwrap import dedent

    from docopt import docopt

    args = docopt(__doc__, version=__version__, options_first=True)

    rootdir = '.'
    if args['--dir']:
        rootdir = args['--dir']

    command = args['<command>']
    if command == 'help':
        command = args['<args>']
        args['<args>'] = '--help'

    try:
        repostack = RepoStack(rootdir=rootdir)
        if hasattr(repostack, command):
            cmd = getattr(repostack, command)
            cmd(docopt(dedent(cmd.__doc__), argv=[command] + args['<args>']))
        else:
            sys.exit('\n'.join((
                __doc__,
                'Error: unknown command "%s".' % command)))
    except Exception, e:
        print e
        raise

if __name__ == '__main__':
    main()

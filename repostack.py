#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Usage: repostack [--version] [--help] [--dir=<path>] <command> [<options>]

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


__all__ = ['RepoStack']
__version__ = '0.1'


class RepoStack(object):

    def __init__(self, rootdir='.', config='.repostack'):
        self.rootdir = os.path.abspath(rootdir)
        self.cfg_path = os.path.join(self.rootdir, config)

    def init(self, options):
        """
        Usage: repostack [--dir=<path>] init [options]

        Global options:
            -d, --dir=<path>      set repostack root directory [default: .]

        Command options:
            -h, --help            show this message

        This will initialize repostack in the specified --dir directory or
        the current directory by default.
        It simply creates a new ".repostack" empty file.
        """
        raise NotImplementedError('Not implemented yet.')

    def add(self, options):
        """
        Usage: repostack [--dir=<path>] add [options] [<filepattern>]

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

    def rm(self, options):
        """
        Usage: repostack [--dir=<path>] rm [options] <filepattern>

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

    def checkout(self, options):
        """
        Usage: repostack [--dir=<path>] checkout [options] <filepattern>

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

    def status(self, options):
        """
        Usage: repostack [--dir=<path>] status [options] [<filepattern>]

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

    def diff(self, options):
        """
        Usage: repostack [--dir=<path>] diff [options] [<filepattern>]

        Global options:
            -d, --dir=<path>      set repostack root directory [default: .]

        Command options:
            -h, --help            show this message

        This will show the diff for all available tracked repos which remotes
        have diverged (or for matched repos if <filepattern> is specified).
        """
        raise NotImplementedError('Not implemented yet.')

    def do(self, options):
        """
        Usage: repostack [--dir=<path>] do [options] <command> [--] [<filepattern>]

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

    if args['--help']:
        print __doc__
        return

    rootdir = '.'
    if args['--dir']:
        rootdir = args['--dir']
    command = args['<command>']
    if command == 'help':
        command = args['<options>']
        args['<options>'] = '--help'
    try:
        repostack = RepoStack(rootdir=rootdir)
        if hasattr(repostack, command):
            cmd = getattr(repostack, command)
            cmd(docopt(dedent(cmd.__doc__), argv=args['<options>']))
        else:
            sys.exit('\n'.join((
                __doc__,
                'Error: unknown command "%s".' % command)))
    except Exception, e:
        print e
        raise

if __name__ == '__main__':
    main()

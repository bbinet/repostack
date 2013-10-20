#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Usage: repostack [--version] [--help] [--dir=<path>] <command> [<args>]

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
    help       Give more information on a specific command

See 'repostack help <command>' for more information on a specific command.
"""
import os


__all__ = ['RepoStack']
__version__ = '0.1'


class RepoStack(object):

    def __init__(self, rootdir='.', config='.repostack'):
        self.rootdir = os.path.abspath(rootdir)
        self.cfg_path = os.path.join(self.rootdir, config)

    def init(self, argv=[]):
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

    def add(self, argv=[]):
        """Add repos to the stack of tracked repos"""
        raise NotImplementedError('Not implemented yet.')

    def rm(self, argv=[]):
        """Remove repos from the stack of tracked repos"""
        raise NotImplementedError('Not implemented yet.')

    def checkout(self, argv=[]):
        """Checkout repos"""
        raise NotImplementedError('Not implemented yet.')

    def status(self, argv=[]):
        """Give repos status"""
        raise NotImplementedError('Not implemented yet.')

    def diff(self, argv=[]):
        """Show repos diff"""
        raise NotImplementedError('Not implemented yet.')

    def do(self, argv=[]):
        """Run a command on repos"""
        raise NotImplementedError('Not implemented yet.')

    def help(self, argv=[]):
        """Give more information on a specific command"""
        raise NotImplementedError('Not implemented yet.')


def main():
    import sys
    from textwrap import dedent

    from docopt import docopt

    args = docopt(__doc__, version=__version__)

    if args['--help']:
        print __doc__
        return

    rootdir = '.'
    if args['--dir']:
        rootdir = args['--dir']
    command = args['<command>']
    try:
        repostack = RepoStack(rootdir=rootdir)
        if hasattr(repostack, command):
            cmd = getattr(repostack, command)
            cmd(docopt(dedent(cmd.__doc__), argv=args['<args>']))
        else:
            sys.exit('\n'.join((
                __doc__,
                'Error: unknown command "%s".' % command)))
    except Exception, e:
        print e
        raise

if __name__ == '__main__':
    main()

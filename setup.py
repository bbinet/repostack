# -*- coding: utf-8 -*-
from setuptools import setup

import repostack


setup(
    name='repostack',
    version=repostack.__version__,
    author='Bruno Binet',
    author_email='bruno.binet@gmail.com',
    description='Keep track of all your git repositories.',
    license='MIT',
    keywords='dvcs git manage multiple repositories stack',
    url='https://github.com/bbinet/repostack',
    py_modules=['repostack'],
    install_requires=['GitPython>=0.3.2.RC1', 'docopt'],
    entry_points={
        'console_scripts': ['repostack = repostack:main']
    },
    long_description='%s\n\n::\n\n%s' % (
        open('README.rst').read(),
        '\n'.join((4 * ' ') + l for l in repostack.__doc__.splitlines())),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: MIT License',
    ],
)

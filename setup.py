#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# BASED ON https://github.com/navdeep-G/setup.py

import io
import os
import sys
from textwrap import dedent

from setuptools import find_packages, setup

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 5)

# This check and everything above must remain compatible with Python 2.7.
if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write(dedent('''
    UNSUPPORTED PYTHON VERSION

    This version of nichtparasoup requires Python {py_required[0]}.{py_required[1]},
    but you're trying to install it on Python {py_current[0]}.{py_current[1]}.

    '''.format(py_current=CURRENT_PYTHON, py_required=REQUIRED_PYTHON)))
    sys.exit(1)

# Package meta-data.
NAME = 'nichtparasoup'
DESCRIPTION = 'A hackspaces entertainment system'
URL = 'https://github.com/k4cg/nichtparasoup/'
AUTHOR = 'K4CG'
EMAIL = 'info@k4cg.org'
REQUIRES_PYTHON = '>={}.{}'.format(*REQUIRED_PYTHON)

URLS = dict(
    Source='https://github.com/k4cg/nichtparasoup/',
    Documentation='https://github.com/k4cg/nichtparasoup/tree/master/docs',
)

# What packages are required for this module to be executed?
REQUIRED = [
    'typing-extensions>=3.7.4;python_version<"3.8"',  # for `_internals`, `imagecrawler/instagram`
    'ruamel.yaml>=0.16', 'yamale>=2.0',  # for `config`
    'werkzeug>=1.0',  # for `webserver`
    'mako>=1.1',  # for `webserver`'s templates
    'setuptools>=40.0',  # for imagecrawler-plugin-architecture
    'argcomplete>=1.11',  # for cli autocompletion
]

# What packages are optional?
EXTRAS = dict(
    colors=[
        'termcolor>=1.1',
    ],
    development=[
        'tox>=3.14',
        'isort>=4.3',
        'autopep8>=1.5',
    ],
    testing=[
        'flake8>=3.7',
        'flake8-annotations>=2.0;python_version>="3.6"',
        'flake8-bugbear>=20.1;python_version>="3.6"',
        'flake8-bugbear>=19.8;python_version<"3.6"',
        'flake8-isort>=2.8',
        'flake8-pep3101>=1.3',
        'pep8-naming>=0.9',
        'mypy>=0.761',
        'coverage>=5.0',
        'pytest>=5.3',
        'ddt>=1.2',
        # 'flake8-builtins',  # nice in general, but seams not bug-free, yet.
        # 'lake8-docstrings', # not in use, until all docs are done.
        # 'flake8-quotes',    # not in use until black code styles are setup
    ],
)

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Where the magic happens:
setup(
    name=NAME,
    use_scm_version=dict(
        root=here,
        fallback_version='UNKNOWN.scm',
        write_to=os.path.join('nichtparasoup', '__version__.py'),
    ),
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    project_urls=URLS,
    packages=find_packages(exclude=['tests', '*.tests', '*.tests.*', 'tests.*', 'examples']),
    entry_points=dict(
        console_scripts=[
            'nichtparasoup = nichtparasoup.cli.main:main',
        ],
    ),
    setup_requires=['setuptools', 'setuptools_scm>=3.3.3'],
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Trove classifiers - https://packaging.python.org/specifications/core-metadata/#metadata-classifier
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Games/Entertainment',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Typing :: Typed',
    ],
    keywords=[
        'image-crawler',
        'instagram',
        'pr0gramm',
        'reddit',
    ],
)

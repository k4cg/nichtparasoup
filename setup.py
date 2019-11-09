#!/usr/bin/env python
# -*- coding: utf-8 -*-

# BASED ON https://github.com/navdeep-G/setup.py

# Note: To use the 'upload' functionality of this file, you must:
#   $ pipenv install twine --dev

import io
import os
import sys
from functools import reduce
from shutil import rmtree

from setuptools import Command, find_packages, setup

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 5)

# This check and everything above must remain compatible with Python 2.7.
if CURRENT_PYTHON < REQUIRED_PYTHON:
    import textwrap

    sys.stderr.write(textwrap.dedent("""
    UNSUPPORTED PYTHON VERSION
    
    This version of Django requires Python {py_required[0]}.{py_required[1]}, but you're trying to
    install it on Python {py_current[0]}.{py_current[1]}.

    """.format(py_current=CURRENT_PYTHON, py_required=REQUIRED_PYTHON)))
    sys.exit(1)

# Package meta-data.
NAME = 'nichtparasoup'
DESCRIPTION = 'A hackspaces entertainment system'
URL = 'https://github.com/k4cg/nichtparasoup'
EMAIL = None
AUTHOR = 'FLorian Baumann, Jan Kowalleck'
REQUIRES_PYTHON = '>={}.{}'.format(*REQUIRED_PYTHON)
VERSION = None  # read from __version__.py

# What packages are required for this module to be executed?
REQUIRED = dict(
    _internals=['typing-extensions;python_version<"3.8"'],
    cmdline=[],
    config=['ruamel.yaml', "yamale"],
    core=[],
    imagecrawler=[],
    webserver=["werkzeug"],
)

# What packages are optional?
EXTRAS = dict(
    colors=[
        "termcolor",
    ],
    development=[
        "tox",
        "isort",
    ],
    testing=[
        "flake8",
        'flake8-annotations;python_version>="3.6"',
        'flake8-bugbear',
        "flake8-isort",
        'flake8-pep3101',
        "pep8-naming",
        "mypy",
        "coverage",
        "pytest",
        "ddt",
        "yamale",
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

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(about['__version__']))
        os.system('git push --tags')

        sys.exit()


# Where the magic happens:
setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    entry_points=dict(
        console_scripts=['nichtparasoup=nichtparasoup.cmdline:main'],
    ),
    setup_requires=["setuptools"],
    install_requires=reduce(lambda r1, r2: r1 + r2, REQUIRED.values(), []),
    extras_require=EXTRAS,
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Trove classifiers
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
    ],
    # $ setup.py publish support.
    cmdclass={
        'upload': UploadCommand,
    },
)

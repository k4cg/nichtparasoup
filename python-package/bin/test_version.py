#!/usr/bin/env python3
import os
import sys
from subprocess import check_output

# region config

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SOURCES_DIR = os.path.join(PROJECT_ROOT, 'src')
SETUP_FILE = os.path.join(PROJECT_ROOT, 'setup.py')

# region config

VERSION_EXPECTED = sys.argv[1] if len(sys.argv) > 1 else os.getenv('NP_VERSION_EXPECTED')
if not VERSION_EXPECTED:
    print(f'VERSION_EXPECTED empty: {VERSION_EXPECTED!r}')
    sys.exit(1)
print(f'expected version {VERSION_EXPECTED!r}')

# region version_src

sys.path.insert(0, SOURCES_DIR)
from nichtparasoup import __version__ as version_src  # noqa isort:skip

if version_src != VERSION_EXPECTED:
    print(f'ERROR version_src: expected {VERSION_EXPECTED!r}, got {version_src!r}', file=sys.stderr)
    sys.exit(2)

# endregion version_src

# region version_setup

version_setup = check_output([sys.executable, SETUP_FILE, '--version'], shell=False, universal_newlines=True).strip()
if version_setup != VERSION_EXPECTED:
    print(f'ERROR version_setup: expected {VERSION_EXPECTED!r}, got {version_setup!r}', file=sys.stderr)
    sys.exit(3)

# endregion version_setup

sys.exit(0)

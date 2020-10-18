#!/usr/bin/env python3

import os
import sys
from glob import glob
from subprocess import call
from tempfile import TemporaryDirectory


def install(dist: str) -> bool:
    with TemporaryDirectory() as temp:
        return 0 == call([
            sys.executable, '-m',
            'pip', 'install', '--force-reinstall', '--ignore-installed', '--target', temp,
            dist
        ])


DIST_DIR = sys.argv[1] if len(sys.argv) > 0 else os.getenv('NP_DIST_DIR')
if not DIST_DIR:
    print(f'DIST_DIR empty: {DIST_DIR!r}')
    sys.exit(11)
print(f'DIST_DIR = {DIST_DIR!r}')

DISTS = glob(os.path.join(DIST_DIR, '*'))
if not DISTS:
    print(f'DISTS empty: {DISTS!r}')
    sys.exit(12)
print(f'DISTS = {DISTS!r}')

INSTALLED = {dist: install(dist) for dist in DISTS}

print(f'INSTALLED = {INSTALLED!r}')
sys.exit(0 if all(INSTALLED.values()) else 1)

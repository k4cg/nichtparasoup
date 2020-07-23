#!/bin/sh
set -e

# dont wanna have nasty path prefixes in created files. so simply cd in here
cd "$(dirname "$0")"

# all requirements are for build/dev
# so it is a MUST that also pip/setuptools is pinned -> use `--allow-unsafe`
find -type f -name '*.in' \
  -exec echo 'precessing {}' \; \
  -exec pip-compile -qUr --allow-unsafe {} \;

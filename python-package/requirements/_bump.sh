#!/bin/sh
set -e

# dont wanna have nasty path prefixes in created files. so simply cd in here
cd "$(dirname "$0")"

find -type f -name '*.in' \
  -exec echo 'precessing {}' \; \
  -exec pip-compile -qUr {} \;

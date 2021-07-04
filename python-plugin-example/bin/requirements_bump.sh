#!/bin/sh
set -e

REQUIREMENTS_DIR='requirements'

# dont wanna have nasty path prefixes in created files. so simply cd in here
cd "$(dirname "$(dirname "$0")")"


find "${REQUIREMENTS_DIR}" -type f -name '*.in' \
  -exec echo 'precessing {}' \; \
  -exec pip-compile -qUr --strip-extras --header --annotate {} \;

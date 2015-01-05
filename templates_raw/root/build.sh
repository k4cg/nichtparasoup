#!/bin/sh

dir=$(dirname $0)

bundler="$dir/../_bundler//bundler.py --compress --strip-comments \
--strip-tags striponbuild \
--strip-markers @striponbuild"

$bundler -i $dir/root.html


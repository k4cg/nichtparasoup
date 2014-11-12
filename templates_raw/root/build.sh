#!/bin/sh

dir=$(dirname $0)

bundler="$dir/../_bundler//bundler.py --strip-tags striponbuild --strip-markers @striponbuild --compress --strip-comments"

$bundler -i $dir/root.html




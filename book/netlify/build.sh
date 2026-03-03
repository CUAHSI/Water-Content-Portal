#!/bin/bash
set -e

# submodule commands should be run from the root of the repo
# update submodules
cd ..
make update

# build documentation
make ci

# inject Heap analytics snippet into the generated HTML
python3 scripts/inject_heap.py

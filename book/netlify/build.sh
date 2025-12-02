#!/bin/bash
set -e

# submodule commands should be run from the root of the repo
# update submodules
cd ..
git submodule init
git submodule update --remote

# build documentation
make ci
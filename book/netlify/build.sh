#!/bin/bash
set -e

# submodule commands should be run from the root of the repo
# update submodules
cd ..
make update

# build documentation
make ci
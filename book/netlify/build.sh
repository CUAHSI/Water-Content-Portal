#!/bin/bash
set -e

# update submodules
git submodule init
git submodule update --remote

# build documentation
make ci
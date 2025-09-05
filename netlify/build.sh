#!/bin/bash

set -e

# # update submodules
# git submodule init
# git submodule update --remote

# install micromamba
curl -Ls https://micro.mamba.pm/api/micromamba/linux-64/latest | tar -xvj -C /tmp
ls -l /tmp
/tmp/micromamba shell init -p ~/micromamba 
eval "$(/tmp/micromamba shell hook -s posix)"

# create and activate environment
/tmp/micromamba env create -f environment.yml
/tmp/micromamba activate water-content-portal-env

# build documentation
mkdocs build
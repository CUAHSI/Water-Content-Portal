#!/bin/bash

set -e

# # update submodules
# git submodule init
# git submodule update --remote

# Download and extract Micromamba
wget -qO- https://micro.mamba.pm/api/micromamba/linux-64/latest | tar -xvj bin/micromamba

# Set up environment variables
export MAMBA_ROOT_PREFIX="$PWD/micromamba"
export PATH="$PWD/bin:$PATH"

# create and activate environment
micromamba env create -f environment.yml
# micromamba activate water-content-portal-env

# build documentation
micromamba run -n water-content-portal-env mkdocs build
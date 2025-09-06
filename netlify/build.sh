#!/bin/bash

set -e

# Download and extract Micromamba
wget -qO- https://micro.mamba.pm/api/micromamba/linux-64/latest | tar -xvj bin/micromamba

# Set up environment variables
export MAMBA_ROOT_PREFIX="$PWD/micromamba"
export PATH="$PWD/bin:$PATH"

# create and activate environment
micromamba env create -f environment.yml

# update submodules
git submodule init
git submodule update --remote

# build documentation
micromamba run -n water-content-portal-env mkdocs build
#!/bin/bash

git submodule init
git submodule update --remote
mkdocs build
# mkdocs build -f mkdocs-minify.yml
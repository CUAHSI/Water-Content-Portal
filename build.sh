#!/bin/bash

# Run the Docker image build
make build

# Run the documentation build within the container
make build-docs
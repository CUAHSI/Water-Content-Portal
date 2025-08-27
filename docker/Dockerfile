FROM ghcr.io/mamba-org/micromamba:latest


USER root
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

RUN git config --global --add safe.directory /home/mambauser

WORKDIR /home/mambauser

COPY environment.yml /home/mambauser/environment.yml


RUN micromamba env update --file environment.yml --name base && \
    micromamba clean -a -y

ENTRYPOINT /bin/bash


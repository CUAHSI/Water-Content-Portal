FROM ghcr.io/mamba-org/micromamba:latest


USER root
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

RUN git config --global --add safe.directory /home/mambauser

WORKDIR /home/mambauser

COPY environment.yml /home/mambauser/environment.yml


RUN micromamba env update --file environment.yml --name base && \
    micromamba clean -a -y

################################################
# BEGIN - install the tmap R package from CRAN #
################################################
RUN apt-get update && apt-get install -y --no-install-recommends \
  libgdal-dev \
  libgeos-dev \
  libproj-dev \
  proj-bin \
  libudunits2-dev \
  libxml2 \
  libxml2-dev \
  libssl-dev \
  libcurl4-openssl-dev \
  make \
  g++ \
  pkg-config \
  && rm -rf /var/lib/apt/lists/*

ENV PROJ_LIB=/opt/conda/share/proj \
    PKG_CONFIG_PATH=/opt/conda/lib/pkgconfig \
    LD_LIBRARY_PATH=/opt/conda/lib:$LD_LIBRARY_PATH \
    PATH=/opt/conda/bin:$PATH \
    WHITEBOX_EXE=/opt/conda/bin/whitebox_tools

#Rscript -e 'install.packages("lwgeom", repos="https://cloud.r-project.org")'
RUN Rscript -e 'install.packages(c("lwgeom", "tmap", "codetools"), repos="https://cloud.r-project.org")' \
 && Rscript -e 'unlink(tempdir(), recursive=TRUE, force=TRUE)'
##############################################
# END - install the tmap R package from CRAN #
##############################################


ENTRYPOINT /bin/bash


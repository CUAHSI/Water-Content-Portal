
This guide outlines the steps to build the **CUAHSI Water Content Portal** locally.

## Why build locally

Building the book locally allows you to preview your changes as you work, ensuring accuracy and intended presentation before submitting a pull request. This process often offers a quicker feedback loop than waiting for a build from a pull request.

-----

## Prerequisites

The following command-line tools and environment setup are required:

  * **`git`**
  * **`conda`** (or a `conda`-based package and environment management system like [**Miniconda**](https://www.anaconda.com/docs/getting-started/miniconda/main))
      * It is recommended to download Miniconda if you don't already have one.

-----

## Step-by-step Guide

### Clone The Repository

First, clone the repository to your local machine:

```console
git clone git@github.com:CUAHSI/Water-Content-Portal.git
```

### Create and Activate a Conda Environment

Navigate into the root directory of the repository root:

```console
cd Water-Content-Portal
```

Create the environment using the provided [`environment.yml`](environment.yml) file, which is configured with the necessary libraries for building and hosting the book. The environment's name is specified in the `environment.yml` file as `cuahsi-open-learning-env`:

```console
conda env create --file environment.yml
```

Activate the newly created environment:

```console
conda activate cuahsi-open-learning-env
```

You will know the environment is active when your command prompt starts with the environment name.

### Install R Dependencies

The project's configuration file ([`myst.yml`](myst.yml)) lists an R script for package requirements:

```console
R --quiet -f install_local.R
```

### Serve the Book Locally

The CUAHSI Water Content Portal is built using **`jupyter-book`**, and all the contents of the portal are under the `book` folder. The [`Makefile`](Makefile) in this folder also has a serve target that uses `jupyter-book start`.

Navigate to the directory containing the `Makefile` and source files:

```console
cd book
```

To start the local development server, run the `make serve` command:

```console
make serve
```

*Note: The `make serve` target in the `Makefile` runs `jupyter-book start`.

Once the build has succeeded, the book will be deployed on a local webserver. Check the command line for the local link (e.g., `http://localhost:3000`) to view the website. The server remains open, and your edits will be dynamically added once saved.

-----

## Other Build Targets

The `Makefile` provides other targets for building and maintaining the book:

| Target | Command | Description |
| :--- | :--- | :--- |
| **Update Submodules** | `make update` | Updates the Git submodules. |
| **Clean** | `make clean` | Cleans any build outputs and artifacts[cite: 37]. |
| **Continuous Integration** | `make ci` | Builds the book in a non-interactive environment for Continuous Integration (CI). |

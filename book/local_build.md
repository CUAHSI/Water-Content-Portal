---
title: Building the page locally
---

This guide outlines the steps to build the **CUAHSI Water Content Portal** locally.

## Why build locally

Building the book locally allows you to preview your changes as you work, ensuring accuracy and intended presentation before submitting a pull request. This process often offers a quicker feedback loop than waiting for a build from a pull request.

---

## Prerequisites

The following command-line tools and environment setup are required:

* **`git`**
* **`conda`** (or a `conda`-based package and environment management system like [**Miniconda**](https://www.anaconda.com/docs/getting-started/miniconda/main))
    * It is recommended to download Miniconda if you don't already have one.

---

## Step-by-step Guide

### Clone The Repository (via SSH)

To contribute to this project, it is recommended to use **SSH** for cloning. Using SSH allows you to interact with GitHub without re-entering your username and password for every transaction. To use this method, you must have an SSH key configured in your GitHub account.

Run the following command to clone the repository using SSH:

```console
git clone git@github.com:CUAHSI/Water-Content-Portal.git
```

### Create and Activate a Conda Environment

Navigate into the root directory of the repository:

```console
cd Water-Content-Portal
```

Create the environment using the provided `environment.yml` file, which is configured with the necessary libraries for building and hosting the book. The environment's name is `cuahsi-open-learning-env`:

```console
conda env create --file environment.yml
```

Activate the newly created environment:

```console
conda activate cuahsi-open-learning-env
```

You will know the environment is active when your command prompt starts with the environment name.

### Update and Serve the Book

The CUAHSI Water Content Portal is built using **`jupyter-book`**, and all the contents are under the `book` folder. Before serving the book, you must ensure your submodules are initialized and up to date.

First, update the git submodules through the `make update` command:

```console
make update
```

_Note: This command runs `git submodule init` and `git submodule update --remote`._

To start the local development server, run the `make serve` command:

```console
make serve
```

_Note: The `make serve` target runs `jupyter-book start`._

Once the build has succeeded, the book will be deployed on a local webserver. Check the command line for the local link (e.g., `http://localhost:3000`) to view the website. The server remains open, and your edits will be dynamically added once saved.

---

## Other Build Targets

The `Makefile` provides additional targets for maintaining the repository:

| Target | Command | Description |
| --- | --- | --- |
| **Update** | `make update` | Initializes and updates git submodules to their remote versions.|
| **Sync** | `make sync` | Points local configuration to remote URLs defined in `.gitmodules`.|
| **Serve** | `make serve` | Starts a webserver to serve the book locally for development.|
| **CI Build** | `make ci` | Builds the book in a non-interactive environment for Continuous Integration.|
| **Clean** | `make clean` | Removes all build outputs and artifacts from the build directory.|
| **Reset** | `make reset` | Performs a hard reset and cleans the repo and submodules of all artifacts.|
| **Help** | `make help` | Displays the list of available commands and their descriptions.|
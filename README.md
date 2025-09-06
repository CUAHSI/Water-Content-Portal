# Water-Content-Portal
Scratch repository for demoing CUAHSI-hosted portal for versioned water content.

## Setup for building site locally

### Configuring project with submodules

There are a few ways for configuring a project containing submodules. First, clone the repository:

```
git clone git@github.com:CUAHSI/Water-Content-Portal.git
```

Then, initialize, fetch and checkout any nested submodules:

```
git submodule update --init --recursive
```

Note that a `git submodule update` command can subsequently be used to fetch all the data from that project and check out the appropriate commit listed in the metaproject.

### Installation using `conda`

If you do not already have a `conda`-based package and environment management system, we recommend downloading [Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/main). To set-up the environment configured with the necessary libraries to build the website locally, use the provided `environment.yml` file and run this command in the root directory:

```
conda env create --file environment.yml
```

Note this may take a few minutes to execute. To activate the newly created environment, in the same directory run this command:
```
conda activate water-content-portal-env
```

You have now configured the required packages and environment to build the website locally!


### Building the website using `mkdocs`

[MkDocs](https://www.mkdocs.org/) comes with a built-in dev-server that lets you preview your documentation as you work on it! In the root directory, you can start the server through this command:
```
mkdocs serve
```
You will see a local link to the server in the command line (e.g., `http://127.0.0.1:8000/`) that you can use to view the website. Note that you can keep the server open while making local edits to the documentation. Once you save your changes, your edits will be dynamically added to your local build of the website.

### Prod deployment

A single deployment of this project exists in Google CloudRun:

1. [Production](TODO)
   - This deployment is configured with Continuous Deployment. Build and deploy is triggered by merge/push to the `main` branch of https://github.com/CUAHSI/Water-Content-Portal

* Load balancer is [here](TODO)
* The backend is considered "serverless" and are permitted to scale down to 0 instances when there is low traffic. This can result in "cold starts" where users will encounted a delay after logging in, as the container "spins up" (should this prove undesireable in the future, we can limit the scaling to at least one replica).
* Because the `mkdocs serve` command is not considered secure for deployment, we use [Caddy](https://caddyserver.com/) as a static file server. The [Caddy configuration](caddy/caddy.docker.json) can be modified for other assets if desired.
* The deployments are built using a single [Dockerfile](docker/Dockerfile.prod)
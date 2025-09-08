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

We have configured DNS CNAME to point at Netlify

[Netlify Configuration](https://app.netlify.com/projects/cuahsi-water-portal/domain-management#production-domains)

[GCP DNS](https://console.cloud.google.com/net-services/dns/zones/cuahsi-io/rrsets/water-content-portal.cuahsi.io./CNAME/view?project=apps-320517)
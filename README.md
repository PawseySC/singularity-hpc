# Singularity Registry HPC (shpc)

[![GitHub actions status](https://github.com/singularityhub/singularity-hpc/workflows/sregistry-ci/badge.svg?branch=master)](https://github.com/singularityhub/singularity-hpc/actions?query=branch%3Amain+workflow%3Asingularity-hpc)

Singularity HPC is based off of the [Singularity Registry Client](https://github.com/singularityhub/sregistry-cli), but instead of
being intended for general interaction with Singularity containers and a local database, it's optimized for managing containers
in an HPC environment. Currently, this includes:

 - [LMOD](https://lmod.readthedocs.io/en/latest/)

You can use shpc if you are:

1. a linux administrator wanting to manage containers as modules for your cluster
2. a cluster user that wants to maintain your own folder of custom modules
3. a cluster user that simply wants to pull Singularity images as GitHub packages.

These use cases will be better flushed out and documented as the library is developed.


## Getting Started

### Installation instructions

You can install it to a system python or conda environment that is activated
as follows:

```bash
$ pip install singularity-hpc[all]
```

But you can also clone the repository and do a local install, and then
easily store your module files along with the install (the default until you
change it, discussed later):

```bash
$ git clone git@github.com:singularityhub/singularity-hpc
$ cd singularity-hpc
$ pip install -e .[all]
```

For either of the above, you can install without the sqlite support (meaning
there will be no admin database to search containers, just lmod):

```bash
$ pip install singularity-hpc[basic]

```

Installation of singularity-hpc adds an executable, `shpc` to your path.

```bash
$ which shpc
/opt/conda/bin/shpc
```

This executable should be accessible by an administrator, or anyone that you want
to be able to manage containers. Your user base will be interacting with your
containers via LMOD, so they do not need access to `shpc`. 
You'll want to configure and create your registry, discussed next.

### Creating a Registry

A registry consists of a database of local containers files, which are added
to LMOD as executables for your user base. This typically means that you are a
linux administrator of your cluster, and shpc should be installed for you to use
(but your users will not be interacting with it).

#### 1. Configure your registry

For any configuration value that you might set, the following variables
are available to you:

 - `$install_dir`: the shpc folder
 - `$root_dir`: the parent directory of shpc (where this README.md is located)


##### Modules Folder

The first thing you want to do is configure your module location, if you want it different
from the default. The path can be absolute or relative to `$install_dir` (the shpc
directory) or `$root_dir` (one above that) in your
configuration file at [shpc/settings.yml](shpc/settings.yml). If you are happy
with module files being stored in a `modules` folder in the present working
directory, you don't need to do any configuration. Otherwise, you can customize
your install:

```bash
# an absolute path
$ shpc config lmod_base:/opt/lmod/modules

# or a path relative to a variable location remember to escape the "$"
$ shpc config lmod_base:\$root_dir/modules
```

This directory will be the base where lua files are added, and container are stored.
For example, if you were to add a container with unique resource identifier `python/3.8`
you would see:

```bash
$install_dir/modules/
└── python
    └── 3.8/
        ├── module.lua
        └── python
```

Although your LMOD path might have multiple locations, Singularity Registry HPC 
assumes this one location to install container modules to in order to ensure
a unique namespace. Since the executables are expected to not have extension sif, at least to start,
we are removing it.


##### Registry

Although you likely will add custom containers, it's very likely that you
want to provide a set of core containers that are fairly standard, like Python
and other scientific packages. For this reason, Singularity Registry HPC
comes with a registry folder, or a folder with different containers and versions
that you can easily install. For example, here is a recipe for a Python 3.8 container
that would be installed to your modules as we showed above:

```yaml
docker: python
latest: 3.9.2
tags:
  - 3.9.2
  - 3.9.2-alpine
  - 3.8
maintainer: @vsoch
```

And then you would install the lmod file and container as follows:

```bash
$ shpc install python:3.9.2
```

And the module folder would be generated as follows:

```bash
$install_dir/modules/
└── python
    └── 3.8/
        ├── module.lua
        └── python
```

If you want to add a new registry file, you are encouraged to contribute it here
for others to use. Once it's added to the repository, the versions will be automatically
updated with a nightly run. This means that you can pull the repository to get
updated recipes, and then check for updates:

```bash
$ shpc check python
==> You have python 3.7 installed, but the latest is 3.8. Would you like to install?
yes/no : yes
```

It's reasonable that you can store your recipes alongside these files, in the [registry](registry)
folder. If you see a conflict and want to request allowing for a custom install path
for recipes, 

##### Database

By default, shpc installs with the ability to create a local database for you
to keep track of your containers (as an admin), which is not accessible to the
user. However, it's not entirely needed because you can easily use lmod. Here
are the configuration options available to you:

```
# disable keeping a sqlite database with metadata
database_disable: false

# default database file
database_file: "$install_dir/shpc.db"
```

So if you want to disable the database (meaning s

##### Module Software

The default module software is currently LMOD, but others could be added. If you
are interested in adding another module type, please [open an issue](https://github.com/singularityhub/singularity-hpc) and
provide description and links to what you have in mind. Currently, only lmod is
supported.

##### Container Technology

The default container technology to pull and then provide to users is Singularity,
which makes sense because we can add executables to the path that are Singularity containers.
If you would like support for a different container technology, please also
[open an issue](https://github.com/singularityhub/singularity-hpc) and
provide description and links to what you have in mind. Currently, only lmod is
supported.

### Commands

The following commands are available!

#### Config

If you want to edit a configuration value, you can either edit the [shpc/settings.yml](shpc/settings.yml)
file directly, or you can use `shpc config`. The following example shows changing
the default lmod_base path from the install directory modules folder.

```bash
# an absolute path
$ shpc config lmod_base:/opt/lmod/modules

# or a path relative to the install directory, remember to escape the "$"
$ shpc config lmod_base:\$install_dir/modules
```

#### List and Install

The most basic thing you might want to do is install an already existing
recipe in the registry. You might first want to list the known packages
first. To list all packages, you can run:

```bash
$ shpc list
[shpc-client] [database|sqlite:////home/vanessa/Desktop/Code/singularity-hpc/shpc.db]
python
```

To get details about a package, you would then do:

```bash
$ shpc show python
[shpc-client] [database|sqlite:////home/vanessa/Desktop/Code/singularity-hpc/shpc.db]
docker: python
latest: 3.9.2
tags:
- 3.9.2
- 3.9.2-alpine
filter:
- 3.9.*
maintainer: '@vsoch'
```

And then you can install a version that you like (or don't specify to default to
the latest, which in this case is 3.9.2).

```bash
$ shpc install python
```

You will see the container pulled, and then a message to indicate that the module
was created. 


```bash
shpc-client] [database|sqlite:////home/vanessa/Desktop/Code/singularity-hpc/shpc.db]
Module python/3.9.2 is created.
```

We can now see the module file and the container in the modules folder!

```bash
$ tree modules/
modules/
└── python
    └── 3.9.2
        ├── module.lua
        └── python-3.9.2.sif

2 directories, 2 files
```

Note that since we only have one module system (lmod) and one
HPC container technology (Singularity) these are the defaults. However, they
are parser options and can be customized to use something else if this is
added in the future.

If you don't have lmod on your system, you can now test interacting
with the module via the [container](#development-or-testing).

#### Add

**todo**


#### Images

**todo**


#### Check

**todo**


### Writing Registry Entries

An entry in the registry is a container.yaml file that lives in the [registry](registry)
folder. You should create subfolders based on a package name. Multiple versions
will be represented in the same file, and will install to the admin user's module
folder with version subfolders. E.g., Python would look like:

```bash
./registry
    python/
      container.yaml
```

And then install to:

```bash
$root_dir/modules/
└── python
    └── 3.8/
        ├── module.lua
        └── python
```

So different versions could exist alongside one another.

#### Registry Yaml Files

The typical registry yaml file will reference a container from a registry,
one or more versions, and a maintainer GitHub alias that can be pinged
for any issues:

```
docker: python
latest:
  3.9.2: "sha256:7d241b7a6c97ffc47c72664165de7c5892c99930fb59b362dd7d0c441addc5ed"
tags:
  3.9.2: "sha256:7d241b7a6c97ffc47c72664165de7c5892c99930fb59b362dd7d0c441addc5ed"
  3.9.2-alpine: "sha256:23e717dcd01e31caa4a8c6a6f2d5a222210f63085d87a903e024dd92cb9312fd"
filter:
  - "3.9.*"
maintainer: "@vsoch"
url: https://hub.docker.com/_/python
aliases:
  python: python
```

##### Registry Yaml Fields

Fields include:

| Field | Description | Required |
|--------|------------|----------|
| docker | A Docker uri, which should include the registry but not tag | true |
| tags  | A list of available tags | true |
| latest | The latest tag, which will be updated by a bot in the repository | true |
| maintainer | the GitHub alias of a maintainer to ping in case of trouble | true |
| filter | A list of patterns to use for adding new tags. If not defined, all are added | false |
| aliases | Named entrypoints for container (dict) | true |
| url | Documentation or other url for the container uri | false |
| description | Additional information for the registry entry | false |

Other supported (but not yet developed) fields could include different unique
resource identifiers to pull/obtain other kinds of containers. For this
current version, since we are assuming HPC and Singularity, we will typically
pull a Docker unique resource identifier with singularity, e.g.,:

```bash
$ singularity pull docker://python:3.9.2
```

##### Updating Registry Yaml Files

We will be developing a GitHub action that automatically parses new versions
for a container, and then updates the registry packages. The algorithm we will
use is the following:

 - If docker, retrieve all tags for the image
 - Update tags:
  - if one or more filters ("filter") are defined, add new tags that match
  - otherwise, add all new tags
 - If latest is defined and a version string can be parsed, update latest
 - For each of latest and tags, add new version information

## Development or Testing

If you first want to test singularity-hpc (shpc) with an LMOD installed in 
a container, a [Dockerfile](Dockerfile) is provided. The assumption is that
you have LMOD installed on your cluster or in the container. If not, you
can find instructions [here](https://lmod.readthedocs.io/en/latest/030_installing.html).

```bash
$ docker build -t singularity-hpc .
```

If you are developing the library and need lmod, you can easily bind your
code as follows:

```bash
$ docker run -it --rm -v $PWD/:/code --entrypoint bash singularity-hpc
```

Once you are in the container, you can direct LMOD to use your module files:

```bash
$ module use /code/modules
```

Then you can use spider to see the modules:

```bash
# module spider python

--------------------------------------------------------------------------------------------------------------------------------------------------------------
  python/3.9.2: python/3.9.2/module
--------------------------------------------------------------------------------------------------------------------------------------------------------------

    This module can be loaded directly: module load python/3.9.2/module
```

Make sure to write to files outside of the container so you don't muck with permissions.
Since we are using module use, this means that you can create module files as a user
or an admin - it all comes down to who has permission to write to the modules
folder, and of course use it. Note that I have not tested this on an HPC system
but plan to shortly.


## Tests to write

 - Settings load, update, get, etc.
 - Ensure that all defaults are present in settings (except for updated at)
 

## Previous Art

There are other tools that you might be interested in!

 - [VA Research Computing](https://www.rc.virginia.edu/userinfo/rivanna/software/containers/) has a similar system, but I couldn't find any code.
 - [Community Collections](https://github.com/community-collections/community-collections)
 - [Spack](https://spack.readthedocs.io/en/latest/module_file_support.html) installs modules for software built from source (not containers).
 
## TODOS

 - finish install, write add and other commands
 - ensure that we print columns to shpc list
 - test singularity build in actions, save to registry
 - develop pull command for shpc for this type, along with GitHub action

## License

This code is licensed under the MPL 2.0 [LICENSE](LICENSE).
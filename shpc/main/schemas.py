__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2021, Vanessa Sochat"
__license__ = "MPL 2.0"


## ContainerConfig Schema

schema_url = "https://json-schema.org/draft-07/schema/#"

# This is also for latest, and a list of tags

# The simplest form of aliases is key/value pairs
aliases = {
    "type": "object",
    "patternProperties": {
        "\\w[\\w-]*": {"type": "string"},
    },
}


# Features in container.yaml can be boolean or null, as they need to be
# container technology agnostic
features = {
    "type": "object",
    "patternProperties": {"\\w[\\w-]*": {"type": ["boolean", "null"]}},
}

# container features can be null or a known string
container_features = {
    "type": "object",
    "properties": {
        "gpu": {
            "oneOf": [{"type": "null"}, {"type": "string", "enum": ["nvidia", "amd"]}]
        }
    },
}


# Or a list
aliases_list = {
    "type": "array",
    "items": {
        "type": "object",
        "required": [
            "name",
            "command",
        ],
        "properties": {
            "name": {"type": "string"},
            "command": {"type": "string"},
            "options": {"type": "string"},
        },
    },
}


latest = {
    "type": "object",
    "minProperties": 1,
    "maxProperties": 1,
    "patternProperties": {
        "\\w[\\w-]*": {"type": "string"},
    },
}

containerConfigProperties = {
    "latest": aliases,
    "docker": {"type": "string"},
    "gh": {"type": "string"},
    "url": {"type": "string"},
    "test": {"type": "string"},
    "maintainer": {"type": "string"},
    "description": {"type": "string"},
    "tags": aliases,
    "filter": {
        "type": "array",
        "items": {"type": "string"},
    },
    "env": aliases,
    "features": features,
    "aliases": {
        "oneOf": [
            aliases,
            aliases_list,
        ]
    },
}


containerConfig = {
    "$schema": schema_url,
    "title": "ContainerConfig Schema",
    "type": "object",
    "required": [
        "latest",
        "tags",
        "maintainer",
        "description",
    ],
    "properties": containerConfigProperties,
}


## Settings.yml (loads as json)

# Currently all of these are required

settingsProperties = {
    "registry": {"type": "string"},
    "module_base": {"type": "string"},
    "singularity_module": {"type": ["string", "null"]},
    "bindpaths": {"type": ["string", "null"]},
    "updated_at": {"type": "string"},
    "environment_file": {"type": "string"},
    "container_tech": {"type": "string", "enum": ["singularity"]},
    "singularity_shell": {"type": "string", "enum": ["/bin/bash", "/bin/sh"]},
    "module_sys": {"type": "string", "enum": ["lmod", "tcl", None]},
    "container_features": container_features,
}


settings = {
    "$schema": schema_url,
    "title": "Settings Schema",
    "type": "object",
    "required": [
        "module_sys",
        "registry",
        "module_base",
        "singularity_module",
        "environment_file",
        "container_tech",
        "bindpaths",
        "singularity_shell",
        "container_features",
    ],
    "properties": settingsProperties,
}

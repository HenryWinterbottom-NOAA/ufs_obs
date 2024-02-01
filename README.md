[![License](https://img.shields.io/badge/License-LGPL_v2.1-black)](https://github.com/HenryWinterbottom-NOAA/ufs_tools/blob/develop/LICENSE)
![Linux](https://img.shields.io/badge/Linux-ubuntu%7Ccentos-lightgrey)
![Python Version](https://img.shields.io/badge/Python-3.5|3.6|3.7-blue)
[![Code style: black](https://img.shields.io/badge/Code%20Style-black-purple.svg)](https://github.com/psf/black)
[![Documentation Status](https://readthedocs.org/projects/ufs-obs/badge/?version=latest)](https://ufs-obs.readthedocs.io/en/latest/?badge=latest)

[![Python Coding Standards](https://github.com/HenryWinterbottom-NOAA/ufs_obs/actions/workflows/pycodestyle.yaml/badge.svg)](https://github.com/HenryWinterbottom-NOAA/ufs_obs/actions/workflows/pycodestyle.yaml)

# Overview

This repository contains tools for reading and writing specified
format observation-type files.

- **Authors:** [Henry R. Winterbottom](mailto:henry.winterbottom@noaa.gov)
- **Maintainers:** Henry R. Winterbottom
- **Version:** 0.0.1
- **License:** LGPL v2.1
- **Copyright**: Henry R. Winterbottom

# Cloning

This repository utilizes several sub-modules from various sources. To
obtain the entire system, do as follows.

~~~shell
user@host:$ /path/to/git clone --recursive https://github.com/HenryWinterbottom-NOAA/ufs_obs
~~~

# Dependencies

The package dependencies and the respective repository and manual
installation attributes are provided in the table below.

<div align="left">

| Dependency Package | <div align="left">Installation Instructions</div> | 
| :-------------: | :-------------: |
| <div align="left">[`pybufrkit`](https://github.com/ywangd/pybufrkit)</div> | <div align="left">`pip install pybufrkit`</div> |
| <div align="left">[`metpy`](https://github.com/Unidata/MetPy)</div> | <div align="left">`pip install metpy`</div> |

</div>

# Installing Package Dependencies

In order to install the respective Python packages upon which
`ufs_obs` is dependent, do as follows.

~~~shell
user@host:$ cd /path/to/ufs_obs
user@host:$ /path/to/pip install update
user@host:$ /path/to/pip install -r /path/to/ufs_obs/requirements.txt
user@host:$ ./build.sh
~~~

For additional information using `pip` and `requirements.txt` type files, see [here](https://pip.pypa.io/en/stable/reference/requirements-file-format/).

# Docker Containers

Docker containers containing the `ufs_obs` dependencies can be
collected as follows.

~~~shell
user@host:$ /path/to/docker pull ghrc.io/henrywinterbottom-noaa/ubuntu20.04.ufs_obs:latest
~~~

To execute within the Docker container, do as follows.

~~~shell
user@host:$ /path/to/docker run -v /localhost/path/to/ufs_obs:/ufs_obs -v /localhost/path/to/work:/work -it ghcr.io/henrywinterbottom-noaa/ubuntu20.04.ufs_obs:latest
~~~

# Forking

If a user wishes to contribute modifications done within their
respective fork(s) to the authoritative repository, we request that
the user first submit an issue and that the fork naming conventions
follow those listed below.

- `docs/user_branch_name`: Documentation additions and/or corrections for the application(s).

- `feature/user_branch_name`: Additions, enhancements, and/or upgrades for the application(s).

- `fix/user_branch_name`: Bug-type fixes for the application(s) that do not require immediate attention.

- `hotfix/user_branch_name`: Bug-type fixes which require immediate attention to fix issues that compromise the integrity of the respective application(s). 


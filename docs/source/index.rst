UFS Observations Toolbox
========================

Description
-----------

Python-based APIs for UFS observation processing.

- **ATCF**: Generates Automated Tropical Cyclone Forecast (ATCF) records from various sources.

Developers
----------

* Henry R. Winterbottom - henry.winterbottom@noaa.gov
  
Cloning
-------

The ``ufs_obs`` repository can be obtained as follows.

.. code-block:: bash

   user@host:$ /path/to/git clone --recursive https://www.github.com/HenryWinterbottom-NOAA/ufs_obs ./ufs_obs

Dependencies
------------

A Fortran compiler is required for the respective Python dependencies. This package has only been tested against GNU (e.g., ``gfortran``). The following table lists the ``ufs_obs`` Python dependencies.

.. list-table::
   :widths: auto
   :header-rows: 1
   :align: left

   * - **Package**
     - **Description**
     - **Installation Instructions**
   * - ``pybufrkit``
     - `Python toolkit to work with WMO BUFR messages <https://github.com/ywangd/pybufrkit>`_
     - ``pip install pybufrkit``
   * - ``metpy``
     - `Python tools for reading, visualizing and performing weather data calculations <https://github.com/Unidata/MetPy>`_
     - ``pip install metpy``

The above packages can be installed as follows:

.. code-block:: bash

   user@host:$ cd /path/to/ufs_obs
   user@host:$ /path/to/pip install --upgrade pip
   user@host:$ /path/to/pip install -r requirements.txt

For additional information and options for building Python packages, see `here <https://docs.python.org/3.5/distutils/setupscript.html)>`_.
   
Container Environments
----------------------

A Docker container environment, supporting and within which the ``ufs_obs`` applications can be executed, may be obtained and executed as follows:

.. code-block:: bash

   user@host:$ /path/to/docker pull ghcr.io/henrywinterbottom-noaa/ubuntu20.04.ufs_obs:latest
   user@host:$ /path/to/docker container run -it ghcr.io/henrywinterbottom-noaa/ubuntu20.04.ufs_obs:latest

.. toctree::
   :hidden:
   :maxdepth: 2

   atcf.rst
   cimss_adt.rst
   examples.rst

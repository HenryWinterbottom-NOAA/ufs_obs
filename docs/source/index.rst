############################
UFS Observations API Toolbox
############################

^^^^^^^^^^^
Description
^^^^^^^^^^^

Python-base API for UFS observation processing.

^^^^^^^^^^
Developers
^^^^^^^^^^

* Henry R. Winterbottom - henry.winterbottom@noaa.gov
  
^^^^^^^
Cloning
^^^^^^^

The ``ufs_obs`` repository may be obtained as follows.

.. code-block:: bash

   user@host:$ /path/to/git clone --recursive https://www.github.com/HenryWinterbottom-NOAA/ufs_obs ./ufs_obs
   
^^^^^^^^^^^^^^^^^^^^^^
Container Environments
^^^^^^^^^^^^^^^^^^^^^^

A Docker container environment, supporting and within which the
``ufs_obs`` applications can be executed, may be obtained and
executed as follows.

.. code-block:: bash

   user@host:$ /path/to/docker pull ghcr.io/henrywinterbottom-noaa/ubuntu20.04.ufs_obs:latest
   user@host:$ /path/to/docker container run -it ghcr.io/henrywinterbottom-noaa/ubuntu20.04.ufs_obs:latest

.. toctree::
   :hidden:
   :maxdepth: 2

   atcf.rst

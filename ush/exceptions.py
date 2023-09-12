"""
Module
------

    exceptions.py

Description
-----------

    This module loads the exceptions package.

Classes
-------

    ATCFError(msg)

        This is the base-class for exceptions encountered within the
        ush/atcf module; it is a sub-class of Error.

    ATCFReadError(msg)

        This is the base-class for exceptions encountered within the
        ush/io/atcf_read module; it is a sub-class of Error.

Requirements
------------

- ufs_pytils; https://github.com/HenryWinterbottom-NOAA/ufs_pyutils

Author(s)
---------

    Henry R. Winterbottom; 11 September 2023

History
-------

    2023-09-11: Henry Winterbottom -- Initial implementation.

"""

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

from utils.error_interface import Error

# ----

# Define all available module properties.
__all__ = [
    "ATCFError",
    "ATCFReadError",
]

# ----


class ATCFError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    ush/atcf module; it is a sub-class of Error.

    """


# ----


class ATCFReadError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    ush/io/atcf_read module; it is a sub-class of Error.

    """

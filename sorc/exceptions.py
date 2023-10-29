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

from utils.error_interface import Error

# ----

# Define all available module properties.
__all__ = [
    "ATCFError",
]

# ----


class ATCFError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    ush/atcf module; it is a sub-class of Error.

    """

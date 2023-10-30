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

    CIMSSADTError(msg)

        This is the base-class for exceptions encountered within the
        ush/cimss_adt module; it is a sub-class of Error.

    ObservationError(msg)

        This is the base-class for exceptions encountered within the
        ush/observation module; it is a sub-class of Error.

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
    "CIMSSADTError",
    "ObservationError",
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


class CIMSSADTError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    ush/cimss_adt module; it is a sub-class of Error.

    """


# ----


class ObservationError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    ush/observation module; it is a sub-class of Error.

    """

"""
Module
------

    location.py

Description
-----------

    This module contains functions to format the location of
    observations collected from a TEMPDROP observation message.

Functions
---------

    obslocation(locstr)

        This method reads a Python string containing the location
        information and parses to return the geographical location for
        the respective observation collected within a TEMPDROP
        message.

Author(s)
---------

    Henry R. Winterbottom; 24 January 2024

History
-------

    2024-01-24: Henry Winterbottom -- Initial implementation.

"""

# ----

import re
from typing import Tuple

# ----


def obslocation(locstr: str) -> Tuple[float, float]:
    """
    Description
    -----------

    This method reads a Python string containing the location
    information and parses to return the geographical location for the
    respective observation collected within a TEMPDROP message.

    Parameters
    ----------

    locstr: ``str``

        A Python string containing the location information to be
        parsed.

    Returns
    -------

    lat: ``float``

        A Python float value containing the latitude coordinate for
        the observation location.

    lon: ``float``

        A Python float value containing the longitude coordinate for
        the observation location.

    """

    # Define and scale the observation locations accordingly.
    (lat_scale, lon_scale) = [1.0, 1.0]
    if "s" in locstr.lower():
        lat_scale = -1.0
    if "e" in locstr.lower():
        lon_scale = -1.0
    locstr = re.sub("[a-zA-Z]", " ", locstr)
    lat = lat_scale * float(locstr.split()[0]) / 100.0
    lon = lon_scale * float(locstr.split()[1]) / 100.0

    return (lat, lon)

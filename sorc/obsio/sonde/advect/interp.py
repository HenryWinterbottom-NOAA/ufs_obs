"""
Module
------

    interp.py

Description
-----------

    This module contains a function to interpolate/extrapolate
    TEMPDROP Hurricane Research Division (HRD) Spline Analysis (HSA)
    formatted observations.

Functions
---------

    interp_hsa(varin, zarr, interp_type="linear", fill_value="extrapolate")

        This method interpolates to find missing values within a
        TEMPDROP HSA-formatted observation variable.

Author(s)
---------

    Henry R. Winterbottom; 24 January 2024

History
-------

    2024-01-24: Henry Winterbottom -- Initial implementation.

"""

# ----

from typing import Any

import numpy
from scipy.interpolate import interp1d

# ----

# Define all available module properties.
__all__ = ["interp_hsa"]

# ----


def interp_hsa(
    varin: numpy.array,
    zarr: numpy.array,
    interp_type: str = "linear",
    fill_value: Any = "extrapolate",
) -> numpy.array:
    """
    Description
    -----------

    This method interpolates to find missing values within a TEMPDROP
    observation variable.

    Parameters
    ----------

    varin: ``numpy.array``

        A Python numpy.array variable containing the TEMPDROP
        observation variable.

    zarr: ``numpy.array``

        A Python numpy.array variable containing the isobaric levels
        for the respective TEMPDROP observation variable.

    Keywords
    --------

    interp_type: ``str``, optional

        A Python string specifying the `interpolation type
        <https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.interp1d.html>`_.

    fill_value: ``Any``, optional

        A Python variable of any type specifying how to address
        missing datum values; see `here
        <https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.interp1d.html>`_.

    Returns
    -------

    varout: ``numpy.array``

        A Python numpy.array variable containing the interpolated
        TEMPDROP observation variable.

    """

    # Interpolate to find any missing data values.
    varout = varin[:]
    idx_list = list(numpy.where(~numpy.isnan(varin))[0])
    if len(idx_list) <= 1:
        varout = numpy.array(varout)
        return varout
    var = [varin[idx] for idx in idx_list]
    lev = [zarr[idx] for idx in idx_list]
    interp = interp1d(lev[:], var[:], kind="linear", fill_value=fill_value)
    varout = varin[:]
    for idx in list(numpy.where(numpy.isnan(varin))[0]):
        varout[idx] = float(interp(zarr[idx]))
    varout = numpy.array(varout)

    return varout

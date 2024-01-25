"""
Module
------

    advect.py

Description
-----------

    This module contains functions to advect observation sondes.

Functions
---------

    __normalize__(tempdrop_obj, xlat_list, xlon_list)

        This method normalizes the advection quantities for the
        geographical location profile for the respective sonde
        observations.

    advect(tempdrop_obj)

        This function returns the advected positions (locations) for
        the respective sonde due to drift during fall.

    fallrate(avgp, avgt, psfc)

        This method interpolates to find missing values within a
        TEMPDROP observation variable.

    interp_hsa(varin, zarr, interp_type="linear", fill_value="extrapolate")

        This method interpolates to find missing values within a
        TEMPDROP HSA-formatted observation variable.

    update_time(tempdrop_obj)

        This function updates the TEMPDROP observation time-stamp/date
        string and returns the Hurricane Research Division (HRD)
        Spline Analysis (HSA) formatted time-stamp/date string.

Requirements
------------

- ufs_pytils; https://github.com/HenryWinterbottom-NOAA/ufs_pyutils

Author(s)
---------

    Henry R. Winterbottom; 24 January 2024

History
-------

    2024-01-24: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=line-too-long
# pylint: disable=no-name-in-module
# pylint: disable=unused-argument

# ----

from types import SimpleNamespace
from typing import Any, List

import numpy
from diags.grids.bearing_geoloc import bearing_geoloc
from diags.grids.haversine import haversine
from obsio.sonde.aoml import gsndfall2
from obsio.sonde.hsa import choparr
from scipy.interpolate import interp1d
from tools import datetime_interface
from utils.logger_interface import Logger
from utils.timestamp_interface import GLOBAL

# ----

# Define all available module properties.
__all__ = ["advect", "fallrate", "interp_hsa", "update_time"]

# ----

logger = Logger(caller_name=__name__)

# ----


def __normalize__(
    tempdrop_obj: SimpleNamespace, xlat_list: List, xlon_list: List
) -> SimpleNamespace:
    """
    Description
    -----------

    This method normalizes the advection quantities for the
    geographical location profile for the respective sonde
    observations.

    Parameters
    ----------

    xlat_list: ``List``

        A Python list of latitude coordinate values collected from the
        respective sonde observations.

    xlon_list: ``List``

        A Python list of longitude coordinate values collected from
        the respective sonde observations.

    Returns
    -------

    tempdrop_obj: ``SimpleNamespace``

        A Python SimpleNamespace object updated to contain the
        normalized latitude and longitude coordinate values for the
        respective sonde observation.

    """

    # Normalize and correct the advected sonde observation
    # geographical locations.
    norma_xlat = min(tempdrop_obj.locate.rel[0], tempdrop_obj.locate.spg[0])
    normb_xlat = max(tempdrop_obj.locate.rel[0], tempdrop_obj.locate.spg[0])
    norma_xlon = min(tempdrop_obj.locate.rel[1], tempdrop_obj.locate.spg[1])
    normb_xlon = max(tempdrop_obj.locate.rel[1], tempdrop_obj.locate.spg[1])
    tempdrop_obj.interp.lat = [
        norma_xlat
        + (xlat_list[idx] - min(xlat_list))
        * (normb_xlat - norma_xlat)
        / (max(xlat_list) - min(xlat_list))
        for idx in range(len(xlat_list))
    ]
    tempdrop_obj.interp.lon = [
        norma_xlon
        + (xlon_list[idx] - min(xlon_list))
        * (normb_xlon - norma_xlon)
        / (max(xlon_list) - min(xlon_list))
        for idx in range(len(xlon_list))
    ]

    return tempdrop_obj


# ----


def advect(tempdrop_obj: SimpleNamespace) -> SimpleNamespace:
    """
    Description
    -----------

    This function returns the advected positions (locations) for the
    respective sonde due to drift during fall.

    Parameters
    ----------

    tempdrop_obj: ``SimpleNamespace``

        A Python SimpleNamespace containing the TEMPDROP
        observation(s) attributes.

    Returns
    -------

    tempdrop_obj: ``SimpleNamespace``

        A Python SimpleNamespace containing the advected TEMPDOP
        observation positions.

    """

    # Compute the advected sonde locations.
    msg = "Computing the sonde location due to advection/drift."
    logger.info(msg=msg)
    xlat_list = [tempdrop_obj.locate.rel[0]]
    xlon_list = [tempdrop_obj.locate.rel[1]]
    (xlat, xlon) = tempdrop_obj.locate.rel
    for idx in range(len(tempdrop_obj.interp.dist[:])):
        (xlat, xlon) = bearing_geoloc(
            loc1=(xlat, xlon),
            dist=tempdrop_obj.interp.dist[idx],
            heading=tempdrop_obj.interp.heading[idx],
        )
        xlat_list.append(xlat)
        xlon_list.append(xlon)
        (xlat, xlon) = (xlat_list[-1], xlon_list[-1])
    tempdrop_obj = __normalize__(
        tempdrop_obj=tempdrop_obj, xlat_list=xlat_list, xlon_list=xlon_list
    )

    return tempdrop_obj


# ----


def fallrate(avgp: numpy.array, avgt: numpy.array, psfc: float) -> numpy.array:
    """
    Description
    -----------

    This function computes the theoretical fall-rate for a sonde.

    Description
    -----------

    avgp: ``numpy.array``

        A Python numpy.array variable containing the average layer
        pressure(s).

    avgt: ``numpy.array``

        A Python numpy.array variable containing the average layer
        temperature(s).

    psfc: ``float``

        A Python float value specifying the surface pressure.

    Returns
    -------

    flrtarr: ``numpy.array``

        A Python numpy.array variable containing the theoretical
        fall-rate(s).

    """

    # Compute the theoretical fall-rate.
    flrtarr = numpy.zeros(len(avgp) + 1)
    for idx in range(1, len(avgp) + 1):
        try:
            flrtarr[idx] = gsndfall2(
                pr=avgp[idx], te=avgt[idx], bad=True, sfcp=psfc, mbps=True
            )
        except IndexError:
            pass

    return flrtarr


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


# ----


def update_time(tempdrop_obj: SimpleNamespace) -> SimpleNamespace:
    """
    Description
    -----------

    This function updates the TEMPDROP observation time-stamp/date
    string and returns the Hurricane Research Division (HRD) Spline
    Analysis (HSA) formatted time-stamp/date string.

    Parameters
    ----------

    tempdrop_obj: ``SimpleNamespace``

        A Python SimpleNamespace containing the TEMPDROP
        observation(s) attributes.

    Returns
    -------

    tempdrop_obj: ``SimpleNamespace``

        A Python SimpleNamespace containing the TEMPDROP
        observation(s) attributes and updated to contain the
        adjust/corrected HSA formatteed time-stamp/date strings.

    """

    # Compute the total number of offset-seconds for the respective
    # TEMPDROP observation(s).
    msg = "Computing the total number of offset-seconds for each TEMPDROP observation."
    logger.info(msg=msg)
    tempdrop_obj.interp.offset_seconds = [0]
    for idx in range(1, len(tempdrop_obj.interp.lat)):
        loc1 = (tempdrop_obj.interp.lat[idx - 1], tempdrop_obj.interp.lon[idx - 1])
        loc2 = (tempdrop_obj.interp.lat[idx], tempdrop_obj.interp.lon[idx])
        uwnd = tempdrop_obj.interp.uwnd[idx - 1]
        vwnd = tempdrop_obj.interp.vwnd[idx - 1]
        dist = haversine(loc1=loc1, loc2=loc2)
        velo = numpy.sqrt(uwnd * uwnd + vwnd * vwnd)
        tempdrop_obj.interp.offset_seconds.append(dist / velo)

    # Define the HSA-formatted TEMPDROP observation time-stamp/date
    # strings and format accordingly.
    msg = "Updating the TEMPDROP HSA-formatted observation time-stamp/date strings."
    logger.info(msg=msg)
    datestr_yymmdd = f"{tempdrop_obj.dateinfo.year_short}{tempdrop_obj.dateinfo.month}{tempdrop_obj.dateinfo.day}."
    datestr_hhmm = f"{tempdrop_obj.dateinfo.hour}{tempdrop_obj.dateinfo.minute}"
    (tempdrop_obj.interp.yymmdd, tempdrop_obj.interp.hhmm) = [[] for idx in range(2)]
    tempdrop_obj.interp.yymmdd.append(datestr_yymmdd)
    tempdrop_obj.interp.hhmm.append(datestr_hhmm)
    dtime_list = [
        sum(tempdrop_obj.interp.offset_seconds[0:idx])
        for idx in range(len(tempdrop_obj.interp.offset_seconds))
    ]
    for dtime in dtime_list:
        tempdrop_obj.interp.yymmdd.append(
            datetime_interface.datestrupdate(
                datestr=tempdrop_obj.dateinfo.cycle,
                in_frmttyp=GLOBAL,
                out_frmttyp="%y%m%d.",
                offset_seconds=dtime,
            )
        )
        tempdrop_obj.interp.hhmm.append(
            datetime_interface.datestrupdate(
                datestr=tempdrop_obj.dateinfo.cycle,
                in_frmttyp=GLOBAL,
                out_frmttyp="%H%M",
                offset_seconds=dtime,
            )
        )
    tempdrop_obj.interp.yymmdd = choparr(vararr=tempdrop_obj.interp.yymmdd)
    tempdrop_obj.interp.hhmm = choparr(vararr=tempdrop_obj.interp.hhmm)

    return tempdrop_obj

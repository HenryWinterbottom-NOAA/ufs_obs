"""
Module
------

    update_time.py

Description
-----------

    This module contains a function to update the TEMPDROP observation
    time-stamp/date strings.

Functions
---------

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

# ----

from types import SimpleNamespace

import numpy
from diags.grids.haversine import haversine
from obsio.sonde.hsa.choparr import choparr
from tools import datetime_interface
from utils.logger_interface import Logger
from utils.timestamp_interface import GLOBAL

# ----

# Define all available module properties.
__all__ = ["update_time"]

# ----

logger = Logger(caller_name=__name__)

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

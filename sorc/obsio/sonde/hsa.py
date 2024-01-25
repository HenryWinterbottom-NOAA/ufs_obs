"""
Module
------

    hsa.py

Description
-----------

    This module contains functions to manipulate Hurricane Research
    Division (HRD) Spline Analysis (HSA) formatted observation files.

Functions
---------

    choparr(vararr)

        This function modifies an input `numpy.array` such that it is
        formatted properly assuming the Hurricane Research Division
        (HRD) Spline Analysis (HSA) format.

    dateinfo(tempdrop_obj)

        This function collects the timestamp information from the
        respective observation file name.

    decode(tempdrop_obj)

        This function decodes a TEMPDROP formatted observation into
        the corresponding HRD Spline Analysis (HSA) format.

    layer_mean(vararr)

        This function computes the layer mean between the TEMPDROP decoded
        message variable interface levels.

    locations(tempdrop_obj)

        This function parses the TEMPDROP message and collects the
        sonde release (REL) time and location and the splash (SPL or
        SPG) time and location.

    obslocation(locstr)

        This function reads a Python string containing the location
        information and parses to return the geographical location for
        the respective observation collected within a TEMPDROP
        message.

    sfcpres(interp_obj, psfc_flag)

        This function defines the surface pressure relative to the
        TEMPDROP message; if the TEMPDROP message cannot be determined
        (i.e., the surface pressure flag cannot be found), numpy.nan
        will be returned.

    write_hsa(tempdrop_obj)

        This function writes the TEMPDROP observation to the Hurricane
        Research Division (HRD) Spline Analysis (HSA) format; the
        output is written to the original file name string but
        appended by `hsa`.

Requirements
------------

- ufs_pytils; https://github.com/HenryWinterbottom-NOAA/ufs_pyutils

Author(s)
---------

    Henry R. Winterbottom; 24 January 2024

History
-------

    2024-01-24: Henry Winterbottom -- Initial implementation.

References
----------

    Franklin, J. L., S. E. Feuer, J. Kaplan, and S. D. Aberson, 1996:
    Tropical cyclone motion and surrounding flow relationships:
    Searching for beta gyres in omega dropwindsonde datasets. Monthly
    Weather Review, 124, 64-84.

    https://doi.org/10.1175/1520-0493(1996)124<0064:TCMASF>2.0.CO;2

"""

# ----

# pylint: disable=expression-not-assigned
# pylint: disable=line-too-long
# pylint: disable=no-name-in-module
# pylint: disable=undefined-loop-variable

# ----

import os
import re
import statistics
from types import SimpleNamespace
from typing import Tuple

import numpy
from obsio.sonde.sondelib import close_hsa, drop
from tools import datetime_interface, fileio_interface, parser_interface
from utils.logger_interface import Logger
from utils.timestamp_interface import GLOBAL

# ----

# Define all available module properties.
__all__ = [
    "dateinfo",
    "decode",
    "layer_mean",
    "locations",
    "obslocation",
    "sfcpres",
    "tempdrop",
    "write_hsa",
]

# ----

logger = Logger(caller_name=__name__)

# ----


def choparr(vararr: numpy.array) -> numpy.array:
    """
    Description
    -----------

    This function modifies an input `numpy.array` such that it is
    formatted properly assuming the Hurricane Research Division (HRD)
    Spline Analysis (HSA) format.

    Parameters
    ----------

    vararr: ``numpy.array``

        A Python numpy.array variable array to be formatted.

    Returns
    -------

    vararr: ``numpy.array``

        A Python numpy.array variable array formatted to comply with
        the HSA format.

    """

    # Modify the input variable array accordingly.
    vararr = vararr[::1][::-1][1::]

    return vararr


# ----


def dateinfo(tempdrop_obj: SimpleNamespace) -> SimpleNamespace:
    """
    Description
    -----------

    This function collects the timestamp information from the
    respective observation file name.

    Parameters
    ----------

    tempdrop_obj: ``SimpleNamespace``

        A Python SimpleNamespace containing the TEMPDROP
        observation(s) attributes.

    Returns
    -------

    tempdrop_obj: ``SimpleNamespace``

        A Python SimpleNamespace object containing the observation
        timestamp information.

    Notes
    -----

    - The observation file path is assumed formatted as
        `%Y%m%d%H%M.[KNHC, KWBC, etc.,]`.

    """

    # Collect the timestamp information for the TEMPDROP
    # observation filename.
    datestr = os.path.basename(tempdrop_obj.filepath).split(".")[0]
    tempdrop_obj.dateinfo = datetime_interface.datestrcomps(
        datestr=datestr, frmttyp=GLOBAL
    )
    msg = f"Observation date information determined from TEMPDROP filepath {tempdrop_obj.filepath}."
    logger.info(msg=msg)

    return tempdrop_obj


# ----


def decode(tempdrop_obj: SimpleNamespace) -> SimpleNamespace:
    """
    Description
    -----------

    This function decodes a TEMPDROP formatted observation into the
    corresponding HRD Spline Analysis (HSA) format.

    Parameters
    ----------

    tempdrop_obj: ``SimpleNamespace``

        A Python SimpleNamespace containing the TEMPDROP
        observation(s) attributes.

    Returns
    -------

    tempdrop_obj: ``SimpleNamespace``

        A Python SimpleNamespace containing the HSA-formatted decoded
        TEMPDROP observation(s).

    """

    # Decode the TEMPDROP formatted observation message.
    luidx = 99
    ftninfile = os.path.join(os.getcwd(), "fort.12")
    ftnoutfile = os.path.join(os.getcwd(), f"fort.{luidx}")
    filelist = [ftninfile, ftnoutfile]
    fileio_interface.removefiles(filelist=filelist)
    for filename in filelist:
        if fileio_interface.fileexist(path=filename):
            fileio_interface.removefiles(filelist=[filename])
            msg = f"Removing existing file {ftnoutfile}."
            logger.warn(msg=msg)
    fileio_interface.symlink(srcfile=tempdrop_obj.filepath, dstfile=ftninfile)
    fileio_interface.touch(path=ftnoutfile)
    iflags = [2]
    for msgstr in tempdrop_obj.tempdrop:
        if "xx" in msgstr.lower():
            [
                drop(
                    luidx,
                    1,
                    iflag,
                    tempdrop_obj.dateinfo.year_short,
                    tempdrop_obj.dateinfo.month,
                    tempdrop_obj.dateinfo.day,
                    msgstr,
                    -9999.0,
                )
                for iflag in iflags
            ]
    close_hsa(luidx)
    close_hsa(12)
    with open(ftnoutfile, "r", encoding="utf-8") as sondefile:
        tempdrop_obj.decode = sondefile.readlines()
    msg = "The HSA formatted decoded TEMPDROP observation(s) is(are):\n\n"
    for line in tempdrop_obj.decode:
        msg = msg + line
    logger.info(msg=msg)
    fileio_interface.removefiles(filelist=filelist)

    return tempdrop_obj


# ----


def layer_mean(vararr: numpy.array) -> numpy.array:
    """
    Description
    -----------

    This function computes the layer mean between the TEMPDROP decoded
    message variable interface levels.

    Parameters
    ----------

    vararr: ``numpy.array``

        A Python numpy.array variable containing the TEMPDROP decoded
        message variable interface levels.

    Returns
    -------

    lymnarr: ``numpy.array``

        A Python numpy.array variable containing the layer means
        computed from the TEMPDROP decoded message variable interface
        levels.

    """

    # Compute the layer mean for the respective variable array.
    lymnarr = numpy.empty(numpy.shape(vararr))
    for idx in range(1, len(vararr)):
        pidx = idx - 1
        lymnarr[pidx] = statistics.mean([vararr[idx], vararr[pidx]])
    lymnarr = numpy.array(lymnarr)

    return lymnarr


# ----


def locations(tempdrop_obj: SimpleNamespace) -> SimpleNamespace:
    """
    Description
    -----------

    This function parses the TEMPDROP message and collects the sonde
    release (REL) time and location and the splash (SPL or SPG) time
    and location.

    Parameters
    ----------

    tempdrop_obj: ``SimpleNamespace``

        A Python SimpleNamespace containing the TEMPDROP
        observation(s) attributes.

    Returns
    -------

    tempdrop_obj: ``SimpleNamespace``

        A Python SimpleNamespace object containing the release and
        splash locations for the TEMPDROP observations.

    """

    # Collect the release and splash location for the respective
    # sonde.
    infostrs_list = ["rel", "spg", "spl"]
    tempdrop_obj.locate = parser_interface.object_define()
    obinfo_list = []
    for infostr in infostrs_list:
        for item in tempdrop_obj.tempdrop:
            if any(infostr in item.lower() for infostr in infostrs_list):
                obinfo_list.append(item.lower())
        obinfo_str = str(set(obinfo_list)).split()
        try:
            for idx, element in enumerate(obinfo_str):
                if infostr.lower() in element:
                    break
            infostr_items = obinfo_str[idx + 1 : idx + 3]
            (locstr, _) = (infostr_items[0], infostr_items[1])
            (lat, lon) = obslocation(locstr=locstr)
            tempdrop_obj.locate = parser_interface.object_setattr(
                object_in=tempdrop_obj.locate, key=infostr, value=(lat, lon)
            )
        except (ValueError, IndexError):
            msg = f"TEMPDROP message string {infostr.upper()} could not be located."
            logger.warn(msg=msg)

    return tempdrop_obj


# ----


def obslocation(locstr: str) -> Tuple[float, float]:
    """
    Description
    -----------

    This function reads a Python string containing the location
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


# ----


def sfcpres(interp_obj: SimpleNamespace, psfc_flag: float) -> float:
    """
    Description
    -----------

    This function defines the surface pressure relative to the
    TEMPDROP message; if the TEMPDROP message cannot be determined
    (i.e., the surface pressure flag cannot be found), numpy.nan will
    be returned.

    Parameters
    ----------

    interp_obj: ``SimpleNamespace``

        A Python SimpleNamespace object containing the interpolated
        decoded TEMPDROP observation message.

    psfc_flag: ``float``

        A Python float value specifying a surface observation; this is
        typically a pressure observation value of 1070.0.

    Returns
    -------

    psfc: ``float``

        A Python float value specifying the surface pressure from the
        TEMPDROP message; if the surface pressure cannot be identified
        from the respective TEMPDROP message, `numpy.nan` is returned.

    """

    # Determine the surface pressure from the TEMPDROP message.
    try:
        psfc_idx = [
            idx
            for idx in range(len(interp_obj.pres))
            if interp_obj.pres[idx] == psfc_flag
        ][0]
        psfc = interp_obj.hgt[psfc_idx]
    except (ValueError, IndexError):
        psfc = numpy.nanmax(interp_obj.pres)

    return psfc


# ----


def tempdrop(tempdrop_obj: SimpleNamespace) -> SimpleNamespace:
    """
    Description
    -----------

    This method collects the TEMPDROP message containing the sonde
    observations.

    Parameters
    ----------

    tempdrop_obj: ``SimpleNamespace``

        A Python SimpleNamespace containing the TEMPDROP
        observation(s) attributes.

    Returns
    -------

    tempdrop_obj: ``SimpleNamespace``

        A Python SimpleNamespace object updated to contain the
        TEMPDROP message containing the sonde observations.

    """

    # Collect the TEMPDROP message containing the sonde observations.
    with open(tempdrop_obj.filepath, "r", encoding="utf-8") as file:
        tempdrop_obj.tempdrop = file.read().split("\n")
    msg = "TEMPDROP formatted observation record is:\n\n"
    for line in tempdrop_obj.tempdrop:
        msg = msg + line + "\n"
    logger.info(msg=msg)

    return tempdrop_obj


# ----


def write_hsa(tempdrop_obj: SimpleNamespace) -> None:
    """
    Description
    -----------

    This function writes the TEMPDROP observation to the Hurricane
    Research Division (HRD) Spline Analysis (HSA) format; the output
    is written to the original file name string but appended by `hsa`.

    Parameters
    ----------

    tempdrop_obj: ``SimpleNamespace``

        A Python SimpleNamespace containing the interpolated HSA
        observation(s) attributes.

    """

    # Write the HSA formatted file.
    hsa_outfile = tempdrop_obj.filepath + ".hsa"
    msg = f"Writing HSA formatted file {hsa_outfile}."
    logger.info(msg=msg)
    format_str = "{:2d} {:7.1f} {:4d} {:7.3f} {:7.3f} {:7.1f} {:7.1f} {:7.1f} {:8.1f} {:6.1f} {:6.1f} {}\n"
    with open(hsa_outfile, "w", encoding="utf-8") as out:
        for idx, _ in enumerate(tempdrop_obj.interp.pres):
            outstr = format_str.format(
                1,
                float(tempdrop_obj.interp.yymmdd[idx]),
                int(tempdrop_obj.interp.hhmm[idx]),
                tempdrop_obj.interp.lat[idx],
                tempdrop_obj.interp.lon[idx],
                tempdrop_obj.interp.pres[idx],
                tempdrop_obj.interp.temp[idx],
                tempdrop_obj.interp.rh[idx],
                tempdrop_obj.interp.hgt[idx],
                tempdrop_obj.interp.uwnd[idx],
                tempdrop_obj.interp.vwnd[idx],
                tempdrop_obj.interp.flag[idx],
            )
            out.write(outstr)

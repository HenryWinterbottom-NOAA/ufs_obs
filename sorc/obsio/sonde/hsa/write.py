"""
Module
------

    write.py

Description
-----------

    This module contains a function to write the TEMPDROP observation
    attributes to the Hurricane Research Division (HRD) Spline
    Analysis (HSA) format and to a output file path.

Functions
---------

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

"""

# ----

# pylint: disable=line-too-long

# ----

from types import SimpleNamespace

from utils.logger_interface import Logger

# ----

# Define all available module properties.
__all__ = ["write_hsa"]

# ----

logger = Logger(caller_name=__name__)

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

        A Python SimpleNamespace containing the TEMPDROP
        observation(s) attributes.

    """

    # Write the HSA formatted file.
    hsa_outfile = tempdrop_obj.filepath + ".hsa"
    msg = f"Writing HSA formatted file {hsa_outfile}."
    logger.info(msg=msg)
    format_str = "{:2d} {:7.1f} {:4d} {:7.3f} {:7.3f} {:7.1f} {:7.1f} {:7.1f} {:8.1f} {:6.1f} {:6.1f} {}\n"
    with open(hsa_outfile, "w", encoding="utf-8") as out:
        for (idx, _) in enumerate(tempdrop_obj.interp.pres):
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

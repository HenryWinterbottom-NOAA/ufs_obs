"""
Module
------

    cimss_adt_read.py

Description
-----------

    This module contains functions to parse Cooperative Institude for
    Meteorological Satellite Studies (CIMSS) Advanced Dvorak Technique
    (ADT) history formatted observation files.

Functions
---------

    filter_adt(func)

        This function is a wrapper function for the filtering of ADT
        observations relative to a specified CIMSS ADT attribute/type.

    __adt_geoloc__(adtobs)

        This function collects the geographical location attributes
        for the respective ADT observation.

    __adt_intns__(adtobs)

        This function collects the intensity metric attributes for the
        respective ADT observation.

    __adt_time__(adtobs)

        This function collects the timestamp for the respective ADT
        observation.

    __build_adt__(adtobs_list)

        This function builds a Python SimpleNamespace object
        containing the relevant CIMSS ADT observations.

    __build_table__(adtobs_obj)

        This function builds a table of the relevant CIMSS ADT
        observations and the respective attributes.

    __filter_fix__(adtobs_list, fix_exclude)

        This function filters ADT observations relative to the CIMSS
        ADT `FIX MTHD` attribute/type.

    __filter_scene__(adtobs_list, scene_exclude)

        This function filters ADT observations relative to the CIMSS
        ADT `SCENE TYPE` attribute/type.

    __get_adtobs__(filepath)

        This function retrieves the ADT observations from the file;
        the observations are determined by evaluating whether the
        respective timestamps (e.g., month of year) strings exist
        within the relevant lines of the respective input file
        `filepath`.

    read_cimssadt_history(filepath, scene_exclude = None, fix_exclude = None)

        This function reads a CIMSS ADT history formatted file and
        returns a Python SimpleNamespace object containing the
        relevant observation attributes.

Requirements
------------

- ufs_pytils; https://github.com/HenryWinterbottom-NOAA/ufs_pyutils

Author(s)
---------

    Henry R. Winterbottom; 29 October 2023

History
-------

    2023-10-29: Henry Winterbottom -- Initial implementation.

"""

# ----


import functools
from types import SimpleNamespace
from typing import Callable, Dict, List, Tuple

from exceptions import CIMSSADTError
from metpy.units import units
from tools import datetime_interface, parser_interface
from utils.constants_interface import hPa2Pa, kts2mps
from utils.logger_interface import Logger
from utils.table_interface import compose, init_table
from utils.timestamp_interface import GLOBAL

# ----

# Define all available module properties.
__all__ = ["read_cimssadt_history"]

# ----

logger = Logger(caller_name=__name__)

# ----


def filter_adt(func: Callable) -> Callable:
    """
    Description
    -----------

    This function is a wrapper function for the filtering of ADT
    observations relative to a specified CIMSS ADT attribute/type.

    Parameters
    ----------

    func: ``Callable``

        A Python Callable object containing the function to be
        wrapped.

    Returns
    -------

    wrapped_function: ``Callable``

        A Python Callable object containing the wrapped function.

    """

    @functools.wraps(func)
    def wrapped_function(*args: Tuple, **kwargs: Dict) -> List:
        """
        Description
        -----------

        This function filters ADT observations relative to the
        specified CIMSS ADT attribute/type.

        Other Parameters
        ----------------

        args: ``Tuple``

            A Python tuple containing additional arguments passed to
            the constructor.

        kwargs: ``Dict``

            A Python dictionary containing additional key and value
            pairs to be passed to the constructor.

        Returns
        -------

        outlist: List

            A Python list of filtered ADT observations.

        """

        # Filter the ADT observations accordingly.
        (inlist, exclude) = func(*args, **kwargs)
        try:
            outlist = [
                item
                for item in inlist
                if not any(ex in item for ex in exclude.rsplit())
            ]
        except AttributeError:
            outlist = [item for item in inlist if not any(
                ex in item for ex in exclude)]

        return outlist

    return wrapped_function


# ----


def __adt_geoloc__(adtobs: str) -> Tuple[float, float]:
    """
    Description
    -----------

    This function collects the geographical location attributes for
    the respective ADT observation.

    Parameters
    ----------

    adtobs: ``str``

        A Python string containing the respective ADT observation to
        be parsed.

    Returns
    -------

    adt_lat: ``float``

        A Python float value defining the ADT observation latitude
        coordinate location.

    adt_lon: ``float``

        A Python float value defining the ADT observation longitude
        coordinate location.

    """

    # Collect the geographical location attributes for the ADT
    # observation.
    try:
        adt_lat = float(adtobs.split()[-5:][0])
        adt_lon = float(adtobs.split()[-4:][0])
    except ValueError:
        try:
            adt_lat = float(adtobs.split()[-6:][0])
            adt_lon = float(adtobs.split()[-5:][0])
        except ValueError as errmsg:
            msg = (
                "Geographical location could not be determined from "
                f"ADT observation {adtobs}. Aborting!!!"
            )
            raise CIMSSADTError(msg=msg) from errmsg

    return (adt_lat, adt_lon)


# ----


def __adt_intns__(adtobs: str) -> Tuple[float, float]:
    """
    Description
    -----------

    This function collects the intensity metric attributes for the
    respective ADT observation.

    Parameters
    ----------

    adtobs: ``str``

        A Python string containing the respective ADT observation to
        be parsed.

    Returns
    -------

    adt_mslp: ``float``

        A Python float value defining the ADT observation minimum
        sea-level pressure value; units are Pascal.

    adt_vmax: ``float``

        A Python float value defining the ADT observation maximum wind
        speed intensity value; units are meters per second.

    """

    # Collect the intensity metric attributes for the ADT observation.
    try:
        adt_mslp = float(adtobs.split()[3])
        adt_vmax = float(adtobs.split()[4])
    except ValueError as errmsg:
        msg = (
            "Intensity attributes could not be determined from ADT "
            f"observation {adtobs}. Aborting!!!"
        )
        raise CIMSSADTError(msg=msg) from errmsg
    adt_mslp = units.Quantity(adt_mslp * hPa2Pa, "pascal")
    adt_vmax = units.Quantity(adt_vmax * kts2mps, "mps")

    return (adt_mslp, adt_vmax)


# ----


def __adt_time__(adtobs: str) -> str:
    """
    Description
    -----------

    This function collects the timestamp for the respective ADT
    observation.

    Parameters
    ----------

    adtobs: ``str``

        A Python string containing the respective ADT observation to
        be parsed.

    Returns
    -------

    adt_time: ``str``

        A Python string defining the ADT observation timestamp; format
        is %Y%m%d%H%M%S assuming the POSIX convention.

    """

    # Collec the timestamp for the ADT observation.
    adt_time = datetime_interface.datestrupdate(
        datestr=f"{adtobs.split()[0].lower()} {adtobs.split()[1]}",
        in_frmttyp="%Y%b%d %H%M%S",
        out_frmttyp=GLOBAL,
    )

    return adt_time


# ----


def __build_adt__(adtobs_list: List) -> SimpleNamespace:
    """
    Description
    -----------

    This function builds a Python SimpleNamespace object containing
    the relevant CIMSS ADT observations.

    Parameters
    ----------

    adtobs_list: ``List``

        A Python list of ADT observations.

    Returns
    -------

    adtobs_obj: ``SimpleNamespace``

        A Python SimpleNamespace object containing the relevant CIMSS
        ADT observations.

    """

    # Construct the Python SimpleNamespace object containing the
    # relevant CIMSS ADT observations.
    msg = "Building the CIMSS ADT observations."
    logger.info(msg=msg)
    adtobs_obj = parser_interface.object_define()
    for idx, adtobs in enumerate(adtobs_list):
        adtobs_dict = {}
        adtobs_dict["timestamp"] = __adt_time__(adtobs=adtobs)
        (adtobs_dict["lat"], adtobs_dict["lon"]
         ) = __adt_geoloc__(adtobs=adtobs)
        (adtobs_dict["mslp"], adtobs_dict["vmax"]
         ) = __adt_intns__(adtobs=adtobs)
        adtobs_obj = parser_interface.object_setattr(
            object_in=adtobs_obj, key=f"ADT{idx:04}", value=adtobs_dict
        )

    return adtobs_obj


# ----


def __build_table__(adtobs_obj: SimpleNamespace) -> None:
    """
    Description
    -----------

    This function builds a table of the relevant CIMSS ADT
    observations and the respective attributes.

    Parameters
    ----------

    adtobs_obj: ``SimpleNamespace``

        A Python SimpleNamespace object containing the relevant CIMSS
        ADT observations.

    """

    # Build a table of the relevant CIMSS ADT observations and the
    # respective attributes.
    table_obj = init_table()
    table_obj.header = [
        "Observation ID",
        "Timestamp",
        "Latitude (degree)",
        "Longitude (degree)",
        "Pressure (Pascal)",
        "Wind Speed (meter per second)",
    ]
    for adtobs in vars(adtobs_obj):
        adtobs_dict = parser_interface.object_getattr(
            object_in=adtobs_obj, key=adtobs)
        row = [
            adtobs,
            adtobs_dict["timestamp"],
            adtobs_dict["lat"],
            adtobs_dict["lon"],
            adtobs_dict["mslp"].magnitude,
            adtobs_dict["vmax"].value,
        ]
        table_obj.table.append(row)

    table = compose(table_obj=table_obj)
    logger.info(msg="\n" + table)


# ----


@filter_adt
def __filter_fix__(adtobs_list: List, fix_exclude: List) -> List:
    """
    Description
    -----------

    This function filters ADT observations relative to the CIMSS ADT
    `FIX MTHD` attribute/type.

    Parameters
    ----------

    adtobs_list: ``List``

        A Python list of ADT observations.

    scene_exclude: ``List``

        A Python list of CIMSS ADT `FIX MTHD` attributes/types to be
        filtered from the ADT observations list specified upon entry.

    Returns
    -------

    adtobs_list: ``List``

        A Python list of filtered ADT observations.

    """

    # Filter the ADT observations relative to the `FIX MTHD`
    # attributes/types.
    if fix_exclude is None:
        msg = "No ADT observations will be filtered relative to `FIX MTHD`."
        logger.warn(msg=msg)
        fix_exclude = []

    return (adtobs_list, fix_exclude)


# ----


@filter_adt
def __filter_scene__(adtobs_list: List, scene_exclude: List) -> List:
    """
    Description
    -----------

    This function filters ADT observations relative to the CIMSS ADT
    `SCENE TYPE` attribute/type.

    Parameters
    ----------

    adtobs_list: ``List``

        A Python list of ADT observations.

    scene_exclude: ``List``

        A Python list of CIMSS ADT `SCENE TYPE` attributes/types to be
        filtered from the ADT observations list specified upon entry.

    Returns
    -------

    adtobs_list: ``List``

        A Python list of filtered ADT observations.

    """

    # Filter the ADT observations relative to the `SCENE TYPE`
    # attributes/types.
    if scene_exclude is None:
        msg = "No ADT observations will be filtered relative to `SCENE TYPE`."
        logger.warn(msg=msg)
        scene_exclude = []

    return (adtobs_list, scene_exclude)


# ----


def __get_adtobs__(filepath: str) -> List:
    """
    Description
    -----------

    This function retrieves the ADT observations from the file; the
    observations are determined by evaluating whether the respective
    timestamps (e.g., month of year) strings exist within the relevant
    lines of the respective input file `filepath`.

    Parameters
    ----------

    filepath: ``str``

        A Python string specifying the file path for the CIMSS-ADT
        formatted file.

    Returns
    -------

    adtobs_list: ``List``

        A Python list of ADT observations.

    """

    # Parse the CIMSS ADT file and collect the relevant file
    # attributes.
    moy_list = [
        "JAN",
        "FEB",
        "MAR",
        "APR",
        "MAY",
        "JUN",
        "JUL",
        "AUG",
        "SEP",
        "OCT",
        "NOV",
        "DEC",
    ]
    adtobs_list = []
    with open(filepath, "r", encoding="utf-8") as adtfile:
        adtobs = adtfile.read().split("\n")
    for adtob in adtobs:
        if any(moy in adtob for moy in moy_list):
            adtobs_list.append(adtob)

    return adtobs_list


# ----


def read_cimssadt_history(
    filepath: str, scene_exclude: List = None, fix_exclude: List = None
) -> SimpleNamespace:
    """
    Description
    -----------

    This function reads a CIMSS ADT history formatted file and returns
    a Python SimpleNamespace object containing the relevant
    observation attributes.

    Parameters
    ----------

    filepath: ``str``

        A Python string specifying the file path for the CIMSS ADT
        history formatted file.

    Keywords
    --------

    scene_exclude: ``List``, optional

        A Python list containing `SCENE TYPE` observation attributes
        to be excluded from the ADT observation collection.

    fix_exclude: ``List``, optional

        A Python list containing `FIX MTHD` observation attributes to
        be excluded from the ADT observation collection.

    Returns
    -------

    adtobs_obj: ``SimpleNamespace``

        A Python SimpleNamespace object containing the relevant CIMSS
        ADT observation attributes.

    """

    # Collect the relevant CIMSS ADT observation attributes.
    adtobs_list = __get_adtobs__(filepath=filepath)
    adtobs_list = __filter_scene__(
        adtobs_list=adtobs_list, scene_exclude=scene_exclude)
    adtobs_list = __filter_fix__(
        adtobs_list=adtobs_list, fix_exclude=fix_exclude)
    adtobs_obj = __build_adt__(adtobs_list=adtobs_list)
    __build_table__(adtobs_obj=adtobs_obj)

    return adtobs_obj

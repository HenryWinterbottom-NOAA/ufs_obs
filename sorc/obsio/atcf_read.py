"""
Module
------

    atcf_read.py

Description
-----------

    This module contains functions to read tropical cyclone (TC)
    attributes for location, intensity, and relevant radii size from
    Automated Tropical Cyclone Forecast (ATCF) records, often referred
    to as "A-Deck" files.

Functions
---------

    __get_tcvrec__(tcvrec_list)

        This function defines a Python dictionary containining the
        attributes for the respective event which have been defined
        from the list of values collected from the respective
        TC-vitals record.

    __scalegeo__(tcvrec_obj)

        This function defines the geographical location coordinates
        for the TC-vitals record accordingly.

    __scaleintns__(tcvrec_obj)

        This function scales the minimum sea-level pressure (`mslp`)
        and maximum wind speed (`vmax`) intensity values to their
        corresponding MKS units.

    __scalesize__(tcvrec_obj)

        This function scales the size metric values to their
        corresponding MKS units.

    read_atcf(filepath)

        This function reads a TC-vitals formatted file and returns a
        Python SimpleNamespace object containing the TC-vitals
        attributes for all records within the filepath.

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

from types import SimpleNamespace
from typing import Dict, List

import numpy
from confs.yaml_interface import YAML
from exceptions import ATCFError
from metpy.units import units
from tools import parser_interface
from utils.constants_interface import hPa2Pa, kn2m, kts2mps
from utils.logger_interface import Logger
from utils.schema_interface import build_schema, validate_schema

# ----

# Define all available module properties.
__all__ = ["read_tcvfile"]

# ----

logger = Logger(caller_name=__name__)

# ----


def __get_tcvrec__(tcvrec_list: List) -> Dict:
    """
    Description
    -----------

    This function defines a Python dictionary containining the
    attributes for the respective event which have been defined from
    the list of values collected from the respective TC-vitals record.

    Parameters
    ----------

    tcvrec_list: ``List``

        A Python list containing the attributes for the respective TC
        event.

    Returns
    -------

    tcvrec_obj: ``SimpleNamespace``

        A Python SimpleNamespace object containing the ATCF attributes
        for the respective TC event.

    """

    # Collect the ATCF attributes for the respective TC event.
    msg = "Formatting ATCF record."
    logger.info(msg=msg)
    atcf_schema = YAML().read_yaml(
        yaml_file=parser_interface.enviro_get("ATCF_READ_SCHEMA")
    )
    tcvrec_dict = {}
    for key, _ in atcf_schema.items():
        try:
            idx = atcf_schema[key]["idx"]
            tcvrec_dict[key] = tcvrec_list[idx]
        except IndexError:
            pass
    if tcvrec_list[-1] in ["X", "S", "M", "D"]:
        key = list(tcvrec_dict.keys())[-1]
        tcvrec_dict.pop(key)
        tcvrec_dict["stormdepth"] = str(tcvrec_list[-1])
    tcvrec_obj = parser_interface.dict_toobject(
        in_dict=validate_schema(
            cls_schema=build_schema(schema_def_dict=atcf_schema), cls_opts=tcvrec_dict
        )
    )

    return tcvrec_obj


# ----


def __scalegeo__(tcvrec_obj: SimpleNamespace) -> SimpleNamespace:
    """
    Description
    -----------

    This function defines the geographical location coordinates for
    the TC-vitals record accordingly.

    Parameters
    ----------

    tcvrec_obj: ``SimpleNamespace``

        A Python SimpleNamespace object containing the ATCF attributes
        for the respective TC event.

    Returns
    -------

    tcvrec_obj: ``SimpleNamespace``

        A Python SimpleNamespace object updated to contain the
        geographical location coordinates.

    """

    # Rescale the ATCF geographical location values accordingly.
    (lat_scale, lon_scale) = [1.0 / 10.0 for idx in range(2)]
    if "S" in tcvrec_obj.lat:
        lat_scale = -1.0 / 10.0
    tcvrec_obj.lat = units.Quantity(lat_scale * int(tcvrec_obj.lat[:-1]), "degrees")
    if "E" in tcvrec_obj.lon:
        lon_scale = -1.0 / 10.0
    tcvrec_obj.lon = units.Quantity(lon_scale * int(tcvrec_obj.lon[:-1]), "degrees")
    tcvrec_obj.stormdir = units.Quantity(tcvrec_obj.stormdir, "degrees")
    tcvrec_obj.stormspd = units.Quantity(tcvrec_obj.stormspd * kts2mps, units="mps")

    return tcvrec_obj


# ----


def __scaleintns__(tcvrec_obj: SimpleNamespace) -> SimpleNamespace:
    """
    Description
    -----------

    This function scales the minimum sea-level pressure (`mslp`) and
    maximum wind speed (`vmax`) intensity values to their
    corresponding MKS units.

    Parameters
    ----------

    tcvrec_obj: ``SimpleNamespace``

        A Python SimpleNamespace object containing the ATCF attributes
        for the respective TC event.

    Returns
    -------

    tcvrec_obj: ``SimpleNamespace``

        A Python SimpleNamespace object updated to contain the
        intensity attribute values.

    """

    # Scale the ATCF intensity values accordingly.
    tcvrec_obj.mslp = units.Quantity(float(tcvrec_obj.mslp) * hPa2Pa, "pascal")
    tcvrec_obj.vmax = units.Quantity(float(tcvrec_obj.vmax), "mps")

    return tcvrec_obj


# ----


def __scalesize__(tcvrec_obj: SimpleNamespace) -> SimpleNamespace:
    """
    Description
    -----------

    This function scales the size metric values to their corresponding
    MKS units.

    Parameters
    ----------

    tcvrec_obj: ``SimpleNamespace``

        A Python SimpleNamespace object containing the ATCF attributes
        for the respective TC event.

    Returns
    -------

    tcvrec_obj: ``SimpleNamespace``

        A Python SimpleNamespace object containing the scaled TC size
        attributes (if necessary).

    """

    # Scale the ATCF size attribute values accordingly.
    if tcvrec_obj.poci > 0:
        tcvrec_obj.poci = units.Quantity(int(tcvrec_obj.poci) * kn2m, "m")
    if tcvrec_obj.rmw > 0:
        tcvrec_obj.rmw = units.Quantity(int(tcvrec_obj.rmw) * kn2m, "m")
    if tcvrec_obj.roci > 0:
        tcvrec_obj.roci = units.Quantity(int(tcvrec_obj.roci) * kn2m, "m")
    for quad in ["ne", "se", "sw", "nw"]:
        for wind in ["34", "50", "64"]:
            windrad = f"{quad}{wind}"
            value = parser_interface.object_getattr(
                object_in=tcvrec_obj, key=windrad, force=True
            )
            if value is None:
                value = numpy.nan
            tcvrec_obj = units.Quantity(
                parser_interface.object_setattr(
                    object_in=tcvrec_obj, key=windrad, value=value
                ),
                "m",
            )

    return tcvrec_obj


# ----


def read_tcvfile(filepath: str) -> SimpleNamespace:
    """
    Description
    -----------

    This function reads a TC-vitals formatted file and returns a
    Python SimpleNamespace object containing the TC-vitals attributes
    for all records within the filepath.

    Parameters
    ----------

    filepath: ``str``

        A Python string specifying the file path for the TC-vitals
        formatted file.

    Returns
    -------

    tcvobj: ``SimpleNamespace``

        A Python SimpleNamespace object containing the attributes for
        each TC record within the file path specified upon entry.

    """

    # Read in TC-vitals records.
    with open(filepath, "r", encoding="utf-8") as file:
        tcvdata = file.read()

    # Collect the attributes for the respective TC-vitals record(s);
    # proceed accordingly.
    try:
        tcvobj = parser_interface.object_define()
        for idx, tcv in enumerate(tcvdata.split("\n")):
            if tcv.strip():
                msg = f"Parsing TC-vitals record {tcv}."
                logger.info(msg)
                tcvrec_obj = __get_tcvrec__(tcvrec_list=tcv.split())
                tcvrec_obj = __scalegeo__(tcvrec_obj=tcvrec_obj)
                tcvrec_obj = __scaleintns__(tcvrec_obj=tcvrec_obj)
                tcvrec_obj = __scalesize__(tcvrec_obj=tcvrec_obj)
                tcvobj = parser_interface.object_setattr(
                    object_in=tcvobj,
                    key=f"TC{idx}",
                    value=__get_tcvrec__(tcvrec_list=tcv.split()),
                )
    except Exception as errmsg:
        msg = (
            f"Parsing ATCF filepath {filepath} failed with error {errmsg}. "
            "Aborting!!!"
        )
        raise ATCFError(msg=msg) from errmsg

    return tcvobj

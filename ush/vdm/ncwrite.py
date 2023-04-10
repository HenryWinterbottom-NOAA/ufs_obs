"""


"""

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

import numpy

import os

from dataclasses import dataclass

from utils.logger_interface import Logger

from ioapps import netcdf4_interface

from tools import parser_interface

# ----


@dataclass
class VDMNCWrite:
    """
    Description
    -----------

    """

    def __init__(self: dataclass, yaml_obj: object):
        """
        Description
        -----------

        Creates a new VDMWrite object.

        """

        # Define the base-class attributes.
        self.logger = Logger()
        self.yaml_obj = yaml_obj

        self.output_path = parser_interface.object_getattr(
            object_in=self.yaml_obj, key="output_path", force=True)
        if self.output_path is None:
            self.output_path = os.getcwd()

            msg = ("The output path `output_path` has not been defined; "
                   f"setting to {self.output_path}."
                   )
            self.logger.warn(msg=msg)

        if self.output_path is not None:
            msg = f"Output will be written to path {self.output_path}."
            self.logger.info(msg=msg)

    def ncwrite(self: dataclass, tcevents_obj: object) -> None:
        """
        Description
        -----------

        """

        # Build netCDF-formatted file paths containing the VDM
        # attributes for each respective TC event.
        for (tcevent, _) in vars(tcevents_obj).items():

            dict_in = {}

            tcevent_info = parser_interface.object_getattr(
                object_in=tcevents_obj, key=tcevent)

            ncfile = os.path.join(self.output_path, f"{tcevent}.nc")
            msg = f"Build netCDF-formatted file path {ncfile}."
            self.logger.info(msg=msg)

            (ncdim_obj, ncvar_obj) = [
                parser_interface.object_define() for idx in range(2)]

            ncdim_obj = parser_interface.object_setattr(
                object_in=ncdim_obj, key="times", value=len(tcevent_info.dates))

            # NEED LOOP OVER ALL VARIABLES HERE.
            dict_in["dims"] = "times"
            dict_in["type"] = "float64"
            dict_in["desc"] = "test"
            dict_in["values"] = tcevent_info.mslp
            dict_in["varname"] = "mslp"

            ncvar_obj = parser_interface.object_setattr(
                object_in=ncvar_obj, key="mslp", value=dict_in)

            # ncvar_obj.mslp = tcevent_info.mslp
            # ncvar_obj.fix_lats = tcevent_info.fix_lats

            netcdf4_interface.ncwrite(
                ncfile=ncfile,
                ncdim_obj=ncdim_obj,
                ncvar_obj=ncvar_obj
            )

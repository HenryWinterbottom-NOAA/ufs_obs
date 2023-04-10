# =========================================================================

# Module: ush/vdm/format.py

# Author: Henry R. Winterbottom

# Email: henry.winterbottom@noaa.gov

# This program is free software: you can redistribute it and/or modify
# it under the terms of the respective public license published by the
# Free Software Foundation and included with the repository within
# which this application is contained.

# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

# =========================================================================

"""
Module
------


"""

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

import os
from dataclasses import dataclass
from typing import Any, List, Tuple, Callable

from utils.decorator_interface import privatemethod
from utils.logger_interface import Logger

import numpy

from vdm.collect import VDMCollect

from tools import datetime_interface

from utils import timestamp_interface

from utils.constants_interface import hPa2Pa, kts2mps

from tools import parser_interface

# ----


@dataclass
class VDMFormat:
    """
    Description
    -----------

    """

    def __init__(self: dataclass, yaml_obj: object):
        """
        Description
        -----------

        Creates a new VDMFormat object.

        """

        # Define the base-class attributes.
        self.logger = Logger()
        self.yaml_obj = yaml_obj
        self.vdm_attr_dict = VDMCollect.VDM_ATTR_DICT

    def format(self: dataclass, vdm_info_obj: object):
        """

        """

        # Define a list of events and proceed accordingly.
        tcevents_obj = parser_interface.object_define()

        tcevent_list = list(set(event.replace(
            self.vdm_attr_dict["event"], "").strip()
            for event in iter(vdm_info_obj.event)))

        msg = ("Processing the following tropical cyclone events: "
               f"{', '.join(tcevent_list)}"
               )
        self.logger.warn(msg=msg)

        # For each event, build a Python dictionary and collect and
        # format the respective attributes.
        for tcevent in tcevent_list:

            tcevent_obj = parser_interface.object_define()
            msg = f"Formatting event {tcevent}."
            self.logger.info(msg=msg)

            # Find the list index values for all VDM attributes
            # corresponding to the respective event.
            for (idx, item) in enumerate(list(vdm_info_obj.event)):

                idx_list = list(idx for (idx, item) in enumerate(
                    vdm_info_obj.event) if tcevent in item)

            # Collect the timestamps for which the respective VDMs are
            # valid.
            tcevent_obj.dates = self.get_dates(
                vdm_info_obj=vdm_info_obj, idx_list=idx_list)

            # Collect the attributes from the respective VDMs.
            (tcevent_obj.fix_lats, tcevent_obj.fix_lons) = self.get_fixes(
                vdm_info_obj=vdm_info_obj, idx_list=idx_list)
            tcevent_obj.mslp = self.get_mslp(
                vdm_info_obj=vdm_info_obj, idx_list=idx_list)

            tcevents_obj = parser_interface.object_setattr(
                object_in=tcevents_obj, key=tcevent, value=tcevent_obj)

        return tcevents_obj

    @privatemethod
    def get_dates(self: dataclass, vdm_info_obj: object, idx_list: List) -> List:
        """
        Description
        -----------

        This method parses the URL paths and determines the VDM valid
        timestamp accordingly.

        Parameters
        ----------

        vdm_info_obj: object

            A Python object containing the VDM information/attributes.

        idx_list: List

            A Python list containing the list index values
            corresponding to valid VDM for a specified TC event; see
            base-class method `format`.

        Returns
        -------

        dates_list: List

            A Python list of date strings for the VDMs valid for a
            specified TC event.

        """

        # Collect the list of VDM URL paths and determine the
        # timestamps for each.
        msg = "Collecting and formatting vortex data message timestamps."
        self.logger.info(msg=msg)

        url_list = [os.path.basename(url) for url in
                    self.get_list_item(vdm_info_attr_list=vdm_info_obj.url,
                                       idx_list=idx_list)]

        dates_list = [datetime_interface.datestrupdate(
            datestr=url, in_frmttyp=self.yaml_obj.vdm_file_frmt,
            out_frmttyp=timestamp_interface.GLOBAL) for url in url_list]

        return dates_list

    @privatemethod
    def get_fixes(self: dataclass, vdm_info_obj: object, idx_list:
                  List) -> Tuple[List, List]:
        """
        Description
        -----------

        This method collects the estimated fix location(s) from the
        respective VMD(s).

        Parameters
        ----------

        vdm_info_obj: object

            A Python object containing the VDM information/attributes.

        idx_list: List

            A Python list containing the list index values
            corresponding to valid VDM for a specified TC event; see
            base-class method `format`.

        Returns
        -------

        lats_list: List

            A Python list containing the VDM fix estimate latitude
            coodinate; this value is assumed to be Northern Hemisphere
            affiliated; this may need to be modified in the future.

        lons_list: List

            A Python list containing the VDM fix estimate latitude
            coodinate; this value is assumed to be Western Hemisphere
            affiliated; this may need to be modified in the future.

        """

        # Collect the list of VDM geographical fix locations and
        # format accordingly.
        msg = "Collecting and defining the vortex data message fix locations."
        self.logger.info(msg=msg)

        fix_list = self.get_list_item(vdm_info_attr_list=vdm_info_obj.fix,
                                      idx_list=idx_list)

        (lats_list, lons_list) = ([] for idx in range(2))

        for fix_str in fix_list:
            fix_items_list = fix_str.split()

            geolocs_list = [value for value in (
                [parser_interface.handler(lambda: float(fix_item), return_none=True)
                 for fix_item in fix_items_list]) if value is not None]

            lats_list.append(geolocs_list[0])
            lons_list.append(-1.0*geolocs_list[1])

        return (lats_list, lons_list)

    @privatemethod
    def get_mslp(self: dataclass, vdm_info_obj: object,
                 idx_list: List) -> List:
        """
        Description
        -----------

        This method collects the minimum sea-level pressure
        estimated/extrapolated values from the respective VDM(s).

        Parameters
        ----------

        vdm_info_obj: object

            A Python object containing the VDM information/attributes.

        idx_list: List

            A Python list containing the list index values
            corresponding to valid VDM for a specified TC event; see
            base-class method `format`.

        Returns
        -------

        mslp_list: List

            A Python list containing the minimum sea-level pressure
            values collected from the respective VDM(s); units are
            Pascals.

        """

        # Collect the list of VDM minimum sea-level pressure
        # estimates/extrapolations and format accordingly.
        msg = "Collecting and defining the vortex data message intensity estimates."
        self.logger.info(msg=msg)

        mslp_est_list = self.get_list_item(vdm_info_attr_list=vdm_info_obj.mslp,
                                           idx_list=idx_list)

        mslp_list = [float(mslp_est.split()[2]) *
                     hPa2Pa for mslp_est in mslp_est_list]

        return mslp_list

    @privatemethod
    def get_list_item(self: dataclass, vdm_info_attr_list: List,
                      idx_list: int) -> List:
        """
        Description
        -----------

        This method collects list values using the respective VDM
        attribute list and the defined index values.

        Parameters
        ----------

        vdm_info_attr_list: List

            A Python list containing a VDM attribute.

        idx_list:

            A Python list containing the list index values
            corresponding to valid VDM for a specified TC event; see
            base-class method `format`.

        Returns
        -------

        vdm_attr_list: List

            A Python list containing valid VDM attributes for a
            specified TC event.

        """

        # Collect and return the respective list slice as defined by
        # the list of index values `idx_list`.
        vdm_attr_list = [vdm_info_attr_list[idx] for idx in idx_list]

        return vdm_attr_list

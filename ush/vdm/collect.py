# =========================================================================

# Module: ush/vdm/collect.py

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

    collect.py

Description
-----------

    This module contains the base-class for all National Oceanic and
    Atmospheric Administration (NOAA) National Hurricane Center (NHC)
    Vortex Data Message (VDM) attribute collections.

Classes
-------

    VDMCollect():

        This is the base-class object for all National Oceanic and
        Atmospheric Administration (NOAA) National Hurricane Center
        (NHC) Vortex Data Message (VDM) attribute collections.

Author(s)
---------

    Henry R. Winterbottom; 08 April 2023

History
-------

    2023-04-08: Henry Winterbottom -- Initial implementation.

"""

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

import os
from dataclasses import dataclass
from typing import Generator, List

from ioapps import url_interface
from tools import parser_interface
from utils.decorator_interface import privatemethod
from utils.logger_interface import Logger

# ----


@dataclass
class VDMCollect:
    """
    Description
    -----------

    This is the base-class object for all National Oceanic and
    Atmospheric Administration (NOAA) National Hurricane Center (NHC)
    Vortex Data Message (VDM) attribute collections.

    """

    # Define a Python dictionary containing the VDM information to be
    # collected.
    VDM_ATTR_DICT = {
        "event": "VORTEX DATA MESSAGE",
        "time": "A. ",
        "fix": "B. ",
        "mhsl": "C. ",
        "mslp": "D. ",
        "fix_wnd": "E. ",
        "eye_type": "F. ",
        "eye_shape": "G. ",
        "inb_mxsfcwnd": "H. ",
        "inb_mxsfcwnd_info": "I. ",
        "inb_mxflwnd": "J. ",
        "inb_mxflwnd_info": "K. ",
        "outb_mxsfcwnd": "L. ",
        "outb_mxsfcwnd_info": "M. ",
        "outb_mxflwnd": "N. ",
        "outb_mxflwnd_info": "O. ",
        "out_fltmp_pres": "P. ",
        "in_fltmp_pres": "Q. ",
    }

    def __init__(self: dataclass, yaml_obj: object):
        """
        Description
        -----------

        Creates a new VDMCollect object.

        """

        # Define the base-class attributes.
        self.yaml_obj = yaml_obj
        self.logger = Logger()
        self.yaml_obj = yaml_obj

    def collect(self: dataclass) -> object:
        """
        Description
        -----------

        This method performs collects and returns a Python object
        containing the VDM attributes to be formatted.

        Returns
        -------

        vdm_info_obj: object

            A Python object containing the VDM attributes to be
            formatted.

        """

        # Collect the VDM attributes to be formatted.
        vdms_list = self.download_vdm()
        vdm_info_obj = self.vdm_info(vdms_list=vdms_list)

        return vdm_info_obj

    @privatemethod
    def download_vdm(self: dataclass) -> List:
        """
        Description
        -----------

        This method attempts to identify and compile the available
        vortex data message (VDM) file attributes from the URL path
        specified in the experiment configuration.

        Returns
        -------

        vdms_list: List

            A Python object containing the available VDM file
            attributes.

        """

        # Download and read the VDM files into memory; proceed
        # accordingly.
        vdm_contents_obj = parser_interface.object_define()

        webpath = self.yaml_obj.webpath
        weblist = url_interface.get_weblist(url=webpath)
        urllist = [os.path.join(webpath, url) for url in weblist]

        # for url in urllist:
        for (i, url) in enumerate(urllist):  # TEST
            data = url_interface.get_contents(url=url)

            # Collect the respective VDM file attributes accordingly.
            if data is not None:

                data = data + f"url_path: {url}"
                vdm_url_obj = parser_interface.object_setattr(
                    object_in=vdm_contents_obj, key=os.path.basename(url), value=data
                )

            if i == 8:  # TEST

                break  # TEST

        # Define a list of the attributes collected from all valid
        # VDMs.
        vdms_list = list(map(str.splitlines, vars(vdm_url_obj).values()))

        return vdms_list

    @privatemethod
    def vdm_getstr(self: dataclass, vdms_list: List, vdm_str: str) -> Generator:
        """Defintion
        ---------

        This method reads a Python list of VDMs and returns a Python
        list of items containing the VDM string specified upon entry
        (`vdm_str`).

        Parameters
        ----------

        vdms_list: List

            A Python list of VDM lists (see base-class method
            `collect`).

        vdm_str: str

            A Python string specifying the sub-string to seek within
            the respective VDMs Python list.

        Yields
        ------

        vdms_str_gen: Generator

            A Python generator containing the VDM list attributes
            containing the specified sub-string `vdm_str`.

        """

        # Define a Python generator for the respective VDM string to
        # be collected.
        vdm_items_list = (
            " ".join([item for item in vdm if vdm_str in item]) for vdm in vdms_list)

        return vdm_items_list

    @privatemethod
    def vdm_info(self: dataclass, vdms_list: List) -> object:
        """
        Description
        -----------

        This method collects and returns VDM attributes to be formatted.

        Parameters
        ----------

        vdms_list:

            A Python list of VDM lists (see base-class method
            `collect`).

        Returns
        -------

        vdm_info_obj: object

            A Python object containing Python generator objects for
            the respective VDM attributes to be formatted.

        """

        # Define the sub-string attributes within the respective VDMs.
        vdm_info_obj = parser_interface.object_define()

        # Collect the VDM information in accordance with the define
        # attributes.
        for vdm_attr in self.VDM_ATTR_DICT:
            vdm_attrs_list = self.vdm_getstr(
                vdms_list=vdms_list, vdm_str=self.VDM_ATTR_DICT[vdm_attr]
            )

            vdm_info_obj = parser_interface.object_setattr(
                object_in=vdm_info_obj, key=vdm_attr, value=vdm_attrs_list
            )

        return vdm_info_obj

# =========================================================================

# Module: ush/vdm/__init__.py

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

"""

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

from dataclasses import dataclass

from confs.yaml_interface import YAML

from exceptions import VDMError
from vdm.collect import VDMCollect
from vdm.format import VDMFormat
from utils.logger_interface import Logger

# ----


@dataclass
class VDM:
    """
    Description
    -----------


    """

    def __init__(self: dataclass, options_obj: object):
        """
        Description
        -----------

        Creates a new VDM object.

        """

        # Define the base-class attributes.
        self.options_obj = options_obj
        self.logger = Logger()
        self.yaml_file = self.options_obj.yaml_file
        self.yaml_obj = YAML().read_yaml(yaml_file=self.yaml_file,
                                         return_obj=True)

        self.vdm_collect = VDMCollect(yaml_obj=self.yaml_obj)
        self.vdm_format = VDMFormat(yaml_obj=self.yaml_obj)

    def run(self: dataclass) -> None:
        """
        Description
        -----------

        """

        vdm_info_obj = self.vdm_collect.collect()
        self.vdm_format.format(vdm_info_obj=vdm_info_obj)

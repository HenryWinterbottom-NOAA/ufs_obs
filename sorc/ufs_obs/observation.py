"""
Module
------

    observation.py

Description
-----------

    This is the base-class object for all observation processing.

Classes
-------

    Observation(obs_type, *args, **kwargs)

        This is the base-class object for all observation processing
        and/or formatting; it is a sub-class of ABC.

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

# pylint: disable=unused-argument

# ----

from abc import ABC, abstractmethod
from typing import Dict, Tuple

from tools import parser_interface
from utils.logger_interface import Logger

# ----

# Define all available module properties.
__all__ = ["Observation"]

# ----


class Observation(ABC):
    """
    Description
    -----------

    This is the base-class object for all observation processing
    and/or formatting; it is a sub-class of ABC.

    Parameters
    ----------

    obs_type: str

        A Python string specifying the supported observation type
        indicator

    Other Parameters
    ----------------

    args: Tuple

        A Python tuple containing additional arguments passed to the
        constructor.

    kwargs: Dict

        A Python dictionary containing additional key and value pairs
        to be passed to the constructor.

    """

    def __init__(self: ABC, obs_type: str, *args: Tuple, **kwargs: Dict):
        """
        Description
        -----------

        Creates a new Observation object.

        """

        # Define the base-class attributes.
        self.logger = Logger(
            caller_name=f"{__name__}.{self.__class__.__name__}")
        self.obs_type = obs_type
        self.obs_obj = parser_interface.object_define()

    @abstractmethod
    def read(self: ABC) -> None:
        """
        Description
        -----------

        This method provides a `read` layer for the respective
        sub-class task.

        """

    @abstractmethod
    def write(self: ABC) -> None:
        """
        Description
        -----------

        This method provides a `write` layer for the respective
        sub-class task.

        """

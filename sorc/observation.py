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
        and/or formatting.

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

import os
from abc import abstractmethod
from types import SimpleNamespace
from typing import Dict, Generic, Tuple

from confs.yaml_interface import YAML
from tools import parser_interface
from utils.decorator_interface import privatemethod
from utils.logger_interface import Logger

from exceptions import ObservationError

# ----

# Define all available module properties.
__all__ = ["Observation"]

# ----


class Observation:
    """
    Description
    -----------

    This is the base-class object for all observation processing
    and/or formatting/

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

    def __init__(self: Generic, obs_type: str, *args: Tuple, **kwargs: Dict):
        """
        Description
        -----------

        Creates a new Observation object.

        """

        # Define the base-class attributes.
        self.logger = Logger(caller_name=f"{__name__}.{self.__class__.__name__}")
        self.obs_type = obs_type
        self.obs_type_obj = self.get_config()
        self.obs_obj = parser_interface.object_define()

    @privatemethod
    def get_config(self: Generic) -> SimpleNamespace:
        """
        Description
        -----------

        This method returns the configuration attributes for the
        respective observation type.

        Returns
        -------

        obs_type_obj: SimpleNamespace

            A Python SimpleNamespace object containing the
            configuration attributes for the respective observation
            type.

        Raises
        ------

        ObservationError:

            - raised if the environment variable `OBS_ROOT` has not
              been specified.

        """

        # Collect the configuration attributes for the respective
        # observation type.
        obs_root = parser_interface.enviro_get(envvar="OBS_ROOT")
        if obs_root is None:
            msg = "The environment variable `OBS_ROOT` has not been specified. Aborting!!!"
            raise ObservationError(msg=msg)
        obs_config = parser_interface.enviro_get(envvar="OBS_CONFIG_YAML")
        if obs_config is None:
            obs_config = os.path.join(obs_root, "parm", "config.yaml")
            msg = (
                "The observation type attributes file has not been defined; "
                f"searching for {obs_config}."
            )
            self.logger.warn(msg=msg)
            obs_type_obj = parser_interface.dict_toobject(
                in_dict=YAML().read_yaml(yaml_file=obs_config)[self.obs_type]
            )

        return obs_type_obj

    @abstractmethod
    def read(self: Generic, *args: Tuple, **kwargs: Dict) -> None:
        """
        Description
        -----------

        This method provides a `read` layer for the respective
        sub-class task.

        Other Parameters
        ----------------

        args: Tuple

            A Python tuple containing additional arguments passed to
            the constructor.

        kwargs: Dict

            A Python dictionary containing additional key and value
            pairs to be passed to the constructor.

        """

    @abstractmethod
    def write(self: Generic, *args: Tuple, **kwargs: Dict) -> None:
        """
        Description
        -----------

        This method provides a `write` layer for the respective
        sub-class task.

        Other Parameters
        ----------------

        args: Tuple

            A Python tuple containing additional arguments passed to
            the constructor.

        kwargs: Dict

            A Python dictionary containing additional key and value
            pairs to be passed to the constructor.

        """

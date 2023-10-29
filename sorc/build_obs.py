"""
Module
------

    build_obs.py

Description
-----------

    This module contains a wrapper function for building Python
    dictionaries containing observation values validated via the
    specified observation-type schema.

Functions
---------

    build_obs(func)

        This function is a wrapper function for the observation Python
        dictionary construction.

Requirements
------------

- ufs_pytils; https://github.com/HenryWinterbottom-NOAA/ufs_pyutils

Author(s)
---------

    Henry R. Winterbottom; 28 October 2023

History
-------

    2023-10-28: Henry Winterbottom -- Initial implementation.

"""

# ----

import functools
from typing import Callable, Dict, Tuple, Type

from confs.yaml_interface import YAML
from utils.schema_interface import build_schema, validate_schema

# ----


def build_obs(func: Callable) -> Callable:
    """
    Description
    -----------

    This function is a wrapper function for the observation Python
    dictionary construction method.

    Parameters
    ----------

    func: Callable

        A Python Callable object containing the function to be
        wrapped.

    Returns
    -------

    wrapped_function: Callable

        A Python Callable object containing the wrapped function.

    """

    @functools.wraps(func)
    def wrapped_function(
        self: Type["MyClass"], *args: Tuple, **kwargs: Dict
    ) -> Tuple[Callable, Dict]:
        """
        Description
        -----------

        This function builds a Python dictionary containing
        observation values validated via the specified
        observation-type schema.

        Other Parameters
        ----------------

        args: Tuple

            A Python tuple containing additional arguments passed to
            the constructor.

        kwargs: Dict

            A Python dictionary containing additional key and value
            pairs to be passed to the constructor.

        Returns
        -------

        obs_dict: Dict

            A Python dictionary containing observation values
            validated via the specified observation-type schema.

        """

        # Validate the observation values vai the specified
        # observation-type schema.
        (schema_path, obs_dict) = func(self, *args, **kwargs)
        cls_schema = build_schema(
            schema_def_dict=YAML().read_yaml(yaml_file=schema_path)
        )
        obs_dict = validate_schema(cls_schema=cls_schema, cls_opts=obs_dict)

        return obs_dict

    return wrapped_function

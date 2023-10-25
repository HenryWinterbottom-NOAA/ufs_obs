"""
Module
------

    atcf.py

Description
-----------

    This is the base-class object for all Automated Tropical Cyclone
    Forecast (ATCF) formatted file read and writing.

Classes
-------

    ATCF()

        This is the base-class object for all Automated Tropical
        Cyclone Forecast (ATCF) formatted file reading and writing; it
        is a sub-class of Observation.

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

# pylint: disable=fixme

# ----

from types import SimpleNamespace

from exceptions import ATCFReadError
from observation import Observation
from obsio.atcf_read import read_tcvfile

# ----

# Define all available module properties.
__all__ = ["ATCF"]

# ----


class ATCF(Observation):
    """
    Description
    -----------

    This is the base-class object for all Automated Tropical Cyclone
    Forecast (ATCF) formatted file reading and writing; it is a
    sub-class of Observation.

    """

    def __init__(self: Observation):
        """
        Description
        -----------

        Creates a new ATCF object.

        """

        # Define the base-class attributes.
        super().__init__(obs_type="atcf")

    def read(self: Observation, atcf_filepath: str = None) -> SimpleNamespace:
        """
        Description
        -----------

        This method reads an ATCF-formatted file and returns a
        SimpleNamespace object containing the attributes for the
        respective ATCF records.

        Keywords
        --------

        atcf_filepath: str, optional

            A Python string specifying the path to the ATCF-formatted
            file containing the respective ATCF records.

        Returns
        -------

        tcvobj: SimpleNamespace

            A Python SimpleNamespace object containing the attributes
            for each ATCF record.

        """

        # Read the ATCF-formatted records.
        super().read()
        if atcf_filepath is None:
            msg = "The ATCF-formatted file path cannot be NoneType. Aborting!!!"
            raise ATCFReadError(msg=msg)
        tcvobj = read_tcvfile(filepath=atcf_filepath)

        return tcvobj

    def write(self: Observation) -> None:
        """
        # TODO


        """

        # TODO
        super().write()

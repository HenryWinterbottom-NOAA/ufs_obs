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

# pylint: disable=arguments-differ

# ----

import os
from types import SimpleNamespace
from typing import Dict

from confs.jinja2_interface import write_from_template
from confs.yaml_interface import YAML
from tools import fileio_interface, parser_interface
from utils.decorator_interface import privatemethod

from build_obs import build_obs
from exceptions import ATCFError
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
        parser_interface.enviro_set(
            envvar="ATCF_READ_SCHEMA", value=self.obs_type_obj.schema
        )

    @privatemethod
    @build_obs
    def build_tcv(self: Observation, tcvobj: SimpleNamespace) -> Dict:
        """
        Description
        -----------

        This method builds the ATCF-formatted record for the
        respective ATCF event.

        Parameters
        ----------

        tcvobj: ``SimpleNamespace``

            A Python SimpleNamespace object containing the attributes
            for the respective ATCF record.

        Return
        ------

        obs_dict: ``Dict``

            A Python dictionary containing the ATCF observations.

        """

        # Build the TC-vitals record.
        schema_path = self.obs_type_obj.schema
        obs_dict = parser_interface.object_todict(object_in=tcvobj)

        return (schema_path, obs_dict)

    @privatemethod
    def format_tcv(self: Observation, obs_dict: Dict) -> Dict:
        """
        Description
        -----------

        This method formats the ATCF record in accordance with the
        ATCF record schema.

        Parameters
        ----------

        obs_dict: ``Dict``

            A Python dictionary containing the ATCF observations.

        Returns
        -------

        tcv_dict: ``Dict``

            A Python dictionary containing the ATCF-formatted record.

        """

        # Format the ATCF observations.
        schema_dict = YAML().read_yaml(yaml_file=self.obs_type_obj.schema)
        tcv_dict = {}
        for obs in obs_dict:
            strfrmt = parser_interface.dict_key_value(
                dict_in=schema_dict[obs], key="format", force=True, no_split=True
            )
            tcv_dict[obs] = strfrmt % obs_dict[obs]

        return tcv_dict

    def read(self: Observation, atcf_filepath: str = None) -> SimpleNamespace:
        """
        Description
        -----------

        This method reads an ATCF-formatted file and returns a
        SimpleNamespace object containing the attributes for the
        respective ATCF records.

        Keywords
        --------

        atcf_filepath: ``str``, optional

            A Python string specifying the path to the ATCF-formatted
            file containing the respective ATCF records.

        Returns
        -------

        tcvobj: ``SimpleNamespace``

            A Python SimpleNamespace object containing the attributes
            for each ATCF record.

        Raises
        ------

        ATCFError:

            - raised if the `atcf_filepath` attribute is NoneType upon
              entry.

        """

        # Read the ATCF-formatted records.
        super().read()
        if atcf_filepath is None:
            msg = "The ATCF-formatted file path cannot be NoneType. Aborting!!!"
            raise ATCFError(msg=msg)
        tcvobj = read_tcvfile(filepath=atcf_filepath)

        return tcvobj

    def write(self: Observation, tcvobj: SimpleNamespace, atcf_filepath: str) -> None:
        """
        Description
        -----------

        This method writes a ATCF-formatted file for the specified
        ATCF record events.

        Parameters
        ----------

        tcvobj: ``SimpleNamespace``

            A Python SimpleNamespace object containing the attributes
            for each ATCF record.

        atcf_filepath: ``str``

            A Python string specifying the path to the ATCF-formatted
            file to contain the respective ATCF records.

        Raises
        ------

        ATCFError:

            - raised if an exception is encountered while building,
              formatting, and/or writing the respective ATCF records.

        """

        # Loop through all ATCF records, format the records, and write
        # the respective records to the specified file path.
        super().write()
        msg = f"Writing ATCF records to {atcf_filepath}."
        self.logger.info(msg=msg)
        try:
            with open(atcf_filepath, "w", encoding="utf-8") as atcf_file:
                for tcid in vars(tcvobj):
                    msg = f"Building ATCF record for TC {tcid}."
                    self.logger.info(msg=msg)
                    obs_dict = self.build_tcv(
                        tcvobj=parser_interface.object_getattr(
                            object_in=tcvobj, key=tcid, force=True
                        )
                    )
                    tcv_dict = self.format_tcv(obs_dict=obs_dict)
                    vfile_jinja = fileio_interface.virtual_file().name
                    write_from_template(
                        tmpl_path=self.obs_type_obj.tmpl,
                        output_file=vfile_jinja,
                        in_dict=tcv_dict,
                        rpl_tmpl_mrks=True,
                        skip_missing=True,
                    )
                    with open(vfile_jinja, "r", encoding="utf-8") as vfile:
                        tcv = vfile.read()
                    msg = f"Writing the following ATCF record: {tcv}"
                    self.logger.info(msg=msg)
                    atcf_file.write(f"{tcv}")
                    os.unlink(vfile_jinja)
        except Exception as errmsg:
            msg = f"Writing the ATCF records failed with error {errmsg}. Aborting!!!"
            raise ATCFError(msg=msg) from errmsg

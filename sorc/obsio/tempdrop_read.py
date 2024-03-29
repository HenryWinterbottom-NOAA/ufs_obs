"""
Module
------

    tempdrop_read.py

Description
-----------

    This module contains function to read TEMPDROP observation
    messages collected from sondes, particularly those dropped within
    tropical cyclone events.

Classes
-------

    TEMPDROP(correct_drift=False, correct_time=False)

        This is the base-class object for decoding TEMPDROP
        observation messages and providing user specified corrections;
        it is a sub-class of Observation.

Requirements
------------

- ufs_pytils; https://github.com/HenryWinterbottom-NOAA/ufs_pyutils

Author(s)
---------

    Henry R. Winterbottom; 25 January 2024

History
-------

    2024-01-25: Henry Winterbottom -- Initial implementation.

References
----------

    NHOP sonde drop format

    https://www.aoml.noaa.gov/hrd/format/tempdrop_format.html

    Franklin, J. L., S. E. Feuer, J. Kaplan, and S. D. Aberson, 1996:
    Tropical cyclone motion and surrounding flow relationships:
    Searching for beta gyres in omega dropwindsonde datasets. Monthly
    Weather Review, 124, 64-84.

    https://doi.org/10.1175/1520-0493(1996)124<0064:TCMASF>2.0.CO;2

"""

# ----

# pylint: disable=abstract-method
# pylint: disable=too-many-instance-attributes

# ----

import collections
from operator import itemgetter
from types import SimpleNamespace

import numpy
from confs.yaml_interface import YAML
from observation import Observation
from tools import parser_interface
from utils.decorator_interface import privatemethod
from utils.schema_interface import build_schema

from obsio.sonde.advect import advect, fallrate, interp_hsa, update_time
from obsio.sonde.hsa import (
    choparr,
    dateinfo,
    decode,
    layer_mean,
    locations,
    sfcpres,
    tempdrop,
    write_hsa,
)

# ----

# Define all available module properties
__all__ = ["TEMPDROP"]

# ----


class TEMPDROP(Observation):
    """
    Description
    -----------

    This is the base-class object for decoding TEMPDROP observation
    messages and providing user specified corrections; it is a
    sub-class of Observation.

    Keywords
    --------

    correct_drift: ``bool``, optional

        Correct the sonde observation locations relative to drift
        during descent; the observation time will also be corrected
        relative to the theoretical fallrate for the sonde.

    correct_time: ``bool``, optional

        Correct the sonde observation time relative to the theoretical
        fallrate for the sonde.

    """

    def __init__(
        self: Observation, correct_drift: bool = False, correct_time: bool = False
    ):
        """
        Description
        -----------

        Creates a new TEMPDROP object.

        """

        # Define the base-class attributes.
        super().__init__(obs_type="tempdrop")
        schema_path = self.obs_type_obj.schema
        parser_interface.enviro_set(envvar="TEMPDROP_READ_SCHEMA", value=schema_path)
        self.correct_drift = correct_drift
        self.correct_time = correct_time
        self.psfc_flag = 1070.0
        self.validlevs_list = ["manl", "sigl"]
        self.varname_list = ["hgt", "pres", "rh", "temp", "uwnd", "vwnd"]
        self.missing_data = -99.0
        self.cls_schema = build_schema(
            schema_def_dict=YAML().read_yaml(yaml_file=schema_path)
        )
        self.hsa_timestamp_frmt = "%y%m%d. %H%M"

    @privatemethod
    def drift(self: Observation, tempdrop_obj: SimpleNamespace) -> SimpleNamespace:
        """
        Description
        -----------

        This method computes the corrected geographical locations for
        the respective sonde observation relative to the sonde drift.

        Parameters
        ----------

        tempdrop_obj: ``SimpleNamespace``

            A Python SimpleNamespace object containing the TEMPDROP
            observation(s) attributes.

        Returns
        -------

        tempdrop_obj: ``SimpleNamespace``

            A Python SimpleNamespace object containing the TEMPDROP
            observations drift corrected geographical locations.

        """

        # Correct the respective sonde observation locations for the
        # respective sonde observation.
        msg = "Correcting the sonde locations due to drift."
        self.logger.info(msg=msg)
        tempdrop_obj = self.layers(tempdrop_obj=tempdrop_obj)
        tempdrop_obj.interp.heading = 90.0 + (
            numpy.degrees(
                numpy.arctan2(tempdrop_obj.interp.uwnd[:], tempdrop_obj.interp.vwnd[:])
            )
        )
        tempdrop_obj.interp.dist = (
            numpy.sqrt(
                tempdrop_obj.interp.uwnd[:] ** 2.0 + tempdrop_obj.interp.vwnd[:] ** 2.0
            )
        ) * tempdrop_obj.interp.fallrate[:]
        tempdrop_obj = advect(tempdrop_obj=tempdrop_obj)
        tempdrop_obj = update_time(tempdrop_obj=tempdrop_obj)

        return tempdrop_obj

    @privatemethod
    def layers(self: Observation, tempdrop_obj: SimpleNamespace) -> SimpleNamespace:
        """
        Description
        -----------

        This method computes the layer mean and the (theoretical)
        fallrate for the sonde.

        Parameters
        ----------

        tempdrop_obj: ``SimpleNamespace``

            A Python SimpleNamespace object containing the TEMPDROP
            observation(s) attributes.

        Returns
        -------

        tempdrop_obj: ``SimpleNamespace``

            A Python SimpleNamespace object containing the TEMPDROP
            observation(s) layer means and the (theoretical) fallrate
            for the sonde.

        """

        # Compute the TEMPDROP message layer means and sonde fallrate.
        tempdrop_obj.layer = parser_interface.object_define()
        psfc = tempdrop_obj.interp.psfc
        tempdrop_obj.layer.avgp = choparr(
            vararr=layer_mean(vararr=tempdrop_obj.interp.pres)
        )
        tempdrop_obj.layer.avgt = choparr(
            vararr=layer_mean(vararr=tempdrop_obj.interp.temp)
        )
        tempdrop_obj.layer.avgu = choparr(
            vararr=layer_mean(vararr=tempdrop_obj.interp.uwnd)
        )
        tempdrop_obj.layer.avgv = choparr(
            vararr=layer_mean(vararr=tempdrop_obj.interp.vwnd)
        )
        tempdrop_obj.interp.fallrate = interp_hsa(
            varin=fallrate(
                avgp=tempdrop_obj.layer.avgp, avgt=tempdrop_obj.layer.avgt, psfc=psfc
            ),
            zarr=tempdrop_obj.interp.pres,
        )

        return tempdrop_obj

    @privatemethod
    def frmtsonde(self: Observation, tempdrop_obj: SimpleNamespace) -> SimpleNamespace:
        """
        Description
        -----------

        This method collects the decoded TEMPDROP message attributes
        and builds a Python dictionary formatted accordingly for the
        HSA related applications.

        Parameters
        ----------

        tempdrop_obj: ``SimpleNamespace``

            A Python SimpleNamespace object containing the TEMPDROP
            message attributes.

        Returns
        -------

        tempdrop_obj: ``SimpleNamespace``

            A Python SimpleNamespace object containing the TEMPDROP
            message attributes formatted for the HSA related
            applications.

        """

        # Format the TEMPDROP message attributes for the HSA related
        # applications.
        frmtdict = {}
        for idx, obs in enumerate(tempdrop_obj.decode):
            obslist = list(obs.split())
            obsdict = collections.OrderedDict(
                {key: None for (key, _) in self.cls_schema.items()}
            )
            for jdx, item in enumerate(obsdict):
                obsdict[item] = obslist[jdx]
            obsdict = parser_interface.dict_formatter(in_dict=obsdict)
            frmtdict[idx] = {
                key: numpy.nan if value == self.missing_data else value
                for (key, value) in obsdict.items()
            }
        tempdrop_obj.frmtsonde = frmtdict

        return tempdrop_obj

    @privatemethod
    def interpsonde(
        self: Observation, tempdrop_obj: SimpleNamespace
    ) -> SimpleNamespace:
        """
        Description
        -----------

        This method interpolates to define any missing values within
        the formatted TEMPDROP observation.

        Parameters
        ----------

        tempdrop_obj: ``SimpleNamespace``

            A Python SimpleNamespace containing the TEMPDROP
            observation(s) attributes.

        Returns
        -------

        tempdrop_obj: ``SimpleNamespace``

            A Python SimpleNamespace object containing the
            interpolated formatted TEMPDROP observations.

        """

        # Interpolate to define any missing formatted TEMPDROP
        # observations.
        tempdrop_obj.interp = parser_interface.object_define()
        msg = "Interpolating decoded TEMPDROP observations."
        self.logger.info(msg=msg)
        interp_obj = parser_interface.object_define()
        varname_list = self.varname_list[:]
        varname_list.append("flag")
        for varname in varname_list:
            interp_obj = parser_interface.object_setattr(
                object_in=interp_obj,
                key=varname,
                value=[
                    tempdrop_obj.frmtsonde[idx][varname]
                    for idx in range(len(tempdrop_obj.frmtsonde))
                ],
            )
        idx_list = [
            idx
            for idx in range(len(interp_obj.pres))
            if (interp_obj.pres[idx]) < self.psfc_flag
            and (interp_obj.flag[idx].lower() in self.validlevs_list)
        ]
        pres = list(itemgetter(*idx_list)(interp_obj.pres))
        tempdrop_obj.interp.flag = list(itemgetter(*idx_list)(interp_obj.flag))
        tempdrop_obj.interp.hgt = interp_hsa(
            varin=list(itemgetter(*idx_list)(interp_obj.hgt)), zarr=pres
        )
        tempdrop_obj.interp.rh = interp_hsa(
            varin=list(itemgetter(*idx_list)(interp_obj.rh)), zarr=pres
        )
        tempdrop_obj.interp.temp = interp_hsa(
            varin=list(itemgetter(*idx_list)(interp_obj.temp)), zarr=pres
        )
        tempdrop_obj.interp.uwnd = interp_hsa(
            varin=list(itemgetter(*idx_list)(interp_obj.uwnd)), zarr=pres
        )
        tempdrop_obj.interp.vwnd = interp_hsa(
            varin=list(itemgetter(*idx_list)(interp_obj.vwnd)), zarr=pres
        )
        tempdrop_obj.interp.pres = interp_hsa(
            varin=list(itemgetter(*idx_list)(interp_obj.pres)), zarr=pres
        )
        tempdrop_obj.interp.psfc = numpy.array(
            sfcpres(interp_obj=interp_obj, psfc_flag=self.psfc_flag)
        )

        return tempdrop_obj

    def run(self: Observation, filepath: str) -> SimpleNamespace:
        """
        Description
        -----------

        This method performs the following tasks:

        (1) Decodes the TEMPDROP message and converts to HSA format.

        (2) Interpolates the HSA formatted observations to estimate
            all missing observation values.

        (3) Optionally computes the sonde position corrections
            relative to sonde drift; note that the HSA formatted
            observation time is also updated if the drift correction
            is computed.

        (4) Optionally updates the HSA formatted observation time
            using the theoretical fallrate for the sonde.

        """

        # Decode and compute the sonde observation attributes.
        tempdrop_obj = parser_interface.object_define()
        tempdrop_obj.filepath = filepath
        tempdrop_obj = tempdrop(tempdrop_obj=tempdrop_obj)
        tempdrop_obj = dateinfo(tempdrop_obj=tempdrop_obj)
        tempdrop_obj = locations(tempdrop_obj=tempdrop_obj)
        tempdrop_obj = decode(tempdrop_obj=tempdrop_obj)
        tempdrop_obj = self.frmtsonde(tempdrop_obj=tempdrop_obj)
        tempdrop_obj = self.interpsonde(tempdrop_obj=tempdrop_obj)
        if self.correct_drift:
            tempdrop_obj = self.drift(tempdrop_obj=tempdrop_obj)
        if self.correct_time:
            tempdrop_obj = update_time(tempdrop_obj=tempdrop_obj)
        write_hsa(tempdrop_obj=tempdrop_obj)

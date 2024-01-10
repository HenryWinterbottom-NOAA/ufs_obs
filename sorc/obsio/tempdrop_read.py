"""

"""

# ----

from types import SimpleNamespace
from typing import Dict, List, Tuple, Generic, Any, Union
import re
import os
import string
import time
from geopy.distance import distance, geodesic
from geopy.point import Point

from tools import datetime_interface, parser_interface, fileio_interface

from pydoc import locate
import numpy
from metpy.units import units
from utils.timestamp_interface import GLOBAL, GENERAL
from build_obs import build_obs
from diags.grids.bearing_geoloc import bearing_geoloc

from obsio.sonde.sondelib import drop, close_hsa
#from obsio.sonde.sonde import sonde_decode
from obsio.sonde.aoml import gsndfall2
from utils.decorator_interface import privatemethod
from observation import Observation
from utils.schema_interface import build_schema
from utils.table_interface import init_table, compose
from confs.yaml_interface import YAML
import collections
from operator import itemgetter

import statistics
import math
from scipy.interpolate import interp1d

# ----

# Define all available module properties
__all__ = ["TEMPDROP"]

# ----

class TEMPDROP(Observation):
    """ """

    def __init__(self: Observation, correct_drift: bool = True, # TODO: For testing.
                 correct_time: bool = False):
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
        (self.iwx, self.iflag, self.psfc_flag) = (1, 1, 1070.0)
        self.validlevs_list = ["manl", "sigl"]
        self.varname_list = ["hgt", "pres", "rh", "temp", "uwnd", "vwnd"]
        self.missing_data = -99.
        self.cls_schema = build_schema(schema_def_dict=YAML().read_yaml(yaml_file=schema_path)
                                       )
        self.infostrs_list = ["rel", "spg", "spl"]

    @staticmethod
    def interp(varin: numpy.array, zarr: numpy.array, interp_type: str = "linear",
               fill_value: Any = "extrapolate") -> numpy.array:
        """
        Description
        -----------

        This method interpolates to find missing values within a
        TEMPDROP observation variable.

        Parameters
        ----------

        varin: ``numpy.array``

            A Python numpy.array variable containing the TEMPDROP
            observation variable.

        zarr: ``numpy.array``

            A Python numpy.array variable containing the isobaric
            levels for the respective TEMPDROP observation variable.

        Keywords
        --------

        interp_type: ``str``, optional

            A Python string specifying the `interpolation type
            <https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.interp1d.html>`_.

        fill_value: ``Any``, optional

            A Python variable of any type specifying how to address
            missing datum values; see `here
            <https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.interp1d.html>`_.

        Returns
        -------

        varout: ``numpy.array``

             A Python numpy.array variable containing the interpolated
             TEMPDROP observation variable.

        """

        # Interpolate to find any missing data values.
        varout = varin[:]
        idx_list = [item for item in numpy.where(~numpy.isnan(varin))[0]]
        if len(idx_list) <= 1:
            return varout
        var = [varin[idx] for idx in idx_list]
        lev = [zarr[idx] for idx in idx_list]
        interp = interp1d(lev[:], var[:], kind="linear", fill_value="extrapolate")
        varout = varin[:]
        for idx in [idx for idx in numpy.where(numpy.isnan(varin))[0]]:
            varout[idx] = float(interp(zarr[idx]))

        return varout

    @staticmethod
    def fallrate(avgp: numpy.array, avgt: numpy.array, psfc: float) -> numpy.array:
        """

        """

        flrtarr = numpy.zeros(len(avgp+1))
        for idx in range(len(avgp)):
            flrtarr[idx] = gsndfall2(pr=avgp[idx], te=avgt[idx], bad=True, sfcp=psfc,
                                     mbps=True)/100.0

        return flrtarr

    @staticmethod
    def layer_mean(vararr: numpy.array) -> numpy.array:
        """


        """

        lymnarr = numpy.empty(numpy.shape(vararr))
        for idx in range(len(vararr) - 1):
            pidx = (idx + 1)
            lymnarr[pidx] = statistics.mean([vararr[idx], vararr[pidx]])
        lymnarr = numpy.array(lymnarr)
            
        return lymnarr

    @staticmethod
    def update_timestamp(fallrate: numpy.array, avgp: numpy.array, cycle: str) -> List:
        """

        """

        timestamp_list = []
        dtime = 0.0
        for idx in range(len(avgp) - 1):
            pidx = (idx + 1)
            dpres = (avgp[idx] - avgp[pidx])
            dtime = dtime + (dpres/fallrate[idx])
            ptime = datetime_interface.datestrupdate(
                datestr=cycle, in_frmttyp=GLOBAL,
                out_frmttyp=GENERAL, offset_seconds=dtime)
            timestamp_list.append(ptime)

        return timestamp_list

    @privatemethod
    def advect(self, tempdrop_obj: SimpleNamespace) -> SimpleNamespace:
        """

        """

        xlat_list = [tempdrop_obj.locate.rel[0]]
        xlon_list = [tempdrop_obj.locate.rel[1]]
        (xlat, xlon) = tempdrop_obj.locate.rel
        for idx in range(len(tempdrop_obj.interp.dist[:])):
            (xlat, xlon) = bearing_geoloc(
                loc1=(xlat, xlon), dist=tempdrop_obj.interp.dist[idx], heading=
                tempdrop_obj.interp.heading[idx]
                )
            xlat_list.append(xlat)
            xlon_list.append(xlon)
            (xlat, xlon) = (xlat_list[-1], xlon_list[-1])
        tempdrop_obj = self.normalize(tempdrop_obj=tempdrop_obj, xlat_list=xlat_list,
                                      xlon_list=xlon_list)

        return tempdrop_obj

    @staticmethod
    def normalize(tempdrop_obj: SimpleNamespace, xlat_list: List, xlon_list: List) -> SimpleNamespace:
        """

        """
        
        norma_xlat = min(tempdrop_obj.locate.rel[0], tempdrop_obj.locate.spg[0])
        normb_xlat = max(tempdrop_obj.locate.rel[0], tempdrop_obj.locate.spg[0])
        norma_xlon = min(tempdrop_obj.locate.rel[1], tempdrop_obj.locate.spg[1])
        normb_xlon = max(tempdrop_obj.locate.rel[1], tempdrop_obj.locate.spg[1])

        tempdrop_obj.interp.lat = [norma_xlat + (xlat_list[idx] - min(xlat_list))*(normb_xlat - norma_xlat)/
                                   (max(xlat_list) - min(xlat_list)) for idx in range(len(xlat_list))]
        tempdrop_obj.interp.lon = [norma_xlon + (xlon_list[idx] - min(xlon_list))*(normb_xlon - norma_xlon)/
                                   (max(xlon_list) - min(xlon_list)) for idx in range(len(xlon_list))]

        return tempdrop_obj

    @staticmethod
    def write_hsa(tempdrop_obj: SimpleNamespace) -> None:
        """

        """

        format_string = "{:2d} {:7.1f} {:4d} {:7.3f} {:7.3f} {:7.1f} {:7.1f} {:7.1f} {:8.1f} {:6.1f} {:6.1f} {}"

        print(tempdrop_obj.interp)
        quit()
        
        for msg in tempdrop_obj.interp:
            print(msg.split())
        
        #print(tempdrop_obj.decode)
        
    @privatemethod
    def drift(self: Observation, tempdrop_obj: SimpleNamespace) -> SimpleNamespace:
        """
        """

        tempdrop_obj = self.correct(tempdrop_obj=tempdrop_obj)
        tempdrop_obj.interp.heading = \
            (numpy.degrees(numpy.arctan2(tempdrop_obj.interp.uwnd[:],
                                         tempdrop_obj.interp.vwnd[:])))
        tempdrop_obj.interp.dist = (numpy.sqrt(tempdrop_obj.interp.uwnd[:]**2.0 +
                                               tempdrop_obj.interp.vwnd[:]**2.0))* \
                                               tempdrop_obj.layer.fallrate[:]
        tempdrop_obj = self.advect(tempdrop_obj = tempdrop_obj)


        self.write_hsa(tempdrop_obj=tempdrop_obj)

        #format_string = "{:2d} {:7.1f} {:4d} {:7.3f} {:7.3f} {:7.1f} {:7.1f} {:7.1f} {:8.1f} {:6.1f} {:6.1f} {}"
        #for 
        #tempdrop_obj.drift = parser_interface.object_define()
        #print(tempdrop_obj.interp)
        #quit()
#        with open("test.out", "w", encoding="utf-8") as file:
#            file.write(format_string.format(tempdrop_obj))
                
            
        
        #xlat_list = [tempdrop_obj.locate.rel[0]]
        #xlon_list = [tempdrop_obj.locate.rel[1]]
        #(xlat, xlon) = tempdrop_obj.locate.rel
        #for idx in range(len(tempdrop_obj.layer.dist[:])):
        #    (xlat, xlon) = bearing_geoloc(
        #        loc1=(xlat, xlon), dist=tempdrop_obj.layer.dist[idx], heading=
        #        tempdrop_obj.layer.heading[idx]
        #        )
        #    xlat_list.append(xlat)
        #    xlon_list.append(xlon)
        #    (xlat, xlon) = (xlat_list[-1], xlon_list[-1])
        #tempdrop_obj = self.normalize(tempdrop_obj=tempdrop_obj, xlat_list=xlat_list,
        #                              xlon_list=xlon_list)
            
        return tempdrop_obj
        
    @privatemethod
    def correct(self: Observation, tempdrop_obj: SimpleNamespace) -> SimpleNamespace:
        """

        """

        tempdrop_obj.layer = parser_interface.object_define()
        (avgp_list, avgt_list, avgu_list, avgv_list, rate_list) = [[] for idx in range(5)]
        psfc = tempdrop_obj.interp.psfc
        tempdrop_obj.layer.avgp = self.layer_mean(vararr=tempdrop_obj.interp.pres)
        tempdrop_obj.layer.avgt = self.layer_mean(vararr=tempdrop_obj.interp.temp)
        tempdrop_obj.layer.avgu = self.layer_mean(vararr=tempdrop_obj.interp.uwnd)
        tempdrop_obj.layer.avgv = self.layer_mean(vararr=tempdrop_obj.interp.vwnd)
        tempdrop_obj.layer.fallrate = self.fallrate(avgp=tempdrop_obj.layer.avgp,
                                                    avgt=tempdrop_obj.layer.avgt,
                                                    psfc=psfc
                                                    )
        
        return tempdrop_obj
        

    @privatemethod
    def dateinfo(self: Observation, tempdrop_obj: SimpleNamespace) -> SimpleNamespace:
        """
        Description
        -----------

        This method collects the timestamp information from the
        respective observation file name.

        Parameters
        ----------

        tempdrop_obj: ``SimpleNamespace``

            A Python SimpleNamespace containing the TEMPDROP
            observation(s) attributes.

        Returns
        -------

        tempdrop_obj: ``SimpleNamespace``

            A Python SimpleNamespace object containing the observation
            timestamp information.

        Notes
        -----

        - The observation file path is assumed formatted as
          `%Y%m%d%H%M.[KNHC, KWBC, etc.,]`.

        """

        # Collect the timestamp information for the TEMPDROP
        # observation filename.
        datestr = os.path.basename(tempdrop_obj.filepath).split(".")[0]
        tempdrop_obj.dateinfo = datetime_interface.datestrcomps(
            datestr=datestr, frmttyp=GLOBAL)
        msg = f"Observation date information determined from TEMPDROP filepath {tempdrop_obj.filepath}."
        self.logger.info(msg=msg)

        return tempdrop_obj

    @privatemethod
    def decode(self: Observation, tempdrop_obj: SimpleNamespace) -> SimpleNamespace:
        """
        Description
        -----------

        This method decodes a TEMPDROP formatted observation into the
        corresponding HRD Spline Analysis (HSA) format.

        Parameters
        ----------

        tempdrop_obj: ``SimpleNamespace``

            A Python SimpleNamespace containing the TEMPDROP
            observation(s) attributes.

        Returns
        -------

        tempdrop_obj: ``SimpleNamespace``

            A Python SimpleNamespace containing the HSA-formatted
            decoded TEMPDROP observation(s).

        """
        
        # Decode the HSA formatted observation message.
        luidx = 99 
        ftninfile = os.path.join(os.getcwd(), "fort.12")
        ftnoutfile = os.path.join(os.getcwd(), f"fort.{luidx}")
        filelist = [ftninfile, ftnoutfile]
        fileio_interface.removefiles(filelist=filelist)
        for filename in filelist:
            if fileio_interface.fileexist:
                fileio_interface.removefiles(filelist=[filename])
                msg = f"Removing existing file {ftnoutfile}."
                self.logger.warn(msg=msg)
        fileio_interface.symlink(srcfile=tempdrop_obj.filepath, dstfile=ftninfile)
        fileio_interface.touch(path=ftnoutfile)
        iflags = [2] # TODO: Move this to constructor.
        for msgstr in tempdrop_obj.tempdrop:
            if "xx" in msgstr.lower():
                [drop(luidx,self.iwx, iflag, tempdrop_obj.dateinfo.year_short,
                      tempdrop_obj.dateinfo.month, tempdrop_obj.dateinfo.day, msgstr,
                      -9999.) for iflag in iflags]
        close_hsa(luidx)
        close_hsa(12)
        with open(ftnoutfile, "r", encoding="utf-8") as sondefile:
            tempdrop_obj.decode = sondefile.readlines()
        msg = "The HSA formatted decoded TEMPDROP observation(s) is(are):\n\n"
        for line in tempdrop_obj.decode:
            msg = msg + line
        self.logger.info(msg=msg)
        fileio_interface.removefiles(filelist=filelist)

        return tempdrop_obj

    @privatemethod
    def frmtsonde(self: Observation, tempdrop_obj: SimpleNamespace) -> SimpleNamespace:
        """

        """

        frmtdict = {}
        for (idx, obs) in enumerate(tempdrop_obj.decode):
            obslist = list(obs.split())
            obsdict = collections.OrderedDict({key: None for (key, _) in self.cls_schema.items()})
            for (jdx, item) in enumerate(obsdict):
                obsdict[item] = obslist[jdx]
            obsdict = parser_interface.dict_formatter(in_dict=obsdict)
            frmtdict[idx] = {key: numpy.nan if value == self.missing_data else \
                             value for (key, value) in obsdict.items()}
        tempdrop_obj.frmtsonde = frmtdict

        return tempdrop_obj

    @privatemethod
    def interpsonde(self: Observation, tempdrop_obj: SimpleNamespace) -> SimpleNamespace:
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
                object_in=interp_obj, key=varname,
                value=[tempdrop_obj.frmtsonde[idx][varname] for
                       idx in range(len(tempdrop_obj.frmtsonde))]
                )
        idx_list = [idx for idx in range(len(interp_obj.pres)) if \
                    (interp_obj.pres[idx]) < self.psfc_flag and (interp_obj.flag[idx].lower()
                                                         in self.validlevs_list)]
        pres = list(itemgetter(*idx_list)(interp_obj.pres))
        tempdrop_obj.interp.hgt = numpy.array(self.interp(varin=list(itemgetter(*idx_list)(interp_obj.hgt)),
                                                          zarr=pres)
                                              )
        tempdrop_obj.interp.rh = numpy.array(self.interp(varin=list(itemgetter(*idx_list)(interp_obj.rh)),
                                             zarr=pres)
                                             )
        tempdrop_obj.interp.temp = numpy.array(self.interp(varin=list(itemgetter(*idx_list)(interp_obj.temp)),
                                               zarr=pres)
                                               )
        tempdrop_obj.interp.uwnd = numpy.array(self.interp(varin=list(itemgetter(*idx_list)(interp_obj.uwnd)),
                                               zarr=pres)
                                               )
        tempdrop_obj.interp.vwnd = numpy.array(self.interp(varin=list(itemgetter(*idx_list)(interp_obj.vwnd)),
                                               zarr=pres)
                                               )
        tempdrop_obj.interp.pres = numpy.array(self.interp(varin=list(itemgetter(*idx_list)(interp_obj.pres)),
                                               zarr=pres)
                                               )
        tempdrop_obj.interp.psfc = numpy.array(self.sfcpres(interp_obj=interp_obj, psfc_flag = self.psfc_flag))

        return tempdrop_obj

    @privatemethod
    def locate(self: Observation, tempdrop_obj: SimpleNamespace) -> SimpleNamespace:
        """
        Description
        -----------

        This method parses the TEMPDROP message and collects the sonde
        release (REL) time and location and the splash (SPL or SPG)
        time and location.

        Parameters
        ----------

        tempdrop_obj: ``SimpleNamespace``

            A Python SimpleNamespace containing the TEMPDROP
            observation(s) attributes.

        Returns
        -------

        tempdrop_obj: ``SimpleNamespace``

            A Python SimpleNamespace object containing the release and
            splash locations for the TEMPDROP observations.

        """

        # Collect the release and splash location for the respective
        # sonde.
        tempdrop_obj.locate = parser_interface.object_define()
        obinfo_list = []
        for infostr in self.infostrs_list:
            for item in tempdrop_obj.tempdrop:
                if any(infostr in item.lower() for infostr in self.infostrs_list):   
                    obinfo_list.append(item.lower())
            obinfo_str = str(set(obinfo_list)).split()
            try:
                for (idx, element) in enumerate(obinfo_str):
                    if infostr.lower() in element:
                        break
                infostr_items = obinfo_str[idx+1:idx+3]
                (locstr, timestr) = (infostr_items[0], infostr_items[1])
                (lat, lon) = self.obslocation(locstr=locstr)
                tempdrop_obj.locate = parser_interface.object_setattr(
                    object_in=tempdrop_obj.locate, key=infostr, value=(lat, lon)
                )
            except (ValueError, IndexError):
                msg = f"TEMPDROP message string {infostr.upper()} could not be located."
                self.logger.warn(msg=msg)
                
        return tempdrop_obj

    @staticmethod
    def obslocation(locstr: str) -> Tuple[float, float]:
        """
        Description
        -----------

        This method reads a Python string containing the location
        information and parses to return the geographical location for
        the respective observation.

        Parameters
        ----------

        locstr: str

            A Python string containing the location information to be
            parsed.

        Returns
        -------

        lat: float

            A Python float value containing the latitude coordinate
            for the observation location.

        lon: float

            A Python float value containing the longitude coordinate
            for the observation location.
        

        """

        # Define and scale the observation locations accordingly.
        (lat_scale, lon_scale) = [1.0, 1.0]
        if "s" in locstr.lower():
            lat_scale = -1.0
        if "e" in locstr.lower():
            lon_scale = -1.0
        locstr = re.sub("[a-zA-Z]", " ", locstr)
        lat = lat_scale * float(locstr.split()[0])/100.0
        lon = lon_scale * float(locstr.split()[1])/100.0

        return (lat, lon)
        
    @staticmethod
    def sfcpres(interp_obj: SimpleNamespace, psfc_flag: float) -> float:
        """
        Description
        -----------

        This method defines the surface pressure relative to the
        TEMPDROP message; if the TEMPDROP message cannot be determined
        (i.e., the surface pressure flag cannot be found), numpy.nan
        will be returned.

        Parameters
        ----------

        psfc_flag: ``float``

            A Python float value specifying a surface observation;
            this is typically a pressure observation value of 1070.0.

        Returns
        -------

        psfc: ``float``

            A Python float value specifying the surface pressure from
            the TEMPDROP message; if the surface pressure cannot be
            identified from the respective TEMPDROP message,
            `numpy.nan` is returned.

        """

        # Determine the surface pressure from the TEMPDROP message.
        try:
            psfc_idx = [idx for idx in range(len(interp_obj.pres)) if interp_obj.pres[idx]
                        == psfc_flag][0]
            psfc = interp_obj.hgt[psfc_idx]
        except (ValueError, IndexError):
            psfc = numpy.nanmax(interp_obj.pres)

        return psfc
            
    @privatemethod
    def tempdrop(self: Observation, tempdrop_obj: SimpleNamespace) -> SimpleNamespace:
        """
        Description
        -----------

        This method collects the HRD Spline Analysis (HSA) formatted
        observation files. # TODO

        Parameters
        ----------

        tempdrop_obj: ``SimpleNamespace``

            A Python SimpleNamespace containing the TEMPDROP
            observation(s) attributes. 

        Returns
        -------

        tempdrop_obj: ``SimpleNamespace``

            A Python SimpleNamespace object updated to contain the
            TEMPDROP formatted observations.

        """

        # Collect the HSA formatted observation(s).
        with open(tempdrop_obj.filepath, "r", encoding="utf-8") as file:
            tempdrop_obj.tempdrop = file.read().split("\n")
        msg = "TEMPDROP formatted observation record is:\n\n"
        for line in tempdrop_obj.tempdrop:
            msg = msg + line + "\n"
        self.logger.info(msg=msg)
            
        return tempdrop_obj

    def run(self: Observation, filepath: str) -> SimpleNamespace:
        """

        """

        tempdrop_obj = parser_interface.object_define()
        tempdrop_obj.filepath = filepath
        tempdrop_obj = self.tempdrop(tempdrop_obj=tempdrop_obj)
        tempdrop_obj = self.locate(tempdrop_obj=tempdrop_obj)
        tempdrop_obj = self.dateinfo(tempdrop_obj=tempdrop_obj)
        tempdrop_obj = self.decode(tempdrop_obj=tempdrop_obj)
        tempdrop_obj = self.frmtsonde(tempdrop_obj=tempdrop_obj)
        tempdrop_obj = self.interpsonde(tempdrop_obj=tempdrop_obj)
        if self.correct_drift:
            tempdrop_obj = self.drift(tempdrop_obj=tempdrop_obj)


    
    

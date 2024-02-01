Example Usages
==============

The following are example usages of the supported API interfaces.

Creating ATCF Records from NHC Advisories
-----------------------------------------

An `Automated Tropical Cyclone Forecast (ATCF)
<https://www.emc.ncep.noaa.gov/mmb/data_processing/tcvitals_description.htm>`_
record can be created as follows. The respective attributes are
collected from the National Hurricane Center (NHC) advisory for `Otis (18E)
<https://www.nhc.noaa.gov/archive/2023/ep18/ep182023.fstadv.003.shtml?>`_. The
units for the respective attributes can be found using the schema
attributes `here <https://github.com/HenryWinterbottom-NOAA/ufs_obs/blob/develop/parm/schema/atcf_read.schema.yaml>`_
(note the ``type`` key).

.. code-block:: python

   # Load Python packages.
   from atcf import ATCF
   from tools import parser_interface

   # Define a Python SimpleNamespace object with ATCF record attributes.
   tcv_dict = {"tcv_center": "NHC", "vmax": numpy.int(numpy.round(18.0056)),
               "mslp": numpy.int(1004), "tcid": "18E", "event_name": "OTIS",
               "time_ymd": numpy.int(20231023), "time_hm": numpy.int(300),
               "lat": "111N", "lon": "973W", "ne34": numpy.int(60), "se34": numpy.int(60),
               "sw34": numpy.int(0), "nw34": numpy.int(0)}
   tcv_obj = parser_interface.object_define()
   tcv_obj = parser_interface.object_setattr(object_in=tcv_obj, key="18E", value=tcv_dict)

   # Write an ATCF formatted file from the NHC advisory observations.
   ATCF().write(tcv_obj=tcv_obj, atcf_filepath="18E.atcf")
   
The resulting ATCF record is as follows.

.. code-block:: shell

   NHC  18E OTIS      20231023 0300 111N 973W -99 -99 1004 -999 -999 18 -99 0060 0060 0000 0000 -999 -999 -999  -999 -999 -999 -999 X

In the above example, a Python dictionary, ``tcv_dict``, is defined
containing the attributes to populate the ATCF record. The Python
dictionary is then converted to a Python SimpleNamespace object,
subsequently used to build the ATCF record following the
Python dictionary attributes. Note the expected datatypes for each
attribute specified `here <https://www.emc.ncep.noaa.gov/mmb/data_processing/tcvitals_description.htm>`_.

Creating ATCF Records from CIMSS ADT Observations
-------------------------------------------------

The `Cooperative Institute for Meteorological Satellite Studies (CIMSS) <https://cimss.ssec.wisc.edu/>`_ provides Advanced Dvorak Technique (ADT)-derived `tropical cyclone (TC) position and intensity estimates <https://tropic.ssec.wisc.edu/misc/adt/info.html>`_. An example for TC 18E is provided `here <https://tropic.ssec.wisc.edu/real-time/adt/archive2023/18E-list.txt>`_ as well as below.

.. code-block:: shell

   ADT91 LIST 18E.ODT CKZ=YES
   =====    ADT-Version 9.1 =====
		               ----Intensity--- -Tno Values-- --------Tno/CI Rules-------- -Temperature-                    
		        Time         MSLP/Vmax   Fnl Adj Ini   Cnstrnt Wkng Rpd   ET   ST   Cntr   Mean   Scene  EstRMW   MW   Storm Location  Fix
		Date    (UTC)   CI  (CKZ)/(kts)  Tno Raw Raw    Limit  Flag Wkng Flag Flag Region  Cloud  Type    (km)  Score   Lat     Lon    Mthd    Sat   VZA  Comments
	     2023OCT22 154020  2.0 1008.0  30.0  2.0 2.0 2.0  NO LIMIT  OFF  OFF  OFF  OFF -50.80 -55.98  UNIFRM   N/A    N/A    9.92   96.70  FCST    GOES16 27.5 
	     2023OCT22 161020  2.1 1008.0  31.0  2.1 2.2 2.2  NO LIMIT  OFF  OFF  OFF  OFF -42.25 -52.36  CRVBND   N/A    N/A    9.94   96.71  FCST    GOES16 27.6 
	     2023OCT22 164020  2.1 1008.0  31.0  2.1 2.1 2.1  NO LIMIT  OFF  OFF  OFF  OFF -24.41 -47.92  CRVBND   N/A    N/A    9.95   96.71  FCST    GOES16 27.6 
	     2023OCT22 171020  2.1 1008.0  31.0  2.1 2.4 2.4  NO LIMIT  OFF  OFF  OFF  OFF -25.37 -45.85  CRVBND   N/A    N/A    9.97   96.72  FCST    GOES16 27.6 
	     2023OCT22 174020  2.2 1008.0  32.0  2.2 2.3 2.5  0.2T/hour OFF  OFF  OFF  OFF -49.79 -45.84  CRVBND   N/A    N/A    9.99   96.72  FCST    GOES16 27.6 
	     2023OCT22 182020  2.2 1008.0  32.0  2.2 2.5 2.5  NO LIMIT  OFF  OFF  OFF  OFF -49.25 -46.95  CRVBND   N/A    N/A   10.01   96.73  FCST    GOES16 27.6 
	     2023OCT22 184020  2.2 1008.0  32.0  2.2 2.5 2.5  NO LIMIT  OFF  OFF  OFF  OFF -48.12 -47.26  CRVBND   N/A    N/A   10.02   96.73  FCST    GOES16 27.6 
	     2023OCT22 191020  2.3 1008.0  33.0  2.3 2.4 2.4  NO LIMIT  OFF  OFF  OFF  OFF -43.34 -47.31  CRVBND   N/A    N/A   10.03   96.74  FCST    GOES16 27.6 
	     2023OCT22 194020  2.3 1008.0  33.0  2.3 2.3 2.1  0.2T/hour OFF  OFF  OFF  OFF -37.86 -46.27  CRVBND   N/A    N/A   10.05   96.75  FCST    GOES16 27.7 
	     2023OCT22 202020  2.3 1008.0  33.0  2.3 2.2 2.1  0.2T/hour OFF  OFF  OFF  OFF -41.45 -45.40  CRVBND   N/A    N/A   10.07   96.76  FCST    GOES16 27.7
	     2023OCT22 204020  2.3 1008.0  33.0  2.3 2.5 2.6  0.2T/hour OFF  OFF  OFF  OFF -49.79 -52.17  CRVBND   N/A    N/A   10.29   96.90  FCST    GOES16 27.9 
	     2023OCT22 211020  2.3 1008.0  33.0  2.3 2.2 2.2  NO LIMIT  OFF  OFF  OFF  OFF -44.72 -51.74  CRVBND   N/A    N/A   10.31   96.90  FCST    GOES16 27.9 
	     2023OCT22 215020  2.3 1008.0  33.0  2.3 2.3 2.1  0.2T/hour OFF  OFF  OFF  OFF -46.94 -49.59  CRVBND   N/A    N/A   10.33   96.91  FCST    GOES16 27.9 
	     2023OCT22 221020  2.3 1008.0  33.0  2.2 2.0 2.0  NO LIMIT   ON  OFF  OFF  OFF -44.86 -47.42  CRVBND   N/A    N/A   10.34   96.91  FCST    GOES16 28.0 
	     2023OCT22 224020  2.3 1008.0  33.0  2.3 2.7 2.7  NO LIMIT  OFF  OFF  OFF  OFF -38.36 -42.12  CRVBND   N/A   -2.2   10.36   96.92  FCST    GOES16 28.0 
	     2023OCT22 232020  2.3 1008.0  33.0  2.3 2.3 2.3  NO LIMIT  OFF  OFF  OFF  OFF -25.84 -35.89  CRVBND   N/A   -2.2   10.39   96.92  FCST    GOES16 28.0 
	     2023OCT22 235020  2.3 1008.0  33.0  2.3 2.3 2.3  NO LIMIT  OFF  OFF  OFF  OFF -10.27 -30.05  CRVBND   N/A   -2.2   10.41   96.93  FCST    GOES16 28.0 
	     2023OCT23 001020  2.3 1008.0  33.0  2.3 2.4 2.4  NO LIMIT  OFF  OFF  OFF  OFF  -4.92 -25.78  CRVBND   N/A   -2.2   10.42   96.93  FCST    GOES16 28.0 
	     2023OCT23 005020  2.3 1008.0  33.0  2.2 1.8 1.5  0.5T/hour  ON  OFF  OFF  OFF  -0.64 -18.30  SHEAR    N/A   -2.2   10.45   96.94  FCST    GOES16 28.0 
	     2023OCT23 011020  2.3 1008.0  33.0  2.1 1.8 1.5  0.5T/hour  ON  OFF  OFF  OFF   5.33 -14.66  SHEAR    N/A   -2.2   10.46   96.95  FCST    GOES16 28.1 
	     2023OCT23 014020  2.3 1008.0  33.0  2.0 1.7 1.5  0.5T/hour  ON  FLG  OFF  OFF   7.14  -9.78  SHEAR    N/A   -2.2   10.48   96.95  FCST    GOES16 28.1 
	     2023OCT23 021020  2.3 1008.0  33.0  1.9 1.6 1.5  0.5T/hour  ON  FLG  OFF  OFF   7.55  -6.72  SHEAR    N/A   -2.2   10.50   96.96  FCST    GOES16 28.1 
	     2023OCT23 024020  2.3 1008.0  33.0  1.9 2.1 2.1  NO LIMIT   ON  FLG  OFF  OFF  -2.85 -21.44  CRVBND   N/A   -2.2   11.08   97.30  FCST    GOES16 28.7 
	     2023OCT23 031020  2.3 1008.0  33.0  1.8 2.0 2.0  NO LIMIT   ON  FLG  OFF  OFF   4.84 -22.82  CRVBND   N/A   -2.2   11.11   97.30  FCST    GOES16 28.7 
	     2023OCT23 034020  2.3 1008.0  33.0  1.9 2.4 2.5  0.5T/hour  ON  FLG  OFF  OFF  12.38 -24.34  SHEAR    N/A   -2.2   11.14   97.30  FCST    GOES16 28.8 
	     2023OCT23 042020  2.3 1008.0  33.0  2.0 2.3 2.5  0.5T/hour  ON  OFF  OFF  OFF  10.66 -25.03  SHEAR    N/A   -2.2   11.19   97.31  FCST    GOES16 28.8 
	     2023OCT23 044020  2.3 1008.0  33.0  2.0 2.4 2.5  0.5T/hour  ON  OFF  OFF  OFF  15.41 -25.70  SHEAR    N/A   -2.2   11.21   97.31  FCST    GOES16 28.8 
	     2023OCT23 051020  2.3 1009.0  33.0  2.1 2.1 2.1  NO LIMIT   ON  OFF  OFF  OFF  -0.38 -27.19  CRVBND   N/A   -2.2   11.24   97.31  FCST    GOES16 28.8 
	     2023OCT23 054020  2.3 1009.0  33.0  2.2 2.1 2.1  NO LIMIT   ON  OFF  OFF  OFF  -7.77 -29.26  CRVBND   N/A   -2.2   11.28   97.32  FCST    GOES16 28.8 
	     2023OCT23 061020  2.3 1009.0  33.0  2.2 2.3 2.3  NO LIMIT   ON  OFF  OFF  OFF -24.81 -31.97  CRVBND   N/A   -2.2   11.31   97.32  FCST    GOES16 28.9 
	     2023OCT23 064020  2.3 1007.9  33.0  2.3 2.5 2.5  NO LIMIT  OFF  OFF  OFF  OFF -49.33 -35.09  CRVBND   N/A   -2.2   11.34   97.33  FCST    GOES16 28.9 
	     2023OCT23 071020  2.3 1007.9  33.0  2.3 2.5 2.5  NO LIMIT  OFF  OFF  OFF  OFF -58.79 -41.41  IRRCDO   N/A   -2.2   11.37   97.33  FCST    GOES16 28.9 
	     2023OCT23 075020  2.3 1007.9  33.0  2.3 2.5 2.5  NO LIMIT  OFF  OFF  OFF  OFF -60.68 -46.86  IRRCDO   N/A   -2.2   11.42   97.34  FCST    GOES16 28.9 
	     2023OCT23 081020  2.4 1007.3  34.0  2.4 2.6 2.7  0.7T/6hr  OFF  OFF  OFF  OFF -64.48 -48.68  IRRCDO   N/A   -2.2   11.44   97.35  FCST    GOES16 28.9 
	     2023OCT23 084020  2.4 1007.4  34.0  2.4 2.3 2.3  NO LIMIT  OFF  OFF  OFF  OFF -15.34 -41.67  CRVBND   N/A   -2.2   11.38   97.10  FCST    GOES16 28.7 
	     2023OCT23 091020  2.4 1007.3  34.0  2.4 2.3 2.3  NO LIMIT  OFF  OFF  OFF  OFF  -4.77 -44.72  CRVBND   N/A   -2.2   11.41   97.10  FCST    GOES16 28.7 
	     2023OCT23 094020  2.4 1007.3  34.0  2.4 2.1 2.1  NO LIMIT  OFF  OFF  OFF  OFF   2.66 -42.92  CRVBND   N/A   -2.2   11.45   97.11  FCST    GOES16 28.7 
	     2023OCT23 101020  2.4 1007.3  34.0  2.3 2.1 2.1  NO LIMIT   ON  OFF  OFF  OFF   0.86 -38.62  CRVBND   N/A   -2.2   11.49   97.11  FCST    GOES16 28.7 
	     2023OCT23 104020  2.4 1007.3  34.0  2.3 2.2 2.2  NO LIMIT   ON  OFF  OFF  OFF  -3.73 -32.82  CRVBND   N/A   -2.2   11.52   97.12  FCST    GOES16 28.8 
	     2023OCT23 113020  2.4 1007.3  34.0  2.2 2.2 2.2  NO LIMIT   ON  OFF  OFF  OFF  -3.65 -25.94  CRVBND   N/A   -2.2   11.59   97.14  FCST    GOES16 28.8 
	     2023OCT23 114020  2.4 1007.3  34.0  2.2 2.2 2.2  NO LIMIT   ON  OFF  OFF  OFF  -2.77 -24.95  CRVBND   N/A   -2.2   11.60   97.14  FCST    GOES16 28.8 
	     2023OCT23 121020  2.4 1007.2  34.0  2.2 2.5 2.5  NO LIMIT   ON  OFF  OFF  OFF   9.35 -21.37  SHEAR    N/A   -2.2   11.64   97.15  FCST    GOES16 28.8 
	     2023OCT23 125020  2.4 1007.2  34.0  2.2 2.3 2.3  NO LIMIT   ON  OFF  OFF  OFF  -0.27 -15.89  CRVBND   N/A   -4.1   11.69   97.17  FCST    GOES16 28.9 
	     2023OCT23 131020  2.4 1007.2  34.0  2.2 2.1 2.1  NO LIMIT   ON  OFF  OFF  OFF   0.65 -17.31  CRVBND   N/A   -4.1   11.72   97.18  FCST    GOES16 28.9 
	     2023OCT23 134020  2.4 1007.2  34.0  2.2 2.3 2.3  NO LIMIT   ON  OFF  OFF  OFF   2.16 -20.82  CRVBND   N/A   -4.1   11.76   97.19  FCST    GOES16 28.9 
	     2023OCT23 141020  2.4 1007.2  34.0  2.1 1.7 1.5  0.5T/hour  ON  OFF  OFF  OFF   1.30 -21.64  SHEAR    N/A   -4.1   11.80   97.20  FCST    GOES16 29.0 
	     2023OCT23 144020  2.4 1007.1  34.0  2.1 2.1 2.1  NO LIMIT   ON  OFF  OFF  OFF   4.84 -28.40  CRVBND   N/A   -4.1   11.97   97.49  FCST    GOES16 29.4 
	     2023OCT23 151020  2.4 1007.1  34.0  2.1 2.1 2.1  NO LIMIT   ON  OFF  OFF  OFF   4.39 -26.76  CRVBND   N/A   -4.1   12.01   97.50  FCST    GOES16 29.4 
	     2023OCT23 155020  2.3 1007.6  33.0  2.1 2.3 2.3  NO LIMIT   ON  OFF  OFF  OFF   2.31 -27.69  CRVBND   N/A   -4.1   12.07   97.52  FCST    GOES16 29.4 
	     2023OCT23 161020  2.3 1007.6  33.0  2.1 2.2 2.2  NO LIMIT   ON  OFF  OFF  OFF  -1.01 -27.38  CRVBND   N/A   -4.1   12.09   97.53  FCST    GOES16 29.5 
	     2023OCT23 164020  2.3 1007.6  33.0  2.1 2.3 2.3  NO LIMIT   ON  OFF  OFF  OFF  -4.53 -27.18  CRVBND   N/A   -4.1   12.13   97.55  FCST    GOES16 29.5 
	     2023OCT23 171020  2.2 1007.0  32.0  2.1 2.3 2.3  NO LIMIT   ON  OFF  OFF  OFF   3.69 -26.22  CRVBND   N/A   -4.1   12.17   97.56  FCST    GOES16 29.5 
	     2023OCT23 175020  2.2 1007.0  32.0  2.2 2.2 2.2  NO LIMIT  OFF  OFF  OFF  OFF -17.32 -27.51  CRVBND   N/A   -4.1   12.21   97.57  FCST    GOES16 29.6 
	     2023OCT23 181020  2.2 1007.0  32.0  2.2 2.0 2.0  NO LIMIT  OFF  OFF  OFF  OFF -13.71 -27.57  CRVBND   N/A   -4.1   12.24   97.58  FCST    GOES16 29.6 
	     2023OCT23 184020  2.2 1007.0  32.0  2.1 2.0 2.0  NO LIMIT   ON  OFF  OFF  OFF -11.23 -27.52  CRVBND   N/A   -4.1   12.27   97.59  FCST    GOES16 29.6 
	     2023OCT23 192020  2.2 1007.0  32.0  2.1 2.0 2.0  NO LIMIT   ON  OFF  OFF  OFF -17.96 -28.73  CRVBND   N/A   -4.1   12.31   97.61  FCST    GOES16 29.7 
	     2023OCT23 194020  2.2 1007.0  32.0  2.1 2.0 2.0  NO LIMIT   ON  OFF  OFF  OFF -15.92 -28.82  CRVBND   N/A   -5.0   12.33   97.61  FCST    GOES16 29.7 
	     2023OCT23 202020  2.2 1007.0  32.0  2.0 2.1 2.1  NO LIMIT   ON  OFF  OFF  OFF -17.78 -29.61  CRVBND   N/A   -5.0   12.37   97.63  FCST    GOES16 29.7 
	     2023OCT23 204020  2.2 1007.8  32.0  2.0 2.3 2.3  NO LIMIT   ON  OFF  OFF  OFF   2.56 -27.25  CRVBND   N/A   -5.0   12.79   97.45  ARCHER  GOES16 29.8 
	     2023OCT23 211020  2.2 1007.5  32.0  2.0 2.1 2.1  NO LIMIT   ON  OFF  OFF  OFF   3.41 -35.02  CRVBND   N/A   -5.0   13.47   97.41  ARCHER  GOES16 30.1 
	     2023OCT23 214020  2.2 1007.6  32.0  2.1 2.3 2.3  NO LIMIT   ON  OFF  OFF  OFF   4.77 -35.42  CRVBND   N/A   -5.0   13.18   97.62  FCST    GOES16 30.1 
	     2023OCT23 222020  2.2 1007.6  32.0  2.1 2.0 2.0  NO LIMIT   ON  OFF  OFF  OFF   2.45 -32.20  CRVBND   N/A   -5.0   13.25   97.64  FCST    GOES16 30.2 
	     2023OCT23 224020  2.2 1007.6  32.0  2.1 2.4 2.4  NO LIMIT   ON  OFF  OFF  OFF   0.24 -31.64  CRVBND   N/A   -2.6   13.28   97.65  FCST    GOES16 30.2 
	     2023OCT23 232020  2.2 1007.6  32.0  2.1 2.0 2.0  NO LIMIT   ON  OFF  OFF  OFF   4.04 -29.89  CRVBND   N/A   -2.6   13.33   97.68  FCST    GOES16 30.3 
	     2023OCT23 235020  2.2 1007.5  32.0  2.1 2.2 2.2  NO LIMIT   ON  OFF  OFF  OFF   1.48 -27.03  CRVBND   N/A   -2.6   13.37   97.69  FCST    GOES16 30.3 
	     2023OCT24 001020  2.2 1007.5  32.0  2.2 2.3 2.3  NO LIMIT  OFF  OFF  OFF  OFF  -1.12 -25.93  CRVBND   N/A   -2.6   13.39   97.70  FCST    GOES16 30.3 
	     2023OCT24 004020  2.2 1006.5  32.0  2.2 2.3 2.3  NO LIMIT  OFF  OFF  OFF  OFF  -2.85 -27.06  CRVBND   N/A   -2.6   13.43   97.72  FCST    GOES16 30.4 
	     2023OCT24 012020  2.2 1006.5  32.0  2.2 2.3 2.3  NO LIMIT  OFF  OFF  OFF  OFF  -7.05 -29.25  CRVBND   N/A   -2.6   13.47   97.74  FCST    GOES16 30.4 
	     2023OCT24 014020  2.2 1006.5  32.0  2.1 2.0 2.0  NO LIMIT   ON  OFF  OFF  OFF  -7.61 -29.06  CRVBND   N/A   -2.6   13.49   97.75  FCST    GOES16 30.4 
	     2023OCT24 022020  2.2 1006.5  32.0  2.1 2.0 2.0  NO LIMIT   ON  OFF  OFF  OFF  -7.45 -30.36  CRVBND   N/A   -2.6   13.52   97.77  FCST    GOES16 30.5 
	     2023OCT24 025020  2.2 1006.4  32.0  2.2 2.3 2.3  NO LIMIT  OFF  OFF  OFF  OFF -10.10 -34.13  CRVBND   N/A   -2.6   13.58   97.89  FCST    GOES16 30.6 
	     2023OCT24 032020  2.2 1006.4  32.0  2.1 2.1 2.1  NO LIMIT   ON  OFF  OFF  OFF -11.70 -35.15  CRVBND   N/A   -2.6   13.63   97.91  FCST    GOES16 30.7 
	     2023OCT24 034020  2.2 1006.4  32.0  2.1 2.3 2.3  NO LIMIT   ON  OFF  OFF  OFF -13.76 -35.31  CRVBND   N/A   -2.6   13.66   97.93  FCST    GOES16 30.7 
	     2023OCT24 042020  2.2 1006.4  32.0  2.1 2.4 2.4  NO LIMIT   ON  OFF  OFF  OFF -28.52 -38.77  CRVBND   N/A   -2.6   13.72   97.95  FCST    GOES16 30.8 
	     2023OCT24 045020  2.2 1006.3  32.0  2.2 2.6 2.7  0.5T/hour OFF  OFF  OFF  OFF -34.58 -42.24  CRVBND   N/A   -2.6   13.77   97.97  FCST    GOES16 30.8 
	     2023OCT24 052020  2.3 1005.8  33.0  2.3 2.5 2.5  NO LIMIT  OFF  OFF  OFF  OFF -65.01 -45.45  IRRCDO   N/A   -2.6   13.82   97.99  FCST    GOES16 30.9 
	     2023OCT24 054020  2.3 1005.7  33.0  2.2 1.7 1.6  0.5T/hour  ON  OFF  OFF  OFF -64.38 -47.93  UNIFRM   N/A   -2.6   13.85   98.01  FCST    GOES16 30.9 
	     2023OCT24 062020  2.3 1005.7  33.0  2.3 2.8 2.9  0.5T/hour OFF  OFF  OFF  OFF -61.55 -53.00  IRRCDO   N/A   -2.6   13.90   98.04  FCST    GOES16 31.0 
	     2023OCT24 064020  2.4 1005.1  34.0  2.4 2.7 3.1  0.5T/hour OFF  OFF  OFF  OFF -59.54 -54.60  IRRCDO   N/A   -2.6   13.93   98.05  FCST    GOES16 31.0 
	     2023OCT24 071020  2.4 1005.1  34.0  2.4 2.2 2.2  NO LIMIT  OFF  OFF  OFF  OFF -55.66 -54.51  UNIFRM   N/A   -2.6   13.98   98.07  FCST    GOES16 31.0 
	     2023OCT24 074020  2.4 1005.1  34.0  2.3 2.2 2.2  NO LIMIT   ON  OFF  OFF  OFF -48.72 -54.86  UNIFRM   N/A   -2.6   14.02   98.09  FCST    GOES16 31.1 
	     2023OCT24 082020  2.4 1005.1  34.0  2.4 2.4 2.7  MW Adjst  OFF  OFF  OFF  OFF -36.69 -53.79  CRVBND   N/A   -2.6   14.08   98.13  FCST    GOES16 31.1 MWinit=2.7/2.4/2.4
	     2023OCT24 085020  2.5 1004.4  35.0  2.5 2.5 2.7  MW Adjst  OFF  OFF  OFF  OFF -63.75 -62.64  UNIFRM   N/A   -2.6   14.18   98.49  FCST    GOES16 31.6 MWinit=2.7/2.5/2.5
	     2023OCT24 092020  2.6 1003.2  37.0  2.6 2.6 2.9  MW Adjst  OFF  OFF  OFF  OFF -69.34 -64.16  UNIFRM   N/A   -2.6   14.23   98.52  FCST    GOES16 31.6 MWinit=2.8/2.5/2.5
	     2023OCT24 095020  2.7 1002.0  39.0  2.7 2.7 3.0  MW Adjst  OFF  OFF  OFF  OFF -65.64 -64.65  UNIFRM   N/A   -2.6   14.28   98.55  FCST    GOES16 31.7 MWinit=2.8/2.5/2.5
	     2023OCT24 102020  2.8 1000.8  41.0  2.8 2.8 3.0  MW Adjst  OFF  OFF  OFF  OFF -70.64 -65.41  UNIFRM   N/A   -2.6   14.33   98.58  FCST    GOES16 31.7 MWinit=2.8/2.6/2.6
	     2023OCT24 105020  2.9  999.6  43.0  2.9 2.9 3.1  MW Adjst  OFF  OFF  OFF  OFF -69.34 -67.62  UNIFRM   N/A   -2.6   14.37   98.61  FCST    GOES16 31.8 MWinit=2.9/2.7/2.7
	     2023OCT24 112020  3.1  997.1  47.0  3.1 3.1 3.4  MW Adjst  OFF  OFF  OFF  OFF -73.13 -68.92  UNIFRM   N/A   -2.6   14.42   98.64  FCST    GOES16 31.8 MWinit=3.0/2.8/2.8
	     2023OCT24 115020  3.2  995.9  49.0  3.2 3.2 3.6  MW Adjst  OFF  OFF  OFF  OFF -71.74 -69.70  UNIFRM   N/A   -2.6   14.46   98.67  FCST    GOES16 31.9 MWinit=2.9/2.8/2.8
	     2023OCT24 122020  3.3  994.6  51.0  3.3 3.3 3.7  MW Adjst  OFF  OFF  OFF  OFF -70.64 -69.61  UNIFRM   N/A   -2.6   14.51   98.69  FCST    GOES16 31.9 MWinit=3.0/2.8/2.8
	     2023OCT24 124020  3.4  993.4  53.0  3.4 3.4 4.3  MW Adjst  OFF  OFF  OFF  OFF -64.38 -71.61  EMBC     N/A  -34.5   14.29   99.03  ARCHER  GOES16 32.1 MWinit=3.1/2.9/2.9
	     2023OCT24 131020  3.5  992.1  55.0  3.5 3.5 4.1  MW Adjst  OFF  OFF  OFF  OFF -63.86 -70.64  UNIFRM   N/A  -34.5   14.31   99.04  ARCHER  GOES16 32.2 MWinit=3.1/2.9/2.9
	     2023OCT24 134020  3.6  990.8  57.0  3.6 3.6 4.0  MW Adjst  OFF  OFF  OFF  OFF -67.73 -70.23  UNIFRM   N/A  -34.5   14.36   99.07  ARCHER  GOES16 32.2 MWinit=3.0/3.0/3.0
	     2023OCT24 141020  3.7  989.3  59.0  3.7 3.7 3.8  MW Adjst  OFF  OFF  OFF  OFF -70.40 -68.23  UNIFRM   N/A  -34.5   14.67   98.79  FCST    GOES16 32.1 MWinit=3.1/3.0/3.0
	     2023OCT24 145020  3.8  987.9  61.0  3.8 3.8 3.9  MW Adjst  OFF  OFF  OFF  OFF -70.40 -72.14  UNIFRM   N/A  -34.5   14.78   99.09  FCST    GOES16 32.5 MWinit=3.2/3.0/3.0
	     2023OCT24 151020  3.9  986.6  63.0  3.9 3.9 4.0  MW Adjst  OFF  OFF  OFF  OFF -65.97 -71.29  UNIFRM   N/A  -34.5   14.82   99.11  FCST    GOES16 32.5 MWinit=3.2/3.1/3.1
	     2023OCT24 154020  4.0  985.2  65.0  4.0 4.0 4.0  MW Adjst  OFF  OFF  OFF  OFF -53.71 -69.79  EMBC     N/A  -34.5   14.86   99.14  FCST    GOES16 32.6 MWinit=3.2/3.1/3.1
	     2023OCT24 161020  4.1  983.5  67.4  4.1 4.1 4.0  MW Adjst  OFF  OFF  OFF  OFF -39.50 -68.55  UNIFRM   N/A  -34.5   14.91   99.16  FCST    GOES16 32.6 MWinit=3.3/3.1/3.1
	     2023OCT24 165020  4.3  980.2  72.2  4.3 4.3 6.0  MW Adjst  OFF  OFF  OFF  OFF -15.43 -68.57  EYE    -99 IR -34.5   14.97   99.20  FCST    GOES16 32.7 MWinit=3.6/3.2/3.2
	     2023OCT24 171020  4.3  980.1  72.2  4.3 4.3 4.1  MW Adjst  OFF  OFF  OFF  OFF -57.07 -69.15  UNIFRM   N/A  -34.5   15.00   99.21  FCST    GOES16 32.7 MWinit=3.5/3.3/3.3
	     2023OCT24 174020  4.5  976.7  77.0  4.5 4.5 4.1  MW Adjst  OFF  OFF  OFF  OFF -63.24 -70.38  UNIFRM   N/A  -34.5   15.05   99.24  FCST    GOES16 32.8 MWinit=3.5/3.3/3.3
	     2023OCT24 182020  4.6  974.8  79.6  4.6 4.6 4.2  MW Adjst  OFF  OFF  OFF  OFF -47.90 -72.08  UNIFRM   N/A  -34.5   15.11   99.27  FCST    GOES16 32.8 MWinit=3.5/3.4/3.4
	     2023OCT24 184020  4.7  973.9  82.2  4.7 4.7 6.4  MW Adjst  OFF  OFF  OFF  OFF -25.89 -72.21  EYE    -99 IR -34.5   15.14   99.28  FCST    GOES16 32.9 MWinit=3.8/3.4/3.4
	     2023OCT24 191020  4.8  971.9  84.8  4.8 4.8 6.3  MW Adjst  OFF  OFF  OFF  OFF -37.92 -72.58  EYE    -99 IR -34.5   15.18   99.30  FCST    GOES16 32.9 MWinit=3.9/3.5/3.5
	     2023OCT24 194020  4.9  969.9  87.4  4.9 4.9 6.4  MW Adjst  OFF  OFF  OFF  OFF -33.13 -73.17  EYE    -99 IR -34.5   15.23   99.32  FCST    GOES16 33.0 MWinit=3.9/3.6/3.6
	     2023OCT24 201020  5.0  967.9  90.0  5.0 5.0 4.2  MW Adjst  OFF  OFF  OFF  OFF -57.97 -73.95  UNIFRM   N/A  -34.5   15.27   99.34  FCST    GOES16 33.0 MWinit=3.7/3.6/3.6
	     2023OCT24 204020  5.0  967.9  90.0  5.0 5.0 4.4  MW ON     OFF  OFF  OFF  OFF -66.40 -76.31  UNIFRM   N/A   80.5   15.26   99.48  FCST    GOES16 33.1 
	     2023OCT24 212020  5.0  967.9  90.0  5.0 5.0 4.4  MW ON     OFF  OFF  OFF  OFF -69.10 -77.53  EMBC     N/A   80.5   15.34   99.52  FCST    GOES16 33.2 
	     2023OCT24 214020  5.0  967.9  90.0  5.0 5.0 4.4  MW ON     OFF  OFF  OFF  OFF -67.96 -77.06  UNIFRM   N/A   80.5   15.27   99.48  ARCHER  GOES16 33.1 
	     2023OCT24 221020  5.0  967.8  90.0  5.0 5.0 5.0  MW ON     OFF  OFF  OFF  OFF -64.38 -77.31  UNIFRM   N/A   80.5   15.44   99.57  ARCHER  GOES16 33.3 
	     2023OCT24 224020  5.0  967.8  90.0  5.0 5.0 5.6  MW ON     OFF  OFF  OFF  OFF -52.08 -76.94  EMBC     N/A   66.0   15.55   99.76  ARCHER  GOES16 33.6 
	     2023OCT24 232020  5.0  967.8  90.0  5.0 5.0 7.0  MW ON     OFF  OFF  OFF  OFF -35.66 -76.45  EYE    -99 IR  66.0   15.59   99.78  ARCHER  GOES16 33.6 
	     2023OCT24 234020  5.0  967.8  90.0  5.0 5.0 7.0  MW ON     OFF  OFF  OFF  OFF -30.86 -76.36  EYE    -99 IR  66.0   15.57   99.53  ARCHER  GOES16 33.3 
	     2023OCT25 001020  5.0  965.7  90.0  5.0 5.5 7.0  MW AdjEnd OFF  OFF  OFF  OFF -42.05 -76.76  EYE    -99 IR  59.4   15.65   99.55  ARCHER  GOES16 33.4 
	     2023OCT25 004020  5.2  962.1  94.8  5.2 6.0 7.3  1.3T/6hr  OFF  OFF  OFF  OFF -17.44 -77.06  EYE/P  -99 IR  59.4   15.52   99.73  ARCHER  GOES16 33.5 
	     2023OCT25 011020  5.3  960.1  97.2  5.3 6.1 7.3  1.3T/6hr  OFF  OFF  OFF  OFF -39.82 -77.85  EYE    -99 IR  59.4   15.78   99.45  ARCHER  GOES16 33.4 
	     2023OCT25 014020  5.6  954.1 104.6  5.6 6.2 7.4  1.3T/6hr  OFF  OFF  OFF  OFF -35.24 -78.41  EYE    -99 IR  62.7   15.92   99.53  ARCHER  GOES16 33.6 
	     2023OCT25 021020  5.7  951.9 107.2  5.7 6.3 7.6  1.3T/6hr  OFF  OFF  OFF  OFF -22.52 -78.39  EYE    -99 IR  62.7   15.95   99.56  ARCHER  GOES16 33.6 
	     2023OCT25 024020  5.9  947.5 112.4  5.9 6.3 7.6  1.3T/6hr  OFF  OFF  OFF  OFF -16.55 -77.93  EYE    -99 IR  62.7   16.03   99.51  ARCHER  GOES16 33.6 
	     2023OCT25 031020  6.2  941.1 119.8  6.2 6.3 7.4  1.3T/6hr  OFF  OFF  OFF  OFF -22.42 -77.51  EYE    -99 IR  62.7   16.18   99.60  ARCHER  GOES16 33.8 
	     2023OCT25 034020  6.2  941.1 119.8  6.2 6.3 7.4  1.3T/6hr  OFF  OFF  OFF  OFF -18.47 -77.38  EYE    -99 IR  62.7   16.24   99.64  ARCHER  GOES16 33.8 
	     2023OCT25 041020  6.2  941.1 119.8  6.2 6.3 7.4  1.3T/6hr  OFF  OFF  OFF  OFF -16.37 -77.39  EYE    -99 IR  62.7   16.31   99.66  ARCHER  GOES16 33.9 
	     2023OCT25 044020  6.2  941.0 119.8  6.2 6.3 7.5  1.3T/6hr  OFF  OFF  OFF  OFF  -7.45 -77.15  EYE    -99 IR  62.7   16.40   99.70  ARCHER  GOES16 34.0 
	     2023OCT25 051020  6.3  938.9 122.2  6.3 6.3 7.2  1.3T/6hr  OFF  OFF  OFF  OFF -17.91 -76.46  EYE    -99 IR  62.7   16.47   99.75  ARCHER  GOES16 34.1 
	     2023OCT25 054020  6.3  938.9 122.2  6.3 6.3 6.7  1.3T/6hr  OFF  OFF  OFF  OFF -42.25 -74.68  EYE    -99 IR  62.7   16.59   99.79  ARCHER  GOES16 34.2 
	     2023OCT25 061020  6.3  938.8 122.2  6.3 6.3 6.4  1.3T/6hr  OFF  OFF  OFF  OFF -54.72 -73.62  EYE    -99 IR  62.7   16.70   99.86  ARCHER  GOES16 34.3 
	     2023OCT25 064020  6.3  939.8 122.2  6.3 6.5 6.7  1.3T/6hr  OFF  OFF  OFF  OFF -24.85 -73.42  EYE/P  -99 IR  62.7   16.77   99.94  ARCHER  GOES16 34.4 
	     2023OCT25 071020  0.0    0.0   0.0  0.0 0.0 0.0            N/A  N/A  N/A  OFF  99.50  99.50  LAND     N/A    N/A   16.89   99.96  ARCHER  GOES16 34.5 
	     2023OCT25 074020  0.0    0.0   0.0  0.0 0.0 0.0            N/A  N/A  N/A  OFF  99.50  99.50  LAND     N/A    N/A   17.00   99.98  ARCHER  GOES16 34.6 
	     2023OCT25 081020  0.0    0.0   0.0  0.0 0.0 0.0            N/A  N/A  N/A  OFF  99.50  99.50  LAND     N/A    N/A   17.39  100.11  ARCHER  GOES16 35.0 
	     2023OCT25 084020  0.0    0.0   0.0  0.0 0.0 0.0            N/A  N/A  N/A  OFF  99.50  99.50  LAND     N/A    N/A   17.49  100.31  ARCHER  GOES16 35.2 
	     2023OCT25 091020  0.0    0.0   0.0  0.0 0.0 0.0            N/A  N/A  N/A  OFF  99.50  99.50  LAND     N/A    N/A   17.58  100.23  ARCHER  GOES16 35.2 
	     2023OCT25 094020  0.0    0.0   0.0  0.0 0.0 0.0            N/A  N/A  N/A  OFF  99.50  99.50  LAND     N/A    N/A   17.58  100.26  ARCHER  GOES16 35.2 
	     2023OCT25 101020  0.0    0.0   0.0  0.0 0.0 0.0            N/A  N/A  N/A  OFF  99.50  99.50  LAND     N/A    N/A   17.64  100.37  ARCHER  GOES16 35.4 
	     2023OCT25 104020  0.0    0.0   0.0  0.0 0.0 0.0            N/A  N/A  N/A  OFF  99.50  99.50  LAND     N/A    N/A   17.74  100.46  ARCHER  GOES16 35.5 
	     2023OCT25 111020  0.0    0.0   0.0  0.0 0.0 0.0            N/A  N/A  N/A  OFF  99.50  99.50  LAND     N/A    N/A   17.81  100.49  ARCHER  GOES16 35.6 
	     2023OCT25 114020  0.0    0.0   0.0  0.0 0.0 0.0            N/A  N/A  N/A  OFF  99.50  99.50  LAND     N/A    N/A   17.98  100.43  ARCHER  GOES16 35.6 
	     2023OCT25 121020  0.0    0.0   0.0  0.0 0.0 0.0            N/A  N/A  N/A  OFF  99.50  99.50  LAND     N/A    N/A   18.15  100.64  ARCHER  GOES16 35.9 
	     2023OCT25 124020  0.0    0.0   0.0  0.0 0.0 0.0            N/A  N/A  N/A  OFF  99.50  99.50  LAND     N/A    N/A   18.26  100.20  ARCHER  GOES16 35.6 
	     2023OCT25 131020  0.0    0.0   0.0  0.0 0.0 0.0            N/A  N/A  N/A  OFF  99.50  99.50  LAND     N/A    N/A   17.74  100.31  FCST    GOES16 35.4 
	     2023OCT25 134020  0.0    0.0   0.0  0.0 0.0 0.0            N/A  N/A  N/A  OFF  99.50  99.50  LAND     N/A    N/A   17.79  100.33  FCST    GOES16 35.4 
	     2023OCT25 141020  0.0    0.0   0.0  0.0 0.0 0.0            N/A  N/A  N/A  OFF  99.50  99.50  LAND     N/A    N/A   17.84  100.35  FCST    GOES16 35.5 
	     2023OCT25 144020  0.0    0.0   0.0  0.0 0.0 0.0            N/A  N/A  N/A  OFF  99.50  99.50  LAND     N/A    N/A   17.90  100.38  FCST    GOES16 35.5 
	     2023OCT25 151020  0.0    0.0   0.0  0.0 0.0 0.0            N/A  N/A  N/A  OFF  99.50  99.50  LAND     N/A    N/A   18.22  100.61  FCST    GOES16 36.0 
	     2023OCT25 154020  0.0    0.0   0.0  0.0 0.0 0.0            N/A  N/A  N/A  OFF  99.50  99.50  LAND     N/A    N/A   18.29  100.64  FCST    GOES16 36.0 
	     2023OCT25 161020  0.0    0.0   0.0  0.0 0.0 0.0            N/A  N/A  N/A  OFF  99.50  99.50  LAND     N/A    N/A   18.36  100.67  FCST    GOES16 36.1 
	     2023OCT25 164020  0.0    0.0   0.0  0.0 0.0 0.0            N/A  N/A  N/A  OFF  99.50  99.50  LAND     N/A    N/A   18.42  100.70  FCST    GOES16 36.2 
	     2023OCT25 171020  0.0    0.0   0.0  0.0 0.0 0.0            N/A  N/A  N/A  OFF  99.50  99.50  LAND     N/A    N/A   18.49  100.73  FCST    GOES16 36.2 
	     2023OCT25 174020  0.0    0.0   0.0  0.0 0.0 0.0            N/A  N/A  N/A  OFF  99.50  99.50  LAND     N/A    N/A   18.56  100.76  FCST    GOES16 36.3 
	     2023OCT25 181020  0.0    0.0   0.0  0.0 0.0 0.0            N/A  N/A  N/A  OFF  99.50  99.50  LAND     N/A    N/A   18.62  100.79  FCST    GOES16 36.4 
	     2023OCT25 184020  0.0    0.0   0.0  0.0 0.0 0.0            N/A  N/A  N/A  OFF  99.50  99.50  LAND     N/A    N/A   18.69  100.82  FCST    GOES16 36.4 
	     2023OCT25 191020  0.0    0.0   0.0  0.0 0.0 0.0            N/A  N/A  N/A  OFF  99.50  99.50  LAND     N/A    N/A   18.76  100.85  FCST    GOES16 36.5 
	     2023OCT25 194020  0.0    0.0   0.0  0.0 0.0 0.0            N/A  N/A  N/A  OFF  99.50  99.50  LAND     N/A    N/A   18.82  100.88  FCST    GOES16 36.6 
	     2023OCT25 201020  0.0    0.0   0.0  0.0 0.0 0.0            N/A  N/A  N/A  OFF  99.50  99.50  LAND     N/A    N/A   18.89  100.91  FCST    GOES16 36.6 
	     Utilizing history file /home/misc/ADTV9.1/scripts/history/18E.ODT
	     Successfully completed listing

An example Python application to read a CIMSS ADT history file and
subsequently builds an ATCF formatted file is provided below. In the
following example, the ADT scene types `SHEAR`, `LAND`, and `UNIFRM`
are excluded. Further, any forecast type `FIX` methods are excluded.

.. code-block:: python

   # Load Python packages.
   from atcf import ATCF
   from obsio.cimss_adt_read import read_cimssadt_history

   # Define the CIMSS ADT archive file path.
   cimss_adt_file = "/path/to/18E-list.txt"

   # Build the Python object containing the relevant attributes.
   tcv_obj = read_cimssadt_history(filepath=cimss_adt_file, scene_exclude=[
       "SHEAR", "LAND", "UNIFRM"], fix_exclude="FCST", atcf_format=True)

   # Write an ATCF formatted file from the CIMSS observations.
   ATCF().write(tcv_obj=tcv_obj, atcf_filepath="cimss_adt.18E.atcf")

The resulting ATCF formatted records are then as follows.

.. code-block:: shell

   CIMSS ADT0000 NONAME    20231023 2040 127N 974E -99 -99 1008 -999 -999 16 -99 -999 -999 -999 -999 -999 -999 -999  -999 -999 -999 -999 X  
   CIMSS ADT0001 NONAME    20231023 2110 134N 974E -99 -99 1008 -999 -999 16 -99 -999 -999 -999 -999 -999 -999 -999  -999 -999 -999 -999 X  
   CIMSS ADT0002 NONAME    20231024 1240 142N 990E -99 -99 0993 -999 -999 27 -99 -999 -999 -999 -999 -999 -999 -999  -999 -999 -999 -999 X  
   CIMSS ADT0003 NONAME    20231024 2240 155N 997E -99 -99 0968 -999 -999 46 -99 -999 -999 -999 -999 -999 -999 -999  -999 -999 -999 -999 X  
   CIMSS ADT0004 NONAME    20231024 2320 155N 997E -99 -99 0968 -999 -999 46 -99 -999 -999 -999 -999 -999 -999 -999  -999 -999 -999 -999 X  
   CIMSS ADT0005 NONAME    20231024 2340 155N 995E -99 -99 0968 -999 -999 46 -99 -999 -999 -999 -999 -999 -999 -999  -999 -999 -999 -999 X  
   CIMSS ADT0006 NONAME    20231025 0010 156N 995E -99 -99 0966 -999 -999 46 -99 -999 -999 -999 -999 -999 -999 -999  -999 -999 -999 -999 X  
   CIMSS ADT0007 NONAME    20231025 0040 155N 997E -99 -99 0962 -999 -999 49 -99 -999 -999 -999 -999 -999 -999 -999  -999 -999 -999 -999 X  
   CIMSS ADT0008 NONAME    20231025 0110 157N 994E -99 -99 0960 -999 -999 50 -99 -999 -999 -999 -999 -999 -999 -999  -999 -999 -999 -999 X  
   CIMSS ADT0009 NONAME    20231025 0140 159N 995E -99 -99 0954 -999 -999 54 -99 -999 -999 -999 -999 -999 -999 -999  -999 -999 -999 -999 X  
   CIMSS ADT0010 NONAME    20231025 0210 159N 995E -99 -99 0952 -999 -999 55 -99 -999 -999 -999 -999 -999 -999 -999  -999 -999 -999 -999 X  
   CIMSS ADT0011 NONAME    20231025 0240 160N 995E -99 -99 0948 -999 -999 58 -99 -999 -999 -999 -999 -999 -999 -999  -999 -999 -999 -999 X  
   CIMSS ADT0012 NONAME    20231025 0310 161N 996E -99 -99 0941 -999 -999 62 -99 -999 -999 -999 -999 -999 -999 -999  -999 -999 -999 -999 X  
   CIMSS ADT0013 NONAME    20231025 0340 162N 996E -99 -99 0941 -999 -999 62 -99 -999 -999 -999 -999 -999 -999 -999  -999 -999 -999 -999 X  
   CIMSS ADT0014 NONAME    20231025 0410 163N 996E -99 -99 0941 -999 -999 62 -99 -999 -999 -999 -999 -999 -999 -999  -999 -999 -999 -999 X  
   CIMSS ADT0015 NONAME    20231025 0440 164N 997E -99 -99 0941 -999 -999 62 -99 -999 -999 -999 -999 -999 -999 -999  -999 -999 -999 -999 X  
   CIMSS ADT0016 NONAME    20231025 0510 164N 997E -99 -99 0939 -999 -999 63 -99 -999 -999 -999 -999 -999 -999 -999  -999 -999 -999 -999 X  
   CIMSS ADT0017 NONAME    20231025 0540 165N 997E -99 -99 0939 -999 -999 63 -99 -999 -999 -999 -999 -999 -999 -999  -999 -999 -999 -999 X  
   CIMSS ADT0018 NONAME    20231025 0610 167N 998E -99 -99 0939 -999 -999 63 -99 -999 -999 -999 -999 -999 -999 -999  -999 -999 -999 -999 X  
   CIMSS ADT0019 NONAME    20231025 0640 167N 999E -99 -99 0940 -999 -999 63 -99 -999 -999 -999 -999 -999 -999 -999  -999 -999 -999 -999 X    

TEMPDROP Message Observations
=============================

Decodes `TEMPDROP-formatted
<https://www.aoml.noaa.gov/hrd/format/tempdrop_format.html>`_
observation messages and generates Hurricane Research Division (HRD)
Spline Analysis (`HSA
<https://www.aoml.noaa.gov/hrd/format/hsa_format.html>`_) formatted
output.

Read and write Automated Tropical Cyclone Forecast (ATCF) formatted
observations.

.. currentmodule:: obsio.tempdrop_read
           
.. autofunction:: TEMPDROP

Once established, the base-class object ``run`` method can be used to
decode the respective TEMPDROP-formatted observation file to a
corresponding HSA-formatted observation file (see the TEMPDROP
examples).

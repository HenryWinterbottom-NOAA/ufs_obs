"""

"""

# ----


from astropy.constants import Rd, g0
from metpy.constants import standard_lapse_rate

def fallrate(avgp: float, avgt: float, sonde_mass: float = 0.430, sonde_cd: float = 0.63,
             sonde_area: float=0.9) -> float:
    """


    """

    rho = (avgp*100.0)/(Rd*(avgt + 273.16))
    rate = 

from astropy import *
import numpy as np
from astropy.time import Time

from astropy.coordinates import SkyCoord ,get_moon,get_sun # High-level coordinates
import astropy.units as u

data_raw = np.load('/beegfs/dampe/users/mmunozsa/anisotripy/maps_calc/ntuples_10_25_ani_gal_coord.npy',unpack=True)
DAMPE_Start=Time("2013-01-01",scale='utc')
Time_data=data_time=DAMPE_Start+data_raw[1]*u.second
dampe_coordinates=SkyCoord(data_raw[2]*u.deg,data_raw[3]*u.deg,frame='galactic')
dampe_event_ra_dec=dampe_coordinates.



 

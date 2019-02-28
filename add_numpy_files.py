import numpy as np
import math
import operator
import glob

file_path='../ntuples_10_25_ani_gal_coord_*'
txt=glob.glob(file_path)
#fermi_data=fits.open('../../Fermi_data/L1810250505202B3DCA7E90_PH06.fits')
for i,file  in enumerate (txt):
    if i==0:
        f=np.load(file)
        s=len(f)
    else:

        dummy=np.load(file)
        f=np.stack([f,dummy])

print(f.shape)

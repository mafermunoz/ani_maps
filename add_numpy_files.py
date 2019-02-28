import numpy as np
import math



file_path='../ntuples_10_25_ani_gal_coord_'
NJOBS=100

for i in range (NJOBS):
    if(i==0):
        f=np.load(file_path+str(i)+".npy")
    else:
        dummy=np.load(file_path+str(i)+".npy")
        f=np.concatenate((f,dummy),axis=1)
        print(f.shape)

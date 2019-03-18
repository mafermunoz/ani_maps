import numpy as np
import ROOT
from ROOT import TVector3

a=np.load("../ntuples_10_25_ani_sat_info.npy")
track_tetha=[]
track_phi=[]
for i in range (len(a[1])):
    t=TVector3(a[2][i][0],a[2][i][1],a[2][i][2])
    track_tetha.append(t.Theta())
    track_phi.append(t.Phi())
    if(i%1000==0):
        print i


track_info=np.stack((track_phi,track_tetha))
np.save("../ntuples_10_25_ani_track_info.npy",track_info)

import ROOT
from ROOT import TFile, TTree,TVector3,TMatrix,TChain
import astropy
import healpy
import numpy as np
#ROOT.gSystem.Load('libDmpEvent.so')
import sys
import os
import yaml
import glob
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import copy
import maps_functions.py

def main(file_name,NJOBS=100,job=0):
   # myTree=TChain("ani")
    f=TFile.Open(file_name)
    myTree=f.Get('ani')
    n_entries=myTree.GetEntries()
    ev_step=np.true_divide(n_entries,int(NJOBS))
    e_min=ev_step*int(job)
    e_max=ev_step+ev_step*int(job)
    print n_entries
    l=np.array([])
    b=np.array([])
    sat_pos=[]
    sat_vel=[]
    track_dir=[]
    time=[]

    for i,event in enumerate(myTree):
        if(i>=e_min and i<e_max):
            SatPosition=TVector3()
            SatVelocity=TVector3()
            StkTrackDirection=TVector3()
            ElectronDirection=TVector3()
            SatPosition,SatVelocity,StkTrackDirection=calc_track(event,SatPosition,SatVelocity,StkTrackDirection)
            sat_pos.append(SatPosition)
            sat_vel.append(SatVelocity)
            track_dir.append(StkTrackDirection)

            ElectronDirection=Orb2Equ_RM(SatPosition,SatVelocity,StkTrackDirection)
            ElectronDirection=Equ2Gal(ElectronDirection)
            ld,bd=get_l_b(ElectronDirection)
            l=np.append(l,ld)
            b=np.append(b,bd)
            time.append(event.sec)
        elif (i>=e_max):
            continue

    sat_info=np.stack((sat_pos,sat_vel,track_dir))
    np.save("sat_info_"+str(job)+".npy",sat_info)
    gal_coord=np.stack((l,n))
    np.save("gal_coord_"+str(job),gal_coord)


if __name__ == '__main__':

    main(sys.argv[1],sys.argv[2],sys.argv[3])

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
from maps_functions import *

def main(file_name,NJOBS=1000,job=0):
   # myTree=TChain("ani")
    f=TFile.Open(file_name)
    name_file=file_name.split("/")[-1].replace(".root","_")
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
    list_e=[]

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
            list_e.append(i)

            ElectronDirection=Orb2Equ_RM(SatPosition,SatVelocity,StkTrackDirection)
            ElectronDirection=Equ2Gal(ElectronDirection)
            ld,bd=get_l_b(ElectronDirection)
            l=np.append(l,ld)
            b=np.append(b,bd)
            time.append((event.sec)+(0.001*event.ms))
        elif (i>=e_max):
            continue

    sat_info=np.stack((list_e,sat_pos,sat_vel,track_dir))
    np.save("../"+name_file+"sat_info_"+str(job)+".npy",sat_info)
    gal_coord=np.stack((list_e,time,l,b))
    np.save("../"+name_file+"gal_coord_"+str(job)+".npy",gal_coord)


if __name__ == '__main__':

    main(sys.argv[1],sys.argv[2],sys.argv[3])

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


#def track_dir():

def deg2rad():
    return np.pi/180

def Orb2Equ_RM(r_sat,v_sat,r_t):
    r_Particle =-r_t
    T=TMatrix(3,3)
    z_sat=r_sat.Unit()
    y_sat=v_sat.Cross(r_sat).Unit()
    x_sat=y_sat.Cross(z_sat).Unit()
    T[0][0]=x_sat.X()
    T[1][0] = x_sat.Y()
    T[2][0] = x_sat.Z()
    T[0][1] = y_sat.X()
    T[1][1] = y_sat.Y()
    T[2][1] = y_sat.Z()
    T[0][2] = z_sat.X()
    T[1][2] = z_sat.Y()
    T[2][2] = z_sat.Z()
    return T*r_Particle

def Equ2Gal(fk5):
    T=TMatrix(3,3)
    T[0][0] = -0.054875539726
    T[0][1] = -0.873437108010
    T[0][2] = -0.483834985808
    T[1][0] =  0.494109453312
    T[1][1] = -0.444829589425
    T[1][2] =  0.746982251810
    T[2][0] = -0.867666135858
    T[2][1] = -0.198076386122
    T[2][2] =  0.455983795705
    return T*fk5


def calc_track(event,SatPosition,SatVelocity,StkTrackDirection):
    SatPosition.SetXYZ(event.satx,event.saty,event.satz)
    SatVelocity.SetXYZ(event.satvx,event.satvy,event.satvz)
    if(event.tt_IX !=-999):
        d0=TVector3(event.tt_IX,event.tt_IY,0)
        d1=TVector3(event.tt_IX+event.tt_SX,event.tt_IY+event.tt_SY,1)
        StkTrackDirection=d1-d0
    else:
        d0=TVector3(event.tbgo_IX,event.tbgo_IY,0)
        d1=TVector3(event.tbgo_IX+event.tbgo_SX,event.tbgo_IY+event.tbgo_SY,1)
        StkTrackDirection=d1-d0
    ##StkTrackDirection.SetMagThetaPhi(1.0,event.theta*deg2rad(),event.phi*deg2rad())
    return SatPosition,SatVelocity,StkTrackDirection


def create_map(NSIDE,glon,glat):
    data = {"L":glat, "B":glon}
    pixels=healpy.ang2pix(NSIDE, (np.radians(90)-np.radians(data['B'])), np.radians(data['L']))
    hitmap= np.zeros(healpy.nside2npix(NSIDE)) * healpy.UNSEEN
    pixels_binned=0
    pixels_binned =np.bincount(pixels)
    hitmap[:len(pixels_binned)] =  pixels_binned
    return hitmap

def get_l_b(e_r):
    ld=e_r.Phi()
    if(ld<0):
            ld=ld+2*np.pi
    bd=np.pi/2-e_r.Theta()
    return ld/deg2rad(),bd/deg2rad()

def plt_map(hitmap,name):
    cmap = plt.cm.jet
    cmap.set_under(color='White')
    fig, ax = plt.subplots(ncols=1,nrows=1,figsize=(30,18))
    healpy.mollview(hitmap,rot=(180), xsize=2000, coord = ["G",'E'], nest=False,fig=0,hold=True, cmap=cmap, norm='',title='DATA MAP')
    healpy.graticule(dpar=10,dmer=10,color='White')
    healpy.graticule(dpar=10,dmer=10,color='Black',coord =['G','E'])
    plt.title("DATA MAP",fontsize=36)
    fig.savefig(name)

def main(file_name,NMAPS=2,repeat=0):
   # myTree=TChain("ani")
    f=TFile.Open(file_name)
    myTree=f.Get('ani')
    n_entries=myTree.GetEntries()
    print n_entries
    l=np.array([])
    b=np.array([])
    sat_pos=[]
    sat_vel=[]
    track_dir=[]


    for event in myTree:
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
#    print(ld,bd)
    print(l.shape)
    hitmap=create_map(16,b,l)
    np.save('hitmap'+str(repeat),hitmap)
    plt_map(hitmap,"test_test"+str(repeat))
    n_maps=int(NMAPS)
    iso_hitmap=[[]for i in range (n_maps)]
    for i  in range (n_maps):
        print len(track_dir)
        dummy_track=copy.deepcopy(track_dir)
        l=np.array([])
        b=np.array([])
        for j,x in enumerate(sat_pos):
            pos=np.arange(0,len(dummy_track),1)
            if(len(pos)==0):
                rpos=0
            else:
                rpos=np.random.choice(pos)

            fake_edir=Orb2Equ_RM(sat_pos[j],sat_vel[j],dummy_track[rpos])
            del dummy_track[rpos]
            fake_edir=Equ2Gal(fake_edir)
            ld,bd=get_l_b(fake_edir)
            l=np.append(l,ld)
            b=np.append(b,bd)
        print(l.shape)
        iso_hitmap[i]=create_map(16,b,l)
        #plt_map(iso_hitmap[i],"test_fake"+str(i))

    np.save("test_fake"+str(repeat),iso_hitmap)

if __name__ == '__main__':

    main(sys.argv[1],sys.argv[2],sys.argv[3])

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

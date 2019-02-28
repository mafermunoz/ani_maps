import numpy as np
import math



file_path='../'
file_name='ntuples_10_25_ani_gal_coord'
file_name2='ntuples_10_25_ani_sat_info'
NJOBS=100
NMAPS=1000
for i in range (NJOBS):

    if(i==0):
        f=np.load(file_path+file_name+"_"+str(i+1)+".npy")
        d=np.load(file_path+file_name2+"_"+str(i+1)+".npy")
    else:
        dummy=np.load(file_path+file_name+"_"+str(i+1)+".npy")
        dummy2=np.load(file_path+file_name2+"_"+str(i+1)+".npy")
        f=np.concatenate((f,dummy),axis=1)
        d=np.concatenate((d,dummy2),axis=1)
        print(d.shape)

np.save(file_path+file_name,f)
np.save(file_path+file_name2,d)


random_map=[[]for i in range (NMAPS)]
pos=np.arange(0,len(d),1)
for i in range (NMAPS):
    random_map[i]=np.random.shuffle(pos)

np.save(file_path+"ntuples_10_25_shuffle_pos.npy",random_map)

#!/bin/bash

NJOBS=100
OUTPATH="/beegfs/dampe/users/mmunozsa/anisotripy/maps_calc/ntuples_10_25_ani_"
for i in {1..100}
do
    OUTF=$OUTPATH"gal_coord_$i.npy"
    if [ ! -f ${OUTF} ]; then
	echo $OUTF
	sbatch submit_calc_var.sh ${NJOBS} ${i}
    fi
done

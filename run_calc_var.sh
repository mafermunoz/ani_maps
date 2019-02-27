#!/bin/bash

NJOBS=1000
OUTPATH="/beegfs/dampe/users/mmunozsa/anisotripy/maps_calc/"
for i in {1..1000}
do
    OUTF=$OUTPATH"gal_coord_$i.npy"
    if [ ! -f ${OUTF} ]; then
	echo $OUTF
	sbatch submit_calc_var.sh ${NJOBS} ${i}
    fi
done

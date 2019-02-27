#!/bin/bash
#SBATCH --partition=rhel6-short
#SBATCH --ntasks=1
#SBATCH --mem=20G
#SBATCH --job-name=ntSelec


export HOME=/atlas/users/mmunozsa/

source /cvmfs/dampe.cern.ch/rhel6-64/etc/setup.sh
dampe_init > /dev/null



python create_real_map_info.py /beegfs/dampe/users/mmunozsa/anisotripy/ntuples_10_25_ani.root ${1}  ${2}

#!/bin/bash -l
# Standard output and error:
#SBATCH -o ./RFI_J1741+6526_out.%j
#SBATCH -e ./RFI_J1741+6526_err.%j
# Initial working directory:
#SBATCH -D ./
# Job Name:
#SBATCH -J RFI_J1741+6526
# Queue (Partition):
#SBATCH --partition=long.q
# Number of nodes and MPI tasks per node:
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=24
#
#SBATCH --mail-type=all
#SBATCH --mail-user=<tilemathan@mpifr.de>
#SBATCH --mem=30700
#
module load impi
module load sigproc
module load presto
module load mkl
module load intel
module load minuit
module load cfitsio
module load anaconda
module load git
module load gsl
module load imagemagick
# Run the program:
python -c 'import sys,os; sys.path.append("/u/mscruces/processing/pipeline/");from RFImit_birdies import *;birdies=RFI_mitigation_FFT("J1741+6526",beams=[0,1,2,3,4,5,6],nbins=1,dir_folder="./",birdies_filename="birdies_J1741+6526")'

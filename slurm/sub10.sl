#!/bin/bash -e
#SBATCH --job-name=MakeDatasets    # job name (shows up in the queue)
#SBATCH --time=00:10:00            # Walltime (HH:MM:SS)
#SBATCH --mem=16000MB              # Memory
#SBATCH --output=R-%x.%j.out
#SBATCH --error=R-%x.%j.err
#SBATCH --mail-user=kvya817@aucklanduni.ac.nz
#SBATCH --mail-type=END,FAIL,TIME_LIMIT_80

source activate /home/kvya817/.conda/envs/ts
cd ..
python subject10.py

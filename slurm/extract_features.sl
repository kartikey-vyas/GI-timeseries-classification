#!/bin/bash -e
#SBATCH --job-name=FeatureExtractionArray    # job name (shows up in the queue)
#SBATCH --time=06:00:00                      # Walltime (HH:MM:SS)
#SBATCH --mem=16000MB                         # Memory
#SBATCH --array=0-59                         # Array jobs
#SBATCH --cpus-per-task=16
#SBATCH --output=R-%x.%j.out
#SBATCH --error=R-%x.%j.err
#SBATCH --mail-user=kvya817@aucklanduni.ac.nz
#SBATCH --mail-type=END,FAIL,TIME_LIMIT_80

source activate /home/kvya817/.conda/envs/ts
cd ..
python extract_features.py ach_at_hex_6000.h5 $SLURM_ARRAY_TASK_ID

#!/bin/bash -e
#SBATCH --job-name=FeatureSelection  # job name (shows up in the queue)
#SBATCH --time=00:30:00              # Walltime (HH:MM:SS)
#SBATCH --mem=4000MB                 # Memory

cd ..
source activate /home/kvya817/.conda/envs/ts
python select_features.py 0.05
python combine_features.py 0.05

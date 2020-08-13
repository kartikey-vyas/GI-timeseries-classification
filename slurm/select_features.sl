#!/bin/bash -e
#SBATCH --job-name=FeatureSelection  # job name (shows up in the queue)
#SBATCH --time=00:30:00              # Walltime (HH:MM:SS)
#SBATCH --mem=4000MB                 # Memory

cd ..
python select_features.py
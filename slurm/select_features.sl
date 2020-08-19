#!/bin/bash -e
#SBATCH --job-name=FeatureSelection  # job name (shows up in the queue)
#SBATCH --time=00:30:00              # Walltime (HH:MM:SS)
#SBATCH --mem=4000MB                 # Memory
#SBATCH --array=0.005,0.01,0.25,0.05,0.1    # Array jobs

cd ..
python select_features.py $SLURM_ARRAY_TASK_ID
python combine_features.py $SLURM_ARRAY_TASK_ID
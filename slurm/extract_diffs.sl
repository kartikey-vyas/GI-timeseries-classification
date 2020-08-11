#!/bin/bash -e
#SBATCH --job-name=FeatureExtractionArray    # job name (shows up in the queue)
#SBATCH --time=01:30:00                      # Walltime (HH:MM:SS)
#SBATCH --mem=16000MB                         # Memory
#SBATCH --array=22,31,39,14,57,47,9,60,52    # Array jobs

cd ..
python extract_features.py ach_at_full_6000.h5 $SLURM_ARRAY_TASK_ID -diffs
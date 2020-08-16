#!/bin/bash -e
#SBATCH --job-name=FeatureExtractionArray    # job name (shows up in the queue)
#SBATCH --time=00:15:00                      # Walltime (HH:MM:SS)
#SBATCH --mem=8000MB                         # Memory
#SBATCH --array=0-59                         # Array jobs


cd ..
python extract_features.py ach_at_full_6000.h5 $SLURM_ARRAY_TASK_ID

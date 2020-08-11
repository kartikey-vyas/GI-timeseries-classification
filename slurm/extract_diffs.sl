#!/bin/bash -e
#SBATCH --job-name=DiffsExtractionArray    # job name (shows up in the queue)
#SBATCH --time=01:30:00                      # Walltime (HH:MM:SS)
#SBATCH --mem=16000MB                         # Memory
#SBATCH --array=21,30,38,13,56,46,8,59,51    # Array jobs

cd ..
python extract_features.py ach_at_full_6000.h5 $SLURM_ARRAY_TASK_ID -diffs
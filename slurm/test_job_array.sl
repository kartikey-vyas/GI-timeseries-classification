#!/bin/bash -e
#SBATCH --job-name=FeatureExtractionArray    # job name (shows up in the queue)
#SBATCH --time=00:02:00                      # Walltime (HH:MM:SS)
#SBATCH --mem=5000MB                         # Memory
#SBATCH --array=1-10                         # Array jobs

cd ..
python simple_pipeline.py ach_at_full_6000.h5 $SLURM_ARRAY_TASK_ID
#!/bin/bash -e
#SBATCH --job-name=FeatureExtractionArray    # job name (shows up in the queue)
#SBATCH --time=00:15:00                      # Walltime (HH:MM:SS)
#SBATCH --mem=8000MB                         # Memory

cd ..
python extract_features.py ach_at_full_6000.h5 0
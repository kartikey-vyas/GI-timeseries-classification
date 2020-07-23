#!/bin/bash -e

#SBATCH --job-name    ExtractAchATDiffs
#SBATCH --time        02:00:00
#SBATCH --mem=20G
#SBATCH --cpus-per-task=4

cd ..
python save_diffs.py
python efficient_features.py ach_at_middle_diffs.h5 diffs
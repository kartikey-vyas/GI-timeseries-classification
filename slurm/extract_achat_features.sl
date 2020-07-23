#!/bin/bash -e

#SBATCH --job-name    ExtractAchATFeatures
#SBATCH --time        02:00:00
#SBATCH --mem=20G
#SBATCH --cpus-per-task=4

cd ..
python efficient_features.py ach_at_full.h5 full
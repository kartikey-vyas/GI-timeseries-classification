#!/bin/bash -e

#SBATCH --job-name    ExtractAchATFeatures
#SBATCH --time        01:00:00
#SBATCH --mem         2048MB

python full_feature_extraction.py
#!/bin/bash -e

#SBATCH --job-name    ExtractAchATFeatures
#SBATCH --time        00:20:00
#SBATCH --mem=20G
#SBATCH --cpus-per-task=2

python full_feature_extraction.py
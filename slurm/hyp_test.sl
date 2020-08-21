#!/bin/bash -e
#SBATCH --job-name=HypTest           # job name (shows up in the queue)
#SBATCH --time=01:00:00              # Walltime (HH:MM:SS)
#SBATCH --mem=8000MB                 # Memory

source activate /home/kvya817/.conda/envs/ts
cd ..
python hypothesis_tests.py

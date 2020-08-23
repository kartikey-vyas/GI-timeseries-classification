#!/bin/bash -e
#SBATCH --job-name=RandomSearch       # job name (shows up in the queue)
#SBATCH --time=03:00:00              # Walltime (HH:MM:SS)
#SBATCH --mem=8000MB                 # Memory
#SBATCH --cpus-per-task=12

source activate /home/kvya817/.conda/envs/ts
cd ..
python experiments.py

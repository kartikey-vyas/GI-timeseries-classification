#!/bin/bash -e
#SBATCH --job-name=GridSearch       # job name (shows up in the queue)
#SBATCH --time=20:00:00              # Walltime (HH:MM:SS)
#SBATCH --mem=16000MB                 # Memory
#SBATCH --cpus-per-task=18

source activate /home/kvya817/.conda/envs/ts
cd ..
python gridsearchCV.py

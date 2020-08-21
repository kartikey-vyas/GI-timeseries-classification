#!/bin/bash -e
#SBATCH --job-name=HypTest           # job name (shows up in the queue)
#SBATCH --time=00:30:00              # Walltime (HH:MM:SS)
#SBATCH --mem=4000MB                 # Memory

cd ..
python make_dataset.py data/raw/Ach-Hex ach_hex_full 6000

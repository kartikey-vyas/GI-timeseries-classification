#!/bin/bash -e
#SBATCH --job-name=MakeDatasets    # job name (shows up in the queue)
#SBATCH --time=00:30:00            # Walltime (HH:MM:SS)
#SBATCH --mem=16000MB              # Memory
#SBATCH --array=4000,6000          # Array jobs
#SBATCH --output=R-%x.%j.out
#SBATCH --error=R-%x.%j.err
#SBATCH --mail-user=kvya817@aucklanduni.ac.nz
#SBATCH --mail-type=END,FAIL,TIME_LIMIT_80

source activate /home/kvya817/.conda/envs/ts
cd ..
python make_dataset.py data/raw/Ach-AT-Hex ach-at-hex $SLURM_ARRAY_TASK_ID

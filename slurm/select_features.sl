#!/bin/bash -e
#SBATCH --job-name=TestSelection  # job name (shows up in the queue)
#SBATCH --time=06:00:00              # Walltime (HH:MM:SS)
#SBATCH --mem=12000MB                 # Memory
#SBATCH --array=4000,6000,10000       # Array jobs
#SBATCH --output=R-%x.%j.out
#SBATCH --error=R-%x.%j.err
#SBATCH --mail-user=kvya817@aucklanduni.ac.nz
#SBATCH --mail-type=END,FAIL,TIME_LIMIT_80

cd ..
source activate /home/kvya817/.conda/envs/ts
python feature_selection_test.py $SLURM_ARRAY_TASK_ID 4
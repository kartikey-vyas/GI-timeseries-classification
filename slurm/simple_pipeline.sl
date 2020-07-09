#!/bin/bash -e

#SBATCH --job-name    SimplePipeline
#SBATCH --time        00:01:00
#SBATCH --mem         1024MB

cd ..
python simple_pipeline.py

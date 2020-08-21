#!/bin/bash

# PUT THIS FILE IN THE DEFAULT DIRECTOTY IN MAHUIKA
echo Which job would you like to run?

read jobname

read -p "Confirm job: ${jobname}.sl (y/n): " answer
case ${answer:0:1} in
    y|Y )
        echo "Submitting job '${jobname}'"
    ;;
    * )
        exit
    ;;
esac

cd project/p4p

git fetch --all
git reset --hard origin/master

cd slurm
sbatch $jobname\.sl
sleep 8
sacct -X
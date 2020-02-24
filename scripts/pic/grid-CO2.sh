#!/bin/bash
#SBATCH -A ceds
#SBATCH -t 10:00:00
#SBATCH -N 2
#SBATCH -p shared

#SBATCH --mail-user matthew.nicholson@pnnl.gov
#SBATCH --mail-type END

#Set up your environment you wish to run in with module commands.
module purge
module load R/3.3.3

#Actually codes starts here
now=$(date)
echo "Current time : $now"

cd /pic/projects/GCAM/mnichol/ceds/worktrees/CEDS-frozen-em
make CO2-gridded

now=$(date)
echo "Current time : $now"


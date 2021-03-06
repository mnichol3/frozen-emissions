#!/bin/bash
#SBATCH -A ceds
#SBATCH -t 10:00:00
#SBATCH -N 1
#SBATCH -p shared
#SBATCH --mail-user YOUR_EMAIL_HERE
#SBATCH --mail-type END

#Set up your environment you wish to run in with module commands.
module purge
module load R/3.3.3

now=$(date)
echo "Current time : $now"

# Change this path to the path of your CEDS project root.
cd /pic/projects/GCAM/mnichol/ceds/worktrees/CEDS-frozen-em

# --- BC ---
Rscript code/module-G/G2.1.chunk_bulk_emissions.R BC --nosave --no-restore
Rscript code/module-G/G2.4.chunk_solidbiofuel_emissions.R BC --nosave --no-restore

# --- CO ---
Rscript code/module-G/G2.1.chunk_bulk_emissions.R CO --nosave --no-restore
Rscript code/module-G/G2.4.chunk_solidbiofuel_emissions.R CO --nosave --no-restore

# --- CO2 ---
Rscript code/module-G/G2.1.chunk_bulk_emissions.R CO2 --nosave --no-restore
Rscript code/module-G/G2.4.chunk_solidbiofuel_emissions.R CO2 --nosave --no-restore

# --- NH3 ---
Rscript code/module-G/G2.1.chunk_bulk_emissions.R NH3 --nosave --no-restore
Rscript code/module-G/G2.4.chunk_solidbiofuel_emissions.R NH3 --nosave --no-restore

# --- NMVOC ---
Rscript code/module-G/G2.1.chunk_bulk_emissions.R NMVOC --nosave --no-restore
Rscript code/module-G/G2.4.chunk_solidbiofuel_emissions.R NMVOC --nosave --no-restore

# --- NOx ---
Rscript code/module-G/G2.1.chunk_bulk_emissions.R NOx --nosave --no-restore
Rscript code/module-G/G2.4.chunk_solidbiofuel_emissions.R NOx --nosave --no-restore

# --- OC ---
Rscript code/module-G/G2.1.chunk_bulk_emissions.R OC --nosave --no-restore
Rscript code/module-G/G2.4.chunk_solidbiofuel_emissions.R OC --nosave --no-restore

# --- SO2 ---
Rscript code/module-G/G2.1.chunk_bulk_emissions.R SO2 --nosave --no-restore
Rscript code/module-G/G2.4.chunk_solidbiofuel_emissions.R SO2 --nosave --no-restore

now=$(date)
echo "Current time : $now"

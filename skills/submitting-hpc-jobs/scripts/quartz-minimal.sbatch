#!/bin/bash
# Minimal Quartz batch job. Directives follow the serial-job example in
# KB0023298 "Use Slurm to submit and manage jobs on IU's research computing
# systems", verified 2026-10-01.
#
# Replace SLURM_ACCOUNT with the Slurm Account Name from RT Projects.
# Submit with:  sbatch quartz-minimal.sbatch

#SBATCH -J hello-quartz
#SBATCH -p general
#SBATCH -A SLURM_ACCOUNT
#SBATCH -o hello-quartz_%j.txt
#SBATCH -e hello-quartz_%j.err
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --time=00:10:00

# Load what the program needs. "module spider <name>" finds a module.
module load python

# Run on scratch, not in the home directory.
cd "/N/scratch/${USER}" || exit 1

srun hostname
srun python3 -c 'import platform; print(platform.python_version())'

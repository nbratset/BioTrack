#!/bin/bash 
#SBATCH --job-name=nextflow_run # Job name
#SBATCH --mail-type=ALL # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=natalie.bratset@colorado.edu # Where to send mail
#SBATCH --nodes=1 # Run on a single node
#SBATCH --ntasks=64
#SBATCH --partition long
#SBATCH --mem=500gb # Memory limit
#SBATCH --time=100:00:00 # Time limit hrs:min:sec
#SBATCH --output=/scratch/Shares/biotracker_csci6118/eofiles/area_run.%j.out # Standard output
#SBATCH --error=/scratch/Shares/biotracker_csci6118/eofiles/area_run.%j.err # Standard error log


dt=$(date '+%d/%m/%Y %H:%M:%S');
echo "$dt"


path_to_venv=$HOME/projects/CSCI6118/micromamba/envs/
source ~/.bashrc
# micromamba activate nextflow_env   <--- tried this and it didn't work
micromamba activate ${path_to_venv}nextflow_env

indir=/scratch/Shares/biotracker_csci6118/

echo $indir

# --- Execution ---
micromamba run -n nextflow_env nextflow help

# Below is what I want to run. For testing if it works, i was just doing the command above

# nextflow run nf-core/taxprofiler -r 1.1.0 -profile conda \
#   --input /scratch/Shares/biotracker_csci6118/samplesheet.csv \
#   --databases /scratch/Shares/biotracker_csci6118/database.csv \
#   --outdir /scratch/Shares/biotracker_csci6118/results \
#   --perform_shortread_qc \
#   --perform_shortread_hostremoval \
#   --hostremoval_reference /scratch/Shares/biotracker_csci6118/GCF_000819615.1_ViralProj14015_genomic.fna.gz \
#   --perform_runmerging \
#   --save_runmerged_reads \
#   --run_metaphlan


dt=$(date '+%d/%m/%Y %H:%M:%S');
echo "$dt"

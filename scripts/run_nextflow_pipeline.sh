#!/bin/bash 
#SBATCH --job-name=nextflow_test # Job name
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


# #turn on the virtual machine you are using if you are using one#
# export MAMBA_ROOT_PREFIX="./micromamba"
# source "${MAMBA_ROOT_PREFIX}/etc/profile.d/micromamba.sh"


# # path_to_venv=$HOME/projects/CSCI6118/
# micromamba activate nextflow_env
# micromamba activate ${path_to_venv}nextflow_env

#set paths to AREA and to files to load in
#path_to_area=$HOME/AREA/src/
#indir=/Shares/down/public/INLCUDE_2024/kallisto_20241030/selfannoated/
#commoncolumn=Participant
#rank_file=${indir}kallisto_200401lines_participants_normcounts.csv
#boolean_attribute_file=${indir}full_HP_binary_attribute.csv
#outdirname=$HOME/area_runs/AREA_2025/outdir/
#include_sample_file=${indir}include_participants_with_RNA_and_completeT21.csv
#include_rank_file_columns=${indir}include_rank_cols_chr21.csv
#include_boolean_file_columns=${indir}include_bool_cols_min_5_cT21_HP.csv
#outdirname_pre=${outdirname}T21_chr21_mincomobid5T21_HP_

indir=/scratch/Shares/biotracker_csci6118/

echo $indir

export MAMBA_ROOT_PREFIX="./micromamba"

# 2. Add the micromamba binary to your PATH if it's not already
#    (Based on your initial setup: export PATH=./bin:$PATH)
export PATH=./bin:$PATH

# --- Execution ---
# 3. Use 'micromamba run' to execute your command directly in the environment.
micromamba run -n nextflow_env nextflow help
# nextflow run nf-core/taxprofiler -r 1.1.0 -profile conda \
#   --input ${indir}samplesheet.csv \
#   --databases ${indir}database.csv \
#   --outdir ./results \
#   --perform_shortread_qc \
#   --perform_shortread_hostremoval \
#   --hostremoval_reference ${indir}GCF_000819615.1_ViralProj14015_genomic.fna.gz \
#   --perform_runmerging \
#   --save_runmerged_reads \
#   --run_metaphlan


dt=$(date '+%d/%m/%Y %H:%M:%S');
echo "$dt"

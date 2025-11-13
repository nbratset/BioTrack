#!/bin/bash 
#SBATCH --job-name=nextflow_metaphlan_1.2.4 # Job name
#SBATCH --mail-type=ALL # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=natalie.bratset@colorado.edu # Where to send mail
#SBATCH --nodes=1 # Run on a single node
#SBATCH --ntasks=64
#SBATCH --partition long
#SBATCH --mem=500gb # Memory limit
#SBATCH --time=200:00:00 # Time limit hrs:min:sec
#SBATCH --output=/scratch/Shares/biotracker_csci6118/eofiles/area_run.%j.out # Standard output
#SBATCH --error=/scratch/Shares/biotracker_csci6118/eofiles/area_run.%j.err # Standard error log


dt=$(date '+%d/%m/%Y %H:%M:%S');
echo "$dt"

# 1. Set up virtual python environment
module purge
module load openjdk/21.0.1

path_to_venv=/scratch/Shares/biotracker_csci6118/micromamba/envs/

source ~/.bashrc
micromamba activate ${path_to_venv}nextflow_env

indir=/scratch/Shares/biotracker_csci6118/
echo $indir

# 2. Create Metaphlan Database -- Run this if you need to 
METAPHLAN_DB_DIR="/scratch/Shares/biotracker_csci6118/metaphlan_db_v3"
mkdir -p $METAPHLAN_DB_DIR

# 3. Run the MetaPhlAn install command -- Un-comment if you need to install the Metaplan database
# echo "Starting MetaPhlAn database installation..."
# metaphlan --install --db_dir $METAPHLAN_DB_DIR
# echo "MetaPhlAn database installation complete."

# 4. --- Execution ---
nextflow run nf-core/taxprofiler -r 1.1.0 -resume \
  --input ${indir}samplesheet.csv \
  --databases ${indir}database.csv \
  --outdir ${indir}nextflow_results \
  --perform_shortread_qc \
  --perform_shortread_hostremoval \
  --hostremoval_reference ${indir}GCF_000819615.1_ViralProj14015_genomic.fna.gz \
  --perform_runmerging \
  --save_runmerged_reads \
  --run_metaphlan

dt=$(date '+%d/%m/%Y %H:%M:%S')
echo "$dt"

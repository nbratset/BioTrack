#!/bin/bash

#SBATCH --job-name=fastq_dl
#SBATCH --mem=16G
#SBATCH --array=1-339%8
#SBATCH --nodes=1
#SBATCH --ntasks=16
#SBATCH --time=24:00:00
#SBATCH -o run_download_fastqs_%A_%a.out
#SBATCH -e run_download_fastqs_%A_%a.err

module purge
source ~/miniconda3/etc/profile.d/conda.sh
conda activate aryafastq

ACCESSION_FILE="SRA5.txt"
SRA_DIR="sra_downloads"
FASTQ_DIR="PRJNA398089"
mkdir -p ${SRA_DIR} ${FASTQ_DIR}

ACCESSION=$(sed -n "${SLURM_ARRAY_TASK_ID}p" ${ACCESSION_FILE})
MAX_SIZE="100G"

echo "Downloading ${ACCESSION}..."
prefetch ${ACCESSION} \
    --output-directory ${SRA_DIR} \
    --max-size ${MAX_SIZE}

SRA_FILE="${SRA_DIR}/${ACCESSION}/${ACCESSION}.sra"
if [[ -f "${SRA_FILE}" ]]; then
    echo "Converting ${ACCESSION} to FASTQ..."
    fastq-dump --split-files --gzip --outdir ${FASTQ_DIR} ${SRA_FILE}

    if [[ $? -eq 0 ]]; then
        echo "FASTQ dump successful for ${ACCESSION}."
        echo "Cleaning up ${ACCESSION}..."
        rm -f ${SRA_FILE}
    else
        echo "fastq-dump failed for ${ACCESSION}"
    fi
else
    echo "Download failed for ${ACCESSION}"
fi

#!/bin/bash

# Load conda (adjust path if needed)
if [ -f ~/miniconda3/etc/profile.d/conda.sh ]; then
    source ~/miniconda3/etc/profile.d/conda.sh
elif [ -f /opt/anaconda3/etc/profile.d/conda.sh ]; then
    source /opt/anaconda3/etc/profile.d/conda.sh
else
    echo "Conda not found. Please install Miniconda or Anaconda."
    exit 1
fi

# Create the environment if it doesn't exist
if ! conda env list | grep -q "metaphlan_analysis"; then
    echo "Creating conda environment 'metaphlan_analysis'..."
    conda env create -f src/env.yml
fi

conda activate metaphlan_analysis
Rscript src/metaphlan_to_phyloseq.R
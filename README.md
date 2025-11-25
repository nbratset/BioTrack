###You can now easily assess your patient's microbiome data!

##Nextflow pipeline:

```

Insert instructions to take sequences and run the nextflow pipeline to create metaphlan output


```

##Metaphlan to phyloseq:

```

Insert instructions to take metaphlan output and create a phyloseq object which is merged with the reference phyloseq. 
This creates 3 outputs: merged otu table (abundances of each taxa), merged taxonomy table (phylogeny of each taxa), and merged metadata
This is based on a R script that takes YOUR patient metaphlan output and their metadata as arguments. It also takes the outputs you want to
create as arguments. 

To run it on your terminal:

Rscript src/metaphlan_to_phyloseq.R \
  input_data/SRR5946632_pe_mpa_v31_CHOCOPhlAn_201901.metaphlan_profile.txt \
  input_data/metadata.csv \
  input_data/tax.csv \
  input_data/otu.csv \
  input_data/combined_metadata.csv
  

This assumes you do everything from the base directory. 

```

##Microbiome analysis:

```
You now provide your output from the R script as input arguments to the analysis pipeline.

To run it on your terminal:

python src/run_pipeline.py \
    --location Netherlands \
    --otu_file input_data/otu.csv \
    --metadata_file input_data/combined_metadata.csv

Location is an optional argument, if you want to limit your analysis to a particular location. 
If not specificed, the analysis will run on the entire data set.

```





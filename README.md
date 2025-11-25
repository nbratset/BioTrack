###You can now easily assess your patient's microbiome data!

##Nextflow pipeline:

```

Insert instructions to take sequences and run the nextflow pipeline to create metaphlan output


```

##Metaphlan to phyloseq:

```

Insert instructions to take metaphlan output and create a phyloseq object which is merged with the reference phyloseq. 
This creates 3 outputs: merged otu table (abundances of each taxa), merged taxonomy table (phylogeny of each taxa), and merged metadata
This is based on a R script that takes YOUR patient metaphlan output and their metadata as arguments. To run it on your terminal:

Rscript src/metaphlan_to_phyloseq.R \
  input_data/SRR5946632_pe_mpa_v31_CHOCOPhlAn_201901.metaphlan_profile.txt \
  input_data/metadata.csv

This assumes you do everything from the base directory. 

```

##Beta diversity:

```
To run it on your terminal:

python main.py

```





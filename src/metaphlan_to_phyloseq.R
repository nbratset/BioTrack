#This script converts the metaphlan output to a phyloseq object, consisting of:
#1. otu_table: table with taxa as rows and samples as columns
#2. taxa_table: taxonomic assignment of all taxa present in the data
#3. metadata: sample data characteristica
#all combined into one data structure.

#install.packages("tidyverse")
library(tidyverse)
library(phyloseq)
library(ggplot2)
library(dplyr)

#Define a function that converts metaphlan output to a phyloseq object
metaphlanToPhyloseq <- function(tax, metadat=NULL, simplenames=TRUE, roundtointeger=FALSE, split="|") {
  xnames = rownames(tax)
  shortnames = gsub(paste0(".+\\", split), "", xnames)
  if(simplenames){
    rownames(tax) = shortnames
  }
  if(roundtointeger){
    tax = round(tax * 1e4)
  }
  x2 = strsplit(xnames, split=split, fixed=TRUE)
  taxmat = matrix(NA, ncol=max(sapply(x2, length)), nrow=length(x2))
  colnames(taxmat) = c("Kingdom", "Phylum", "Class", "Order", "Family", "Genus", "Species", "Strain")[1:ncol(taxmat)]
  rownames(taxmat) = rownames(tax)
  for (i in 1:nrow(taxmat)){
    taxmat[i, 1:length(x2[[i]])] <- x2[[i]]
  }
  taxmat = gsub("[a-z]__", "", taxmat)
  taxmat = phyloseq::tax_table(taxmat)
  otutab = phyloseq::otu_table(tax, taxa_are_rows=TRUE)
  if(is.null(metadat)){
    res = phyloseq::phyloseq(taxmat, otutab)
  }else{
    res = phyloseq::phyloseq(taxmat, otutab, phyloseq::sample_data(metadat))
  }
  return(res)
}

#Implement the function on metaphlan output
data <- read.delim("input_data/metaphlan_output.txt",header = F)
colnames(data) <- data[2,] #second row has sample names always (necessary case for a magic number!)
data <- data %>% dplyr::slice(c(3:nrow(data)))
head(data[1:4,1:4]) #check the structure is okay
dim(data)
row.names(data) <- data$clade_name
head(row.names(data)) 
data <- data[grepl("s__", data$clade_name),]
data$clade_name <- c() 
data$NCBI_tax_id <- c() 
data2 <- mutate_all(data, function(x) as.numeric(as.character(x)))
phyloseqin= metaphlanToPhyloseq(data2)
phyloseqin
otu <- as.data.frame(otu_table(phyloseqin))
colnames(otu) <- sub("_.*", "", colnames(otu))
otu <- as.matrix(t(otu))
metadata <- read.csv("input_data/metadata.csv",header=T)
rownames(metadata) <- metadata$Sample
phyloseqin <- merge_phyloseq(otu_table(otu, taxa_are_rows = FALSE),tax_table(phyloseqin),sample_data(metadata))
phyloseqin

#Sanity check and save phyloseq
otu <- as.data.frame(otu_table(phyloseqin)) 
tax <- as.data.frame(tax_table(phyloseqin))
sampledf <- as.data.frame(sample_data(phyloseqin))
saveRDS(phyloseqin,"input_data/ps.cln.rds")
write.csv(tax,"input_data/tax.csv")
write.csv(otu,"input_data/otu.csv")

#This script converts the metaphlan output to a phyloseq object, consisting of:
#1. otu_table: table with taxa as rows and samples as columns
#2. taxa_table: taxonomic assignment of all taxa present in the data
#3. metadata: sample data characteristics
#all combined into one data structure.

#install.packages("tidyverse")
library(tidyverse)
library(phyloseq)
library(ggplot2)
library(dplyr)
library(openxlsx)

#Path to metaphlan output and metadata can be passed as arguments
args <- commandArgs(trailingOnly = TRUE)

#Error handling: Stop if two inputs are not provided
if (length(args) < 2) {
  stop("Usage: Rscript metaphlan_to_phyloseq.R <metaphlan_file> <metadata_file>\n")
}
metaphlan_file <- args[1]
metadata_file  <- args[2]

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
data <- read.delim(metaphlan_file, header = FALSE)
colnames(data) <- data[4,] #forth row has sample names always (necessary case for a magic number!)
sample_name <- unique(regmatches(data[2,1], gregexpr("SRR[0-9]+", data[2,1]))[[1]]) #second row first col has sample name
colnames(data)[3] <- sample_name #third column should be sample name, (necessary case for a magic number!)
data <- data %>% dplyr::slice(c(5:nrow(data)))
head(data) #check the structure is okay
dim(data)
row.names(data) <- data$`#clade_name`
head(row.names(data)) 
data <- data[grepl("s__", data$`#clade_name`),]
data$`#clade_name` <- c() 
data$NCBI_tax_id <- c() 
data$additional_species <- c()
data2 <- data %>% mutate(across(everything(), ~ as.numeric(as.character(.))))
phyloseqin= metaphlanToPhyloseq(data2)
phyloseqin
otu <- as.data.frame(otu_table(phyloseqin))
colnames(otu) <- sub("_.*", "", colnames(otu))
otu <- as.matrix(t(otu))

#Read metadata
metadata <- read.csv(metadata_file)
rownames(metadata) <- metadata$Sample
phyloseqin <- merge_phyloseq(otu_table(otu, taxa_are_rows = FALSE),tax_table(phyloseqin),sample_data(metadata))
phyloseqin

#Merge with reference phyloseq
ps <- readRDS("input_data/phyloseq.ref.rds")
ps.cln <- merge_phyloseq(phyloseqin,ps)
tax <- as.data.frame(tax_table(ps.cln))
otu <- as.data.frame(otu_table(ps.cln))
sampledf <- as(sample_data(ps.cln), "data.frame")

#Save new phyloseq: reference+patient
saveRDS(ps.cln,"input_data/phyloseq.rds")
write.csv(tax,"input_data/tax.csv")
write.csv(otu,"input_data/otu.csv")
write.csv(sampledf, "input_data/combined_metadata.csv")

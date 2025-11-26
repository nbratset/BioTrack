##This script was used to clean the metadata from publicly available data and make a reference phyloseq object which can anchor any new patient data.
##We took out sample SRR5946632 (generated randomly) from this phyloseq because we want to use this as an example of a test case for a new patient. 

#PRJEB39813
table1 <- read.csv("/Users/aryagautam/Desktop/BioTrack/public data/SraRunTable_PRJEB39813.csv")
table1 <- table1 %>% dplyr::select(c("Run","geo_loc_name_country","host_disease_status","gastrointestinal_tract_disorder"))
table1$host_disease_status <- ifelse(
  table1$host_disease_status == "" | is.na(table1$host_disease_status),
  table1$gastrointestinal_tract_disorder,
  table1$host_disease_status
)
table1$host_disease_status[table1$host_disease_status=="Health controls"] <- "Healthy control"
names(table1) <- c("Sample","Location","Condition")
table1 <- table1 %>% dplyr::select(c("Sample","Location","Condition"))

#PRJNA398089
table2 <- read.csv("/Users/aryagautam/Desktop/BioTrack/public data/SraRunTable_PRJNA398089.csv")
table2 <- table2 %>% dplyr::select(c("Run","geo_loc_name_country","Host_disease"))
table2$Host_disease[table2$Host_disease=="CD"] <- "Crohn's disease"
table2$Host_disease[table2$Host_disease=="Crohn''s disease"] <- "Crohn's disease"
table2$Host_disease[table2$Host_disease=="nonIBD"] <- "Healthy control"
table2$Host_disease[table2$Host_disease=="UC"] <- "Ulcerative colitis"
table2$Host_disease[table2$Host_disease=="ulcerative colitis"] <- "Ulcerative colitis"
table2$Host_disease[table2$Host_disease==""] <- "Healthy control"
names(table2) <- c("Sample","Location","Condition")

#PRJNA945504
table6 <- read.csv("/Users/aryagautam/Desktop/BioTrack/public data/SraRunTable_PRJNA945504.csv")
table6 <- table6 %>% dplyr::select(c("Run","geo_loc_name","Host_disease"))
table6$Host_disease[table6$Host_disease=="CD"] <- "Crohn's disease"
table6$Host_disease[table6$Host_disease=="HC"] <- "Healthy control"
table6$Host_disease[table6$Host_disease=="UC"] <- "Ulcerative colitis"
names(table6) <- c("Sample","Location","Condition")

#PRJNA400072
table3 <- read.xlsx("/Users/aryagautam/Desktop/BioTrack/public data/SraRunTable_PRJNA400072_v2.xlsx")
colnames(table3) <- table3[1,]
table3 <- table3 %>% dplyr::slice(c(3))
names(table3)[1] <- "feature"
table3 <- pivot_longer(
  data = table3,
  cols = -"feature",            
  names_to = "Sample.Name",
  values_to = "Condition"
)
table3$Sample.Name <- sub("_Validation$", "", table3$Sample.Name)
table3$Sample.Name <- gsub("\\|", "_", table3$Sample.Name)
table3$Sample.Name <- sub("^Validation_", "", table3$Sample.Name)
table4 <- read.csv("/Users/aryagautam/Desktop/BioTrack/public data/SraRunTable_PRJNA400072.csv")
table4 <- left_join(table4,table3,by="Sample.Name")
table4 <- table4 %>% dplyr::select(c("Run","geo_loc_name_country","Condition"))
names(table4) <- c("Sample","Location","Condition")
table4$Condition[table4$Condition=="CD"] <- "Crohn's disease"
table4$Condition[table4$Condition=="HC"] <- "Healthy control"
table4$Condition[table4$Condition=="UC"] <- "Ulcerative colitis"
table4$Condition[table4$Condition=="Control"] <- "Healthy control"

table5 <- rbind(table1,table2,table4,table6)
table5$Condition[table5$Condition=="Crohn's Disease"] <- "Crohn's disease"
table5$Condition[table5$Condition=="Healthy Controls"] <- "Healthy control"
write.csv(table5,"/Users/aryagautam/Desktop/BioTrack/public data/metadata.csv")

metadata <- read.csv("/Users/aryagautam/Desktop/BioTrack/public data/metadata.csv",header=TRUE)
metadata$X <- c()
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

data <- read.delim("/Users/aryagautam/Desktop/BioTrack/input_data/metaphlan_output.txt",header = F)
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
rownames(metadata) <- metadata$Sample
phyloseqin <- merge_phyloseq(otu_table(otu, taxa_are_rows = FALSE),tax_table(phyloseqin),sample_data(metadata))
phyloseqin
zero_samps <- names(which(rowSums(otu) == 0)) #Remove 0 abundance samples
ps.cln <- prune_samples(!(sample_names(phyloseqin) %in% zero_samps), phyloseqin)
ps.cln    
set.seed(1)   #for reproducibility
one_sample <- sample_names(ps.cln)[sample(length(sample_names(ps.cln)), 1)]
one_sample
ps.cln <- prune_samples(!(sample_names(ps.cln) %in% one_sample), ps.cln) #Randomly remove one sample (our test case)
ps.cln #1024 taxa and 2021 samples
saveRDS(ps.cln,"/Users/aryagautam/Desktop/BioTrack/input_data/phyloseq.ref.rds")


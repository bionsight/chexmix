#!/bin/bash


# See https://ctdbase.org/reports/
# Please read the file, CTD_curation_summary.docx, for the annotation information
CTD_PATH=../data

mkdir -p $CTD_PATH

# Chemical–gene interactions
wget -c https://ctdbase.org/reports/CTD_chem_gene_ixns.tsv.gz -P $CTD_PATH
wget -c https://ctdbase.org/reports/CTD_chem_gene_ixns_structured.xml.gz -P $CTD_PATH

wget -c https://ctdbase.org/reports/CTD_chem_gene_ixns_structured.xsd -P $CTD_PATH

# Chemical–gene interaction types
wget -c https://ctdbase.org/reports/CTD_chem_gene_ixn_types.tsv -P $CTD_PATH

# Chemical–disease associations
wget -c https://ctdbase.org/reports/CTD_chemicals_diseases.tsv.gz -P $CTD_PATH

# Chemical–GO enriched associations
wget -c https://ctdbase.org/reports/CTD_chem_go_enriched.tsv.gz -P $CTD_PATH

# Chemical–pathway enriched associations
wget -c https://ctdbase.org/reports/CTD_chem_pathways_enriched.tsv.gz -P $CTD_PATH

# Gene–disease associations
wget -c https://ctdbase.org/reports/CTD_genes_diseases.tsv.gz -P $CTD_PATH

# Gene–pathway associations
wget -c https://ctdbase.org/reports/CTD_genes_pathways.tsv.gz -P $CTD_PATH

# Disease–pathway associations
wget -c https://ctdbase.org/reports/CTD_diseases_pathways.tsv.gz -P $CTD_PATH

# Chemical–phenotype interactions
wget -c https://ctdbase.org/reports/CTD_pheno_term_ixns.tsv.gz -P $CTD_PATH

# Exposure–study associations
wget -c https://ctdbase.org/reports/CTD_exposure_studies.tsv.gz -P $CTD_PATH

# Exposure–event associations
wget -c https://ctdbase.org/reports/CTD_exposure_events.tsv.gz -P $CTD_PATH

# Phenotype (GO)–Disease Inference Networks
wget -c https://ctdbase.org/reports/CTD_Phenotype-Disease_biological_process_associations.tsv.gz -P $CTD_PATH
wget -c https://ctdbase.org/reports/CTD_Phenotype-Disease_cellular_component_associations.tsv.gz -P $CTD_PATH
wget -c https://ctdbase.org/reports/CTD_Phenotype-Disease_molecular_function_associations.tsv.gz -P $CTD_PATH

# wget -c https://ctdbase.org/reports/CTD_Disease-GO_biological_process_associations.tsv.gz -P $CTD_PATH
# wget -c https://ctdbase.org/reports/CTD_Disease-GO_cellular_component_associations.tsv.gz -P $CTD_PATH
# wget -c https://ctdbase.org/reports/CTD_Disease-GO_molecular_function_associations.tsv.gz -P $CTD_PATH

# Chemical vocabulary
wget -c https://ctdbase.org/reports/CTD_chemicals.tsv.gz -P $CTD_PATH

# Disease vocabulary (MEDIC)
wget -c https://ctdbase.org/reports/CTD_diseases.tsv.gz -P $CTD_PATH

# Gene vocabulary
wget -c https://ctdbase.org/reports/CTD_genes.tsv.gz -P $CTD_PATH

# Pathway vocabulary
wget -c https://ctdbase.org/reports/CTD_pathways.tsv.gz -P $CTD_PATH

# Exposure Ontology (ExO)
wget -c https://ctdbase.org/reports/CTD_exposure_ontology.obo -P $CTD_PATH

# Old stuff

# wget -c https://ctdbase.org/reports/CTD_curation_summary.docx -P $CTD_PATH
# wget -c https://ctdbase.org/reports/CTD_curated_cas_nbrs.tsv.gz -P $CTD_PATH
# wget -c https://ctdbase.org/reports/CTD_UniProtToCTDIdMapping.txt.gz -P $CTD_PATH
# wget -c https://ctdbase.org/reports/CTD_pheno_ixns.xls -P $CTD_PATH

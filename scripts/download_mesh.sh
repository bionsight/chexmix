#!/bin/bash

# See https://www.nlm.nih.gov/databases/dtd/ for other DTD files
DTD_PATH=../data/mesh/dtd

mkdir -p $DTD_PATH

wget -c https://www.nlm.nih.gov/databases/dtd/nlmqualifierrecordset_20200101.dtd -P $DTD_PATH
wget -c https://www.nlm.nih.gov/databases/dtd/nlmsupplementalrecordset_20200101.dtd -P $DTD_PATH
wget -c https://www.nlm.nih.gov/databases/dtd/nlmpharmacologicalactionset_20200101.dtd -P $DTD_PATH

lftp -e "mirror -n /online/mesh/MESH_FILES/xmlmesh/ ../data/mesh/MESH_FILES/xmlmesh/;quit;" nlmpubs.nlm.nih.gov

#!/bin/bash

OMIM_PATH=../data/omim

mkdir -p $OMIM_PATH

wget -c https://omim.org/static/omim/data/mim2gene.txt -P $OMIM_PATH
wget -c https://data.omim.org/downloads/Yle-qm9-T1KV9LzpkXfJng/mimTitles.txt -P $OMIM_PATH
wget -c https://data.omim.org/downloads/Yle-qm9-T1KV9LzpkXfJng/genemap2.txt -P $OMIM_PATH
wget -c https://data.omim.org/downloads/Yle-qm9-T1KV9LzpkXfJng/morbidmap.txt -P $OMIM_PATH

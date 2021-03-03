#!/bin/bash
lftp -e "mirror -n -e -P 8 /pub/taxonomy/ ../data/taxonomy/;quit;" https://ftp.ncbi.nlm.nih.gov

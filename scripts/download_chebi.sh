#!/bin/bash

lftp -e "mirror -n /pub/databases/chebi ../data;quit;" ftp://ftp.ebi.ac.uk

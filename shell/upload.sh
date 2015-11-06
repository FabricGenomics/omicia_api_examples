#!/bin/bash

#upload.sh
#---------

#Usage: upload.sh 131 "Sample123" male vcf file.vcg.gz

CURL=/usr/bin/curl
CURLOPTS=-s

URL=https://${OMICIA_API_LOGIN}:${OMICIA_API_PASSWORD}@api.omicia.com

PROJECT_ID=$1
LABEL=$2
# sex must be one of: male, female, unspecified
SEX=$3
# use vcf for uncompressed or vcf.gz/bz2/Z for compressed (preferred)
FORMAT=$4
FILE=$5

#upload genome
$CURL $CURLOPTS --data-urlencode "$URL/projects/$PROJECT_ID/genomes?genome_label=$LABEL&genome_sex=$SEX&assembly_version=hg19&format=$FORMAT" --upload-file $FILE
echo
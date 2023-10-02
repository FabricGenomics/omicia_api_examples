#!/bin/sh

if [ $# -ne 3 ] ; then
    echo "Usage: $0 <CONTAINER_ID> <MEMBER_ID> <GENOME.VCF>"  
    exit 1  
fi

CURL=/usr/bin/curl
CURLOPTS=

container_id=$1
member_id=$2
vcf_file=$3

URL="${FABRIC_API_URL:=https://api-test.omicia-remote.com}/case_containers/${container_id}/members/${member_id}/genome \
    -F genome_file=@${vcf_file} \
    -F genome_name=`basename ${vcf_file}` \
    -F assembly_version=b38"

echo POST $URL >&2
$CURL $CURLOPTS -u ${FABRIC_API_LOGIN}:${FABRIC_API_PASSWORD} ${URL}



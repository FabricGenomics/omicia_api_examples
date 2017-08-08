#!/bin/bash
#  Omicia Opal API uploader: place in your PATH
#  1) Request an API key for your workspace - keep this information secure as
#     it gives admin access to Opal
#  2) Set up your environment variables so that the API key and password are
#     available as
#       OMICIA_API_KEY
#       OMICIA_API_PASSWORD
#
#     For example, you could add the following to your .bashrc file
#        export OMICIA_API_KEY=<YOUR KEY HERE>
#        export OMICIA_API_PASSWORD=<YOUR KEY HERE>
#
#   3) Make the script executable: chmod +x upload_folder.sh
#

display_usage() {
    echo "Upload all VCF files to Opal (include .vcf, .vcf.gz or .vcf.bz2)"
	echo "\nUsage:\n$0 folder project_id \n"
}

if [ ! $# == 2 ]
then
    display_usage
    exit 1
fi

if [[ ( $# == "--help") ||  $# == "-h" ]]
then
    display_usage
    exit 0
fi

if [[ ! -d "$1" ]]; then
    echo "Please specify a folder name"
    exit 1
fi

login=$OMICIA_API_LOGIN
password=$OMICIA_API_PASSWORD

if [ -z $login ] || [ -z $password ]
then
    echo "Please get an API key and set the OMICI_API_KEY and OMICIA_API_PASSWORD environment variables"
    exit 1
fi

CURL=/usr/bin/curl
CURLOPTS="-s -q"

URL=https://api.fabricgenomics.com
PROJECT_ID=$2

for f in "$1"/*.vcf.gz; do
    if [[ -f $f ]]
    then
        FNAME=${f##*/}
        default="${FNAME%.*}"
        read -p "Edit the Label [$default]: " -e LABEL
        LABEL=${LABEL:-$default}
        echo Uploading ${f}: label ${LABEL}
        SEX=unspecified
        OUT=`$CURL $CURLOPTS -u $login:$password "$URL/projects/$PROJECT_ID/genomes?genome_label=$LABEL&genome_sex=$SEX&filename=$FILE&assembly_version=hg19&format=vcf.gz" --upload-file $f`
    fi
done

echo ...done
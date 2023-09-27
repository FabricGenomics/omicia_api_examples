#!/bin/bash

CURL=/usr/bin/curl
CURLOPTS=

URL=https:api.fabricgenomics.com

# create new project
$CURL $CURLOPTS -u ${FABRIC_API_LOGIN}:${FABRIC_API_PASSWORD} $URL/projects/ --data "project_name=$1&description=$2&share_role=CONTRIBUTOR" -o /tmp/$$.out

echo
cat /tmp/$$.out
rm /tmp/$$.out
echo

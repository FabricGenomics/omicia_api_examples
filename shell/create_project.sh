#!/bin/bash

CURL=/usr/bin/curl
CURLOPTS=-s 

URL=https://${OMICIA_API_LOGIN}:${OMICIA_API_PASSWORD}@api.omicia.com

# create new project
$CURL $CURLOPTS   $URL/projects/ --data-urlencode "project_name=$1&description=&share_role=CONTRIBUTOR" -o /tmp/$$.out

echo
cat /tmp/$$.out
rm /tmp/$$.out
echo

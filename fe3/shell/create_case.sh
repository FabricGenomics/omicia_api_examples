#!/bin/sh

if [ $# -ne 1 ] ; then
    echo "Usage: $0 newcase.json"  
    exit 1  
fi

CASE_JSON=$1
CURL=/usr/bin/curl
CURLOPTS=

URL="${FABRIC_API_URL:=https://api-test.omicia-remote.com}/case_containers -d @${CASE_JSON}"
echo POST ${URL} >&2

$CURL $CURLOPTS -u ${FABRIC_API_LOGIN}:${FABRIC_API_PASSWORD} ${URL}



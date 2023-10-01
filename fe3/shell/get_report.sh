#!/bin/sh

if [ $# -lt 1 -o $# -gt 2 ] ; then
    echo "Usage: $0 <CONTAINER_ID> [<REPORT_ID>]"  
    exit 1  
fi

CURL=/usr/bin/curl
CURLOPTS=

container_id=$1
report_id=$2


URL="${FABRIC_API_URL:=https://api-test.omicia-remote.com}/case_containers/${container_id}/report"

if [ "${report_id}" != "" ]; then URL="${URL}/pdf/${report_id}"; fi

echo GET $URL >&2
$CURL $CURLOPTS -u ${FABRIC_API_LOGIN}:${FABRIC_API_PASSWORD} ${URL}



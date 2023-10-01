#!/bin/sh

CURL=/usr/bin/curl
CURLOPTS=

URL=${FABRIC_API_URL:=https://api-test.omicia-remote.com}/case_containers
echo GET ${URL} >&2

$CURL $CURLOPTS -u ${FABRIC_API_LOGIN}:${FABRIC_API_PASSWORD} $URL


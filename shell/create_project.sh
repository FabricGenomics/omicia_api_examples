create_project.sh
-----------------
# Usage: create_project.sh "Project Name"

CURL=/usr/bin/curl
CURLOPTS=-s --data-urlencode

URL=https://${OMICIA_API_LOGIN}:${OMICIA_API_PASSWORD}@api.omicia.com

# create new project
$CURL $CURLOPTS $URL/projects/ --data "project_name=$1&description=&share_role=CONTRIBUTOR" -o /tmp/$$.out

echo
cat /tmp/$$.out
rm /tmp/$$.out
echo
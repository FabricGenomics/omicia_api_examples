All of these scripts require the environment variables OMICIA_API_LOGIN and
OMICIA_API_PASSWORD to be set to the API user's login and password API
credentials, respectively.

To check whether you have these variables set correctly set, type:

echo $OMICIA_API_LOGIN
echo $OMICIA_API_PASSWORD

If these commands yield the correct credentials everything is set to go.
If they are blank or incorrect, to set them to the correct values type:

export OMICIA_API_LOGIN=<your api login string>
export OMICIA_API_LOGIN=<your api password string>
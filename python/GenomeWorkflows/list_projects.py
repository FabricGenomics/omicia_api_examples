"""List all projects
"""

import os
import requests
from requests.auth import HTTPBasicAuth
import sys
import json

# Load environment variables for request authentication parameters
if "OMICIA_API_PASSWORD" not in os.environ:
    sys.exit("OMICIA_API_PASSWORD environment variable missing")

if "OMICIA_API_LOGIN" not in os.environ:
    sys.exit("OMICIA_API_LOGIN environment variable missing")

OMICIA_API_LOGIN = os.environ['OMICIA_API_LOGIN']
OMICIA_API_PASSWORD = os.environ['OMICIA_API_PASSWORD']
OMICIA_API_URL = os.environ.get('OMICIA_API_URL', 'https://api.omicia.com')
auth = HTTPBasicAuth(OMICIA_API_LOGIN, OMICIA_API_PASSWORD)


def list_projects():
    """
      list all projects
    """
    # Construct request
    url = "{}/projects/"
    url = url.format(OMICIA_API_URL)

    result = requests.get(url, auth=auth)
    return result.json()


def main():
    """main function, lists all projects 
    """
    json_response = list_projects()
    try:
        sys.stdout.write("Projects\n")
        sys.stdout.write(json.dumps(json_response, indent=2))

    except KeyError:
        if json_response['description']:
            sys.stdout.write('Error: {}\n'.format(json_response['description']))
        else:
            sys.stdout.write('Something went wrong...')


if __name__ == "__main__":
    main()

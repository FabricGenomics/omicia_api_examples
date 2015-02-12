"""Create a new project.
"""

import os
import requests
from requests.auth import HTTPBasicAuth
import sys

# Load environment variables for request authentication parameters
if "OMICIA_API_PASSWORD" not in os.environ:
    sys.exit("OMICIA_API_PASSWORD environment variable missing")

if "OMICIA_API_LOGIN" not in os.environ:
    sys.exit("OMICIA_API_LOGIN environment variable missing")

OMICIA_API_LOGIN = os.environ['OMICIA_API_LOGIN']
OMICIA_API_PASSWORD = os.environ['OMICIA_API_PASSWORD']
OMICIA_API_URL = os.environ.get('OMICIA_API_URL', 'https://api.omicia.com')
auth = HTTPBasicAuth(OMICIA_API_LOGIN, OMICIA_API_PASSWORD)

def create_project(name, description, share_role):
    """Use the Omicia API to create a new project.
    Returns the newly created project's id.

    :param name: str for project name
    :param description: str for project description
    :param share_role: str -- "CONTRIBUTOR," "VIEWER" or "NONE"
    """

    # Construct request
    url = "{}/projects/"
    url = url.format(OMICIA_API_URL)
    payload = {'project_name': name,
               'description': description,
               'share_role': share_role}

    # Post request and return newly created project's id
    result = requests.post(url, headers=payload, data=payload, auth=auth)
    return result.json()["id"]

def main(argv):
    """main function, creates a project with a command-line specified name
    """

    if len(argv) != 3:
        sys.exit("Usage: python create_project.py <name> <desc> <sharerole>")
    name = argv[0]
    description = argv[1]
    share_role = argv[2]
    project_id = create_project(name, description, share_role)
    sys.stdout.write(project_id)

if __name__ == "__main__":
    main(sys.argv[1:])

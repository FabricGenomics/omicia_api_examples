"""Create a new project.
"""

import argparse
import os
import requests
from requests.auth import HTTPBasicAuth
import sys
import simplejson as json
import certifi

# Load environment variables for request authentication parameters
if "OMICIA_API_PASSWORD" not in os.environ:
    sys.exit("OMICIA_API_PASSWORD environment variable missing")

if "OMICIA_API_LOGIN" not in os.environ:
    sys.exit("OMICIA_API_LOGIN environment variable missing")

OMICIA_API_LOGIN = os.environ['OMICIA_API_LOGIN']
OMICIA_API_PASSWORD = os.environ['OMICIA_API_PASSWORD']
OMICIA_API_URL = os.environ.get('OMICIA_API_URL', 'https://api.fabricgenomics.com')
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
    result = requests.post(url, data=payload, auth=auth, verify=certifi.where())
    return result.json()


def main():
    """main function, creates a project with a command-line specified name
    """
    parser = argparse.ArgumentParser(description='Create a new project')
    parser.add_argument('n', metavar='name', type=str)
    parser.add_argument('d', metavar='description', type=str)
    parser.add_argument('s', metavar='share_role', type=str, choices=['CONTRIBUTOR', 'VIEWER', 'NONE'])

    args = parser.parse_args()
    name = args.n
    description = args.d
    share_role = args.s

    json_response = create_project(name, description, share_role)
    try:
        sys.stdout.write(json.dumps(json_response, indent=4))
    except KeyError:
        if json_response['description']:
            sys.stdout.write('Error: {}\n'.format(json_response['description']))
        else:
            sys.stdout.write('Something went wrong...')


if __name__ == "__main__":
    main()

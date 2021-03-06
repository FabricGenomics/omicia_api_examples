"""Get all genomes in a project.
"""

import argparse
import os
import requests
from requests.auth import HTTPBasicAuth
import sys
import simplejson as json

# Load environment variables for request authentication parameters
if "FABRIC_API_PASSWORD" not in os.environ:
    sys.exit("FABRIC_API_PASSWORD environment variable missing")

if "FABRIC_API_LOGIN" not in os.environ:
    sys.exit("FABRIC_API_LOGIN environment variable missing")

FABRIC_API_LOGIN = os.environ['FABRIC_API_LOGIN']
FABRIC_API_PASSWORD = os.environ['FABRIC_API_PASSWORD']
FABRIC_API_URL = os.environ.get('FABRIC_API_URL', 'https://api.fabricgenomics.com')
auth = HTTPBasicAuth(FABRIC_API_LOGIN, FABRIC_API_PASSWORD)


def get_genomes(project_id):
    """Fetch all the genomes associated with a particular project.
    """

    # Construct request
    url = "{}/projects/{}/genomes".format(FABRIC_API_URL, project_id)

    # Get request and return json object of genomes
    result = requests.get(url, auth=auth)
    return result.json()


def main():
    """main function, get all genomes in a project.
    """
    parser = argparse.ArgumentParser(description='Get all genomes in a project.')
    parser.add_argument('project_id', metavar='project_id')
    args = parser.parse_args()

    project_id = args.project_id

    json_response = get_genomes(project_id)

    try:
        sys.stdout.write(json.dumps(json_response, indent=4))
    except KeyError:
        if json_response['description']:
            sys.stdout.write("Error: {}\n".format(json_response))
        else:
            sys.stdout.write('Something went wrong ...')

if __name__ == "__main__":
    main()

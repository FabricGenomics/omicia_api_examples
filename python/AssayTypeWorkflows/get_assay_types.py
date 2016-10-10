"""Get all assay_types in a workspace.
"""

import argparse
import os
import requests
from requests.auth import HTTPBasicAuth
import sys
import simplejson as json

# Load environment variables for request authentication parameters
if "OMICIA_API_PASSWORD" not in os.environ:
    sys.exit("OMICIA_API_PASSWORD environment variable missing")

if "OMICIA_API_LOGIN" not in os.environ:
    sys.exit("OMICIA_API_LOGIN environment variable missing")

OMICIA_API_LOGIN = os.environ['OMICIA_API_LOGIN']
OMICIA_API_PASSWORD = os.environ['OMICIA_API_PASSWORD']
OMICIA_API_URL = os.environ.get('OMICIA_API_URL', 'https://api.omicia.com')
auth = HTTPBasicAuth(OMICIA_API_LOGIN, OMICIA_API_PASSWORD)


def get_assay_type(assay_type_id):
    """Fetch all the assay_types associated with the api user's workspace
    """

    # Construct request
    url = "{}/assay_types/{}".format(OMICIA_API_URL, assay_type_id)

    # Get request and return json object of an assay type
    result = requests.get(url, auth=auth)
    return result.json()


def get_assay_types():
    """Fetch all the assay_types associated with the api user's workspace
    """

    # Construct request
    url = "{}/assay_types".format(OMICIA_API_URL)

    # Get request and return json object of assay types
    result = requests.get(url, auth=auth)
    return result.json()


def main():
    """main function, get all assay_types in a project.
    """
    parser = argparse.ArgumentParser(description='Upload a genome.')
    parser.add_argument('--assay_type_id', metavar='assay_type_id')
    args = parser.parse_args()

    assay_type_id = args.assay_type_id

    if assay_type_id:
        assay_type = get_assay_type(assay_type_id)
        sys.stdout.write(json.dumps(assay_type, indent=4))

    else:
        json_response = get_assay_types()
        sys.stdout.write(json.dumps(json_response, indent=4))

if __name__ == "__main__":
    main()
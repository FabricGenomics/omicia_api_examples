"""Get a list of panels, either all or filtered by some attribute.
"""

import os
import requests
from requests.auth import HTTPBasicAuth
import sys
import json
import argparse

# Load environment variables for request authentication parameters
if "OMICIA_API_PASSWORD" not in os.environ:
    sys.exit("OMICIA_API_PASSWORD environment variable missing")

if "OMICIA_API_LOGIN" not in os.environ:
    sys.exit("OMICIA_API_LOGIN environment variable missing")

OMICIA_API_LOGIN = os.environ['OMICIA_API_LOGIN']
OMICIA_API_PASSWORD = os.environ['OMICIA_API_PASSWORD']
OMICIA_API_URL = os.environ.get('OMICIA_API_URL', 'https://api.omicia.com')
auth = HTTPBasicAuth(OMICIA_API_LOGIN, OMICIA_API_PASSWORD)


def update_job(accession_id, id):
    """creates a new job and returns a UUID"""
    # Construct request
    path = "{}/jobs/{}"

    payload = {
        'accession_id': accession_id
    }
    url = path.format(OMICIA_API_URL, id)

    result = requests.put(url, json=payload, auth=auth)
    return result.json()


def main():
    """Main function. Get panels. All, or by name, description or test code.
    """
    parser = argparse.ArgumentParser(description='Get panel')
    parser.add_argument('--acc', metavar='accession_id', type=str)
    parser.add_argument('--id', metavar='id', type=int)

    args = parser.parse_args()

    accession_id = args.acc
    id = args.id

    json_response = update_job(accession_id, id)
    panel_ids = json.dumps(json_response, indent=4)

    sys.stdout.write('{}'.format(panel_ids))
    sys.stdout.write('\n')

if __name__ == "__main__":
    main()

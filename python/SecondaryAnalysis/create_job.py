"""
Request creation of a new job. Requires an accession id. Returns a unique ID that can
be used to launch secondary analysis processes.
"""

import os
import requests
from requests.auth import HTTPBasicAuth
import sys
import json
import argparse

# Load environment variables for request authentication parameters
if "FABRIC_API_PASSWORD" not in os.environ:
    sys.exit("FABRIC_API_PASSWORD environment variable missing")

if "FABRIC_API_LOGIN" not in os.environ:
    sys.exit("FABRIC_API_LOGIN environment variable missing")

FABRIC_API_LOGIN = os.environ['FABRIC_API_LOGIN']
FABRIC_API_PASSWORD = os.environ['FABRIC_API_PASSWORD']
FABRIC_API_URL = os.environ.get('FABRIC_API_URL', 'https://api.fabricgenomics.com')
auth = HTTPBasicAuth(FABRIC_API_LOGIN, FABRIC_API_PASSWORD)


def create_job(accession_id):
    """creates a new job and returns a UUID"""
    # Construct request
    path = "{}/jobs"

    payload = {
        'accession_id': accession_id
    }
    url = path.format(FABRIC_API_URL)

    result = requests.post(url, json=payload, auth=auth)
    return result.json()


def main():
    """Main function. Get panels. All, or by name, description or test code.
    """
    parser = argparse.ArgumentParser(description='Get panel')
    parser.add_argument('--a', metavar='accession_id', type=str)

    args = parser.parse_args()

    accession_id = args.a

    json_response = create_job(accession_id)
    panel_ids = json.dumps(json_response, indent=4)

    sys.stdout.write('{}'.format(panel_ids))
    sys.stdout.write('\n')

if __name__ == "__main__":
    main()

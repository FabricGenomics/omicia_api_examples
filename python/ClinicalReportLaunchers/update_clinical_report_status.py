"""Update a clinical report's status.
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


def update_cr_status(cr_id, status):
    """Update a clinical report's status.
    """
    # Construct request
    url = "{}/reports/{}/update_status/"
    url = url.format(FABRIC_API_URL, cr_id, status)
    # Build the patch payload
    url_payload = json.dumps([{"op": "replace",
                              "path": "/status",
                              "value": status}])
    headers = {"content-type": "application/json-patch+json"}

    sys.stdout.flush()
    result = requests.patch(url, auth=auth, json=url_payload, headers=headers)
    return result


def main():
    """Main function. Patch a report variant.
    """
    parser = argparse.ArgumentParser(description='Set clinical report status')
    parser.add_argument('cr_id', metavar='clinical_report_id', type=int)
    parser.add_argument('status', metavar='status', type=str)

    args = parser.parse_args()

    cr_id = args.cr_id
    status = args.status

    response = update_cr_status(cr_id, status)
    try:
        sys.stdout.write(response.text)
    except KeyError:
        sys.stderr.write(response.text)
    sys.stdout.write('\n')

if __name__ == "__main__":
    main()

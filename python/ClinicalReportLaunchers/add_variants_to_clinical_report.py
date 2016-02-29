"""Add variant report variants to a Clinical Report by ID.
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


def add_variants_to_cr(cr_id, vmv_ids):
    """Add variants from vmv_base to a clinical report by ID.
    """
    # Construct request
    url = "{}/reports/{}/add_variants/"
    url = url.format(OMICIA_API_URL, cr_id)

    # Build the patch payload
    url_payload = json.dumps([{"op": "add",
                              "path": "/variants",
                              "value": vmv_ids}])
    headers = {"content-type": "application/json-patch+json"}
    sys.stdout.flush()
    result = requests.patch(url, auth=auth, json=url_payload, headers=headers)
    return result


def main():
    """Main function. Patch a report variant.
    """
    parser = argparse.ArgumentParser(description='Add report variants to an existing clinical report.')
    parser.add_argument('cr_id', metavar='clinical_report_id', type=int)
    parser.add_argument('variant_ids', metavar='variant_ids', type=str)

    args = parser.parse_args()

    cr_id = args.cr_id
    vmv_base_variant_ids = args.variant_ids

    # Take a string of comma-separated vmv ids and make a list out of them
    vmv_base_variant_ids = vmv_base_variant_ids.split(",")

    response = add_variants_to_cr(cr_id, vmv_base_variant_ids)
    try:
        sys.stdout.write(response.text)
    except KeyError:
        sys.stderr.write(response.text)
    sys.stdout.write('\n')

if __name__ == "__main__":
    main()

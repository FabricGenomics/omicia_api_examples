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


def make_selectable_variants_from_vmv_variants(cr_id, vmv_ids):
    """Add variants from report_variant_selectable to a clinical report by ID.
    """
    # Construct request
    url = "{}/reports/{}/make_selectable_variants_from_vmv_variants/"
    url = url.format(OMICIA_API_URL, cr_id)

    # Build the patch payload
    url_payload = json.dumps([{"op": "add",
                              "path": "/variants",
                              "value": [{"id": vmv_id,
                                         "inheritance_mode": 'RECESSIVE'} for vmv_id in vmv_ids]}])
    headers = {"content-type": "application/json-patch+json"}
    sys.stdout.flush()
    result = requests.patch(url, auth=auth, json=url_payload, headers=headers)
    return result


def main():
    """Main function. Patch a report variant.
    """
    parser = argparse.ArgumentParser(description='Add report selectable variants to an existing clinical report.')
    parser.add_argument('cr_id', metavar='clinical_report_id', type=int)
    parser.add_argument('selectable_ids', metavar='selectable_ids', type=str)

    args = parser.parse_args()

    cr_id = args.cr_id
    selectable_ids = args.selectable_ids

    # Take a string of comma-separated vmv ids and make a list out of them
    vmv_base_variant_ids = selectable_ids.split(",")

    response = make_selectable_variants_from_vmv_variants(cr_id, vmv_base_variant_ids)
    try:
        sys.stdout.write(response.text)
    except KeyError:
        sys.stderr.write(response.text)
    sys.stdout.write('\n')

if __name__ == "__main__":
    main()

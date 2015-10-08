"""Get a clinical report's variants.
Usage: python patch_report_variant.py 1542 --status "FAILED_CONFIRMATION"
"""

import os
import requests
from requests.auth import HTTPBasicAuth
import sys
import json
import argparse

#Load environment variables for request authentication parameters
if "OMICIA_API_PASSWORD" not in os.environ:
    sys.exit("OMICIA_API_PASSWORD environment variable missing")

if "OMICIA_API_LOGIN" not in os.environ:
    sys.exit("OMICIA_API_LOGIN environment variable missing")

OMICIA_API_LOGIN = os.environ['OMICIA_API_LOGIN']
OMICIA_API_PASSWORD = os.environ['OMICIA_API_PASSWORD']
OMICIA_API_URL = os.environ.get('OMICIA_API_URL', 'https://api.omicia.com')
auth = HTTPBasicAuth(OMICIA_API_LOGIN, OMICIA_API_PASSWORD)


def patch_cr_variant(cr_id, report_variant_id, patch_values):
    """Change values in a clinical report variant. Patch values is a dictionary
    of report variant base attributes and their intended new values.
    """
    # Construct request
    url = "{}/reports/{}/variants/{}"
    url = url.format(OMICIA_API_URL, cr_id, report_variant_id)

    patch_attributes = [key for key,value in patch_values.items()]
    # Build the patch payload
    url_payload = json.dumps([{"op": "replace", "path": attribute, "value": patch_values.get(attribute)}
                              for attribute in patch_attributes])
    headers = {"content-type": "application/json-patch"}
    sys.stdout.flush()
    result = requests.patch(url, auth=auth, json=url_payload, headers=headers)
    return result


def main():
    """Main function. Patch a report variant.
    """
    parser = argparse.ArgumentParser(description='Patch a variant in an existing clinical report.')
    parser.add_argument('cr_id', metavar='clinical_report_id', type=int)
    parser.add_argument('report_variant_id', metavar='report_variant_id', type=int)
    parser.add_argument('--status', metavar='status', type=str)

    args = parser.parse_args()

    cr_id = args.cr_id
    report_variant_id = args.report_variant_id
    status = args.status

    patch_values = {}
    if status:
        patch_values['status'] = status

    response = patch_cr_variant(cr_id, report_variant_id, patch_values)
    try:
        sys.stdout.write(response.text)
    except KeyError:
        sys.stderr.write(response.text)


if __name__ == "__main__":
    main()
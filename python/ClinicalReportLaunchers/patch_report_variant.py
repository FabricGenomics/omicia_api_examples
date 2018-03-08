"""Get a clinical report's variants.
Usage: python patch_report_variant.py 1542 --status "FAILED_CONFIRMATION"
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


def patch_cr_variant(cr_id, report_variant_id, patch_values):
    """Change values in a clinical report variant. Patch values is a dictionary
    of report variant base attributes and their intended new values.
    """
    # Construct request
    url = "{}/reports/{}/variants/{}"
    url = url.format(FABRIC_API_URL, cr_id, report_variant_id)

    patch_attributes = [key for key, value in patch_values.items()]
    # Build the patch payload
    url_payload = json.dumps([{"op": "replace",
                               "path": "/{}".format(attribute),
                               "value": patch_values.get(attribute)}
                              for attribute in patch_attributes])
    headers = {"content-type": "application/json-patch+json"}
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
    parser.add_argument('--to_report', metavar='to_report', type=str, choices=['PRIMARY_FINDING',
                                                                               'SECONDARY_FINDING',
                                                                               'DO_NOT_REPORT'])
    args = parser.parse_args()

    cr_id = args.cr_id
    report_variant_id = args.report_variant_id
    status = args.status
    to_report = args.to_report

    patch_values = {}
    if status:
        patch_values['status'] = status
    if to_report:
        patch_values['to_report'] = to_report

    response = patch_cr_variant(cr_id, report_variant_id, patch_values)
    try:
        sys.stdout.write(response.text)
    except KeyError:
        sys.stderr.write(response.text)
    sys.stdout.write('\n')

if __name__ == "__main__":
    main()

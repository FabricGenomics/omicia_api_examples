"""Add a variant note.
"""

import os
import requests
from requests.auth import HTTPBasicAuth
import sys
import json
import argparse

#Load environment variables for request authentication parameters
if "FABRIC_API_PASSWORD" not in os.environ:
    sys.exit("FABRIC_API_PASSWORD environment variable missing")

if "FABRIC_API_LOGIN" not in os.environ:
    sys.exit("FABRIC_API_LOGIN environment variable missing")

FABRIC_API_LOGIN = os.environ['FABRIC_API_LOGIN']
FABRIC_API_PASSWORD = os.environ['FABRIC_API_PASSWORD']
FABRIC_API_URL = os.environ.get('FABRIC_API_URL', 'https://api.fabricgenomics.com')
auth = HTTPBasicAuth(FABRIC_API_LOGIN, FABRIC_API_PASSWORD)


def add_variant_note(cr_id, report_variant_id, note):
    """Add an internal note to a clinical report variant
    """
    # Construct request
    url = "{}/reports/{}/variants/{}/internal_notes"
    url = url.format(FABRIC_API_URL, cr_id, report_variant_id)

    # Build the patch payload
    url_payload = {"note": note}

    sys.stdout.flush()
    result = requests.post(url, auth=auth, json=url_payload)
    return result


def main():
    """Main function. Add an internal note to a variant.
    """
    parser = argparse.ArgumentParser(description='Add an internal note to a clinical report variant.')
    parser.add_argument('cr_id', metavar='clinical_report_id', type=int)
    parser.add_argument('report_variant_id', metavar='report_variant_id', type=int)
    parser.add_argument('note', metavar='note', type=str)
    args = parser.parse_args()

    cr_id = args.cr_id
    report_variant_id = args.report_variant_id
    note = args.note

    response = add_variant_note(cr_id, report_variant_id, note)
    try:
        sys.stdout.write(json.dumps(response.json(), indent=4))
    except KeyError:
        sys.stderr.write(response.text)
    sys.stdout.write('\n')

if __name__ == "__main__":
    main()

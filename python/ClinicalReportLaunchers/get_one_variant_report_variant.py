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


def get_variant_report_variant(variant_report_id, variant_location=None, variant_id=None):
    """Add variants from vmv_base to a clinical report by ID.
    """
    # Construct request
    url = "{}/variant_reports/{}/variants"
    url = url.format(OMICIA_API_URL, variant_report_id)
    if variant_id:
        url = "{}?id={}".format(url, variant_id)
    elif variant_location:
        url = "{}?location={}".format(url, variant_location)
    else:
        sys.exit("Variant ID or location must be specified to retrieve a variant")

    sys.stdout.flush()
    result = requests.get(url, auth=auth)
    return result


def main():
    """Main function. Patch a report variant.
    """
    parser = argparse.ArgumentParser(description='Get variant report variant ID.')
    parser.add_argument('variant_report_id', metavar='variant_report_id', type=int)
    parser.add_argument('--variant_id', metavar='variant_id', type=int)
    parser.add_argument('--variant_location', metavar='variant_location', type=int)

    args = parser.parse_args()

    variant_report_id = args.variant_report_id
    variant_location = args.variant_location
    variant_id = args.variant_id

    if not (variant_id or variant_location):
        sys.exit("Variant ID or location must be specified to retrieve a variant")

    response = get_variant_report_variant(variant_report_id, variant_id=variant_id, variant_location=variant_location)
    try:
        sys.stdout.write(response.text)
    except KeyError:
        sys.stderr.write(response.text)
    sys.stdout.write('\n')

if __name__ == "__main__":
    main()

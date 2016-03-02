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


def get_variant_report_variant(variant_report_id,
                               variant_location=None,
                               variant_id=None,
                               offset=None,
                               limit=None):
    """Get report variants by location, id or simply all.
    """
    # Construct request
    url = "{}/variant_reports/{}/variants"
    url = url.format(OMICIA_API_URL, variant_report_id)
    if (variant_id or variant_location):
        if variant_id:
            url = "{}/{}".format(url, variant_id)
        elif variant_location:
            url = "{}?location={}".format(url, variant_location)
    elif (offset or limit):
        url += "?"
        if offset:
            url = "{}&offset={}".format(url, offset)
        if limit:
            url = "{}&limit={}".format(url, limit)

    sys.stdout.flush()
    result = requests.get(url, auth=auth)
    return result


def main():
    """Main function. Patch a report variant.
    """
    parser = argparse.ArgumentParser(description='Get variant report variant ID.')
    parser.add_argument('variant_report_id', metavar='variant_report_id', type=int)
    parser.add_argument('--variant_id', metavar='variant_id', type=int)
    parser.add_argument('--variant_location', metavar='variant_location', type=str)
    parser.add_argument('--offset', metavar='offset', type=int)
    parser.add_argument('--limit', metavar='limit', type=int)
    args = parser.parse_args()

    variant_report_id = args.variant_report_id
    variant_location = args.variant_location
    variant_id = args.variant_id
    offset = args.offset
    limit = args.limit

    if not (variant_id or variant_location) and not (offset or limit):
        sys.exit("Variant ID or location must be specified to retrieve a variant, "
                 "or offset and limit must be specified to fetch a batch of variants.")

    response = get_variant_report_variant(variant_report_id,
                                          variant_id=variant_id,
                                          variant_location=variant_location,
                                          offset=offset,
                                          limit=limit)
    try:
        sys.stdout.write(json.dumps(response.json(), indent=4))
    except KeyError:
        sys.stderr.write(response.json)
    sys.stdout.write('\n')

if __name__ == "__main__":
    main()

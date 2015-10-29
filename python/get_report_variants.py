"""Get a clinical report's variants.
Usages: python get_report_variants.py 1542
        python get_report_variants.py 1542 --status "FAILED_CONFIRMATION,REVIEWED"
        python get_report_variants.py 1542 --status "CONFIRMED" --format "VCF"
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


def get_cr_variants(cr_id, statuses, _format):
    """Use the Omicia API to get report variants.
    """
    #Construct request
    url = "{}/reports/{}/variants"
    url = url.format(OMICIA_API_URL, cr_id)

    # Generate the url to be able to query for multiple statuses
    if statuses:
        url += "?"
        for i, status in enumerate(statuses):
            if i > 0:
                url += "&"
            url = url + "status={}&extended=True".format(status)

    # Add a paremeter for format. If not set, default is json
    if _format == "VCF":
        if not statuses:
            url += "?"
        url += '&format=VCF'

    sys.stdout.flush()
    result = requests.get(url, auth=auth)
    return result


def main():
    """Main function. Get report variants, all or filtering by status.
    """
    parser = argparse.ArgumentParser(description='Get variants for existing clinical reports.')
    parser.add_argument('cr_id', metavar='clinical_report_id', type=int)
    parser.add_argument('--status', metavar='status', type=str)
    parser.add_argument('--format', metavar='_format', type=str, choices=['json', 'VCF'], default='json')

    args = parser.parse_args()

    cr_id = args.cr_id
    status = args.status
    _format = args.format

    statuses = status.split(",") if status else None

    response = get_cr_variants(cr_id, statuses, _format)
    if _format == 'VCF':
        for block in response.iter_content(1024):
            sys.stdout.write(block)
    else:
        try:
            response_json = response.json()
            variants = response_json['objects']
            for variant in variants:
                sys.stdout.write(json.dumps(variant))
                sys.stdout.write('\n')
        except KeyError:
            sys.stderr.write(response.json())


if __name__ == "__main__":
    main()
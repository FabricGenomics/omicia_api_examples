"""Get a clinical report's variants.
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


def get_cr_variants(cr_id, status):
    """Use the Omicia API to fill in custom patient fields for a clinical report
    """
    #Construct request
    url = "{}/reports/{}/variants"
    url = url.format(OMICIA_API_URL, cr_id)

    if status:
        url = url + "?status={}".format(status)

    sys.stdout.flush()
    result = requests.get(url, auth=auth)
    return result.json()


def main():
    """main function. Upload a specified VCF file to a specified project.
    """
    parser = argparse.ArgumentParser(description='Get variants for existing clinical reports.')
    parser.add_argument('cr_id', metavar='clinical_report_id', type=int)
    parser.add_argument('--status', metavar='status', type=str)

    args = parser.parse_args()

    cr_id = args.cr_id
    status = args.status

    json_reponse = get_cr_variants(cr_id, status)
    variants = json_reponse['objects']
    for variant in variants:
        print variant
        print '\n'

if __name__ == "__main__":
    main()
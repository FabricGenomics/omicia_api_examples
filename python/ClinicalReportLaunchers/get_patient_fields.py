"""Get a report's custom fields.
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
OMICIA_API_URL = os.environ.get('OMICIA_API_URL', 'https://api.fabricgenomics.com')
auth = HTTPBasicAuth(OMICIA_API_LOGIN, OMICIA_API_PASSWORD)


def get_fields_for_cr(cr_id):
    """Use the Omicia API to fill in custom patient fields for a clinical report
    """
    # Construct request
    url = "{}/reports/{}/patient_fields"
    url = url.format(OMICIA_API_URL, cr_id)

    sys.stdout.flush()
    result = requests.get(url, auth=auth)
    return result.json()


def main():
    """main function. Upload a specified VCF file to a specified project.
    """
    parser = argparse.ArgumentParser(description='View custom fields for existing clinical reports.')
    parser.add_argument('c', metavar='clinical_report_id', type=int)
    args = parser.parse_args()

    cr_id = args.c

    json_response = get_fields_for_cr(cr_id)
    sys.stdout.write(json.dumps(json_response, indent=4))

if __name__ == "__main__":
    main()

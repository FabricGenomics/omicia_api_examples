"""Get all clinical reports, either with extended information or not.
Fetching extended information for many reports could take a long time.
Example usages:
 python get_clinical_reports.py
 python get_clinical_reports.py --e true
"""

import os
import requests
from requests.auth import HTTPBasicAuth
import sys
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


def get_clinical_reports(extended=False):
    """Use the Omicia API to get all clinical reports
    """
    # Construct request
    url = "{}/reports/"
    if extended:
        url += "?extended=True"
    url = url.format(OMICIA_API_URL)

    sys.stdout.flush()
    result = requests.get(url, auth=auth)
    return result.json()


def main():
    """Get all clinical reports.
    """
    parser = argparse.ArgumentParser(description='Fetch all clinical report')
    parser.add_argument('--e', metavar='extended', type=bool, default=False)
    args = parser.parse_args()

    extended = args.e

    json_response = get_clinical_reports(extended=extended)
    print json_response

if __name__ == "__main__":
    main()

"""
Get a clinical report selected variants, this only works for non-panel reports
"""

import os
import requests
from requests.auth import HTTPBasicAuth
import sys
import simplejson as json
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


def get_report_selectable_variants(clinical_report_id):
    """Get report variants by location, id or simply all.
    """
    # Construct request
    url = "{}/reports/{}/selectable_variants"
    url = url.format(FABRIC_API_URL, clinical_report_id)

    # If target variants JSON is specified, post with the target variants JSON
    result = requests.get(url, params={'limit': 10000, 'format': 'vcf'}, auth=auth)
    return result


def main():
    """Main function. Get a clinical report by ID.
    """
    parser = argparse.ArgumentParser(description='Fetch a clinical report\'s variants')
    parser.add_argument('c', metavar='clinical_report_id', type=int)
    parser.add_argument('p', metavar='path', type=str)
    args = parser.parse_args()

    cr_id = args.c
    dest_path = args.p

    response = get_report_selectable_variants(cr_id)

    if response.status_code == 200:
        contents = response.content
        filename = response.headers.get('content-disposition').split('filename=')[-1]

        with open (os.path.join(dest_path, filename), 'w') as target_file:
            target_file.write(contents)
    else:
        print(response.text)

if __name__ == "__main__":
    main()

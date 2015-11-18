"""Get all clinical reports, or search for reports by accession id or genome id.
Example usages:
 python get_clinical_reports.py
 python get_clinical_reports.py --a ABCA4
 python get_clinical_reports.py --g 103
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


def get_clinical_reports(accession_id, genome_id):
    """Use the Omicia API to get all clinical reports
    """
    # Construct request
    url = "{}/reports/"
    if any([accession_id, genome_id]):
        url += "?"
    if accession_id:
        url += "accession_id={}&".format(accession_id)
    if genome_id:
        url += "genome_id={}&".format(genome_id)
    # Remove any trailing '&'
    if url.endswith('&'):
        url = url[:-1]
    url = url.format(OMICIA_API_URL)

    sys.stdout.flush()
    result = requests.get(url, auth=auth)
    return result.json()


def main():
    """Get all clinical reports.
    """
    parser = argparse.ArgumentParser(description='Fetch all clinical reports, or search '
                                                 'by accession id or genome id')
    parser.add_argument('--a', metavar='acccession_id', type=str, default=False)
    parser.add_argument('--g', metavar='genome_id', type=int, default=False)

    args = parser.parse_args()

    # Get query elements
    accession_id = args.a
    genome_id = args.g

    json_response = get_clinical_reports(accession_id, genome_id)
    print json_response

if __name__ == "__main__":
    main()

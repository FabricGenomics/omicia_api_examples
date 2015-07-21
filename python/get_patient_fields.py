"""Populate a report's custom fields.
Usage: post_patient_fields.py 2029 '{"Patient Name": "Eric", "Gender": "Male", "Accession Number": "1234"}'
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


def add_fields_to_cr(cr_id):
    """Use the Omicia API to fill in custom patient fields for a clinical report
    """
    #Construct request
    url = "{}/reports/{}/patient_fields"
    url = url.format(OMICIA_API_URL, cr_id)

    sys.stdout.flush()
    # If patient information was not provided, make a post request to reports
    # without a patient information parameter in the url
    result = requests.get(url, auth=auth)
    return result.json()


def main():
    """main function. Upload a specified VCF file to a specified project.
    """
    parser = argparse.ArgumentParser(description='View custom fields for existing clinical reports.')
    parser.add_argument('c', metavar='clinical_report_id', type=int)
    args = parser.parse_args()

    cr_id = args.c

    json_response = add_fields_to_cr(cr_id)
    print json_response

if __name__ == "__main__":
    main()

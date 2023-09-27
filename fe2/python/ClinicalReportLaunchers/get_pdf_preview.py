"""Populate a report's custom fields.
Usage: post_patient_fields.py 2029 '{"Patient Name": "Eric", "Gender": "Male", "Accession Number": "1234"}'
"""

import os
import requests
from requests.auth import HTTPBasicAuth
import sys
import json
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


def pdf_preview(cr_id):
    """Use the Omicia API to fill in custom patient fields for a clinical report
    """
    # Construct request
    url = "{}/reports/{}/pdf_preview"
    url = url.format(FABRIC_API_URL, cr_id)

    sys.stdout.write("Getting a PDF Preview...")
    sys.stdout.write("\n\n")
    sys.stdout.flush()
    response = requests.get(url, auth=auth)
    with open('report_{}.pdf'.format(cr_id), 'wb') as pdf_file:
        for block in response.iter_content(1024):
            pdf_file.write(block)
    sys.stdout.write("wrote report_{}.pdf\n".format(cr_id))


def main():
    """main function. Upload a specified VCF file to a specified project.
    """
    parser = argparse.ArgumentParser(description='Get PDF preview for current report.')
    parser.add_argument('c', metavar='clinical_report_id', type=int)
    args = parser.parse_args()

    cr_id = args.c

    pdf_preview(cr_id)

if __name__ == "__main__":
    main()

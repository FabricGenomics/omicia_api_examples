"""Add a quality control data entry to a clinical report.
Usage: post_qc_data.py 2029 '{"Cluster Density": "170", "Clusters PF": ".82"}'
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


def add_fields_to_cr(cr_id, qc_fields):
    """Use the Omicia API to fill in custom patient fields for a clinical report
    """
    #Construct request
    url = "{}/reports/{}/qc_data"
    url = url.format(OMICIA_API_URL, cr_id)
    url_payload = qc_fields

    sys.stdout.write("Adding quality control data entry to report...")
    sys.stdout.write("\n\n")
    sys.stdout.flush()
    # If patient information was not provided, make a post request to reports
    # without a patient information parameter in the url
    result = requests.post(url, auth=auth, data=url_payload)
    return result.json()


def main():
    """main function. Upload a specified VCF file to a specified project.
    """
    parser = argparse.ArgumentParser(description='Add a quality control data entry to a clinical report')
    parser.add_argument('c', metavar='clinical_report_id', type=int)
    parser.add_argument('f', metavar='qc_fields', type=str)
    args = parser.parse_args()

    cr_id = args.c
    qc_fields = args.f

    json_response = add_fields_to_cr(cr_id, qc_fields)
    print json.dumps(json_response, indent=4)

if __name__ == "__main__":
    main()

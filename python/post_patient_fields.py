"""Upload a genome to an existing project.
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
    url_payload = {'proband_genome_id': proband_genome_id,
                   'mother_genome_id': mother_genome_id,
                   'father_genome_id': father_genome_id,
                   'sibling_genome_id': sibling_genome_id,
                   'vaast_report_id': vaast_report_id}

    sys.stdout.write("Adding custom patient fields to report...")
    sys.stdout.write("\n\n")
    sys.stdout.flush()
    # If patient information was not provided, make a post request to reports
    # without a patient information parameter in the url
    result = requests.put(url, auth=auth, data=json.dumps(url_payload))
    return result.json()


def main(argv):
    """main function. Upload a specified VCF file to a specified project.
    """
    parser = argparse.ArgumentParser(description='Fill patient info fields for existing clinical reports.')
    parser.add_argument('c', metavar='clinical_report_id', type=int)
    args = parser.parse_args()

    cr_id = args.c

    json_response = add_fields_to_cr(cr_id)

if __name__ == "__main__":
    main(sys.argv[1:])

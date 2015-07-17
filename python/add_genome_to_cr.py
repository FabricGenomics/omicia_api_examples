"""Upload a genome to an existing project.
"""

import os
import json
import requests
from requests.auth import HTTPBasicAuth
import sys
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


def add_genome_to_clinical_report(clinical_report_id,
                                  proband_genome_id=None,
                                  mother_genome_id=None,
                                  father_genome_id=None,
                                  sibling_genome_id=None,
                                  vaast_report_id=None):
    """Use the Omicia API to add genome(s) to a clinical report
    """
    # Construct url and request
    url = "{}/reports/{}".format(OMICIA_API_URL, clinical_report_id)
    url_payload = {'proband_genome_id': proband_genome_id,
                   'mother_genome_id': mother_genome_id,
                   'father_genome_id': father_genome_id,
                   'sibling_genome_id': sibling_genome_id,
                   'vaast_report_id': vaast_report_id}

    sys.stdout.write("Adding genome(s) to report...")
    sys.stdout.write("\n\n")
    sys.stdout.flush()
    # If patient information was not provided, make a post request to reports
    # without a patient information parameter in the url
    result = requests.put(url, auth=auth, data=json.dumps(url_payload))
    return result.json()


def main(argv):
    """main function. Upload a specified VCF file to a specified project.
    """
    parser = argparse.ArgumentParser(description='Add genome ids or vaast report ids to existing clinical reports.')
    parser.add_argument('c', metavar='clinical_report_id', type=int)
    parser.add_argument('--p', metavar='proband_genome_id', type=int)
    parser.add_argument('--m', metavar='mother_genome_id', type=int)
    parser.add_argument('--f', metavar='father_genome_id', type=int)
    parser.add_argument('--s', metavar='sibling_genome_id', type=int)
    parser.add_argument('--v', metavar='vaast_report_id', type=int)
    args = parser.parse_args()

    cr_id = args.c
    proband_genome_id = args.p
    mother_genome_id = father_genome_id = sibling_genome_id = None
    mother_genome_id = args.m
    father_genome_id = args.f
    sibling_genome_id = args.s
    vaast_report_id = args.v

    json_response = add_genome_to_clinical_report(cr_id,
                                                  proband_genome_id=proband_genome_id,
                                                  mother_genome_id=mother_genome_id,
                                                  father_genome_id=father_genome_id,
                                                  sibling_genome_id=sibling_genome_id,
                                                  vaast_report_id=vaast_report_id)
    print json_response

if __name__ == "__main__":
    main(sys.argv[1:])

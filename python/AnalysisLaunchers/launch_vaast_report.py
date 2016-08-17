"""Launch a vaast solo or trio report for existing genomes, by genome ID.
"""

import csv
import simplejson as json
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


def launch_vaast_report(report_type,
                        proband_genome_id,
                        proband_sex,
                        father_genome_id,
                        mother_genome_id):
    """Launch a flexible family report. Return the JSON response.
    """
    # Construct url and request
    url = "{}/analysis/".format(OMICIA_API_URL)

    data_payload = {'report_type': report_type,
                    'proband_genome_id': proband_genome_id,
                    'proband_sex': proband_sex,
                    'mother_genome_id': mother_genome_id,
                    'father_genome_id': father_genome_id}

    result = requests.post(url, auth=auth, data=json.dumps(data_payload), verify=False)
    return result.json()


def main():
    """Launch a flexible family report.
    """
    parser = argparse.ArgumentParser(
        description='Launch a vaast solo or trio report.')
    parser.add_argument('report_type',
                        metavar='report_type',
                        type=str,
                        choices=['VAAST Solo', 'VAAST Trio'])
    parser.add_argument('--proband_genome_id', metavar='proband_genome_id', type=int)
    parser.add_argument('--proband_sex', metavar='proband_sex', type=str, choices=['m', 'f'])
    parser.add_argument('--mother_genome_id', metavar='mother_genome_id', type=int)
    parser.add_argument('--father_genome_id', metavar='father_genome_id', type=int)

    args = parser.parse_args()
    proband_genome_id = args.proband_genome_id
    proband_sex = args.proband_sex
    mother_genome_id = args.mother_genome_id
    father_genome_id = args.father_genome_id
    report_type = args.report_type

    vaast_report_json = launch_vaast_report(report_type,
                                            proband_genome_id,
                                            proband_sex,
                                            father_genome_id,
                                            mother_genome_id)
    sys.stdout.write(json.dumps(vaast_report_json, indent=4))


if __name__ == "__main__":
    main()

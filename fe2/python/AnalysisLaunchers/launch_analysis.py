"""Launch a phevor report, vaast solo or trio report for existing genomes,
by genome ID or vaast report ID.
"""

import csv
import simplejson as json
import os
import requests
from requests.auth import HTTPBasicAuth
import sys
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


def launch_analysis(report_type,
                    proband_genome_id,
                    proband_sex,
                    father_genome_id,
                    mother_genome_id,
                    sibling_genome_id,
                    sibling_sex,
                    sibling_affected,
                    hpo_terms=None,
                    proband_vaast_report_id=None):
    """Launch a flexible family report. Return the JSON response.
    """
    # Construct url and request
    url = "{}/analysis/".format(FABRIC_API_URL)

    data_payload = {'report_type': report_type,
                    'proband_genome_id': proband_genome_id,
                    'proband_sex': proband_sex,
                    'mother_genome_id': mother_genome_id,
                    'father_genome_id': father_genome_id,
                    'sibling_genome_id': sibling_genome_id,
                    'sibling_sex': sibling_sex,
                    'sibling_affected': sibling_affected,
                    'hpo_terms': hpo_terms,
                    'proband_vaast_report_id': proband_vaast_report_id}

    result = requests.post(url, auth=auth, data=json.dumps(data_payload))
    return result.json()


def main():
    """Launch a flexible family report.
    """
    parser = argparse.ArgumentParser(
        description='Launch a vaast solo or trio report.')
    parser.add_argument('report_type',
                        metavar='report_type',
                        type=str,
                        choices=['VAAST Solo Report', 'VAAST Trio Report', 'VAAST Quad Report', 'Phevor Report'])
    parser.add_argument('--proband_genome_id', metavar='proband_genome_id', type=int)
    parser.add_argument('--proband_sex', metavar='proband_sex', type=str, choices=['m', 'f'])
    # Proband VAAST Report ID is only necessary when running Phevor on an existing vaast run
    parser.add_argument('--proband_vaast_report_id', metavar='proband_vaast_report_id', type=int)
    parser.add_argument('--mother_genome_id', metavar='mother_genome_id', type=int)
    parser.add_argument('--father_genome_id', metavar='father_genome_id', type=int)
    parser.add_argument('--sibling_genome_id', metavar='sibling_genome_id', type=int)
    parser.add_argument('--sibling_sex', metavar='sibling_sex', type=str, choices=['m', 'f'])
    parser.add_argument('--sibling_affected', metavar='sibling_affected', type=str, choices=['true', 'false'])
    # HPO Terms should be a comma-separated list (e.g. 'HP:XXXXXX,HP:XXXXX')
    parser.add_argument('--hpo_terms', metavar='hpo_terms', type=str)

    args = parser.parse_args()
    proband_genome_id = args.proband_genome_id
    proband_sex = args.proband_sex
    proband_vaast_report_id = args.proband_vaast_report_id
    mother_genome_id = args.mother_genome_id
    father_genome_id = args.father_genome_id
    sibling_genome_id = args.sibling_genome_id
    sibling_sex = args.sibling_sex
    sibling_affected = args.sibling_affected == 'true'
    if not args.sibling_affected:
        sibling_affected = None

    report_type = args.report_type
    hpo_terms = args.hpo_terms

    vaast_report_json = launch_analysis(report_type,
                                        proband_genome_id,
                                        proband_sex,
                                        father_genome_id,
                                        mother_genome_id,
                                        sibling_genome_id,
                                        sibling_sex,
                                        sibling_affected,
                                        hpo_terms=hpo_terms,
                                        proband_vaast_report_id=proband_vaast_report_id)
    sys.stdout.write(json.dumps(vaast_report_json, indent=4))


if __name__ == "__main__":
    main()

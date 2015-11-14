"""Create a new family report with no genome
"""

import csv
import simplejson as json
import os
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

def launch_family_report(score_indels, reporting_cutoff, accession_id, sex, hpo_terms):
    """Launch a family report. Return the JSON response.
    """
    # Construct url and request
    url = "{}/reports/".format(OMICIA_API_URL)

    url_payload = {'report_type': "Trio",
                   'mother_genome_id': None,
                   'father_genome_id': None,
                   'proband_genome_id': None,
                   'proband_sex': sex,
                   'background': 'FULL',
                   'score_indels': bool(score_indels),
                   'reporting_cutoff': int(reporting_cutoff),
                   'accession_id': accession_id,
                   'hpo_terms': json.dumps(hpo_terms)}

    sys.stdout.write("Launching family report...\n")
    result = requests.post(url, auth=auth, data=json.dumps(url_payload))

    return result.json()


def main(argv):
    """Launch a family report with no genomes.
    """
    parser = argparse.ArgumentParser(
        description='Launch a family report with no genomes')
    parser.add_argument('indels', metavar='score_indels')
    parser.add_argument('cutoff', metavar='reporting_cutoff')
    parser.add_argument('acc', metavar='accession_id')
    parser.add_argument('sex', metavar='sex (m|f)')
    parser.add_argument('--hpo', metavar='hpo_terms')
    args = parser.parse_args()

    score_indels = args.indels
    reporting_cutoff = args.cutoff
    accession_id = args.acc
    sex = args.sex
    hpo_terms = args.hpo or None
    if hpo_terms is not None:
        hpo_terms = hpo_terms.split(',')

    family_report_json = launch_family_report(
        score_indels,
        reporting_cutoff,
        accession_id,
        sex,
        hpo_terms)

    # Confirm launched report data
    sys.stdout.write("\n")

    if "clinical_report" not in family_report_json.keys():
        print family_report_json
        sys.exit("Failed to launch. Check report parameters for correctness.")
    clinical_report = family_report_json['clinical_report']
    sys.stdout.write('Launched Family Report:\n'
                     'id: {}\n'
                     'test_type: {}\n'
                     'accession_id: {}\n'
                     'created_on: {}\n'
                     'created_by: {}\n'
                     'status: {}\n'
                     'filter_id: {}\n'
                     'panel_id: {}\n'
                     'hpo_terms: {}\n'
                     'filter_name: {}\n'
                     'workspace_id: {}\n'
                     'sample_collected_date: {}\n'
                     'sample_received_date: {}\n'
                     'include_cosmic: {}\n'
                     'vaast_report_id: {}\n'
                     'mother_genome_id: {}\n'
                     'father_genome_id: {}\n'
                     'genome_id: {}\n'
                     'version: {}\n'
                     .format(clinical_report.get('id', 'Missing'),
                             clinical_report.get('test_type','Missing'),
                             clinical_report.get('accession_id','Missing'),
                             clinical_report.get('created_on','Missing'),
                             clinical_report.get('created_by','Missing'),
                             clinical_report.get('status', 'Missing'),
                             clinical_report.get('filter_id','Missing'),
                             clinical_report.get('panel_id','Missing'),
                             clinical_report.get('hpo_terms', 'Missing'),
                             clinical_report.get('filter_name', 'Missing'),
                             clinical_report.get('workspace_id','Missing'),
                             clinical_report.get('sample_collected_date','Missing'),
                             clinical_report.get('sample_received_date','Missing'),
                             clinical_report.get('include_cosmic','Missing'),
                             clinical_report.get('vaast_report_id', 'Missing'),
                             clinical_report.get('mother_genome_id', 'Missing'),
                             clinical_report.get('father_genome_id', 'Missing'),
                             clinical_report.get('genome_id', 'Missing'),
                             clinical_report.get('version', 'Missing')))

if __name__ == "__main__":
    main(sys.argv[1:])

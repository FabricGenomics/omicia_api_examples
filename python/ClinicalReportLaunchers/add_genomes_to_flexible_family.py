"""Attach genomes to a clinical report using the new flexible family report nomenclature.
"""

import csv
import simplejson as json
import os
import requests
from requests.auth import HTTPBasicAuth
import sys
import argparse
import certifi

# Load environment variables for request authentication parameters
if "OMICIA_API_PASSWORD" not in os.environ:
    sys.exit("OMICIA_API_PASSWORD environment variable missing")

if "OMICIA_API_LOGIN" not in os.environ:
    sys.exit("OMICIA_API_LOGIN environment variable missing")

OMICIA_API_LOGIN = os.environ['OMICIA_API_LOGIN']
OMICIA_API_PASSWORD = os.environ['OMICIA_API_PASSWORD']
OMICIA_API_URL = os.environ.get('OMICIA_API_URL', 'https://api.fabricgenomics.com')
auth = HTTPBasicAuth(OMICIA_API_LOGIN, OMICIA_API_PASSWORD)


def add_genomes_to_clinical_report(clinical_report_id,
                                   proband,
                                   family_1,
                                   family_2,
                                   family_3,
                                   family_4,
                                   score_indels,
                                   reporting_cutoff,
                                   project_id,
                                   hpo_terms):
    """Launch a flexible family report. Return the JSON response.
    """
    # Construct url and request
    url = "{}/reports/{}".format(OMICIA_API_URL, clinical_report_id)

    if proband.get('genome_id') is None:
        proband = None
    if family_1.get('genome_id') is None:
        family_1 = None
    if family_2.get('genome_id') is None:
        family_2 = None
    if family_3.get('genome_id') is None:
        family_3 = None
    if family_4.get('genome_id') is None:
        family_4 = None

    data_payload = {'proband': proband,
                    'family_1': family_1,
                    'family_2': family_2,
                    'family_3': family_3,
                    'family_4': family_4,
                    'background': 'FULL',
                    'score_indels': score_indels,
                    'reporting_cutoff': reporting_cutoff,
                    'project_id': project_id,
                    'hpo_terms': json.dumps(hpo_terms) if hpo_terms else None}

    sys.stdout.write("Attaching genomes to clinical report...\n")
    result = requests.put(url, auth=auth, data=json.dumps(data_payload), verify=certifi.where())
    return result.json()


def main():
    """Launch a flexible family report.
    """
    parser = argparse.ArgumentParser(
        description='Launch a flexibly family report.')
    parser.add_argument('--proband_genome_id', metavar='proband_genome_id', type=int)
    parser.add_argument('--proband_sex', metavar='proband_sex', type=str, choices=['m', 'f'])

    parser.add_argument('--family_1_genome_id', metavar='family_1_genome_id', type=int)
    parser.add_argument('--family_1_sex', metavar='family_1_sex', type=str, choices=['m', 'f'])
    parser.add_argument('--family_1_affected', metavar='family_1_affected', type=int, choices=[0,1], default=None)
    parser.add_argument('--family_1_relationship', metavar='family_1_relationship', type=str, choices=['mother', 'father', 'sibling', 'other'])
    parser.add_argument('--family_1_label', metavar='family_1_label', type=str)

    parser.add_argument('--family_2_genome_id', metavar='family_2_genome_id', type=int)
    parser.add_argument('--family_2_sex', metavar='family_2_sex', type=str, choices=['m', 'f'])
    parser.add_argument('--family_2_affected', metavar='family_2_affected', type=int, choices=[0,1], default=None)
    parser.add_argument('--family_2_relationship', metavar='family_2_relationship', type=str, choices=['mother', 'father', 'sibling', 'other'])
    parser.add_argument('--family_2_label', metavar='family_2_label', type=str)

    parser.add_argument('--family_3_genome_id', metavar='family_3_genome_id', type=int)
    parser.add_argument('--family_3_sex', metavar='family_3_sex', type=str, choices=['m', 'f'])
    parser.add_argument('--family_3_affected', metavar='family_3_affected', type=int, choices=[0,1], default=None)
    parser.add_argument('--family_3_relationship', metavar='family_3_relationship', type=str, choices=['mother', 'father', 'sibling', 'other'])
    parser.add_argument('--family_3_label', metavar='family_3_label', type=str)

    parser.add_argument('--family_4_genome_id', metavar='family_4_genome_id', type=int)
    parser.add_argument('--family_4_sex', metavar='family_4_sex', type=str, choices=['m', 'f'])
    parser.add_argument('--family_4_affected', metavar='family_4_affected', type=int, choices=[0,1], default=None)
    parser.add_argument('--family_4_relationship', metavar='family_4_relationship', type=str, choices=['mother', 'father', 'sibling', 'other'])
    parser.add_argument('--family_4_label', metavar='family_4_label', type=str)

    parser.add_argument('--indels', metavar='score_indels', type=int, choices=[0,1], default=0)
    parser.add_argument('--cutoff', metavar='reporting_cutoff', type=int)
    parser.add_argument('clinical_report_id', metavar='clinical_report_id')
    parser.add_argument('--project_id', metavar='project_id', type=int)
    parser.add_argument('--hpo', metavar='hpo_terms')
    args = parser.parse_args()

    proband = {
        'genome_id': args.proband_genome_id,
        'sex': args.proband_sex
    }

    family_1 = {
        'genome_id': args.family_1_genome_id,
        'sex': args.family_1_sex,
        'affected': bool(args.family_1_affected) if args.family_1_affected in [0, 1] else None,
        'relationship': args.family_1_relationship,
        'label': args.family_1_label
    }

    family_2 = {
        'genome_id': args.family_2_genome_id,
        'sex': args.family_2_sex,
        'affected': bool(args.family_2_affected) if args.family_2_affected in [0, 1] else None,
        'relationship': args.family_2_relationship,
        'label': args.family_2_label
    }

    family_3 = {
        'genome_id': args.family_3_genome_id,
        'sex': args.family_3_sex,
        'affected': bool(args.family_3_affected) if args.family_3_affected in [0, 1] else None,
        'relationship': args.family_3_relationship,
        'label': args.family_3_label
    }

    family_4 = {
        'genome_id': args.family_4_genome_id,
        'sex': args.family_4_sex,
        'affected': bool(args.family_4_affected) if args.family_4_affected in [0, 1] else None,
        'relationship': args.family_4_relationship,
        'label': args.family_4_label
    }

    score_indels = bool(args.indels)
    reporting_cutoff = args.cutoff
    clinical_report_id = args.clinical_report_id
    project_id = args.project_id
    hpo_terms = args.hpo or None
    if hpo_terms is not None:
        hpo_terms = hpo_terms.split(',')

    family_report_json = add_genomes_to_clinical_report(
        clinical_report_id,
        proband,
        family_1,
        family_2,
        family_3,
        family_4,
        score_indels,
        reporting_cutoff,
        project_id,
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
                     'members: {}\n'
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
                             json.dumps(clinical_report.get('members', '{}'), indent=1),
                             clinical_report.get('genome_id', 'Missing'),
                             clinical_report.get('version', 'Missing')))

if __name__ == "__main__":
    main()

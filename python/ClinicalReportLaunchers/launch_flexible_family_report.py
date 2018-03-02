"""Create a new flexible family report.
"""

import certifi
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
OMICIA_API_URL = os.environ.get('OMICIA_API_URL', 'https://api.fabricgenomics.com')
auth = HTTPBasicAuth(OMICIA_API_LOGIN, OMICIA_API_PASSWORD)


def launch_family_report(report_type,
                         proband,
                         family_1,
                         family_2,
                         family_3,
                         family_4,
                         score_indels, reporting_cutoff, accession_id, project_id, hpo_terms):
    """Launch a flexible family report. Return the JSON response.
    """
    # Construct url and request
    url = "{}/reports/".format(OMICIA_API_URL)

    data_payload = {'report_type': report_type,
                    'proband': proband,
                    'family_1': family_1,
                    'family_2': family_2,
                    'family_3': family_3,
                    'family_4': family_4,
                    'background': 'FULL',
                    'score_indels': score_indels,
                    'reporting_cutoff': reporting_cutoff,
                    'accession_id': accession_id,
                    'project_id': project_id,
                    'hpo_terms': json.dumps(hpo_terms) if hpo_terms else None}

    sys.stdout.write("Launching flexible family report...\n")
    result = requests.post(url, auth=auth, data=json.dumps(data_payload), verify=certifi.where())
    return result.json()


def main():
    """Launch a flexible family report.
    """
    parser = argparse.ArgumentParser(
        description='Launch a flexibly family report.')
    parser.add_argument('report_type',
                        metavar='report_type',
                        type=str,
                        choices=['Solo', 'Duo', 'Trio', 'Quad', 'Quintet'])
    parser.add_argument('--proband_genome_id', metavar='proband_genome_id', type=int)
    parser.add_argument('--proband_sex', metavar='proband_sex', type=str, choices=['m', 'f'])

    parser.add_argument('--family_1_genome_id', metavar='family_1_genome_id', type=int)
    parser.add_argument('--family_1_sex', metavar='family_1_sex', type=str, choices=['m', 'f'])
    parser.add_argument('--family_1_affected', metavar='family_1_affected', type=bool)
    parser.add_argument('--family_1_relationship', metavar='family_1_relationship', type=str, choices=['mother', 'father', 'sibling', 'other'])
    parser.add_argument('--family_1_label', metavar='family_1_label', type=str)

    parser.add_argument('--family_2_genome_id', metavar='family_2_genome_id', type=int)
    parser.add_argument('--family_2_sex', metavar='family_2_sex', type=str, choices=['m', 'f'])
    parser.add_argument('--family_2_affected', metavar='family_2_affected', type=bool)
    parser.add_argument('--family_2_relationship', metavar='family_2_relationship', type=str, choices=['mother', 'father', 'sibling', 'other'])
    parser.add_argument('--family_2_label', metavar='family_2_label', type=str)

    parser.add_argument('--family_3_genome_id', metavar='family_3_genome_id', type=int)
    parser.add_argument('--family_3_sex', metavar='family_3_sex', type=str, choices=['m', 'f'])
    parser.add_argument('--family_3_affected', metavar='family_3_affected', type=bool)
    parser.add_argument('--family_3_relationship', metavar='family_3_relationship', type=str, choices=['mother', 'father', 'sibling', 'other'])
    parser.add_argument('--family_3_label', metavar='family_3_label', type=str)

    parser.add_argument('--family_4_genome_id', metavar='family_4_genome_id', type=int)
    parser.add_argument('--family_4_sex', metavar='family_4_sex', type=str, choices=['m', 'f'])
    parser.add_argument('--family_4_affected', metavar='family_4_affected', type=bool)
    parser.add_argument('--family_4_relationship', metavar='family_4_relationship', type=str, choices=['mother', 'father', 'sibling', 'other'])
    parser.add_argument('--family_4_label', metavar='family_4_label', type=str)

    parser.add_argument('--indels', metavar='score_indels', type=bool, default=False)
    parser.add_argument('--cutoff', metavar='reporting_cutoff', type=int)
    parser.add_argument('acc', metavar='accession_id')
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
        'affected': args.family_1_affected,
        'relationship': args.family_1_relationship,
        'label': args.family_1_label
    }

    family_2 = {
        'genome_id': args.family_2_genome_id,
        'sex': args.family_2_sex,
        'affected': args.family_2_affected,
        'relationship': args.family_2_relationship,
        'label': args.family_2_label
    }

    family_3 = {
        'genome_id': args.family_3_genome_id,
        'sex': args.family_3_sex,
        'affected': args.family_3_affected,
        'relationship': args.family_3_relationship,
        'label': args.family_3_label
    }

    family_4 = {
        'genome_id': args.family_4_genome_id,
        'sex': args.family_4_sex,
        'affected': args.family_4_affected,
        'relationship': args.family_4_relationship,
        'label': args.family_4_label
    }

    report_type = args.report_type
    score_indels = args.indels
    reporting_cutoff = args.cutoff
    accession_id = args.acc
    project_id = args.project_id
    hpo_terms = args.hpo or None
    if hpo_terms is not None:
        hpo_terms = hpo_terms.split(',')

    family_report_json = launch_family_report(
        report_type,
        proband,
        family_1,
        family_2,
        family_3,
        family_4,
        score_indels,
        reporting_cutoff,
        accession_id,
        project_id,
        hpo_terms)

    # Confirm launched report data
    sys.stdout.write("\n")

    if "clinical_report" not in family_report_json.keys():
        print family_report_json
        sys.exit("Failed to launch. Check report parameters for correctness.")
    clinical_report = family_report_json['clinical_report']
    sys.stdout.write(json.dumps(clinical_report, indent=4))

if __name__ == "__main__":
    main()

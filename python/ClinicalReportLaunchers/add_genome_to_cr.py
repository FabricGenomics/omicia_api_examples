"""Add genomes to an existing clinical report.
Example usages:

* Adding male proband genome (id = 1) to a solo or panel report (clinical_report_id = 100)
    python add_genome_to_cr.py --p 1 --sex m 100

* Adding female proband (id =1), mother (id = 2) and father genome (id = 3) to a family or panel
  trio report (clinical_report_id = 100)
    python add_genome_to_cr.py --p 1 --sex f --f 2 --m 3 1000

Sample console output:

Adding genome(s) to report...

Clinical Report Info:
id: 3340
test_type: panel
accession_id: PGX15-010311
created_on: 2015-11-18T17:02:39
created_by: 185
status: WAITING
filter_id: None
panel_id: 1987
filter_name: None
workspace_id: 233
sample_collected_date: None
sample_received_date: None
include_cosmic: False
vaast_report_id: None
mother_genome_id: None
father_genome_id: None
genome_id: 206164
version: 4

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
                                  proband_sex=None,
                                  mother_genome_id=None,
                                  father_genome_id=None,
                                  sibling_genome_id=None,
                                  sibling_affected=None,
                                  duo_relation_genome_id=None,
                                  duo_relation_affected=None,
                                  vaast_report_id=None):
    """Use the Omicia API to add genome(s) to a clinical report
    """
    # Construct url and request
    url = "{}/reports/{}".format(OMICIA_API_URL, clinical_report_id)
    url_payload = {'proband_genome_id': proband_genome_id,
                   'proband_sex': proband_sex,
                   'mother_genome_id': mother_genome_id,
                   'father_genome_id': father_genome_id,
                   'sibling_genome_id': sibling_genome_id,
                   'sibling_affected': sibling_affected,
                   'duo_relation_genome_id': duo_relation_genome_id,
                   'duo_relation_affected': duo_relation_affected,
                   'vaast_report_id': vaast_report_id}

    sys.stdout.write("Adding genome(s) to report...")
    sys.stdout.write("\n\n")
    sys.stdout.flush()
    result = requests.put(url, auth=auth, data=json.dumps(url_payload))
    return result.json()


def main():
    """Main function. Add genomes and metadata to an existing clinical report.
    """
    parser = argparse.ArgumentParser(description='Add genome ids or vaast report ids to existing clinical reports.')
    parser.add_argument('c', metavar='clinical_report_id', type=int)
    parser.add_argument('--p', metavar='proband_genome_id', type=int)
    parser.add_argument('--m', metavar='mother_genome_id', type=int)
    parser.add_argument('--f', metavar='father_genome_id', type=int)
    parser.add_argument('--s', metavar='sibling_genome_id', type=int)
    parser.add_argument('--sibling_affected', metavar='sibling_affected', type=str, choices=['true', 'false'])
    parser.add_argument('--d', metavar='duo_relation_genome_id', type=int)
    parser.add_argument('--duo_affected', metavar='duo_relation_affected', type=str, choices=['true', 'false'])
    parser.add_argument('--v', metavar='vaast_report_id', type=int)
    parser.add_argument('--sex', metavar='sex', type=str, choices=['f', 'm'])
    args = parser.parse_args()

    cr_id = args.c
    proband_genome_id = args.p
    mother_genome_id = args.m
    father_genome_id = args.f
    sibling_genome_id = args.s
    sibling_affected = args.sibling_affected
    duo_relation_genome_id = args.d
    duo_relation_affected = args.duo_affected
    vaast_report_id = args.v
    proband_sex = args.sex

    json_response = add_genome_to_clinical_report(cr_id,
                                                  proband_genome_id=proband_genome_id,
                                                  proband_sex=proband_sex,
                                                  mother_genome_id=mother_genome_id,
                                                  father_genome_id=father_genome_id,
                                                  sibling_genome_id=sibling_genome_id,
                                                  sibling_affected=sibling_affected,
                                                  duo_relation_genome_id=duo_relation_genome_id,
                                                  duo_relation_affected=duo_relation_affected,
                                                  vaast_report_id=vaast_report_id)
    if "clinical_report" not in json_response.keys():
        sys.stderr(json_response)
        sys.exit("Failed to launch. Check report parameters for correctness.")
    clinical_report = json_response['clinical_report']
    sys.stdout.write('Clinical Report Info:\n'
                     'id: {}\n'
                     'test_type: {}\n'
                     'accession_id: {}\n'
                     'created_on: {}\n'
                     'created_by: {}\n'
                     'status: {}\n'
                     'filter_id: {}\n'
                     'panel_id: {}\n'
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
    main()

"""Add a genome to an existing (genomeless) panel report.
"""

import os
import json
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


def add_genome_to_clinical_report(clinical_report_id,
                                  proband_genome_id=None,
                                  proband_sex=None):
    """Use the Omicia API to add genome(s) to a clinical report
    """
    # Construct url and request
    url = "{}/reports/{}".format(OMICIA_API_URL, clinical_report_id)
    url_payload = {
        'proband_genome_id': proband_genome_id,
        'proband_sex': proband_sex
    }

    sys.stdout.write("Adding genome(s) to report...")
    sys.stdout.write("\n\n")
    sys.stdout.flush()
    result = requests.put(url, auth=auth, data=json.dumps(url_payload))
    return result.json()


def upload_genome_to_project(project_id, label, sex, file_format, file_name, external_id=""):
    """Use the Omicia API to add a genome, in vcf format, to a project.
    Returns the newly uploaded genome's id.
    """

    #Construct request
    url = "{}/projects/{}/genomes?genome_label={}&genome_sex={}&external_id={}\
           &assembly_version=hg19&format={}"
    url = url.format(OMICIA_API_URL, project_id, label, sex, external_id, file_format)

    sys.stdout.write("Uploading genome...\n")
    with open(file_name, 'rb') as file_handle:
        #Post request and return id of newly uploaded genome
        result = requests.put(url, auth=auth, data=file_handle, verify=False)
        return result.json()


def main():
    """Main function. Add genomes and metadata to an existing clinical report.
    """
    parser = argparse.ArgumentParser(description='Add genome ids or vaast report ids to existing clinical reports.')
    parser.add_argument('clinical_report_id', metavar='clinical_report_id', type=int)
    parser.add_argument('project_id', metavar='project_id', type=int)
    parser.add_argument('genome_label', metavar='genome_label', type=str)
    parser.add_argument('sex', metavar='sex', type=str, choices=['female', 'male', 'unspecified'])
    parser.add_argument('file_format', metavar='file_format', type=str, choices=['vcf', 'vcf.gz', 'vcf.bz2'])
    parser.add_argument('file_name', metavar='file_name', type=str)
    parser.add_argument('--genome_external_id', metavar='genome_external_id', type=str)
    args = parser.parse_args()

    cr_id = args.clinical_report_id
    project_id = args.project_id
    genome_label = args.genome_label
    sex = args.sex
    file_format = args.file_format
    file_name = args.file_name
    genome_external_id = args.genome_external_id

    genome_json = upload_genome_to_project(project_id,
                                           genome_label,
                                           sex,
                                           file_format,
                                           file_name,
                                           genome_external_id)

    try:
        genome_id = genome_json["genome_id"]
        sys.stdout.write("genome_id: {}\n".format(genome_id))
    except KeyError:
        if genome_json['description']:
            sys.stdout.write('Error: {}\n'.format(genome_json['description']))
        else:
            sys.stdout.write('Something went wrong...')
        sys.exit("Exiting...")

    if sex == 'male':
        proband_sex = 'm'
    elif sex == 'female':
        proband_sex = 'f'
    else:
        proband_sex = 'u'

    json_response = add_genome_to_clinical_report(cr_id,
                                                  proband_genome_id=genome_id,
                                                  proband_sex=sex,
                                                  )
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

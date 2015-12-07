"""Upload a genome to an existing project.
"""

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


def upload_genome_to_project(project_id, sex, file_format, file_path, label="", external_id=""):
    """Use the Omicia API to add a genome, in vcf format, to a project.
    Returns the newly uploaded genome's id.
    """
    # Construct request
    url = "{}/projects/{}/genomes?genome_label={}&genome_sex={}&external_id={}\
           &assembly_version=hg19&format={}&file_path={}"
    url = url.format(OMICIA_API_URL, project_id, label, sex, external_id, file_format, file_path)

    sys.stdout.write("Linking...\n")
    # Post request and return id of newly uploaded genome
    result = requests.put(url, auth=auth)
    return result.json()


def main():
    """main function. Upload a specified VCF file to a specified project.
    """
    parser = argparse.ArgumentParser(
        description='Create or edit a panel. Name and description must be '
                    'specified for panel creation. Panel id must be '
                    'specified for panel editing.')
    parser.add_argument('project_id', metavar='project_id', type=int)
    parser.add_argument('--label', metavar='label', type=str)
    parser.add_argument('sex', metavar='sex', type=str, choices=['male', 'female', 'unspecified'])
    parser.add_argument('file_format', metavar='file_format', type=str)
    parser.add_argument('file_path', metavar='file_path', type=str)
    parser.add_argument('--external_id', metavar='external_id', type=str)
    args = parser.parse_args()

    project_id = args.project_id
    label = args.label
    sex = args.sex
    file_format = args.file_format
    file_path = args.file_path
    external_id = args.external_id

    json_response = upload_genome_to_project(project_id,
                                             sex,
                                             file_format,
                                             file_path,
                                             label=label,
                                             external_id=external_id)

    try:
        genome_object = json_response
        sys.stdout.write("genome_label: {}, genome_id: {}, size: {}\n"
                         .format(genome_object.get('genome_label', 'Missing'),
                                 genome_object.get('genome_id', 'Missing'),
                                 genome_object.get('size', 'Missing')))
    except KeyError:
        if json_response['description']:
            sys.stdout.write('Error: {}\n'.format(json_response['description']))
        else:
            sys.stdout.write('Something went wrong...')

if __name__ == "__main__":
    main()

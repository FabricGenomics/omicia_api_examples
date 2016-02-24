"""Upload a genome to an existing project.
"""
import argparse
import os
import requests
from requests.auth import HTTPBasicAuth
import sys

# Load environment variables for request authentication parameters
if "OMICIA_API_PASSWORD" not in os.environ:
    sys.exit("OMICIA_API_PASSWORD environment variable missing")

if "OMICIA_API_LOGIN" not in os.environ:
    sys.exit("OMICIA_API_LOGIN environment variable missing")

OMICIA_API_LOGIN = os.environ['OMICIA_API_LOGIN']
OMICIA_API_PASSWORD = os.environ['OMICIA_API_PASSWORD']
OMICIA_API_URL = os.environ.get('OMICIA_API_URL', 'https://api.omicia.com')
auth = HTTPBasicAuth(OMICIA_API_LOGIN, OMICIA_API_PASSWORD)


def upload_genome_to_project(project_id, label, sex, file_format, file_name, bam_file,
                             external_id=""):
    """Use the Omicia API to add a genome, in vcf format, to a project.
    Returns the newly uploaded genome's id.
    """
    # Construct request
    url = "{}/projects/{}/genomes?genome_label={}&genome_sex={}&external_id={}\
           &assembly_version=hg19&format={}"
    url = url.format(OMICIA_API_URL, project_id, label, sex, external_id, file_format)

    if bam_file is not None:
        url = "{}&bam_file={}".format(url, bam_file)

    sys.stdout.write("Uploading genome...\n")
    with open(file_name, 'rb') as file_handle:
        # Post request and return id of newly uploaded genome
        result = requests.put(url, auth=auth, data=file_handle, verify=False)
        return result.json()


def main():
    """Main function. Upload a specified VCF file to a specified project.
    """
    parser = argparse.ArgumentParser(description='Upload a genome.')
    parser.add_argument('project_id', metavar='project_id')
    parser.add_argument('label', metavar='label')
    parser.add_argument('sex', metavar='sex')
    parser.add_argument('file_format', metavar='file_format')
    parser.add_argument('file_name', metavar='file_name')
    parser.add_argument('--external_id', metavar='external_id')
    parser.add_argument('--bam_file', metavar='bam_file')
    args = parser.parse_args()

    project_id = args.project_id
    label = args.label
    sex = args.sex
    file_format = args.file_format
    file_name = args.file_name
    external_id = args.external_id
    bam_file = args.bam_file

    json_response = upload_genome_to_project(project_id, label, sex,
                                             file_format, file_name, bam_file,
                                             external_id=external_id)
    try:
        genome_id = json_response["genome_id"]
        sys.stdout.write("genome_id: {}\n".format(genome_id))
    except KeyError:
        if json_response.get('description'):
            sys.stdout.write('Error: {}\n'.format(json_response.get('description')))
        else:
            sys.stdout.write('Something went wrong...')

if __name__ == "__main__":
    main()

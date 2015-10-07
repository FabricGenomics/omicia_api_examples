"""Upload a genome to an existing project.
"""

import os
import requests
from requests.auth import HTTPBasicAuth
import sys

#Load environment variables for request authentication parameters
if "OMICIA_API_PASSWORD" not in os.environ:
    sys.exit("OMICIA_API_PASSWORD environment variable missing")

if "OMICIA_API_LOGIN" not in os.environ:
    sys.exit("OMICIA_API_LOGIN environment variable missing")

OMICIA_API_LOGIN = os.environ['OMICIA_API_LOGIN']
OMICIA_API_PASSWORD = os.environ['OMICIA_API_PASSWORD']
OMICIA_API_URL = os.environ.get('OMICIA_API_URL', 'https://api.omicia.com')
auth = HTTPBasicAuth(OMICIA_API_LOGIN, OMICIA_API_PASSWORD)


def upload_genome_to_project(project_id, label, sex, file_format, file_path, external_id=""):
    """Use the Omicia API to add a genome, in vcf format, to a project.
    Returns the newly uploaded genome's id.
    """

    assert(os.path.exists(file_path))

    #Construct request
    url = "{}/projects/{}/genomes?genome_label={}&genome_sex={}&external_id={}\
           &assembly_version=hg19&format={}&file_path={}"
    url = url.format(OMICIA_API_URL, project_id, label, sex, external_id, file_format, file_path)

    sys.stdout.write("Linking...\n")
    #Post request and return id of newly uploaded genome
    result = requests.put(url, auth=auth)
    return result.json()


def main(argv):
    """main function. Upload a specified VCF file to a specified project.
    """
    if len(argv) < 5:
        sys.exit("Usage: python upload_genome.py <project_id> <label>"
                 "<sex (male|female|unspecified)> <format> <file_path>")
    project_id = argv[0]
    label = argv[1]
    sex = argv[2]
    file_format = argv[3]
    file_path = argv[4]
    if len(argv) > 5:
        external_id = argv[5]
    else:
        external_id = ""
    json_response = upload_genome_to_project(project_id, label, sex,
                                             file_format, file_path, external_id)

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
    main(sys.argv[1:])

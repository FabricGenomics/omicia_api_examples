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


def upload_genome_to_project(project_id, label, sex, file_format, file_name, external_id=""):
    """Use the Omicia API to add a genome, in vcf format, to a project.
    Returns the newly uploaded genome's id.
    """

    #Construct request
    url = "{}/projects/{}/genomes?genome_label={}&genome_sex={}&external_id={}\
           &assembly_version=hg19&format={}"
    url = url.format(OMICIA_API_URL, project_id, label, sex, external_id, file_format)

    sys.stdout.write("Uploading genome...")
    with open(file_name, 'rb') as file_handle:
        #Post request and return id of newly uploaded genome
        result = requests.put(url, auth=auth, data=file_handle)
        return result.json()["genome_id"]


def main(argv):
    """main function. Upload a specified VCF file to a specified project.
    """
    if len(argv) < 5:
        sys.exit("Usage: python upload_genome.py <project_id> <label>"
                 "<sex (male|female|unspecified)> <format> <file.vcf>")
    project_id = argv[0]
    label = argv[1]
    sex = argv[2]
    file_format = argv[3]
    file_name = argv[4]
    if len(argv) > 5:
        external_id = argv[5]
    else:
        external_id = ""
    genome_id = upload_genome_to_project(project_id, label, sex,
                                         file_format, file_name, external_id)
    sys.stdout.write("genome_id: {}".format(genome_id))

if __name__ == "__main__":
    main(sys.argv[1:])

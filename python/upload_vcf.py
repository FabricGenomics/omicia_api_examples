"""Upload a genome to an existing project.
"""

import json
import os
import requests
from requests.auth import HTTPBasicAuth
import sys

#Load environment variables for request authentication parameters
OMICIA_API_LOGIN = os.environ['OMICIA_API_LOGIN']
OMICIA_API_PASSWORD = os.environ['OMICIA_API_PASSWORD']
OMICIA_API_URL = os.environ['OMICIA_API_URL']


def upload_genome_to_project(project_id, label, sex, file_format, file_name):
    """Use the Omicia API to add a genome, in vcf format, to a project.
    Returns the newly uploaded genome's id.
    """

    #Construct request
    url = "{}/projects/{}/genomes?genome_label={}&genome_sex={}" \
          "&assembly_version=hg19&format={}"
    url = url.format(OMICIA_API_URL, project_id, label, sex, file_format)

    with open(file_name, 'rb') as file_handle:
        files = {'file_name': file_handle}
        auth = HTTPBasicAuth(OMICIA_API_LOGIN, OMICIA_API_PASSWORD)
        #Post request and return id of newly uploaded genome
        result = requests.put(url, files=files, auth=auth)
        json_data = json.loads(result.text)
        return json_data["genome_id"]


def main(argv):
    """main function. Upload a specified VCF file to a specified project.
    """
    if len(argv) != 5:
        sys.exit("Usage: python upload_vcf.py <project_id> <label>"
                 "<sex> <format> <file.vcf>")
    project_id = argv[0]
    label = argv[1]
    sex = argv[2]
    file_format = argv[3]
    file_name = argv[4]
    genome_id = upload_genome_to_project(project_id, label, sex, \
    	                                file_format, file_name)
    print genome_id

if __name__ == "__main__":
    main(sys.argv[1:])

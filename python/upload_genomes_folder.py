"""Upload multiple genomes to an existing project from a folder.
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


def get_genome_files(folder):
    """Return a dict of .vcf, .vcf.gz, and vcf.bz2 genomes in a given folder
    """
    genome_files = []
    for file_name in os.listdir(folder):
        if file_name.endswith(".vcf"):
            genome_file_extension = "vcf"
        elif file_name.endswith(".vcf.gz"):
            genome_file_extension = "vcf.gz"
        elif file_name.endswith(".vcf.bz2"):
            genome_file_extension = "vcf.bz2"
        else:
            genome_file_extension = None
        if genome_file_extension:
            genome_info = {"name": file_name,
                           "format": genome_file_extension,
                           "assembly_version": "hg19",
                           "genome_sex": "unspecified",
                           "genome_label": file_name[0:100]}
            genome_files.append(genome_info)
    return genome_files


def upload_genomes_to_project(project_id, folder):
    """upload all of the genomes in the given folder to the project with
    the given project id
    """
    # Construct request
    genome_files = get_genome_files(folder)
    # List where returned genome JSON information will be stored
    genome_json_objects = []

    for genome_file in genome_files:
        url = "{}/projects/{}/genomes?genome_label={}&genome_sex={}&external_id=\
               &assembly_version=hg19&format={}"
        url = url.format(OMICIA_API_URL,
                         project_id,
                         genome_file["genome_label"],
                         genome_file["genome_sex"],
                         genome_file["format"])

        with open(folder + "/" + genome_file["name"], 'rb') as file_handle:
            files = {'file_name': file_handle}
            auth = HTTPBasicAuth(OMICIA_API_LOGIN, OMICIA_API_PASSWORD)
            # Post request and store id of newly uploaded genome
            result = requests.put(url, files=files, auth=auth)
            json_data = json.loads(result.text)
            genome_json_objects.append(json_data)
    return genome_json_objects


def main(argv):
    """main function. Upload VCF files from a folder to a specified project.
    """
    if len(argv) < 2:
        sys.exit("Usage: python upload_vcf.py <project_id> <folder>")
    project_id = argv[0]
    folder = argv[1]

    genome_objects = upload_genomes_to_project(project_id, folder)

    # Output genome labels, ids, and sizes
    for genome_object in genome_objects:
        print {"genome_label": genome_object["genome_label"],
               "genome_id": genome_object["genome_id"],
               "size": genome_object["size"]}


if __name__ == "__main__":
    main(sys.argv[1:])
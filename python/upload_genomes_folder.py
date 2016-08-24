"""Upload multiple genomes to an existing project from a folder.
"""
import argparse
import os
import requests
from requests.auth import HTTPBasicAuth
import sys
import simplejson as json

# Load environment variables for request authentication parameters
if "OMICIA_API_PASSWORD" not in os.environ:
    sys.exit("OMICIA_API_PASSWORD environment variable missing")

if "OMICIA_API_LOGIN" not in os.environ:
    sys.exit("OMICIA_API_LOGIN environment variable missing")

OMICIA_API_LOGIN = os.environ['OMICIA_API_LOGIN']
OMICIA_API_PASSWORD = os.environ['OMICIA_API_PASSWORD']
OMICIA_API_URL = os.environ.get('OMICIA_API_URL', 'https://api.omicia.com')
auth = HTTPBasicAuth(OMICIA_API_LOGIN, OMICIA_API_PASSWORD)


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
            continue
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
    # List where returned genome JSON information will be stored
    genome_json_objects = []

    for genome_file in get_genome_files(folder):
        url = "{}/projects/{}/genomes?genome_label={}&genome_sex={}&external_id=&assembly_version=hg19&format={}"
        url = url.format(OMICIA_API_URL,
                         project_id,
                         genome_file["genome_label"],
                         genome_file["genome_sex"],
                         genome_file["format"])

        with open(folder + "/" + genome_file["name"], 'rb') as file_handle:
            # Post request and store id of newly uploaded genome
            result = requests.put(url, auth=auth, data=file_handle, verify=False)
            genome_json_objects.append(result.json())
    return genome_json_objects


def main():
    """Main function. Upload VCF files from a folder to a specified project.
    """
    parser = argparse.ArgumentParser(description='Upload a folder of genomes.')
    parser.add_argument('project_id', metavar='project_id')
    parser.add_argument('folder', metavar='folder')
    args = parser.parse_args()

    project_id = args.project_id
    folder = args.folder

    genome_objects = upload_genomes_to_project(project_id, folder)

    sys.stdout.write(json.dumps(genome_objects, indent=4))


if __name__ == "__main__":
    main()
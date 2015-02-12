"""Upload multiple genomes to an existing project from a folder,
using a manifest to outline each genome's attributes. The manifest
must contain five columns with headers. The first column should
contain the genome filename, the second the genome label, the third
the genome's internal_id, the fourth its sex ('male', 'female' or
'unspecified', and the fifth should contain its format ('vcf', 'vcf.gz',
or 'vcf.b2z'). This manifest must be stored in the same folder as
all of the genomes it describes, and must be named 'manifest.csv.'

Example:

"""

import csv
import json
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


def get_manifest_info(folder):
    """Generate an object containing the data from the manifest.csv
    file in the genomes folder, including each filename along with
    its genome label, external id, sex, and format.
    """

    # First check to make sure there is in fact a manifest.csv file
    if 'manifest.csv' not in os.listdir(folder):
        sys.exit("No manifest.csv file in folder provided.")

    manifest_info = {}
    with open(folder + '/manifest.csv') as f:
        reader = csv.reader(f)
        next(reader, None)  # Skip the header
        for row in reader:
            genome_filename = row[0]
            manifest_info[genome_filename] = {"genome_label": row[1],
                                               "external_id": row[2],
                                               "genome_sex": row[3],
                                               "format": row[4]}
    return manifest_info


def upload_genomes_to_project(project_id, folder):
    """upload all of the genomes in the given folder to the project with
    the given project id
    """

    # Assuming there is a manifest file, generate an object containing its info
    manifest_info = get_manifest_info(folder)

    # List where returned genome JSON information will be stored
    genome_json_objects = []

    # Upload each genome to the desired project
    sys.stdout.write("Uploading")
    for genome_file_name in manifest_info.keys():
        genome_attrs = manifest_info[genome_file_name]
        url = "{}/projects/{}/genomes?genome_label={}&genome_sex={}&external_id={}&assembly_version=hg19&format={}"
        url = url.format(OMICIA_API_URL,
                         project_id,
                         genome_attrs["genome_label"],
                         genome_attrs["genome_sex"],
                         genome_attrs["external_id"],
                         genome_attrs["format"])

        with open(folder + "/" + genome_file_name, 'rb') as file_handle:
            # Post request and store newly uploaded genome's information
            result = requests.put(url, auth=auth, data=file_handle)
            sys.stdout.write(".")
            sys.stdout.flush()
            genome_json_objects.append(result.json())
    sys.stdout.write("\n")
    return genome_json_objects


def main(argv):
    """Main function. Upload VCF files from a folder to a specified project,
    using a manifest to specify each genome's attributes.
    """
    if len(argv) != 2:
        sys.exit("Usage: python upload_genomes_folder_with_manifest.py <project_id> <folder>")
    project_id = argv[0]
    folder = argv[1]

    genome_objects = upload_genomes_to_project(project_id, folder)

    # Output genome labels, ids, external ids, and sizes
    for genome_object in genome_objects:
        sys.stdout.write("genome_label: {}, genome_id: {}, external_id: {}, size: {} \n"
                         .format(genome_object.get('genome_label', 'Missing'),
                                 genome_object.get('genome_id', 'Missing'),
                                 genome_object.get('external_id', 'Missing'),
                                 genome_object.get('size', 'Missing')))

if __name__ == "__main__":
    main(sys.argv[1:])
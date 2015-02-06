"""Upload multiple genomes to an existing project from a folder,
using a manifest to outline each genome's attributes. The manifest
must contain five columns with headers. The first column should
contain the genome filename, the second the genome label, the third
the genome's internal_id, the fourth its sex ('male', 'female' or
'unspecified', and the fifth should contain its format ('vcf', 'vcf.gz',
or 'vcf.b2z')
"""

import csv
import json
import os
import requests
from requests.auth import HTTPBasicAuth
import sys

#Load environment variables for request authentication parameters
OMICIA_API_LOGIN = os.environ['OMICIA_API_LOGIN']
OMICIA_API_PASSWORD = os.environ['OMICIA_API_PASSWORD']
OMICIA_API_URL = os.environ['OMICIA_API_URL']


def get_manifest_info(folder):
    """Generate an object containing the data from the manifest.csv
    file in the genomes folder, including each filename along with
    its genome label, external id, sex, and format.
    """
    manifest_info = {}
    with open(folder + '/manifest.csv') as f:
        reader = csv.reader(f)
        next(reader, None)  # skip the header
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

    # Assuming there is a manifest file, this will generate
    manifest_info = get_manifest_info(folder)

    # List where returned genome JSON information will be stored
    genome_json_objects = []

    for genome_file_name in manifest_info:
        genome_attrs = manifest_info[genome_file_name]
        url = "{}/projects/{}/genomes?genome_label={}&genome_sex={}&external_id={}&assembly_version=hg19&format={}"
        url = url.format(OMICIA_API_URL,
                         project_id,
                         genome_attrs["genome_label"],
                         genome_attrs["genome_sex"],
                         genome_attrs["external_id"],
                         genome_attrs["format"])

        with open(folder + "/" + genome_file_name, 'rb') as file_handle:
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

    # Output genome labels, ids, external_id, and size
    for genome_object in genome_objects:
        print {"genome_label": genome_object["genome_label"],
               "genome_id": genome_object["genome_id"],
               "external_id": genome_object["external_id"],
               "size": genome_object["size"]}

if __name__ == "__main__":
    main(sys.argv[1:])
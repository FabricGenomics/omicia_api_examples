"""Upload multiple genomes to an existing project from a folder,
using a manifest to outline each genome's attributes. The manifest
must contain five columns with headers. The first column should
contain the genome filename, the second the genome label, the third
the genome's internal_id, the fourth its sex ('male', 'female' or
'unspecified', and the fifth should contain its format ('vcf', 'vcf.gz',
or 'vcf.b2z'). This manifest must be stored in the same folder as
all of the genomes it describes, and must be named 'manifest.csv.'

Example manifest.csv contents:
filename,label,external_id,sex,format
TR4091_exome_copy.vcf.gz,abc1,55,male
TR4091_exome.vcf,abc2,56,female
TR4092_exome.vcf,abc3,57,unspecified
TR4093_exome.vcf,abc4,58,female
TR4094_exome.vcf,abc5,59,male
"""
import argparse
import csv
import os
import requests
from requests.auth import HTTPBasicAuth
import sys
import simplejson as json

# Load environment variables for request authentication parameters
if "FABRIC_API_PASSWORD" not in os.environ:
    sys.exit("FABRIC_API_PASSWORD environment variable missing")

if "FABRIC_API_LOGIN" not in os.environ:
    sys.exit("FABRIC_API_LOGIN environment variable missing")

FABRIC_API_LOGIN = os.environ['FABRIC_API_LOGIN']
FABRIC_API_PASSWORD = os.environ['FABRIC_API_PASSWORD']
FABRIC_API_URL = os.environ.get('FABRIC_API_URL', 'https://api.fabricgenomics.com')
auth = HTTPBasicAuth(FABRIC_API_LOGIN, FABRIC_API_PASSWORD)


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
                                              "genome_sex": row[3]}
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
    for genome_file_name in manifest_info.keys():
        genome_attrs = manifest_info[genome_file_name]
        url = "{}/projects/{}/genomes?genome_label={}&genome_sex={}&external_id={}&assembly_version=hg19"
        url = url.format(FABRIC_API_URL,
                         project_id,
                         genome_attrs["genome_label"],
                         genome_attrs["genome_sex"],
                         genome_attrs["external_id"])
        sys.stdout.write("uploading {}...".format(genome_file_name))

        with open(folder + "/" + genome_file_name, 'rb') as file_handle:
            # Post request and store newly uploaded genome's information
            result = requests.put(url, auth=auth, data=file_handle)
            genome_json_objects.append(result.json())

        sys.stdout.write("*\n")
        sys.stdout.flush()

    return genome_json_objects


def main():
    """Main function. Upload VCF files from a folder to a specified project,
    using a manifest to specify each genome's attributes.
    """
    parser = argparse.ArgumentParser(description='Upload a folder of genomes.')
    parser.add_argument('project_id', metavar='project_id')
    parser.add_argument('folder', metavar='folder')
    args = parser.parse_args()

    project_id = args.project_id
    folder = args.folder

    genome_objects = upload_genomes_to_project(project_id, folder)

    # Output genome labels, ids, external ids, and sizes
    sys.stdout.write(json.dumps(genome_objects, indent=4))

if __name__ == "__main__":
    main()

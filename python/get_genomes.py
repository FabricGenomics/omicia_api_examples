"""Create a new project.
"""

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

def get_genomes(project_id):
    """Fetch all the genomes associated with a particular project.
    """

    # Construct request
    url = "{}/projects/{}/genomes".format(OMICIA_API_URL, project_id)

    # Get request and return json object of genomes
    result = requests.get(url, auth=auth)
    return result.json()


def main(argv):
    """main function, get all genomes in a project.
    """

    if len(argv) != 1:
        sys.exit("Usage: python get_genomes.py <project_id>")
    project_id = argv[0]
    genome_objects = get_genomes(project_id)
    for genome in genome_objects['objects']:
        sys.stdout.write('name: {}\n'
                         'upload_date: {}\n'
                         'genome_status: {}\n'
                         'report_count: {}\n'
                         'uploaded_by: {}\n'
                         'is_upgraded: {}\n'
                         'project_id: {}\n'
                         'external_id: {}\n'
                         'id: {}\n'
                         .format(genome['name'],
                                 genome['upload_date'],
                                 genome['genome_status'],
                                 genome['report_count'],
                                 genome['uploaded_by'],
                                 genome['is_upgraded'],
                                 genome['project_id'],
                                 genome['external_id'],
                                 genome['id']))
        sys.stdout.write('\n')

if __name__ == "__main__":
    main(sys.argv[1:])
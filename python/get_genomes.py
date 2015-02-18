"""Get all genomes in a project.
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

    json_response = get_genomes(project_id)

    try:
        for genome in json_response['objects']:
            sys.stdout.write('name: {}\n'
                             'upload_date: {}\n'
                             'genome_status: {}\n'
                             'report_count: {}\n'
                             'uploaded_by: {}\n'
                             'is_upgraded: {}\n'
                             'project_id: {}\n'
                             'external_id: {}\n'
                             'id: {}\n'
                             .format(genome.get('name', 'Missing'),
                                     genome.get('upload_date', 'Missing'),
                                     genome.get('genome_status', 'Missing'),
                                     genome.get('report_count', 'Missing'),
                                     genome.get('uploaded_by', 'Missing'),
                                     genome.get('is_upgraded', 'Missing'),
                                     genome.get('project_id', 'Missing'),
                                     genome.get('external_id', 'Missing'),
                                     genome.get('id', 'Missing')))
            sys.stdout.write('\n')
    except KeyError:
        if json_response['description']:
            sys.stdout.write("Error: {}\n".format(json_response['description']))
        else:
            sys.stdout.write('Something went wrong ...')

if __name__ == "__main__":
    main(sys.argv[1:])
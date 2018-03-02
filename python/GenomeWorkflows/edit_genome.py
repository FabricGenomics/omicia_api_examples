"""Edit a genome
"""

import os
import requests
from requests.auth import HTTPBasicAuth
import sys
import json
import argparse
import certifi

#Load environment variables for request authentication parameters
if "OMICIA_API_PASSWORD" not in os.environ:
    sys.exit("OMICIA_API_PASSWORD environment variable missing")

if "OMICIA_API_LOGIN" not in os.environ:
    sys.exit("OMICIA_API_LOGIN environment variable missing")

OMICIA_API_LOGIN = os.environ['OMICIA_API_LOGIN']
OMICIA_API_PASSWORD = os.environ['OMICIA_API_PASSWORD']
OMICIA_API_URL = os.environ.get('OMICIA_API_URL', 'https://api.fabricgenomics.com')
auth = HTTPBasicAuth(OMICIA_API_LOGIN, OMICIA_API_PASSWORD)


def put_genome(genome_id, name=None, external_id=None, project_id=None):
    """Use the Omicia API to edit an existing genome or move it to a different project.
    """
    # Construct request
    url = "{}/genomes/{}"
    url = url.format(OMICIA_API_URL, genome_id)
    url_payload = json.dumps({"name": name,
                              "external_id": external_id,
                              "project_id": project_id
                              })

    result = requests.put(url, auth=auth, data=url_payload, verify=certifi.where())
    return result.json()


def main():
    """Main function. Edit a genome.
    """
    parser = argparse.ArgumentParser(
        description='Edit a genome or move it to another project.')
    parser.add_argument('g', metavar='genome_id')
    parser.add_argument('--n', metavar='name')
    parser.add_argument('--e', metavar='external_id')
    parser.add_argument('--p', metavar='project_id')
    args = parser.parse_args()

    genome_id = args.g
    name = args.n
    external_id = args.e
    project_id = args.p

    json_response = put_genome(genome_id,
                              name=name,
                              external_id=external_id,
                              project_id=project_id)
    try:
        sys.stdout.write(json.dumps(json_response, indent=4))
        sys.stdout.write('\n')
    except TypeError:
        sys.stdout.write("Unexpected error. Perhaps the genome you specified no longer exists?\n\n")


if __name__ == "__main__":
    main()

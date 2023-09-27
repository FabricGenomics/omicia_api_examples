"""Upload a genome to an existing project.
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
OMICIA_API_URL = os.environ.get('OMICIA_API_URL', 'https://api.fabricgenomics.com')
auth = HTTPBasicAuth(OMICIA_API_LOGIN, OMICIA_API_PASSWORD)


def delete_genome(genome_id):
    """Use the Omicia API to delete a genome, by genome id."""
    # Construct request
    url = "{}/genomes/{}"

    url = url.format(OMICIA_API_URL, genome_id)
    result = requests.delete(url, auth=auth)
    original_response = result.json()

    return original_response


def main():
    """Main function. Upload a specified VCF file to a specified project.
    """
    parser = argparse.ArgumentParser(description='Delete a genome.')
    parser.add_argument('genome_id', metavar='genome_id')
    args = parser.parse_args()

    genome_id = args.genome_id
    json_response = delete_genome(genome_id)

    try:
        sys.stdout.write(json.dumps(json_response, indent=4))
    except KeyError:
        if json_response.get('description'):
            sys.stdout.write('Error: {}\n'.format(json_response.get('description')))
        else:
            sys.stdout.write('Something went wrong...')

if __name__ == "__main__":
    main()

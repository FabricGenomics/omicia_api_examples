"""Get an analysis, or all analyses in the workspace.
Example usages:
 python get_analysis.py --id 1802
 python get_analysis.py
"""

import os
import requests
from requests.auth import HTTPBasicAuth
import sys
import simplejson as json
import argparse

# Load environment variables for request authentication parameters
if "OMICIA_API_PASSWORD" not in os.environ:
    sys.exit("OMICIA_API_PASSWORD environment variable missing")

if "OMICIA_API_LOGIN" not in os.environ:
    sys.exit("OMICIA_API_LOGIN environment variable missing")

OMICIA_API_LOGIN = os.environ['OMICIA_API_LOGIN']
OMICIA_API_PASSWORD = os.environ['OMICIA_API_PASSWORD']
OMICIA_API_URL = os.environ.get('OMICIA_API_URL', 'https://api.fabricgenomics.com')
auth = HTTPBasicAuth(OMICIA_API_LOGIN, OMICIA_API_PASSWORD)


def get_analysis(analysis_id=None, genome_id=None):
    """Use the Omicia API to get an analysis
    """
    # Construct request
    if analysis_id:
        url = "{}/analysis/{}/"
        url = url.format(OMICIA_API_URL, analysis_id)
    else:
        url = "{}/analysis"
        url = url.format(OMICIA_API_URL, analysis_id)
        if genome_id:
            url = '{}?genome_id={}'.format(url, genome_id)

    sys.stdout.flush()
    result = requests.get(url, auth=auth)
    return result.json()


def main():
    """Main function. Get analyses or one analysis by ID.
    """
    parser = argparse.ArgumentParser(description='Fetch a Variant, VAAST or Phevor Report')
    parser.add_argument('--id', metavar='analysis_id', type=int)
    parser.add_argument('--genome_id', metavar='genome_id', type=int)
    args = parser.parse_args()

    analysis_id = args.id
    genome_id = args.genome_id

    json_response = get_analysis(analysis_id=analysis_id, genome_id=genome_id)
    sys.stdout.write(json.dumps(json_response, indent=4))

if __name__ == "__main__":
    main()

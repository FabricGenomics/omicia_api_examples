"""
    Delete analysis by id
    Example usages:
        python delete_analysis.py --id 1802
"""

import os
import requests
from requests.auth import HTTPBasicAuth
import sys
import certifi
import argparse

# Load environment variables for request authentication parameters
if "OMICIA_API_PASSWORD" not in os.environ:
    sys.exit("OMICIA_API_PASSWORD environment variable missing")

if "OMICIA_API_LOGIN" not in os.environ:
    sys.exit("OMICIA_API_LOGIN environment variable missing")

FABRIC_API_LOGIN = os.environ['OMICIA_API_LOGIN']
FABRIC_API_PASSWORD = os.environ['OMICIA_API_PASSWORD']
FABRIC_API_URL = os.environ.get('OMICIA_API_URL', 'https://api.fabricgenomics.com')
auth = HTTPBasicAuth(FABRIC_API_LOGIN, FABRIC_API_PASSWORD)


def delete_analysis(args):
    """Use the Fabric API to get variants
    """

    url = '{}/analysis/{}'.format(FABRIC_API_URL, args.id)

    result = requests.delete(url, auth=auth, verify=certifi.where())

    return result.text


def main():
    """Main function. Delete analysis by ID.
    """
    parser = argparse.ArgumentParser(
        description='Delete a Variant, VAAST or Phevor Analysis')
    parser.add_argument('--id', required=True, metavar='Analysis ID', type=int)
    args = parser.parse_args()

    sys.stdout.write(delete_analysis(args))
    sys.stdout.write('\n')

if __name__ == "__main__":
    main()

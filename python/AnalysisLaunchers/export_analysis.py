"""
    Export analysis by id
    Example usages:
        python export_analysis.py --id 1802 --filter_id 1234  --format JSON
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

FABRIC_API_LOGIN = os.environ['OMICIA_API_LOGIN']
FABRIC_API_PASSWORD = os.environ['OMICIA_API_PASSWORD']
FABRIC_API_URL = os.environ.get('OMICIA_API_URL', 'https://api.fabricgenomics.com')
auth = HTTPBasicAuth(FABRIC_API_LOGIN, FABRIC_API_PASSWORD)


def export_analysis(args):
    """Use the Fabric API to get variants
    """

    if args.structural:
        url = '{}/analysis/{}/structural_variants'.format(FABRIC_API_URL, args.id)
    else:
        url = '{}/analysis/{}/variants'.format(FABRIC_API_URL, args.id)

    result = requests.post(url, auth=auth, data=json.dumps(vars(args)), verify=False)

    return result.text


def main():
    """Main function. Get analyses or one analysis by ID.
    """
    parser = argparse.ArgumentParser(
        description='Fetch a Variant, VAAST or Phevor Report variants. '
                    'One of filter_id, panel_id or gene_set_id must be specified')
    parser.add_argument('--id', required=True, metavar='Analysis ID', type=int)
    parser.add_argument('--filter_id', metavar='Filter ID', type=int)
    parser.add_argument('--panel_id', metavar='Panel/Test ID', type=int)
    parser.add_argument('--gene_set_id', metavar='Gene Set ID', type=int)
    parser.add_argument('--format', metavar='[JSON, VCF, CSV]', type=str, default='JSON')
    parser.add_argument('--limit', metavar='Max number of variants to return',
                        type=int, default=None)
    parser.add_argument('--offset', metavar='Number of variants to skip', type=int, default=0)
    parser.add_argument('--structural', dest='structural', action='store_true', default=False)
    args = parser.parse_args()

    if not (args.filter_id or args.panel_id or args.gene_set_id):
        exit(parser.parse_args(['-h']))

    sys.stdout.write(export_analysis(args))
    sys.stdout.write('\n')

if __name__ == "__main__":
    main()

"""
Upload a spreadhseet of condiiton genes to prime a workspace
"""

import os
import requests
import gzip
from requests.auth import HTTPBasicAuth
import sys
import logging
import argparse
from csv import DictReader

_LOGGER = logging.getLogger(__name__)

# Load environment variables for request authentication parameters
if "FABRIC_API_PASSWORD" not in os.environ:
    sys.exit("FABRIC_API_PASSWORD environment variable missing")

if "FABRIC_API_LOGIN" not in os.environ:
    sys.exit("FABRIC_API_LOGIN environment variable missing")

FABRIC_API_LOGIN = os.environ['FABRIC_API_LOGIN']
FABRIC_API_PASSWORD = os.environ['FABRIC_API_PASSWORD']
FABRIC_API_URL = os.environ.get('FABRIC_API_URL', 'https://api.fabricgenomics.com')
auth = HTTPBasicAuth(FABRIC_API_LOGIN, FABRIC_API_PASSWORD)


def parse_null(value):
    return None if value == 'NULL' else value


def check_first(cui, gene_symbol):
    # Construct request
    url = "{}/condition_genes/?cui={}&gene_symbol={}"
    url = url.format(FABRIC_API_URL, cui, gene_symbol)
    result = requests.get(url, auth=auth)
    result_dict = result.json()
    return len(result_dict.get('objects')) > 1


def upload_condition_genes(filename, check):
    """Use the Omicia API to get the regions for a panel.
    """
    # Construct request
    url = "{}/condition_genes/"
    url = url.format(FABRIC_API_URL)

    _LOGGER.info("Opening {}".format(filename))
    with gzip.open(filename, 'rb') as file:
        reader = DictReader(file)
        for row in reader:
            cui = parse_null(row.get('cui'))
            gene_symbol = row.get('gene_symbol')
            if check and cui and gene_symbol and check_first(cui, gene_symbol):
                _LOGGER.info("Found record for CUI: {} and gene: {} - skipping...".format(cui, gene_symbol))
                continue

            _LOGGER.info("Creating record for CUI: {} and gene: {}".format(cui, gene_symbol))

            payload = {
                'CUI': cui,
                'gene_symbol': gene_symbol,
                'condition': row.get('condition'),
                'inheritance': parse_null(row.get('inheritance')),
                'prevalence': parse_null(row.get('prevalence')),
                'penetrance': parse_null(row.get('penetrance')),
                'notes': parse_null(row.get('notes')),
                'age_of_onset': parse_null(row.get('age_of_onset')),
                'pmids': parse_null(row.get('pmids'))
            }
            result = requests.post(url, json=payload, auth=auth)
            if result.status_code == 200:
                _LOGGER.info("Created condition-gene: {}".format(result.json))
            else:
                _LOGGER.warn("Error! {}".format(result.text))

    _LOGGER.info("Done with {}".format(filename))

def main():
    """Main function. Get the regions in a panel and print out their gene symbols.
    """
    parser = argparse.ArgumentParser(description='Upload a zipped spreadsheet of condition-genes.')
    parser.add_argument('f', metavar='file', type=str)
    parser.add_argument("--check", help="Check first for gene/CUI presence",
                        action="store_true")
    parser.add_argument("--verbose", help="Enable logging",
                        action="store_true")

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    _LOGGER.info("Running script with args: verbose {} check {}".format(args.verbose, args.check))

    upload_condition_genes(args.f, args.check)


if __name__ == "__main__":
    main()

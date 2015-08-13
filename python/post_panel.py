"""Post a panel
"""

import os
import requests
from requests.auth import HTTPBasicAuth
import sys
import json
import argparse

#Load environment variables for request authentication parameters
if "OMICIA_API_PASSWORD" not in os.environ:
    sys.exit("OMICIA_API_PASSWORD environment variable missing")

if "OMICIA_API_LOGIN" not in os.environ:
    sys.exit("OMICIA_API_LOGIN environment variable missing")

OMICIA_API_LOGIN = os.environ['OMICIA_API_LOGIN']
OMICIA_API_PASSWORD = os.environ['OMICIA_API_PASSWORD']
OMICIA_API_URL = os.environ.get('OMICIA_API_URL', 'https://api.omicia.com')
auth = HTTPBasicAuth(OMICIA_API_LOGIN, OMICIA_API_PASSWORD)


def post_panel(name, description, methodology=None,
               limitations=None, fda_disclosure=None, test_code=None):
    """Use the Omicia API to post a new panel
    """
    #Construct request
    url = "{}/panels/"
    url = url.format(OMICIA_API_URL)
    url_payload = json.dumps({"name": name,
                              "description": description,
                              "methodology": methodology,
                              "limitations": limitations,
                              "fda_disclosure": fda_disclosure,
                              "test_code": test_code})

    sys.stdout.write("Creating a new panel...")
    sys.stdout.write("\n\n")
    sys.stdout.flush()
    # If patient information was not provided, make a post request to reports
    # without a patient information parameter in the url
    result = requests.post(url, auth=auth, data=url_payload)
    return result.json()

def add_gene_symbols_to_panel(panel_id, gene_symbols):
    """Add a list of gene symbols to a panel"""
    pass

def main():
    """main function. Upload a specified VCF file to a specified project.
    """
    parser = argparse.ArgumentParser(description='Post a panel')
    parser.add_argument('n', metavar='name')
    parser.add_argument('d', metavar='description')
    parser.add_argument('--m', metavar='methodology')
    parser.add_argument('--l', metavar='limitations')
    parser.add_argument('--f', metavar='fda_disclosure')
    parser.add_argument('--t', metavar='test_code')
    parser.add_argument('--g', metavar='gene_symbols')
    args = parser.parse_args()

    name = args.n
    description = args.d
    methodology = args.m
    limitations = args.l
    fda_disclosure = args.f
    test_code = args.t
    gene_symbols = args.g

    json_response = post_panel(name,
                               description,
                               methodology=methodology,
                               limitations=limitations,
                               fda_disclosure=fda_disclosure,
                               test_code=test_code)
    panel_object = json.loads(json_response)
    panel_id = panel_object.get('id')

    print json_response
    json_response = add_gene_symbols_to_panel(panel_id, gene_symbols)


if __name__ == "__main__":
    main()

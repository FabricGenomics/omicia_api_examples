"""Get the genes in a panel.
"""

import os
import requests
from requests.auth import HTTPBasicAuth
import sys
import simplejson as json
import argparse

# Load environment variables for request authentication parameters
if "FABRIC_API_PASSWORD" not in os.environ:
    sys.exit("FABRIC_API_PASSWORD environment variable missing")

if "FABRIC_API_LOGIN" not in os.environ:
    sys.exit("FABRIC_API_LOGIN environment variable missing")

FABRIC_API_LOGIN = os.environ['FABRIC_API_LOGIN']
FABRIC_API_PASSWORD = os.environ['FABRIC_API_PASSWORD']
FABRIC_API_URL = os.environ.get('FABRIC_API_URL', 'https://api.fabricgenomics.com')
auth = HTTPBasicAuth(FABRIC_API_LOGIN, FABRIC_API_PASSWORD)


def get_panel_regions(panel_id):
    """Use the Omicia API to get the regions for a panel.
    """
    # Construct request
    url = "{}/panels/{}/regions"
    url = url.format(FABRIC_API_URL, panel_id)

    sys.stdout.flush()
    result = requests.get(url, auth=auth)
    return result.json()


def main():
    """Main function. Get the regions in a panel and print out their gene symbols.
    """
    parser = argparse.ArgumentParser(description='Get Panel Regions.')
    parser.add_argument('p', metavar='panel_id', type=int)
    args = parser.parse_args()

    panel_id = args.p

    json_response = get_panel_regions(panel_id)
    panel_regions = json_response

    sys.stdout.write(json.dumps(panel_regions, indent=4))

if __name__ == "__main__":
    main()
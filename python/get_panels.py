"""Get a list of panels, either all or filtered by some attribute.
"""

import os
import requests
from requests.auth import HTTPBasicAuth
import sys
import json
import argparse

# Load environment variables for request authentication parameters
if "OMICIA_API_PASSWORD" not in os.environ:
    sys.exit("OMICIA_API_PASSWORD environment variable missing")

if "OMICIA_API_LOGIN" not in os.environ:
    sys.exit("OMICIA_API_LOGIN environment variable missing")

OMICIA_API_LOGIN = os.environ['OMICIA_API_LOGIN']
OMICIA_API_PASSWORD = os.environ['OMICIA_API_PASSWORD']
OMICIA_API_URL = os.environ.get('OMICIA_API_URL', 'https://api.omicia.com')
auth = HTTPBasicAuth(OMICIA_API_LOGIN, OMICIA_API_PASSWORD)


def get_panels(panel_name, panel_description, panel_test_code):
    """Use the Omicia API to get all panels, or get panels by name, description, or test code.
    """
    # Construct request
    url = "{}/panels/"
    if panel_name or panel_description or panel_test_code:
        url += "?"
    if panel_name:
        url += "name={}&".format(panel_name)
    if panel_description:
        url += "description={}&".format(panel_description)
    if panel_test_code:
        url += "test_code={}".format(panel_test_code)
    url = url.format(OMICIA_API_URL)

    sys.stdout.flush()
    result = requests.get(url, auth=auth)
    return result.json()


def main():
    """Main function. Get panels. All, or by name, description or test code.
    """
    parser = argparse.ArgumentParser(description='Get panel')
    parser.add_argument('--n', metavar='panel_name', type=str)
    parser.add_argument('--d', metavar='panel_description', type=str)
    parser.add_argument('--t', metavar='panel_test_code', type=str)

    args = parser.parse_args()

    panel_name = args.n
    panel_description = args.d
    panel_test_code = args.t

    json_response = get_panels(panel_name, panel_description, panel_test_code)
    panel_ids = json.dumps(json_response, indent=4)

    sys.stdout.write('{}'.format(panel_ids))
    sys.stdout.write('\n')

if __name__ == "__main__":
    main()

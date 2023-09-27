"""Get all variants in a clinical report"""

import os
import sys
import requests
import simplejson as json
from requests.auth import HTTPBasicAuth

# Load environment variables for request authentication parameters
if "FABRIC_API_PASSWORD" not in os.environ:
    sys.exit("FABRIC_API_PASSWORD environment variable missing")

if "FABRIC_API_LOGIN" not in os.environ:
    sys.exit("FABRIC_API_LOGIN environment variable missing")

FABRIC_API_LOGIN = os.environ['FABRIC_API_LOGIN']
FABRIC_API_PASSWORD = os.environ['FABRIC_API_PASSWORD']
FABRIC_API_URL = os.environ.get('FABRIC_API_URL', 'https://testweb-api.omicia.us')
auth = HTTPBasicAuth(FABRIC_API_LOGIN, FABRIC_API_PASSWORD)


def get_variants(report_id):
    """Fetch all the variants in a clinical report"""

    # Construct request
    url = "{}/reports/{}/variants".format(FABRIC_API_URL, report_id)

    # Get request and return json object of variants
    result = requests.get(url, auth=auth)
    return result.json()


def main(argv):
    """ main function, get variants in a clinical report """

    if len(argv) != 1:
        sys.exit("Usage: python get_clinical_report_variants.py <clinical_report_id>")
    report_id = argv[0]

    json_response = get_variants(report_id)

    try:
        for variant in json_response['objects']:
            sys.stdout.write(json.dumps(variant, indent=4))
            sys.stdout.write('\n')
    except KeyError:
        if json_response['description']:
            sys.stdout.write("Error: {}\n".format(json_response))
        else:
            sys.stdout.write('Something went wrong ...')

if __name__ == "__main__":
    main(sys.argv[1:])

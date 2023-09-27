"""Query for a report by id to see its status.
"""

import os
import requests
from requests.auth import HTTPBasicAuth
import sys

#Load environment variables for request authentication parameters
if "FABRIC_API_PASSWORD" not in os.environ:
    sys.exit("FABRIC_API_PASSWORD environment variable missing")

if "FABRIC_API_LOGIN" not in os.environ:
    sys.exit("FABRIC_API_LOGIN environment variable missing")

FABRIC_API_LOGIN = os.environ['FABRIC_API_LOGIN']
FABRIC_API_PASSWORD = os.environ['FABRIC_API_PASSWORD']
FABRIC_API_URL = os.environ.get('FABRIC_API_URL', 'https://api.fabricgenomics.com')
auth = HTTPBasicAuth(FABRIC_API_LOGIN, FABRIC_API_PASSWORD)


def get_report(report_id):
    """Query for a report by its id.
    """

    url = "{}/reports/{}"
    url = url.format(FABRIC_API_URL,
                     report_id)

    result = requests.get(url, auth=auth)
    return result.json()


def main(argv):
    """Main function. Retrieve a report's status by id.
    """
    if len(argv) < 1:
        sys.exit("Usage: python get_report.py <report_id>")
    report_id = argv[0]

    json_response = get_report(report_id)

    # Access the JSON object's 'status' attribute
    try:
        sys.stdout.write("Report Status: {}\n".format(json_response['status']))
    except KeyError:
        if json_response['description']:
            sys.stderr.write('Error: {}\n'.format(json_response['description']))
        else:
            sys.stderr.write('Something went wrong...')

if __name__ == "__main__":
    main(sys.argv[1:])
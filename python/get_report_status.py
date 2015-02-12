"""Query for a report by id to see its status.
"""

import os
import requests
from requests.auth import HTTPBasicAuth
import sys

#Load environment variables for request authentication parameters
if "OMICIA_API_PASSWORD" not in os.environ:
    sys.exit("OMICIA_API_PASSWORD environment variable missing")

if "OMICIA_API_LOGIN" not in os.environ:
    sys.exit("OMICIA_API_LOGIN environment variable missing")

OMICIA_API_LOGIN = os.environ['OMICIA_API_LOGIN']
OMICIA_API_PASSWORD = os.environ['OMICIA_API_PASSWORD']
OMICIA_API_URL = os.environ.get('OMICIA_API_URL', 'https://api.omicia.com')
auth = HTTPBasicAuth(OMICIA_API_LOGIN, OMICIA_API_PASSWORD)


def get_report(report_id):
    """Query for a report by its id.
    """

    url = "{}/reports/{}"
    url = url.format(OMICIA_API_URL,
                     report_id)

    result = requests.get(url, auth=auth)
    return result.json()


def main(argv):
    """Main function. Retrieve a report's status by id.
    """
    if len(argv) < 1:
        sys.exit("Usage: python get_report.py <report_id>")
    report_id = argv[0]

    report = get_report(report_id)

    # Access the JSON object's 'status' attribute
    sys.stdout.write(report['status'])

if __name__ == "__main__":
    main(sys.argv[1:])
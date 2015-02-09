"""Query for a report by id to see its status.
"""

import json
import os
import requests
from requests.auth import HTTPBasicAuth
import sys

#Load environment variables for request authentication parameters
OMICIA_API_LOGIN = os.environ['OMICIA_API_LOGIN']
OMICIA_API_PASSWORD = os.environ['OMICIA_API_PASSWORD']
OMICIA_API_URL = os.environ['OMICIA_API_URL']


def get_report(report_id):
    """Query for a report by its id.
    """

    url = "{}/reports/{}"
    url = url.format(OMICIA_API_URL,
                     report_id)

    auth = HTTPBasicAuth(OMICIA_API_LOGIN, OMICIA_API_PASSWORD)
    result = requests.get(url, auth=auth)
    json_data = json.loads(result.text)
    return json_data


def main(argv):
    """Main function. Retrieve a report's status by id.
    """
    if len(argv) < 1:
        sys.exit("Usage: python get_report.py <report_id>")
    report_id = argv[0]

    report = get_report(report_id)

    # Access the JSON object's 'status' attribute
    print report['status']

if __name__ == "__main__":
    main(sys.argv[1:])
"""
Get a clinical report's scored variants.
"""

import os
import requests
from requests.auth import HTTPBasicAuth
import sys
import json
import argparse
import urllib

# Load environment variables for request authentication parameters
if "FABRIC_API_PASSWORD" not in os.environ:
    sys.exit("FABRIC_API_PASSWORD environment variable missing")

if "FABRIC_API_LOGIN" not in os.environ:
    sys.exit("FABRIC_API_LOGIN environment variable missing")

FABRIC_API_LOGIN = os.environ['FABRIC_API_LOGIN']
FABRIC_API_PASSWORD = os.environ['FABRIC_API_PASSWORD']
FABRIC_API_URL = os.environ.get('FABRIC_API_URL', 'https://api.fabricgenomics.com')
auth = HTTPBasicAuth(FABRIC_API_LOGIN, FABRIC_API_PASSWORD)


def get_cr_scored_variants(cr_id, scoring_status=None, audit_log=None):
    params = []
    if scoring_status:
        params.append(('scoring_status', scoring_status))
    if audit_log:
        params.append(('audit_log', audit_log))

    data = urllib.urlencode(params)

    url = "{}/reports/{}/variants/scored?{}"
    url = url.format(FABRIC_API_URL, cr_id, data)

    result = requests.get(url, auth=auth)
    return result

def main():
    """Main function. Get scored report variants, all or filtering by scoring status. Audit Logs
       may also be included.
    """
    parser = argparse.ArgumentParser(description='Get scored variants for existing clinical report.')
    parser.add_argument('cr_id', metavar='clinical_report_id', type=int)
    parser.add_argument('--scoring_status',
                        metavar='extended',
                        type=str,
                        choices=['scored', 'scoring', 'classified'],
                        default=None)
    parser.add_argument('--audit_log', metavar='status', type=str, choices=['true'], default=None)

    args = parser.parse_args()

    cr_id = args.cr_id
    scoring_status = args.scoring_status
    audit_log = args.audit_log

    response = get_cr_scored_variants(cr_id, scoring_status, audit_log)
    try:
        response_json = response.json()
        sys.stdout.write(json.dumps(response_json, indent=4))
    except KeyError:
        sys.stderr.write(response.json())


if __name__ == "__main__":
    main()

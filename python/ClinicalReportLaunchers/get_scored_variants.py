"""Get a clinical report's variants.
Usages: python get_report_variants.py 1542
        
"""

import os
import requests
from requests.auth import HTTPBasicAuth
import sys
import json
import argparse
import urllib

# Load environment variables for request authentication parameters
if "OMICIA_API_PASSWORD" not in os.environ:
    sys.exit("OMICIA_API_PASSWORD environment variable missing")

if "OMICIA_API_LOGIN" not in os.environ:
    sys.exit("OMICIA_API_LOGIN environment variable missing")

OMICIA_API_LOGIN = os.environ['OMICIA_API_LOGIN']
OMICIA_API_PASSWORD = os.environ['OMICIA_API_PASSWORD']
OMICIA_API_URL = os.environ.get('OMICIA_API_URL', 'https://api.fabricgenomics.com')
auth = HTTPBasicAuth(OMICIA_API_LOGIN, OMICIA_API_PASSWORD)


def get_cr_scored_variants(cr_id, scoring_status=None, audit_log=False):
    params = []
    if scoring_status:
        params.append(('scoring_status', scoring_status))
    if audit_log:
        params.append(('audit_log', audit_log))
    data = urllib.urlencode(params, doseq=True)

    url = "{}/reports/{}/variants/scored?{}"
    url = url.format(OMICIA_API_URL, cr_id, data)

    result = requests.get(url, auth=auth, verify=False)
    return result

def main():
    """Main function. Get scored report variants, all or filtering by scoring status. Audit Logs
       may also be included.
    """
    parser = argparse.ArgumentParser(description='Get variants for existing clinical reports.')
    parser.add_argument('cr_id', metavar='clinical_report_id', type=int)
    parser.add_argument('--scoring_status',
                        metavar='extended',
                        type=str,
                        choices=['scored', 'scoring', 'classified'],
                        default=None)
    parser.add_argument('--audit_log', metavar='status', type=str, choices=['true'], default=None)

    args = parser.parse_args()

    cr_id = args.cr_id

    response = get_cr_scored_variants(cr_id)
    try:
        response_json = response.json()
        sys.stdout.write(json.dumps(response_json, indent=4))
    except KeyError:
        sys.stderr.write(response.json())


if __name__ == "__main__":
    main()

"""Get a clinical report pdf, either a preview or approved one.
Example usages:
 Fetch a preview report PDF:
    python get_clinical_report_pdf.py 5327 . --preview True
 Fetch an approved report PDF:
    python get_clinical_report_pdf.py 5327 .
"""

import os
import requests
from requests.auth import HTTPBasicAuth
import sys
import certifi
import argparse

# Load environment variables for request authentication parameters
if "OMICIA_API_PASSWORD" not in os.environ:
    sys.exit("OMICIA_API_PASSWORD environment variable missing")

if "OMICIA_API_LOGIN" not in os.environ:
    sys.exit("OMICIA_API_LOGIN environment variable missing")

OMICIA_API_LOGIN = os.environ['OMICIA_API_LOGIN']
OMICIA_API_PASSWORD = os.environ['OMICIA_API_PASSWORD']
OMICIA_API_URL = os.environ.get('OMICIA_API_URL', 'https://api.fabricgenomics.com')
auth = HTTPBasicAuth(OMICIA_API_LOGIN, OMICIA_API_PASSWORD)


def get_clinical_report_pdf(cr_id, preview=False):
    """Use the Omicia API to get a clinical report PDF, whether preview or complete
    """
    # Construct request
    if not preview:
        url = "{}/reports/{}/pdf_report"
    else:
        url = "{}/reports/{}/pdf_preview"
    url = url.format(OMICIA_API_URL, cr_id)

    sys.stdout.flush()
    result = requests.get(url, auth=auth, verify=certifi.where())
    return result


def main():
    """Main function. Get a clinical report by ID.
    """
    parser = argparse.ArgumentParser(description='Fetch a clinical report\'s draft or completed PDF report')
    parser.add_argument('c', metavar='clinical_report_id', type=int)
    parser.add_argument('p', metavar='path', type=str)
    parser.add_argument('--preview', metavar='preview', type=bool)
    args = parser.parse_args()

    cr_id = args.c
    dest_path = args.p
    preview = args.preview is not None

    response = get_clinical_report_pdf(cr_id, preview=preview)

    if response.status_code == 200:
        contents = response.content
        filename = response.headers.get('content-disposition').split('filename=')[-1]

        with open (os.path.join(dest_path, filename), 'w') as target_file:
            target_file.write(contents)
    else:
        print response.text

if __name__ == "__main__":
    main()

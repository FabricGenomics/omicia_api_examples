"""Get selectable variants from a clinical_report by JSON list.

Examples:
python get_report_selectable_variants.py 12345 --target_variants '[{"chromosome": "chr1", "start_on_chrom": 1635004, "end_on_chrom": 1635004}, {"chromosome": "chr5", "start_on_chrom": 175956271, "end_on_chrom": 175956271}]'
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
OMICIA_API_URL = os.environ.get('OMICIA_API_URL', 'https://api.fabricgenomics.com')
auth = HTTPBasicAuth(OMICIA_API_LOGIN, OMICIA_API_PASSWORD)

def get_report_selectable_variants(clinical_report_id, target_variants=None):
    """Get report variants by location, id or simply all.
    """
    # Construct request
    url = "{}/reports/{}/selectable_variants"
    url = url.format(OMICIA_API_URL, clinical_report_id)

    target_variants = [{"chromosome": "chr1",
                        "start_on_chrom": 94512602,
                        "gene_symbol": "ABCA4",
                        "inheritance_mode": "DOMINANT"}]
    # If target variants JSON is specified, post with the target variants JSON
    if target_variants:
        headers = {'content-type': 'application/json'}
        result = requests.post(url, auth=auth, data=json.dumps(target_variants), headers=headers)
        return result


def main():
    """Main function. Patch a report variant.
    """
    parser = argparse.ArgumentParser(description='Get variant report variant ID.')
    parser.add_argument('clinical_report_id', metavar='clinical_report_id', type=int)
    parser.add_argument('--target_variants', metavar='target_variants', type=str)
    args = parser.parse_args()

    clinical_report_id = args.clinical_report_id
    target_variants = args.target_variants

    """if not target_variants:
        sys.exit("Target variants JSON (e.g. [{\"chromosome\": \"chr1\", \"start_on_chrom\": "
                 "1635004, \"end_on_chrom\": 1635004}] must be specified")
    """
    response = get_report_selectable_variants(clinical_report_id,
                                              target_variants=target_variants)
    try:
        sys.stdout.write(json.dumps(response.json(), indent=4))
    except KeyError:
        sys.stderr.write(response.json)
    sys.stdout.write('\n')

if __name__ == "__main__":
    main()

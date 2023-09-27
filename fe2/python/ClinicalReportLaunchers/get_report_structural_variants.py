"""Get a clinical report's variants.
Usages: python get_report_variants.py 1542
        python get_report_variants.py 1542 --status "FAILED_CONFIRMATION,REVIEWED"
        python get_report_variants.py 1542 --status "CONFIRMED" --format "VCF"
        python get_report_variants.py 1542 --chr "Y" --start_on_chrom 1339 --status "REVIEWED"
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


def get_cr_variants(cr_id, statuses, _format, chrom, start_on_chrom, end_on_chrom, extended=False):
    """Use the Omicia API to get report variants that meet the filtering criteria.
    """
    params = []
    # Generate the url to be able to query for multiple statuses
    if statuses:
        for i, status in enumerate(statuses):
            params.append(('status', status))

    if extended:
        params.append(('extended', 'True'))

    if chrom:
        params.append(('chrom', chrom))

    if start_on_chrom:
        params.append(('start_on_chrom', start_on_chrom))

    if end_on_chrom:
        params.append(('end_on_chrom', end_on_chrom))

    # Add a parameter for format. If not set, default is json
    if _format in ["VCF", "CSV"]:
        params.append(('format', _format))

    # Do seq allows for the multiple values for one parameter name, as could be the case for the
    # status or to_report parameters.
    data = urllib.urlencode(params, doseq=True)

    # Construct request
    url = "{}/reports/{}/structural_variants?{}"
    url = url.format(FABRIC_API_URL, cr_id, data)

    sys.stdout.flush()
    result = requests.get(url, auth=auth)
    return result


def main():
    """Main function. Get report variants, all or filtering by status.
    """
    parser = argparse.ArgumentParser(description='Get structural variants for existing clinical reports.')
    parser.add_argument('cr_id', metavar='clinical_report_id', type=int)
    parser.add_argument('--status', metavar='status', type=str)
    parser.add_argument('--format', metavar='_format', type=str, choices=['json', 'VCF'], default='json')
    parser.add_argument('--chrom', metavar='chr', type=str, choices=['1', '2', '3', '4', '5', '6',
                                                                   '7', '8', '9', '10', '11', '12',
                                                                   '13', '14', '15', '16', '17',
                                                                   '18', '19', '20', '21', '22',
                                                                   'X', 'Y', 'M'])
    parser.add_argument('--start_on_chrom', metavar='start_on_chrom', type=int)
    parser.add_argument('--end_on_chrom', metavar='end_on_chrom', type=int)

    args = parser.parse_args()

    cr_id = args.cr_id
    status = args.status
    _format = args.format
    chrom = args.chrom
    start_on_chrom = args.start_on_chrom
    end_on_chrom = args.end_on_chrom

    statuses = status.split(",") if status else None

    response = get_cr_variants(cr_id, statuses, _format, chrom, start_on_chrom, end_on_chrom)
    if _format == 'VCF':
        for block in response.iter_content(1024):
            sys.stdout.write(block)
    else:
        try:
            response_json = response.json()
            variants = response_json['objects']
            for variant in variants:
                sys.stdout.write(json.dumps(variant, indent=4))
                sys.stdout.write('\n')
        except KeyError:
            sys.stderr.write(response.json())


if __name__ == "__main__":
    main()

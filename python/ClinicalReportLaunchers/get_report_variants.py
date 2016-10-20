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

# Load environment variables for request authentication parameters
if "OMICIA_API_PASSWORD" not in os.environ:
    sys.exit("OMICIA_API_PASSWORD environment variable missing")

if "OMICIA_API_LOGIN" not in os.environ:
    sys.exit("OMICIA_API_LOGIN environment variable missing")

OMICIA_API_LOGIN = os.environ['OMICIA_API_LOGIN']
OMICIA_API_PASSWORD = os.environ['OMICIA_API_PASSWORD']
OMICIA_API_URL = os.environ.get('OMICIA_API_URL', 'https://api.omicia.com')
auth = HTTPBasicAuth(OMICIA_API_LOGIN, OMICIA_API_PASSWORD)


def get_cr_variants(cr_id, statuses, to_reports, _format, chrom, start_on_chrom, end_on_chrom, alt, extended=False):
    """Use the Omicia API to get report variants that meet the filtering criteria.
    """
    # Construct request
    url = "{}/reports/{}/variants"
    url = url.format(OMICIA_API_URL, cr_id)

    # Generate the url to be able to query for multiple statuses
    if statuses:
        if url.endswith(u"variants"):
            url += u"?"
        for i, status in enumerate(statuses):
            if i > 0:
                url += u"&"
            url = u"{}status={}".format(url, status)

    # Generate the url to be able to query for multiple to_report statuses
    if to_reports:
        if url.endswith(u"variants"):
            url += u"?"
        for i, to_report in enumerate(to_reports):
            if i > 0:
                url += u"&"
            url = u"{}&or_to_report={}".format(url, to_report)

    if extended:
        if url.endswith(u"variants"):
            url += u"?"
        url = u"{}&extended=True".format(url)

    if chrom:
        if url.endswith(u"variants"):
            url += u"?"
        url = u"{}&chrom={}".format(url, chr)

    if start_on_chrom:
        if url.endswith(u"variants"):
            url += u"?"
        url = u"{}&start_on_chrom={}".format(url, start_on_chrom)

    if end_on_chrom:
        if url.endswith(u"variants"):
            url += u"?"
        url = u"{}&end_on_chrom={}".format(url, end_on_chrom)

    if alt:
        if url.endswith(u"variants"):
            url += u"?"
        url = u"{}&alt={}".format(url, alt)

    # Add a parameter for format. If not set, default is json
    if _format in ["VCF", "CSV"]:
        if url.endswith(u"variants"):
            url += u"?"
        url += '&format={}'.format(_format)

    sys.stdout.flush()
    result = requests.get(url, auth=auth, verify=False)
    return result


def main():
    """Main function. Get report variants, all or filtering by status.
    """
    parser = argparse.ArgumentParser(description='Get variants for existing clinical reports.')
    parser.add_argument('cr_id', metavar='clinical_report_id', type=int)
    parser.add_argument('--extended', metavar='extended', type=str, choices=['true'])
    parser.add_argument('--status', metavar='status', type=str)
    parser.add_argument('--to_report', metavar='to_report', type=str)
    parser.add_argument('--format', metavar='_format', type=str, choices=['JSON', 'VCF', 'CSV'], default='JSON')
    parser.add_argument('--chrom', metavar='chr', type=str, choices=['1', '2', '3', '4', '5', '6',
                                                                     '7', '8', '9', '10', '11', '12',
                                                                     '13', '14', '15', '16', '17',
                                                                     '18', '19', '20', '21', '22',
                                                                     'X', 'Y', 'M'])
    parser.add_argument('--start_on_chrom', metavar='start_on_chrom', type=int)
    parser.add_argument('--end_on_chrom', metavar='end_on_chrom', type=int)
    parser.add_argument('--alt', metavar='alt', type=str, choices=['A', 'T', 'C', 'G'])

    args = parser.parse_args()

    cr_id = args.cr_id
    extended = args.extended
    status = args.status
    to_report = args.to_report
    _format = args.format
    chrom = args.chrom
    start_on_chrom = args.start_on_chrom
    end_on_chrom = args.end_on_chrom
    alt = args.alt

    statuses = status.split(",") if status else None
    to_reports = to_report.split(",") if to_report else None

    response = get_cr_variants(cr_id, statuses, to_reports, _format, chrom, start_on_chrom, end_on_chrom, alt, extended=extended=='true')
    if _format == 'CSV':
        for block in response.iter_content(1024):
            sys.stdout.write(block)
    elif _format == 'VCF':
        for block in response.iter_content(1024):
            sys.stdout.write(block)
    else:
        try:
            response_json = response.json()
            sys.stdout.write(json.dumps(response_json, indent=4))
        except KeyError:
            sys.stderr.write(response.json())


if __name__ == "__main__":
    main()

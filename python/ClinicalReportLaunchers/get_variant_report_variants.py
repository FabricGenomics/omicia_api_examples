"""Get variants from a variant report by ID, location, BED file, or JSON list.

Examples:
python get_variant_report_variants.py 12345 --target_variants '[{"chromosome": "chr1", "start_on_chrom": 1635004, "end_on_chrom": 1635004}, {"chromosome": "chr5", "start_on_chrom": 175956271, "end_on_chrom": 175956271}]'
python get_variant_report_variants.py 12345 --bed_file variants.bed
python get_variant_report_variants.py 12345 --variant_location "chr1:1635004-1635004"
python get_variant_report_variants.py 12345 --variant_id 54321
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


def get_variant_report_variant(variant_report_id,
                               variant_location=None,
                               variant_id=None,
                               offset=None,
                               limit=None,
                               bed_file_path=None,
                               target_variants=None):
    """Get report variants by location, id or simply all.
    """
    # Construct request
    url = "{}/variant_reports/{}/variants"
    url = url.format(OMICIA_API_URL, variant_report_id)

    # If target variants JSON is specified, post with the target variants JSON
    if target_variants:
        headers= {'content-type': 'application/json'}
        result = requests.post(url, auth=auth, data=target_variants, headers=headers)
        return result
    else:
        if not bed_file_path:
            if (variant_id or variant_location):
                if variant_id:
                    url = "{}/{}".format(url, variant_id)
                elif variant_location:
                    url = "{}?location={}".format(url, variant_location)
            elif (offset or limit):
                url += "?"
                if offset:
                    url = "{}&offset={}".format(url, offset)
                if limit:
                    url = "{}&limit={}".format(url, limit)
            sys.stdout.flush()
            result = requests.get(url, auth=auth)
            return result
        elif bed_file_path:
            # If BED file is specified, post using the target variants bed file as the payload
            if not os.path.isfile(bed_file_path):
                sys.exit("BED file path does not point to a real file.")
            with open(bed_file_path,'rb') as payload:
                headers = {'content-type': 'application/x-www-form-urlencoded'}
                result = requests.post(url, auth=auth, data=payload, headers=headers)
                return result


def main():
    """Main function. Patch a report variant.
    """
    parser = argparse.ArgumentParser(description='Get variant report variant ID.')
    parser.add_argument('variant_report_id', metavar='variant_report_id', type=int)
    parser.add_argument('--bed_file_path', metavar='bed_file_path', type=str)
    parser.add_argument('--target_variants', metavar='target_variants', type=str)
    parser.add_argument('--variant_id', metavar='variant_id', type=int)
    parser.add_argument('--variant_location', metavar='variant_location', type=str)
    parser.add_argument('--offset', metavar='offset', type=int)
    parser.add_argument('--limit', metavar='limit', type=int)
    args = parser.parse_args()

    variant_report_id = args.variant_report_id
    bed_file_path = args.bed_file_path
    target_variants = args.target_variants
    variant_location = args.variant_location
    variant_id = args.variant_id
    offset = args.offset
    limit = args.limit

    if not (variant_id or variant_location) and not (offset or limit) and not (bed_file_path or target_variants):
        sys.exit("Variant ID or location must be specified to retrieve a variant, "
                 "or offset and limit must be specified to fetch a batch of variants,"
                 "or a BED file must be posted to fetch a group of variants,"
                 "or target variants JSON (e.g. [{\"chromosome\": \"chr1\", \"start_on_chrom\": "
                 "1635004, \"end_on_chrom\": 1635004}] must be specified")

    response = get_variant_report_variant(variant_report_id,
                                          variant_id=variant_id,
                                          variant_location=variant_location,
                                          offset=offset,
                                          limit=limit,
                                          bed_file_path=bed_file_path,
                                          target_variants=target_variants)
    try:
        sys.stdout.write(json.dumps(response.json(), indent=4))
    except KeyError:
        sys.stderr.write(response.json)
    sys.stdout.write('\n')

if __name__ == "__main__":
    main()

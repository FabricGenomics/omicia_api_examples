"""Set a report's variants.
Usage: python set_report_variants.py 1542 --format vcf vcf_variant.vcf
Example vcf_variant.vcf file:
##fileformat=VCFv4.2
##fileDate=2015-08-27
##source=Omicia Opal
##reference=GRCh37
##FILTER=<ID=FAIL,Description="Failed external confirmation">
##FILTER=<ID=CONFIRMED,Description="Passed external confirmation">
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
##FORMAT=<ID=GQ,Number=1,Type=Integer,Description="Genotype Quality">
##FORMAT=<ID=AD,Number=A,Type=Integer,Description="Allele Depth">
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	SAMPLE
chr7	87160618	rs2032582	A	C	1484.13	CONFIRMED	.	GT:GQ:AD	1/1:5000.00:.,.
"""

import os
import requests
from requests.auth import HTTPBasicAuth
import sys
import json
import argparse

#Load environment variables for request authentication parameters
if "OMICIA_API_PASSWORD" not in os.environ:
    sys.exit("OMICIA_API_PASSWORD environment variable missing")

if "OMICIA_API_LOGIN" not in os.environ:
    sys.exit("OMICIA_API_LOGIN environment variable missing")

OMICIA_API_LOGIN = os.environ['OMICIA_API_LOGIN']
OMICIA_API_PASSWORD = os.environ['OMICIA_API_PASSWORD']
OMICIA_API_URL = os.environ.get('OMICIA_API_URL', 'https://api.omicia.com')
auth = HTTPBasicAuth(OMICIA_API_LOGIN, OMICIA_API_PASSWORD)


def set_cr_variants(cr_id, file_name, _format):
    """Use the Omicia API to set report variants' statuses to 'FAIL' or 'CONFIRMED'
    """
    #Construct request
    url = "{}/reports/{}/variants?format={}"
    url = url.format(OMICIA_API_URL, cr_id, _format)

    sys.stdout.write("Uploading vcf file...\n")
    with open(file_name, 'rb') as file_handle:
        #Post request
        result = requests.put(url, auth=auth, data=file_handle)
        return result.json()

def main():
    """Main function. Get report variants, all or filtering by status.
    """
    parser = argparse.ArgumentParser(description='Get variants for existing clinical reports.')
    parser.add_argument('cr_id', metavar='clinical_report_id', type=int)
    parser.add_argument('file_name', metavar='file_name', type=str)
    parser.add_argument('--format', metavar='_format', type=str, choices=['vcf', 'vcf.gz', 'vcf.bz2'], default='vcf')

    args = parser.parse_args()

    cr_id = args.cr_id
    file_name = args.file_name
    _format = args.format

    result_json = set_cr_variants(cr_id, file_name, _format)
    sys.stdout.write(json.dumps(result_json))

if __name__ == "__main__":
    main()
"""Get all clinical reports, or search for reports by accession id or genome id.
Example usages:
 python get_clinical_reports.py
 python get_clinical_reports.py --a ABCA4
 python get_clinical_reports.py --g 103

Sample output:

[
    {
        "filter_name": "None",
        "father_variant_report_id": 15316,
        "submitted_on": "2015-11-09T11:06:57",
        "created_on": "2015-03-26T09:44:43",
        "submitted_for_review_by": null,
        "accession_id": "ek1",
        "pipeline_version": "4.1.2.58",
        "mother_variant_report_id": 15322,
        "id": 1801,
        "report_approved_date": "2015-11-09T11:12:45",
        "duo_relation_variant_report_id": null,
        "submitted_by": 185,
        "duo_relation": null,
        "duo_relation_genome_id": null,
        "test_type": "Trio",
        "created_by": 185,
        "version": 4,
        "has_refcalls": null,
        "filter_id": null,
        "vaast_report_id": 15321,
        "status": "READY TO REVIEW",
        "phevor_terms": null,
        "qc_status": null,
        "workspace_id": 233,
        "variant_report_id": 15315,
        "father_genome_id": 206032,
        "sample_collected_date": "2015-02-03T08:00:00",
        "submitted_for_review_on": null,
        "sample_received_date": "2015-02-05T08:00:00",
        "mother_genome_id": 206033,
        "genome_id": 206031,
        "panel_id": null,
        "duo_affected": null,
        "sibling_sex": null,
        "assay_type_id": null,
        "sibling_variant_report_id": null,
        "include_cosmic": false,
        "sibling_genome_id": null,
        "sibling_affected": null
    }
]
"""

import os
import requests
from requests.auth import HTTPBasicAuth
import sys
import simplejson as json
import argparse

# Load environment variables for request authentication parameters
if "FABRIC_API_PASSWORD" not in os.environ:
    sys.exit("FABRIC_API_PASSWORD environment variable missing")

if "FABRIC_API_LOGIN" not in os.environ:
    sys.exit("FABRIC_API_LOGIN environment variable missing")

FABRIC_API_LOGIN = os.environ['FABRIC_API_LOGIN']
FABRIC_API_PASSWORD = os.environ['FABRIC_API_PASSWORD']
FABRIC_API_URL = os.environ.get('FABRIC_API_URL', 'https://api.fabricgenomics.com')
auth = HTTPBasicAuth(FABRIC_API_LOGIN, FABRIC_API_PASSWORD)


def get_clinical_reports(accession_id, genome_id, external_id, genome_name):
    """Use the Omicia API to get all clinical reports
    """
    # Construct request
    url = "{}/reports/"
    if any([accession_id, genome_id, external_id, genome_name]):
        url += "?"
    if accession_id:
        url += "accession_id={}&".format(accession_id)
    if genome_id:
        url += "genome_id={}&".format(genome_id)
    if external_id:
        url += "external_id={}&".format(external_id)
    if genome_name:
        url += "genome_name={}&".format(genome_name)
    # Remove any trailing '&'
    if url.endswith('&'):
        url = url[:-1]
    url = url.format(FABRIC_API_URL)

    sys.stdout.flush()
    result = requests.get(url, auth=auth)
    return result.json()


def main():
    """Get all clinical reports.
    """
    parser = argparse.ArgumentParser(description='Fetch all clinical reports, or search '
                                                 'by accession id or genome id')
    parser.add_argument('--a', metavar='acccession_id', type=str, default=False)
    parser.add_argument('--g', metavar='genome_id', type=int, default=False)
    parser.add_argument('--e', metavar='external_id', type=str, default=False)
    parser.add_argument('--n', metavar='genome_name', type=str, default=False)

    args = parser.parse_args()

    # Get query elements
    accession_id = args.a
    genome_id = args.g
    external_id = args.e
    genome_name = args.n

    json_response = get_clinical_reports(accession_id, genome_id, external_id, genome_name)
    print json.dumps(json_response, indent=4)

if __name__ == "__main__":
    main()

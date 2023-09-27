"""Create a genomeless panel report.
"""

import argparse
import json
import os
import requests
from requests.auth import HTTPBasicAuth
import sys

#Load environment variables for request authentication parameters
if "FABRIC_API_PASSWORD" not in os.environ:
    sys.exit("FABRIC_API_PASSWORD environment variable missing")

if "FABRIC_API_LOGIN" not in os.environ:
    sys.exit("FABRIC_API_LOGIN environment variable missing")

FABRIC_API_LOGIN = os.environ['FABRIC_API_LOGIN']
FABRIC_API_PASSWORD = os.environ['FABRIC_API_PASSWORD']
FABRIC_API_URL = os.environ.get('FABRIC_API_URL', 'https://api.fabricgenomics.com')
auth = HTTPBasicAuth(FABRIC_API_LOGIN, FABRIC_API_PASSWORD)


def launch_panel_report(filter_id, panel_id, accession_id, project_id):
    """Launch a genomeless panel report given filter id, and panel id
    parameters. Return the JSON response.
    """
    # Construct url and request
    url = "{}/reports/".format(FABRIC_API_URL)
    url_payload = {'report_type': "panel",
                   'genome_id': None,
                   'filter_id': filter_id,
                   'panel_id': panel_id,
                   'project_id': project_id,
                   'accession_id': accession_id}

    sys.stdout.write("Launching report...")
    sys.stdout.write("\n\n")
    sys.stdout.flush()
    result = requests.post(url, auth=auth, data=json.dumps(url_payload))
    return result.json()


def main():
    """Main function, creates a panel report.
    """
    parser = argparse.ArgumentParser(description='Launch a panel report with no genome.')
    parser.add_argument('p', metavar='panel_id', type=int)
    parser.add_argument('a', metavar='accession_id', type=str)
    parser.add_argument('--project_id', metavar='project_id', type=int)
    parser.add_argument('--f', metavar='filter_id', type=int)
    args = parser.parse_args()

    filter_id = args.f
    panel_id = args.p
    accession_id = args.a
    project_id = args.project_id

    json_response = launch_panel_report(filter_id,
                                        panel_id,
                                        accession_id,
                                        project_id)
    if "clinical_report" not in json_response.keys():
        print json_response
        sys.exit("Failed to launch. Check report parameters for correctness.")
    clinical_report = json_response['clinical_report']

    # Print out the object's fields. This represents a confirmation of the
    # information for the launched report.
    sys.stdout.write('Launched Clinical Report:\n'
                     'id: {}\n'
                     'test_type: {}\n'
                     'accession_id: {}\n'
                     'created_on: {}\n'
                     'created_by: {}\n'
                     'status: {}\n'
                     'filter_id: {}\n'
                     'panel_id: {}\n'
                     'workspace_id: {}\n'
                     'sample_collected_date: {}\n'
                     'sample_received_date: {}\n'
                     'include_cosmic: {}\n'
                     .format(clinical_report.get('id', 'Missing'),
                             clinical_report.get('test_type', 'Missing'),
                             clinical_report.get('accession_id', 'Missing'),
                             clinical_report.get('created_on', 'Missing'),
                             clinical_report.get('created_by', 'Missing'),
                             clinical_report.get('status', 'Missing'),
                             clinical_report.get('filter_id', 'Missing'),
                             clinical_report.get('panel_id', 'Missing'),
                             clinical_report.get('workspace_id', 'Missing'),
                             clinical_report.get('sample_collected_date', 'Missing'),
                             clinical_report.get('sample_received_date', 'Missing'),
                             clinical_report.get('include_cosmic', 'Missing')))


if __name__ == "__main__":
    main()

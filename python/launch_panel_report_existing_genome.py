"""Upload a genome and use it to create a panel report. Optionally, include
a file containing patient information to populate patient information
fields in the clinical report. This file should be a csv formatted in this way:

Opal Patient Information,value
Patient Last Name,John
Patient First Name,Doe
Patient DOB,1/1/00
Accession ID,JD1
Patient Sex,Male/Female
Patient Ethnicity,Caucasian
Indication for Testing,Disease
Specimen Type,Blood
Date Specimen Collected,9/9/14
Date Specimen Received,9/13/14
Ordering Physician,Paul Billings

If you are having trouble with the patient information file, make sure its
line endings are newlines (\n) and not the deprecated carriage returns (\r)
"""

import csv
import json
import os
import requests
from requests.auth import HTTPBasicAuth
import sys

#Load environment variables for request authentication parameters
if "OMICIA_API_PASSWORD" not in os.environ:
    sys.exit("OMICIA_API_PASSWORD environment variable missing")

if "OMICIA_API_LOGIN" not in os.environ:
    sys.exit("OMICIA_API_LOGIN environment variable missing")

OMICIA_API_LOGIN = os.environ['OMICIA_API_LOGIN']
OMICIA_API_PASSWORD = os.environ['OMICIA_API_PASSWORD']
OMICIA_API_URL = os.environ.get('OMICIA_API_URL', 'https://api.omicia.com')
auth = HTTPBasicAuth(OMICIA_API_LOGIN, OMICIA_API_PASSWORD)

# A map between the row numbers and fields from the patient information csv
patient_info_row_map = {
    0: 'last_name',
    1: 'first_name',
    2: 'dob',
    3: 'accession_id',
    4: 'sex',
    5: 'ethnicity',
    6: 'indication_for_testing',
    7: 'specimen_type',
    8: 'date_collected',
    9: 'date_received',
    10: 'ordering_physician'
}


def generate_patient_info_json(patient_info_file_name):
    """Given a properly formatted csv file containing the patient information,
    generate and return a JSON object representing its contents.
    """
    patient_info = {}
    with open(patient_info_file_name) as f:
        reader = csv.reader(f)
        next(reader, None)  # Skip the header
        for i, row in enumerate(reader):
            patient_info[patient_info_row_map[i]] = row[1]
    return patient_info


def launch_panel_report(genome_id, filter_id, panel_id,
                        accession_id, patient_info_file_name):
    """Launch a panel report given genome id, filter id, and panel id
    parameters. Return the JSON response.
    """

    # If a patient information csv file is provided, use it to generate a
    # representative JSON object
    if patient_info_file_name:
        patient_info = generate_patient_info_json(patient_info_file_name)

    # Construct url and request
    url = "{}/reports/".format(OMICIA_API_URL)
    url_payload = {'report_type': "Panel Report",
                   'genome_id': int(genome_id),
                   'filter_id': int(filter_id),
                   'panel_id': int(panel_id),
                   'accession_id': accession_id}

    sys.stdout.write("Launching report...")
    sys.stdout.write("\n\n")
    sys.stdout.flush()
    # If patient information was not provided, make a post request to reports
    # without a patient information parameter in the url
    if not patient_info_file_name:
        result = requests.post(url, auth=auth, data=json.dumps(url_payload))
    else:
    # If patient information was provided, add it to the request url
        url_payload['patient_info'] = patient_info
        result = requests.post(url, auth=auth, data=json.dumps(url_payload))

    return result.json()


def main(argv):
    """Main function, creates a panel report.
    """
    if len(argv) < 4:
        sys.exit("Usage: python launch_panel_report_existing_genome.py \
        <genome_id> <filter_id> <panel_id> <accession_id>\
        optional: <patient_info_file>")
    genome_id = argv[0]
    filter_id = argv[1]
    panel_id = argv[2]
    accession_id = argv[3]

    # If a patient information file name is provided, use it. Otherwise
    # leave it empty as a None object.
    if len(argv) == 5:
        patient_info_file_name = argv[4]
    else:
        patient_info_file_name = None

    json_response = launch_panel_report(genome_id,
                                        filter_id,
                                        panel_id,
                                        accession_id,
                                        patient_info_file_name)

    if "clinical_report" not in json_response.keys():
        sys.exit("Failed to launch. Check report parameters for correctness.")
    clinical_report = json_response['clinical_report']

    # Print out the object's fields. This represents a confirmation of the
    # information for the launched report.
    sys.stdout.write('Launched Clinical Report:\n'
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
                     .format(clinical_report.get('test_type','Missing'),
                             clinical_report.get('accession_id','Missing'),
                             clinical_report.get('created_on','Missing'),
                             clinical_report.get('created_by','Missing'),
                             clinical_report.get('status','Missing'),
                             clinical_report.get('filter_id','Missing'),
                             clinical_report.get('panel_id','Missing'),
                             clinical_report.get('workspace_id','Missing'),
                             clinical_report.get('sample_collected_date','Missing'),
                             clinical_report.get('sample_received_date','Missing'),
                             clinical_report.get('include_cosmic','Missing')))


if __name__ == "__main__":
    main(sys.argv[1:])
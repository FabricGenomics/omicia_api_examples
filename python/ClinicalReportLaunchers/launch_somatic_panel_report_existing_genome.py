"""
Using an existing genome id, launch a somatic panel report. Optionally, include
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

import argparse
import csv
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

# A map between the row numbers and fields from the patient information csv
patient_info_row_map = {
    0: 'Last Name',
    1: 'First Name',
    2: 'Patient DOB',
    3: 'Accession ID',
    4: 'Patient Sex',
    5: 'Patient Ethnicity',
    6: 'Indication for Testing',
    7: 'Specimen Type',
    8: 'Date Specimen Collected',
    9: 'Date Specimen Received',
    10: 'Ordering Physician'
}


def generate_patient_info_json(patient_info_file_name):
    """Given a properly formatted csv file containing the patient information,
    generate and return a JSON object representing its contents.
    """
    patient_info = {}
    with open(patient_info_file_name, 'rU') as f:
        reader = csv.reader(f)
        next(reader, None)  # Skip the header
        for i, row in enumerate(reader):
            if i < 11:
                patient_info[patient_info_row_map[i]] = row[1]
    return patient_info


def add_fields_to_cr(cr_id, patient_fields):
    """Use the Omicia API to fill in custom patient fields for a clinical report
    e.g. patient_fields: '{"Patient Name": "Eric", "Gender": "Male", "Accession Number": "1234"}'
    """
    #Construct request
    url = "{}/reports/{}/patient_fields"
    url = url.format(FABRIC_API_URL, cr_id)
    url_payload = json.dumps(patient_fields)

    sys.stdout.write("Adding custom patient fields to report...")
    sys.stdout.write("\n\n")
    sys.stdout.flush()
    result = requests.post(url, auth=auth, data=url_payload)
    return result.json()


def launch_somatic_panel_report(genome_id, filter_id, panel_id, disease_id, accession_id):
    """Launch a panel report given genome id, filter id, and panel id
    parameters. Return the JSON response.
    """
    # Construct url and request
    url = "{}/reports/".format(FABRIC_API_URL)
    url_payload = {'report_type': "somatic_panel",
                   'proband_genome_id': genome_id,
                   'filter_id': filter_id,
                   'panel_id': panel_id,
                   'disease_id': disease_id,
                   'accession_id': accession_id,
                   'include_cosmic': True}

    sys.stdout.write("Launching report...")
    sys.stdout.write("\n\n")
    sys.stdout.flush()
    # If patient information was not provided, make a post request to reports
    # without a patient information parameter in the url
    result = requests.post(url, auth=auth, data=json.dumps(url_payload))
    return result.json()


def main(argv):
    """Main function, creates a panel report.
    """
    parser = argparse.ArgumentParser(description='Launch a panel report with no genome.')
    parser.add_argument('g', metavar='genome_id', type=int)
    parser.add_argument('p', metavar='panel_id', type=int)
    parser.add_argument('d', metavar='disease_id', type=str)
    parser.add_argument('a', metavar='accession_id', type=str)
    parser.add_argument('--f', metavar='filter_id', type=int)
    parser.add_argument('--patient_info_file', metavar='patient_info_file', type=str)
    args = parser.parse_args()

    sys.stdout.write('=================================================\n')
    sys.stdout.write('NOTE: THIS WILL NOT WORK UNTIL FE 6.2 IS RELEASED\n')
    sys.stdout.write('=================================================\n')

    genome_id = args.g
    filter_id = args.f
    panel_id = args.p
    accession_id = args.a
    disease_id = args.d
    patient_info_file_name = args.patient_info_file

    json_response = launch_somatic_panel_report(genome_id,
                                                filter_id,
                                                panel_id,
                                                disease_id,
                                                accession_id)
    if "clinical_report" not in json_response.keys():
        print(json_response)
        sys.exit("Failed to launch. Check report parameters for correctness.")
    clinical_report = json_response['clinical_report']

    # If a patient information csv file is provided, use it to generate a
    # representative JSON object
    if patient_info_file_name:
        clinical_report_id = clinical_report.get('id')
        patient_info = generate_patient_info_json(patient_info_file_name)
        add_fields_to_cr(clinical_report_id, patient_info)

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
    main(sys.argv[1:])

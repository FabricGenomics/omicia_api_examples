"""Create a new exome report from an uploaded genome. Optionally, include
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
"""

import csv
import json
import os
import requests
from requests.auth import HTTPBasicAuth
import sys

#Load environment variables for request authentication parameters
OMICIA_API_LOGIN = os.environ['OMICIA_API_LOGIN']
OMICIA_API_PASSWORD = os.environ['OMICIA_API_PASSWORD']
OMICIA_API_URL = os.environ['OMICIA_API_URL']


def generate_patient_info_json(patient_info_file_name):
    """Given a properly formatted csv file containing the patient information,
    generate and return a JSON object representing its contents.
    """
    patient_info = {}
    with open(patient_info_file_name) as f:
        reader = csv.reader(f)
        next(reader, None)  # Skip the header
        for i,row in enumerate(reader):
            if i == 0:
                patient_info['last_name'] = row[1]
            elif i == 1:
                patient_info['first_name'] = row[1]
            elif i == 2:
                patient_info['dob'] = row[1]
            elif i == 4:
                patient_info['sex'] = row[1]
            elif i == 5:
                patient_info['ethnicity'] = row[1]
            elif i == 6:
                patient_info['indication_for_testing'] = row[1]
            elif i == 7:
                patient_info['specimen_type'] = row[1]
            elif i == 8:
                patient_info['date_collected'] = row[1]
            elif i == 9:
                patient_info['date_received'] = row[1]
            elif i == 10:
                patient_info['ordering_physician'] = row[1]
    return patient_info


def launch_exome_report(genome_id, accession_id, patient_info_file_name):
    """Launch a panel report given genome id, filter id, and panel id
    parameters. Return the JSON response.
    """

    # If a patient information csv file is provided, use it to generate a
    # representative JSON object
    if patient_info_file_name:
        patient_info = generate_patient_info_json(patient_info_file_name)

    auth = HTTPBasicAuth(OMICIA_API_LOGIN, OMICIA_API_PASSWORD)

    # Construct url and request
    url = "{}/reports/".format(OMICIA_API_URL)
    url_payload = {'report_type': "Exome Report",
                   'genome_id': int(genome_id),
                   'accession_id': accession_id}

    # If patient information was not provided, make a post request to reports
    # without a patient information parameter in the url
    if not patient_info_file_name:
        result = requests.post(url, auth=auth, data=json.dumps(url_payload))
    else:
    # If patient information was provided, add it to the request url
        url_payload['patient_info'] = patient_info
        result = requests.post(url, auth=auth, data=json.dumps(url_payload))

    json_data = json.loads(result.text)
    return json_data


def main(argv):
    """Main function, creates an exome report.
    """
    if len(argv) < 2:
        sys.exit("Usage: python launch_exome_report.py \
        <genome_id> <accession_id>\
        optional: <patient_info_file>")
    genome_id = argv[0]
    accession_id = argv[1]

    # If a patient information file name is provided, use it. Otherwise
    # leave it empty as a None object.
    if len(argv) == 3:
        patient_info_file_name = argv[2]
    else:
        patient_info_file_name = None

    exome_report_json = launch_exome_report(genome_id,
                                            accession_id,
                                            patient_info_file_name)

    # Print out the json object. This represents a confirmation of the
    # information for the launched report.
    print exome_report_json


if __name__ == "__main__":
    main(sys.argv[1:])
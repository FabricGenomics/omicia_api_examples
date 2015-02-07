"""Create a new family report from an new genome trio. Optionally, include
a file containing patient (proband) information to populate patient information
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


def get_family_manifest_info(family_folder):
    """Generate an object containing the data from the manifest.csv
    file in the genomes folder, including each filename along with
    its genome label, external id, sex, and format.
    """
    family_manifest_info = {}
    with open(family_folder + '/family_manifest.csv') as f:
        reader = csv.reader(f)
        next(reader, None)  # Skip the header
        for i, row in enumerate(reader):
            if i == 0:
                family_member = "mother"
            elif i == 1:
                family_member = "father"
            elif i == 2:
                family_member = "proband"
            else:
                break
            family_manifest_info[family_member] = {"genome_filename": row[0],
                                                   "genome_label": row[1],
                                                   "external_id": row[2],
                                                   "genome_sex": row[3],
                                                   "format": row[4]}
    return family_manifest_info


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


def launch_family_report(mother_genome_id, father_genome_id,
                         proband_genome_id, proband_sex, score_indels,
                         reporting_cutoff, accession_id,
                         patient_info_file_name):
    """Launch a family report. Return the JSON response.
    """
    print mother_genome_id
    print father_genome_id
    print proband_genome_id
    print proband_sex
    print score_indels
    print reporting_cutoff
    print accession_id
    print patient_info_file_name

    # If a patient information csv file is provided, use it to generate a
    # representative JSON object
    if patient_info_file_name:
        patient_info = generate_patient_info_json(patient_info_file_name)
        print patient_info

        """
    auth = HTTPBasicAuth(OMICIA_API_LOGIN, OMICIA_API_PASSWORD)

    # Construct url and request
    url = "{}/reports/".format(OMICIA_API_URL)
    url_payload = {'report_type': "Family Report",
                   'mother_genome_id': int(mother_genome_id),
                   'father_genome_id': int(father_genome_id),
                   'proband_genome_id': int(proband_genome_id),
                   'proband_sex': proband_sex,
                   'background': 'FULL',
                   'score_indels': score_indels,
                   'reporting_cutoff': reporting_cutoff,
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
"""

def upload_genome(project_id, genome_info, family_folder):
    """Upload a genome from a given folder to a specified project
    """
    # Construct url and request
    url = "{}/projects/{}/genomes?".format(OMICIA_API_URL, project_id)
    payload = {'genome_label': genome_info['genome_label'],
               'genome_sex': genome_info['genome_sex'],
               'external_id': genome_info['external_id'],
               'assembly_version': 'hg19',
               'format': genome_info['format']}

    # Upload genome
    with open(family_folder + "/" + genome_info['genome_filename'], 'rb') as file_handle:
        files = {'file_name': file_handle}
        auth = HTTPBasicAuth(OMICIA_API_LOGIN, OMICIA_API_PASSWORD)
        # Post request and store newly uploaded genome's information
        result = requests.put(url, files=files, params=payload, auth=auth)
        json_data = json.loads(result.text)
        return json_data["genome_id"]


def upload_genomes_to_project(project_id, family_folder):
    """Upload each of the three genomes in the folder containing the
    family trio to the specified project
    """
     # Get information about each of the family members from the family manifest
    family_manifest_info = get_family_manifest_info(family_folder)

    # Use the family genome information to upload each genome to the project
    mother_genome_id = upload_genome(project_id,
                                     family_manifest_info['mother'],
                                     family_folder)

    father_genome_id = upload_genome(project_id,
                                     family_manifest_info['father'],
                                     family_folder)

    proband_genome_id = upload_genome(project_id,
                                      family_manifest_info['proband'],
                                      family_folder)

    return {'mother_genome_id': mother_genome_id,
            'father_genome_id': father_genome_id,
            'proband_genome': {'id': proband_genome_id,
                               'sex': family_manifest_info['proband']['genome_sex']}
            }


def main(argv):
    """Main function, creates a panel report.
    """
    if len(argv) < 5:
        sys.exit("Usage: python launch_family_report.py <project_id> \
        <family_folder> <score_indels> <reporting_cutoff> <accession_id> \
        optional: <patient_info_file>")
    project_id = argv[0]
    family_folder = argv[1]
    score_indels = argv[2]
    reporting_cutoff = argv[3]
    accession_id = argv[4]

    family_genome_ids = upload_genomes_to_project(project_id, family_folder)
    print family_genome_ids

    # If a patient information file name is provided, use it. Otherwise
    # leave it empty as a None object.
    if len(argv) == 6:
        patient_info_file_name = argv[5]
    else:
        patient_info_file_name = None

    family_report_json = launch_family_report(
        family_genome_ids['mother_genome_id'],
        family_genome_ids['father_genome_id'],
        family_genome_ids['proband_genome']['id'],
        family_genome_ids['proband_genome']['sex'],
        score_indels,
        reporting_cutoff,
        accession_id,
        patient_info_file_name)


if __name__ == "__main__":
    main(sys.argv[1:])
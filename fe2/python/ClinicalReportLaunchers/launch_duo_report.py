"""Create a new family report from an new genome duo. This requires putting all
three family genomes in a folder along with a descriptor file titled 'family_manifest.csv,'
which should have the following format:

filename,label,external_id,sex,format,affected,relation
NA19238.vcf.gz,Proband,1,female,vcf.gz,affected,self
NA19239.vcf.gz,related,2,male,vcf.gz,unaffected,father

Optionally, include a file containing patient (proband) information to populate
patient information fields in the clinical report. This file should be a csv
formatted in this way:

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

If you are having trouble with using either csv file, make sure its
line endings are newlines (\n) and not the deprecated carriage returns (\r)
"""

import csv
import json
import os
import requests
from requests.auth import HTTPBasicAuth
import sys

_MANIFEST_FILENAME = 'duo_manifest.csv'

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


def get_family_manifest_info(family_folder):
    """Generate an object containing the data from the manifest.csv
    file in the genomes folder, including each filename along with
    its genome label, external id, sex, and format.
    """
    family_manifest_info = {}
    # A map between the row numbers and family member from the family manifest csv
    family_info_row_map = {
        0: 'proband',
        1: 'related'
    }

    # First check to make sure there is in fact a family_manifest.csv file
    if 'family_manifest.csv' not in os.listdir(family_folder):
        sys.exit("No family_manifest.csv file in folder provided.")

    with open(os.path.join(family_folder, _MANIFEST_FILENAME)) as f:
        reader = csv.reader(f)
        next(reader, None)  # Skip the header
        for i, row in enumerate(reader):
            if i < 3:
                # family_member is mother, father, or proband
                family_member = family_info_row_map[i]
                family_manifest_info[family_member] = {"genome_filename": row[0],
                                                       "genome_label": row[1],
                                                       "external_id": row[2],
                                                       "genome_sex": row[3],
                                                       "format": row[4],
                                                       "affected": row[5],
                                                       "relation": row[6]}
    return family_manifest_info


def launch_duo_report(related_genome_id, duo_relation, duo_affected,
                      proband_genome_id, proband_sex, score_indels,
                      accession_id):
    """Launch a family report. Return the JSON response.
    """
    # Construct url and request
    url = "{}/reports/".format(FABRIC_API_URL)
    url_payload = {'report_type': "Duo",
                   'duo_relation_genome_id': int(related_genome_id),
                   'duo_relation': duo_relation,
                   'duo_affected': duo_affected == 'affected',
                   'proband_genome_id': int(proband_genome_id),
                   'proband_sex': ('f' if proband_sex == 'female' else 'm'),
                   'background': 'FULL',
                   'score_indels': bool(score_indels),
                   'accession_id': accession_id}

    sys.stdout.write("Launching family report...\n")
    result = requests.post(url, auth=auth, data=json.dumps(url_payload))

    return result.json()


def upload_genome(project_id, genome_info, family_folder):
    """Upload a genome from a given folder to a specified project
    """
    # Construct url and request
    url = "{}/projects/{}/genomes?".format(FABRIC_API_URL, project_id)
    payload = {'genome_label': genome_info['genome_label'],
               'genome_sex': genome_info['genome_sex'],
               'external_id': genome_info['external_id'],
               'assembly_version': 'hg19',
               'format': genome_info['format']}

    # Upload genome
    with open(family_folder + "/" + genome_info['genome_filename'], 'rb') as file_handle:
        # Post request and store newly uploaded genome's information
        result = requests.put(url, data=file_handle, params=payload, auth=auth)
        sys.stdout.write(".")
        sys.stdout.flush()
        return result.json()["genome_id"]


def upload_genomes_to_project(project_id, family_folder):
    """Upload each of the three genomes in the folder containing the
    family trio to the specified project
    """
     # Get information about each of the family members from the family manifest
    family_manifest_info = get_family_manifest_info(family_folder)

    # Use the family genome information to upload each genome to the project
    sys.stdout.write("Uploading")
    sys.stdout.flush()

    related_genome_id = \
        upload_genome(project_id, family_manifest_info['related'], family_folder)

    proband_genome_id = \
        upload_genome(project_id, family_manifest_info['proband'], family_folder)

    sys.stdout.write("\n")

    return {'related_genome': {
                'id': related_genome_id,
                'relation': family_manifest_info['related']['relation'],
                'affected': family_manifest_info['related']['affected']
            },
            'proband_genome':
                {
                'id': proband_genome_id,
                'sex': family_manifest_info['proband']['genome_sex']
                }
            }


def main(argv):
    """Main function, creates a panel report.
    """
    if len(argv) < 4:
        sys.exit("Usage: python launch_family_report.py <project_id> \
        <family_folder> <score_indels> <accession_id> \
        optional: <patient_info_file>")
    project_id = argv[0]
    family_folder = argv[1]
    score_indels = argv[2]
    accession_id = argv[3]

    family_genome_ids = upload_genomes_to_project(project_id, family_folder)

    # Confirm uploaded genomes' data
    sys.stdout.write("Uploaded 2 genomes:\n")
    sys.stdout.write("related_genome_id: {}\n"
                     "relation: {}\n"
                     "related_affected: {}\n"
                     "proband_genome_id: {}\n"
                     "proband_sex: {}\n"
                     .format(family_genome_ids['related_genome']['id'],
                             family_genome_ids['related_genome']['relation'],
                             family_genome_ids['related_genome']['affected'],
                             family_genome_ids['proband_genome']['id'],
                             family_genome_ids['proband_genome']['sex']))

    # If a patient information file name is provided, use it. Otherwise
    # leave it empty as a None object.
    if len(argv) == 5:
        patient_info_file_name = argv[4]
    else:
        patient_info_file_name = None

    family_report_json = launch_duo_report(
        family_genome_ids['related_genome']['id'],
        family_genome_ids['related_genome']['relation'],
        family_genome_ids['related_genome']['affected'],
        family_genome_ids['proband_genome']['id'],
        family_genome_ids['proband_genome']['sex'],
        score_indels,
        accession_id)

    # Confirm launched report data
    sys.stdout.write("\n")

    if "clinical_report" not in family_report_json.keys():
        print family_report_json
        sys.exit("Failed to launch. Check report parameters for correctness.")
    clinical_report = family_report_json['clinical_report']

     # If a patient information csv file is provided, use it to generate a
    # representative JSON object and add the patient fields to the report
    if patient_info_file_name:
        clinical_report_id = clinical_report.get('id')
        patient_info = generate_patient_info_json(patient_info_file_name)
        add_fields_to_cr(clinical_report_id, patient_info)

    sys.stdout.write('Launched Family Report:\n'
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
                     'vaast_report_id: {}\n'
                     'duo_relation_genome_id: {}\n'
                     'genome_id: {}\n'
                     'status: {}\n'
                     'version: {}\n'
                     .format(clinical_report.get('id', 'Missing'),
                             clinical_report.get('test_type','Missing'),
                             clinical_report.get('accession_id','Missing'),
                             clinical_report.get('created_on','Missing'),
                             clinical_report.get('created_by','Missing'),
                             clinical_report.get('status','Missing'),
                             clinical_report.get('filter_id','Missing'),
                             clinical_report.get('panel_id','Missing'),
                             clinical_report.get('workspace_id','Missing'),
                             clinical_report.get('sample_collected_date','Missing'),
                             clinical_report.get('sample_received_date','Missing'),
                             clinical_report.get('include_cosmic','Missing'),
                             clinical_report.get('vaast_report_id', 'Missing'),
                             clinical_report.get('duo_relation_genome_id', 'Missing'),
                             clinical_report.get('genome_id', 'Missing'),
                             clinical_report.get('status', 'Missing'),
                             clinical_report.get('version', 'Missing')))

if __name__ == "__main__":
    main(sys.argv[1:])

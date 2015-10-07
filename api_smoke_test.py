__author__ = 'erickofman'
"""Usage: python api_smoke_test.py ../omicia_api_examples/python family_folder family_folder/NA19240_small.vcf.gz 727 1506 205781

On test1 in API Testing Workspace:
python api_smoke_test.py ../omicia_api_examples/python family_folder family_folder/NA19240_small.vcf.gz 727 1881 206280

Make sure to cancel any VAAST jobs that are launched as a byproduct of running this script.
"""

import sys
import subprocess
import argparse
import simplejson as json
import datetime
import re
import os

# Colors (OK green color and default color)
OKGREEN = '\033[92m'
ENDC = '\033[0m'

# API example script names
CREATE_PROJECT = "create_project.py"
UPLOAD_GENOMES_FOLDER = "upload_genomes_folder.py"
UPLOAD_GENOMES_FOLDER_WITH_MANIFEST = "upload_genomes_folder_with_manifest.py"
UPLOAD_GENOME = "upload_genome.py"
GET_GENOMES = "get_genomes.py"
LAUNCH_GENOMELESS_PANEL_REPORT = "launch_panel_report_no_genome.py"
ADD_GENOME_TO_REPORT = "add_genome_to_cr.py"
LAUNCH_PANEL_REPORT_EXISTING_GENOME = "launch_panel_report_existing_genome.py"
LAUNCH_PANEL_REPORT_NEW_GENOME = "launch_panel_report_new_genome.py"
LAUNCH_FAMILY_REPORT_NEW_GENOMES = "launch_family_report.py"
LAUNCH_GENOMELESS_FAMILY_REPORT = "launch_family_report_no_genome.py"
GET_REPORT_PATIENT_FIELDS = "get_patient_fields.py"
POST_REPORT_PATIENT_FIELDS = "post_patient_fields.py"
POST_QC_DATA_ENTRY = "post_qc_data.py"
GET_REPORT_STATUS = "get_report_status.py"
POST_PANEL = "post_panel.py"

def print_ok_output(output):
    """Print the parameter in OKGREEN color"""
    sys.stdout.write("{}{}\n{}".format(OKGREEN, output, ENDC))


def test_upload_genome(path, project_id, genome_vcf):
    """Test uploading a single vcf file"""
    sys.stdout.write("\n{}: Testing uploading one genome...\n".format(UPLOAD_GENOME))
    p = subprocess.Popen(["python", os.path.join(path, UPLOAD_GENOME), str(project_id), "genome{}/{}".format(month, day), "unspecified", "vcf", os.path.join(path, genome_vcf)],
                         stdout=subprocess.PIPE)
    output, err = p.communicate()

    output_lines = output.split('\n')
  
    assert(output_lines[0] == "Uploading...")
    assert(re.match("genome_label: genome\d+/\d+, genome_id: \d+, size: \d+\.\d+ kB", output_lines[1]))

    sys.stdout.write("Uploaded one genome.\n")
    print_ok_output(output)


def test_upload_genomes_folder(path, project_id, family_folder):
    """Test uploading an entire folder of genomes"""
    sys.stdout.write("\n{}: Testing uploading a folder of genomes...\n".format(UPLOAD_GENOMES_FOLDER))
    p = subprocess.Popen(["python", os.path.join(path, UPLOAD_GENOMES_FOLDER), str(project_id), os.path.join(path, family_folder)],
                         stdout=subprocess.PIPE)
    output, err = p.communicate()

    output_lines = output.split('\n')
    assert(output_lines[0] == "Uploading...")
    assert(re.match("genome_label: NA19238_small.vcf.gz, genome_id: \d+, size: 1.8 kB", output_lines[1]))
    assert(re.match("genome_label: NA19239_small.vcf.gz, genome_id: \d+, size: 1.8 kB", output_lines[2]))
    assert(re.match("genome_label: NA19240_small.vcf.gz, genome_id: \d+, size: 1.7 kB", output_lines[3]))

    sys.stdout.write("Uploaded a folder of genomes.\n")
    print_ok_output(output)


def test_upload_genomes_folder_with_manifest(path, project_id, family_folder):
    """Test uploading an entire folder of genomes"""
    sys.stdout.write("\n{}: Testing uploading a folder of genomes with a manifest...\n".format(UPLOAD_GENOMES_FOLDER_WITH_MANIFEST))
    p = subprocess.Popen(["python", os.path.join(path, UPLOAD_GENOMES_FOLDER_WITH_MANIFEST), str(project_id), os.path.join(path, family_folder)],
                         stdout=subprocess.PIPE)
    output, err = p.communicate()

    output_lines = output.split('\n')
    assert(output_lines[0] == "Uploading...")
    assert(re.match("genome_label: CG Yoruban Daughter, genome_id: \d+, external_id: 3, size: 1.7 kB", output_lines[1]))
    assert(re.match("genome_label: CG Yoruban Mother, genome_id: \d+, external_id: 1, size: 1.8 kB", output_lines[2]))
    assert(re.match("genome_label: CG Yoruban Father, genome_id: \d+, external_id: 2, size: 1.8 kB", output_lines[3]))

    sys.stdout.write("Uploaded a folder of genomes with a manifest.\n")
    print_ok_output(output)


def test_create_project(path, month, day):
    """Test the api example script that creates a project"""
    sys.stdout.write("{}: Testing project creation...\n".format(CREATE_PROJECT))
    p = subprocess.Popen(["python", os.path.join(path, CREATE_PROJECT), "SmokeTest{}/{}".format(month, day), "SmokeTestDescription", "CONTRIBUTOR"],
                         stdout=subprocess.PIPE)
    output, err = p.communicate()

    # output should be Project id: <id>
    project_id = int(output.split(':')[1].strip())
    sys.stdout.write("Created project. ID is {}.\n".format(project_id))
    print_ok_output(output)

    return project_id


def test_get_genomes(path, project_id):
    """Test retrieving the genomes from a project"""
    sys.stdout.write("{}: Testing get genomes...\n".format(GET_GENOMES))
    p = subprocess.Popen(["python", os.path.join(path, GET_GENOMES), str(project_id)],
                         stdout=subprocess.PIPE)
    output, err = p.communicate()

    output_lines = output.split('\n')
    assert(re.match("name: genome\d+/\d+", output_lines[0]))
    assert(re.match("upload_date: *", output_lines[1]))
    assert(re.match("genome_status: *", output_lines[2]))
    assert(re.match("report_count: 1", output_lines[3]))
    assert(re.match("uploaded_by: \d+", output_lines[4]))
    assert(re.match("is_upgraded: False", output_lines[5]))
    assert(re.match("project_id: \d+", output_lines[6]))
    assert(re.match("external_id:", output_lines[7].strip()))
    assert(re.match("id: \d+", output_lines[8]))

    sys.stdout.write("Got genomes.\n")
    print_ok_output(output)


def test_launch_panel_report_new_genome(path, filter_id, panel_id, project_id, genome_vcf):
    """Test launching a panel report with new genome"""
    accession_id = "new_genome_panel"
    sys.stdout.write("{}: Testing launch panel report with a new genome...\n".format(LAUNCH_PANEL_REPORT_NEW_GENOME))
    p = subprocess.Popen(["python", os.path.join(path, LAUNCH_PANEL_REPORT_NEW_GENOME), str(project_id), "new_panel_genome",
                          "unspecified", "vcf", os.path.join(path, genome_vcf), str(filter_id), str(panel_id), accession_id],
                         stdout=subprocess.PIPE)
    output, err = p.communicate()

    output_lines = output.split('\n')
    assert(re.match("Uploading genome...", output_lines[0]))
    assert(re.match("genome_id: \d+", output_lines[1]))
    assert(re.match("Launching report...", output_lines[2]))
    assert(re.match("Launched Clinical Report:", output_lines[4]))
    assert(re.match("id: \d+", output_lines[5]))
    assert(re.match("test_type: panel", output_lines[6]))
    assert(re.match("accession_id: {}".format(accession_id), output_lines[7]))
    assert(re.match("created_on: [\d+|\-|:]+", output_lines[8]))
    assert(re.match("created_by: \d+", output_lines[9]))
    assert(re.match("status: WAITING", output_lines[10]))
    assert(re.match("filter_id: {}".format(filter_id), output_lines[11]))
    assert(re.match("panel_id: {}".format(panel_id), output_lines[12]))

    clinical_report_id = int(output_lines[5].split(":")[1])

    sys.stdout.write("Launched panel report with a new genome. ID is {}.\n".format(clinical_report_id))
    print_ok_output(output)
    return clinical_report_id


def test_launch_family_report_new_genomes(path, project_id, family_folder):
    """Test launching a family report with new genomes"""
    accession_id = "new_genome_family"
    sys.stdout.write("{}: Testing launch family report with new genomes...\n".format(LAUNCH_FAMILY_REPORT_NEW_GENOMES))
    p = subprocess.Popen(["python", os.path.join(path, LAUNCH_FAMILY_REPORT_NEW_GENOMES), str(project_id), os.path.join(path, family_folder), "false", "10", accession_id],
                         stdout=subprocess.PIPE)
    output, err = p.communicate()
    output_lines = output.split('\n')

    assert(re.match("Uploading...", output_lines[0]))
    assert(re.match("Uploaded 3 genomes:", output_lines[1]))
    assert(re.match("mother_genome_id: \d+", output_lines[2]))
    assert(re.match("father_genome_id: \d+", output_lines[3]))
    assert(re.match("proband_genome_id: \d+", output_lines[4]))
    assert(re.match("proband_sex: female", output_lines[5]))
    assert(re.match("Launching family report...", output_lines[6]))

    assert(re.match("Launched Family Report:", output_lines[8]))
    assert(re.match("id: \d+", output_lines[9]))
    assert(re.match("test_type: Trio", output_lines[10]))
    assert(re.match("accession_id: {}".format(accession_id), output_lines[11]))
    assert(re.match("created_on: [\d+|\-|:]+", output_lines[12]))
    assert(re.match("created_by: \d+", output_lines[13]))
    assert(re.match("status: WAITING", output_lines[14]))
    assert(re.match("filter_id: None", output_lines[15]))
    assert(re.match("panel_id: None", output_lines[16]))

    clinical_report_id = int(output_lines[9].split(":")[1])

    sys.stdout.write("Launched a family report with new genomes. ID is {}.\n".format(clinical_report_id))
    print_ok_output(output)
    return clinical_report_id


def test_launch_family_report_no_genomes(path, project_id, family_folder):
    """Test launching a family report with new genomes"""
    accession_id = "no_genome_family"
    sys.stdout.write("{}: Testing launch family report with new genomes...\n".format(LAUNCH_GENOMELESS_FAMILY_REPORT))
    p = subprocess.Popen(["python", os.path.join(path, LAUNCH_GENOMELESS_FAMILY_REPORT), "false", "10", accession_id],
                         stdout=subprocess.PIPE)
    output, err = p.communicate()
    output_lines = output.split('\n')

    assert(re.match("Launching family report...", output_lines[0]))
    assert(re.match("Launched Family Report:", output_lines[2]))
    assert(re.match("id: \d+", output_lines[3]))
    assert(re.match("test_type: Trio", output_lines[4]))
    assert(re.match("accession_id: {}".format(accession_id), output_lines[5]))
    assert(re.match("created_on: [\d+|\-|:]+", output_lines[6]))
    assert(re.match("created_by: \d+", output_lines[7]))
    assert(re.match("status: WAITING FOR SAMPLE", output_lines[8]))
    assert(re.match("filter_id: None", output_lines[9]))
    assert(re.match("panel_id: None", output_lines[10]))

    clinical_report_id = int(output_lines[3].split(":")[1])

    sys.stdout.write("Launched a family report with no genomes. ID is {}.\n".format(clinical_report_id))
    print_ok_output(output)
    return clinical_report_id


def test_launch_panel_report_existing_genome(path, filter_id, panel_id, genome_id):
    """Test launching a panel report with no genome"""
    accession_id = "existing_genome_panel"
    sys.stdout.write("{}: Testing launch panel report with existing genome...\n".format(LAUNCH_PANEL_REPORT_EXISTING_GENOME))
    p = subprocess.Popen(["python", os.path.join(path, LAUNCH_PANEL_REPORT_EXISTING_GENOME), str(genome_id), str(filter_id), str(panel_id), accession_id],
                         stdout=subprocess.PIPE)
    output, err = p.communicate()

    output_lines = output.split('\n')

    assert(re.match("Launching report...", output_lines[0]))
    assert(re.match("Launched Clinical Report:", output_lines[2]))
    assert(re.match("id: \d+", output_lines[3]))
    assert(re.match("test_type: panel", output_lines[4]))
    assert(re.match("accession_id: {}".format(accession_id), output_lines[5]))
    assert(re.match("created_on: [\d+|\-|:]+", output_lines[6]))
    assert(re.match("created_by: \d+", output_lines[7]))
    assert(re.match("status: WAITING", output_lines[8]))
    assert(re.match("filter_id: {}".format(filter_id), output_lines[9]))
    assert(re.match("panel_id: {}".format(panel_id), output_lines[10]))

    clinical_report_id = int(output_lines[3].split(":")[1])

    sys.stdout.write("Launched panel report with existing genome. ID is {}.\n".format(clinical_report_id))
    print_ok_output(output)
    return clinical_report_id


def test_launch_panel_report_no_genome(path, filter_id, panel_id):
    """Test launching a panel report with no genome"""
    accession_id = "genomeless_panel"
    sys.stdout.write("{}: Testing launch panel report with no genomes...\n".format(LAUNCH_GENOMELESS_PANEL_REPORT))
    p = subprocess.Popen(["python", os.path.join(path, LAUNCH_GENOMELESS_PANEL_REPORT), str(filter_id), str(panel_id), accession_id],
                         stdout=subprocess.PIPE)
    output, err = p.communicate()

    output_lines = output.split('\n')
    assert(re.match("Launching report...", output_lines[0]))
    assert(re.match("Launched Clinical Report:", output_lines[2]))
    assert(re.match("id: \d+", output_lines[3]))
    assert(re.match("test_type: panel", output_lines[4]))
    assert(re.match("accession_id: {}".format(accession_id), output_lines[5]))
    assert(re.match("created_on: [\d+|\-|:]+", output_lines[6]))
    assert(re.match("created_by: \d+", output_lines[7]))
    assert(re.match("status: WAITING FOR SAMPLE", output_lines[8]))
    assert(re.match("filter_id: {}".format(filter_id), output_lines[9]))
    assert(re.match("panel_id: {}".format(panel_id), output_lines[10]))

    clinical_report_id = int(output_lines[3].split(":")[1])

    sys.stdout.write("Created genomeless panel report. ID is {}.\n".format(clinical_report_id))
    print_ok_output(output)
    return clinical_report_id


def test_post_patient_info_fields(path, clinical_report_id):
    """Test adding patient info fields to a clinical report. Assumes default fields."""
    sys.stdout.write("{}: Testing posting patient info fields to a clinical report...\n".format(POST_REPORT_PATIENT_FIELDS))

    patient_info_fields = json.dumps({"Patient Sex": "Male", "Last Name": "Kofman", "First Name": "Eric", "Patient DOB": "10/09/1991"})

    p = subprocess.Popen(["python", os.path.join(path, POST_REPORT_PATIENT_FIELDS), str(clinical_report_id), patient_info_fields],
                         stdout=subprocess.PIPE)
    output, err = p.communicate()

    output_lines = output.split('\n')
    assert(re.match("Adding custom patient fields to report...", output_lines[0]))
    assert(re.match("\[(\{.+:.+\},?)*\]", output_lines[2]))

    print_ok_output(output)
    return json.loads(output_lines[2])


def test_get_patient_info_fields(path, clinical_report_id):
    """Test getting the custom patient info fields for a clinical report"""
    sys.stdout.write("{}: Testing getting patient info fields for a clinical report...\n".format(GET_REPORT_PATIENT_FIELDS))
    p = subprocess.Popen(["python", os.path.join(path, GET_REPORT_PATIENT_FIELDS), str(clinical_report_id)],
                         stdout=subprocess.PIPE)
    output, err = p.communicate()
    assert(re.match("\[(\{.+:.+\},?)*\]", output))

    print_ok_output(output)
    return json.loads(output)


def test_post_qc_entry(path, clinical_report_id):
    """Test posting a quality control data entry to a clinical report"""
    sys.stdout.write("{}: Testing posting a quality control data entry to a clinical report...\n".format(POST_QC_DATA_ENTRY))
    p = subprocess.Popen(["python", os.path.join(path, POST_QC_DATA_ENTRY), str(clinical_report_id)],
                         stdout=subprocess.PIPE)
    output, err = p.communicate()
    assert(re.match("\[(\{.+:.+\},?)*\]", output))


def test_add_genome_to_cr(path, clinical_report_id, genome_id):
    """Test adding a genome to a clinical report"""
    sys.stdout.write("{}: Testing adding genome to clinical report...\n".format(ADD_GENOME_TO_REPORT))
    p = subprocess.Popen(["python", os.path.join(path, ADD_GENOME_TO_REPORT), "--p", str(genome_id), str(clinical_report_id)],
                         stdout=subprocess.PIPE)
    output, err = p.communicate()

    output_lines = output.split('\n')
    assert(re.match("Adding genome\(s\) to report...", output_lines[0]))
    assert(re.match("Clinical Report Info:", output_lines[2]))
    assert(re.match("id: \d+", output_lines[3]))
    assert(re.match("test_type: *", output_lines[4]))
    assert(re.match("accession_id: *", output_lines[5]))
    assert(re.match("created_on: [\d+|\-|:]+", output_lines[6]))
    assert(re.match("created_by: \d+", output_lines[7]))
    assert(re.match("status: WAITING", output_lines[8]))
    assert(re.match("filter_id: \d+", output_lines[9]))
    assert(re.match("panel_id: \d+", output_lines[10]))

    sys.stdout.write("Added genome to report.\n")
    print_ok_output(output)


def test_get_report_status(path, clinical_report_id, status):
    """Test getting a report's status"""
    sys.stdout.write("{}: Testing getting a clinical report's status...\n".format(GET_REPORT_STATUS))
    p = subprocess.Popen(["python", os.path.join(path, GET_REPORT_STATUS), str(clinical_report_id)],
                         stdout=subprocess.PIPE)
    output, err = p.communicate()

    # Assumes returned output is 'Report Status: <status>'
    returned_status = output.split(':')[1].strip()
    assert(re.match("{}".format(status), returned_status))
    print_ok_output(output)


def test_post_panel(path, month, day):
    """Test creating a new panel"""
    sys.stdout.write("{}: Testing creating a panel...\n".format(POST_PANEL))
    p = subprocess.Popen(["python",
                          os.path.join(path, POST_PANEL),
                          "--n",
                          "newpanel{}/{}".format(month, day),
                          "--d",
                          "newdescription",
                          "--m",
                          "methodology",
                          "--l",
                          "limitations",
                          "--f",
                          "fda_disclosure",
                          "--t",
                          "999",
                          "--g",
                          "BRCA1, BRCA2, APOE, AGRN, NOTFOUND"
                          ],
                         stdout=subprocess.PIPE)
    output, err = p.communicate()
    output_lines = output.split('\n')

    assert(re.match("Creating a new panel...", output_lines[0]))
    assert(re.match("\{.*\}", output_lines[2]))
    assert(re.match("Adding regions to panel...", output_lines[3]))
    assert(re.match("ambiguous : {}", output_lines[5]))
    assert(re.match("not_found : \[u'NOTFOUND'\]", output_lines[6]))
    assert(re.match("already_added : \[\]", output_lines[7]))
    assert(re.match("added : \[u'BRCA1', u'AGRN', u'BRCA2', u'APOE'\]", output_lines[8]))

    print_ok_output(output)


if __name__ == '__main__':
    month = datetime.datetime.today().month
    day = datetime.datetime.today().day

    parser = argparse.ArgumentParser(description='Supply arguments for API smoke test.')
    parser.add_argument('--project_id', metavar='project_id', type=int)
    parser.add_argument('example_scripts_repo', metavar='example_scripts_repo', type=str)
    parser.add_argument('family_folder', metavar='family_folder', type=str)
    parser.add_argument('genome_vcf', metavar='genome_vcf', type=str)
    parser.add_argument('filter_id', metavar='filter_id', type=int)
    parser.add_argument('panel_id', metavar='panel_id', type=int)
    parser.add_argument('genome_id', metavar='genome_id', type=int)
    args = parser.parse_args()

    path = args.example_scripts_repo
    family_folder = args.family_folder
    genome_vcf = args.genome_vcf
    project_id = args.project_id
    filter_id = args.filter_id
    panel_id = args.panel_id
    genome_id = args.genome_id

    if not project_id:
        #1.  Test project creation
        project_id = test_create_project(path, month, day)

    #2. Test upload one genome
    test_upload_genome(path, project_id, genome_vcf)

    #3. Test get genomes
    test_get_genomes(path, project_id)

    #4. Test upload folder of genomes
    test_upload_genomes_folder(path, project_id, family_folder)

    #5. Test upload of folder of genomes with manifest
    test_upload_genomes_folder_with_manifest(path, project_id, family_folder)

    #6. Test creation of a panel report with an existing genome
    test_launch_panel_report_existing_genome(path, filter_id, panel_id, genome_id)

    #7. Test creation of a panel report with a new genome
    test_launch_panel_report_new_genome(path, filter_id, panel_id, project_id, genome_vcf)

    #8. Test creation of panel report with no genome
    panel_report_id = test_launch_panel_report_no_genome(path, filter_id, panel_id)

    #9. Test getting a report's status
    test_get_report_status(path, panel_report_id, 'WAITING')

    #10. Test getting the custom patient info fields for a clinical report
    patient_info_fields = test_get_patient_info_fields(path, panel_report_id)

    #11. Test posting patient info to report
    test_post_patient_info_fields(path, panel_report_id)

    #12. Test adding a genome to a genomeless panel clinical report
    test_add_genome_to_cr(path, panel_report_id, genome_id)

    #13. Test creation of a family report
    test_launch_family_report_new_genomes(path, project_id, family_folder)


    #14. Test creation of a family report with no genomes
    test_launch_family_report_no_genomes(path, project_id, family_folder)


    #15. Test creation of a panel
    test_post_panel(path, month, day)
    

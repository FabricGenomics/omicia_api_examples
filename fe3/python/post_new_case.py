#!/usr/bin/env python

"""Create a new case_container and, optionally, upload genomes. 

Author: Fabric Genomics (2023)
Maintainer: support@fabricgenomics.com

Usage: post_new_case.py --analysis [ PANEL WGS MT_PANEL ] [ --test_id <test_id> ] [ --accession <identifier> ] [ --assembly b38 ] [ --genome <label> ] [ --vcf <file> ]

Create a case with the specified analysis types.
Panel cases:
If PANEL is specified no other analyses can be specified. The test ID --test_id is required. The members object for panel cases 
consists only of the proband (no family members). 

WGS cases:
The test ID --test_id is optional for WGS and MT_PANEL.
WGS and MT_PANEL may be specified together. One or two family members can be added

Optionally upload all vcfs for the case.

Optionally, include a file containing patient information to populate patient information fields.
This file should be a csv formatted. If custom fields are set up in the workspace the dictionary
phi_template needs to be updated with the appropriate key for each field and sections (patient, sample , order, report, family).

example for a trio:

key,value
accession,JD1
first_name,John
last_name,Doe
dob,2021-01-01
sex,MALE
ethnicity,Caucasian
indication,Disease
specimen_collected,2023-09-14
specimen_received,2023-09-16
specimen_type,Blood
ordering_physician,Dr. Med
f1_accession,mother
f1_affected,False
f1_dob,1965-11-30
f1_sex,FEMALE
f2_accession,father
f2_affected,False
f2_dob,1964-12-21
f2_sex,MALE

IF PHI for family members is included in the file make sure to use the matching f1 and f2 parameters for the command line options!
"""

## phi_template to map phi keys to phi sections
phi_sections = ["patient", "sample", "order", "report", "family"]
phi_template = {
"accession": "patient",
"first_name": "patient",
"last_name": "patient",
"sex": "patient",
"age": "patient",
"dob": "patient",
"ethnicity": "patient",
"indication": "patient",
"family_id": "patient",
"specimen_collected": "sample",
"specimen_received": "sample",
"specimen_type": "sample",
"ordering_physician": "order",
"f1_accession": "family",
"f1_affected": "family",
"f1_dob": "family",
"f1_sex": "family",
"f2_accession": "family",
"f2_affected": "family",
"f2_dob": "family",
"f2_sex": "family"
}

import argparse
import csv
import json
import os
import requests
from requests.auth import HTTPBasicAuth
import sys

#Load environment variables for request authentication parameters
if "FABRIC_API_PASSWORD" not in os.environ:
	sys.exit("FABRIC_API_PASSWORD environment variable missing\n")

if "FABRIC_API_LOGIN" not in os.environ:
	sys.exit("FABRIC_API_LOGIN environment variable missing\n")

FABRIC_API_LOGIN = os.environ['FABRIC_API_LOGIN']
FABRIC_API_PASSWORD = os.environ['FABRIC_API_PASSWORD']
FABRIC_API_URL = os.environ.get('FABRIC_API_URL', 'https://api.fabricgenomics.com')
auth = HTTPBasicAuth(FABRIC_API_LOGIN, FABRIC_API_PASSWORD)


def read_patient_info(patient_info_file):
	"""Read csv file containing the patient information,
	 return a dictionary representing its contents.
	"""
	patient_info = {}
	with open(patient_info_file, 'r') as f:
		reader = csv.reader(f)
		next(reader, None)  # Skip the header
		for i, row in enumerate(reader):
			if row[0] in phi_template:
				section = phi_template[row[0]]
				if section in ("patient", "sample", "order", "report"):
					if "proband" not in patient_info:
						patient_info["proband"] = {}
						for item in phi_sections:
							patient_info["proband"][item] = {}
					patient_info["proband"][section][row[0]] = row[1]
				elif section == "family":
					key = row[0].split("_")
					if key[0] not in patient_info:
						patient_info[key[0]] = {}
					if section not in patient_info[key[0]]:
						patient_info[key[0]][section] = {}
					patient_info[key[0]][section][key[1]] = row[1]
	#sys.stdout.write(f"patient_info: {patient_info}\n")
	return patient_info


def format_member_object(relationship, accession, sex, affected, phi=None):
	"""Create the member data object
	"""
	member = {"accession": accession,
			  "sex": sex,
			  "affected": affected,
			  "relationship": relationship
			  }
	if phi:
		member["phi"] = phi
	else:
		member["phi"] = {}
	return member


def create_case_container(analysis_types, test_id, members, hpo_ids, platform, assembly_version="b38"):
	"""Create a new case container
	"""
	# Construct url and request
	url = "{}/case_containers".format(FABRIC_API_URL)
	url_payload = {"analysis_types": analysis_types,
				   "assembly_version": assembly_version,
				   "members": members,
				   "hpo_terms": hpo_ids}
	if platform:
		url_payload["sequencing_platform"] = platform
	if test_id:
		url_payload["test_id"] = test_id

	sys.stdout.write("Creating case container ...\n")
	sys.stdout.flush()
	result = requests.post(url, auth=auth, data=json.dumps(url_payload))
	if result.status_code == 200:
		print(json.dumps(result.json(), indent=4))
		return result.json()
	else:
		sys.stderr.write("{}\n".format(result.text))
		return None


def upload_genome_to_url(url, genome_name, vcf_file, assembly_version="b38", platform=None, checksum=None):
	"""Upload a genome to a url with a specific case container and member id.
	"""
	# Construct request
	# example: 'url': 'https://api-test.omicia-remote.com/case_containers/460897/members/1855/genome'
	sys.stdout.write("Uploading {}  ...\n".format(url))
	payload = {"genome_name": genome_name,
			   "assembly_version": assembly_version}
	if checksum:
		payload["checksum"] = checksum
	if platform:
		payload["sequencing_platform"] = platform

	vcf = {"genome_file": open(vcf_file ,'rb')}

	result = requests.post(url, auth=auth, data=payload, files=vcf)

	if result.status_code == 201:
		return True
	else:
		sys.stderr.write("{}\n".format(result.text))
		return None


def main(argv):
	parser = argparse.ArgumentParser(description='Create a new case_container and upload all vcf files to the container. Optionally, include a file containing PHI.')
	parser.add_argument('--analysis', metavar='type', required=True, choices=["PANEL", "WGS", "MT_PANEL"], type=str, nargs='+', help='allowed values are PANEL, or WGS and/or MT_PANEL.')
	parser.add_argument('--test_id', metavar='id', type=int, help='unique numerical ID (int) for the test in Fabric, must be an existing test in the workspace.')
	parser.add_argument('--assembly', metavar='version', default="b38", choices=["b38"], type=str, help='only allowed value is b38. Defaults to b38.')
	parser.add_argument('--genome', metavar='name', help='label for the proband genome shown in projects.')
	parser.add_argument('--vcf', metavar='file.vcf.gz', type=str, help='vcf file for the proband, including path.')

	parser.add_argument('--patient_info_file', metavar='file.csv', type=str, help='csv file with patient information, entries must be comma separated key value pairs.')
	parser.add_argument('--accession', metavar='identifier', type=str, help='unique identifier for the proband sample, can also be provided through the patient_info_file.')
	parser.add_argument('--sex', metavar='[MALE,FEMALE,UNSPECIFIED]', choices=["MALE", "FEMALE", "UNSPECIFIED"], type=str, help='proband sex, allowed values are MALE, FEMALE or UNSPECIFIED, can also be provided through the patient_info_file.')
	parser.add_argument('--hpo_terms', metavar='term', type=str, nargs='+', help='one or multiple HPO term IDs, e.g. HP:0000018.')
	parser.add_argument('--checksum', metavar='checksum', help='optional checksum for the proband vcf file.')
	parser.add_argument('--platform', metavar='ONT', choices=["ONT"], type=str, help='optional sequencing platform. Allowed value is ONT. Defaults to Illumina.')

	parser.add_argument('--f1_accession', metavar='identifier', type=str, help='unique identifier for family member 1, can also be obtained from patient_info_file.')
	parser.add_argument('--f1_sex', metavar='[MALE,FEMALE,UNSPECIFIED]', choices=["MALE", "FEMALE", "UNSPECIFIED"], type=str, help='family member 1 sex, allowed values are MALE, FEMALE or UNSPECIFIED, can also be obtained from patient_info_file.')
	parser.add_argument('--f1_affected', metavar='True', type=bool, default=False, help='provide only if family member 1 is affected, can also be obtained from patient_info_file. Defaults to False.')
	parser.add_argument('--f1_relationship', metavar='[MOTHER,FATHER]', choices=["MOTHER", "FATHER"], type=str, help='family member 1 relationship to proband, allowed values are MOTHER and FATHER.')
	parser.add_argument('--f1_genome', metavar='label', type=str, help='label for the family member 1 genome shown in projects.')
	parser.add_argument('--f1_vcf', metavar='file.vcf.gz', type=str, help='vcf file for family member 1, including path.')
	parser.add_argument('--f1_checksum', metavar='checksum', help='optional checksum for the family member 1 vcf file.')

	parser.add_argument('--f2_accession', metavar='identifier', type=str, help='unique identifier for family member 2, can also be obtained from patient_info_file.')
	parser.add_argument('--f2_sex', metavar='[MALE,FEMALE,UNSPECIFIED]', choices=["MALE", "FEMALE", "UNSPECIFIED"], type=str, help='family member 2 sex, allowed values are MALE, FEMALE or UNSPECIFIED, can also be obtained from patient_info_file.')
	parser.add_argument('--f2_affected', metavar='True', type=bool, default=False, help='provide only if family member 2 is affected, can also be obtained from patient_info_file. Defaults to False.')
	parser.add_argument('--f2_relationship', metavar='[MOTHER,FATHER]', choices=["MOTHER", "FATHER"], type=str, help='family member 2 relationship to proband, allowed values are MOTHER and FATHER.')
	parser.add_argument('--f2_genome', metavar='label', type=str, help='label for the family member 2 genome shown in projects.')
	parser.add_argument('--f2_vcf', metavar='file.vcf.gz', type=str, help='vcf file for family member 1, including path.')
	parser.add_argument('--f2_checksum', metavar='checksum', help='optional checksum for the family member 2 vcf file.')


	args = parser.parse_args()

	analysis_types = args.analysis
	test_id = args.test_id
	assembly_version = args.assembly

	genome_name = args.genome
	vcf = args.vcf
	patient_info_file = args.patient_info_file
	hpo_terms = args.hpo_terms
	checksum = args.checksum
	platform = args.platform

	options = {}
	options["accession"] = args.accession
	options["sex"] = args.sex
	options["f1_accession"] = args.f1_accession
	options["f1_sex"] = args.f1_sex
	options["f1_affected"] = args.f1_affected
	f1_relationship = args.f1_relationship
	f1_genome_name = args.f1_genome
	f1_vcf = args.f1_vcf
	f1_checksum = args.f1_checksum

	options["f2_accession"] = args.f2_accession
	options["f2_sex"] = args.f2_sex
	options["f2_affected"] = args.f2_affected
	f2_relationship = args.f2_relationship
	f2_genome_name = args.f2_genome
	f2_vcf = args.f2_vcf
	f2_checksum = args.f2_checksum


	### Parse patient_info_file for PHI
	patient_info = {}
	if patient_info_file != None:
		patient_info = read_patient_info(patient_info_file)
		
		#get get required options from PHI if not provided in command line
		for item in ("accession", "sex"):
			if item in patient_info["proband"]["patient"]:
				if not options[item]:
					options[item] = patient_info["proband"]["patient"][item]
				del patient_info["proband"]["patient"][item]
		for item in ("f1_accession", "f1_sex", "f1_affected", "f2_accession", "f2_sex", "f2_affected"):
			new = item.split("_")
			if new[0] in patient_info:
				if new[1] in patient_info[new[0]]["family"]:
					if not options[item]:
						options[item] = patient_info[new[0]]["family"][new[1]]
					del patient_info[new[0]]["family"][new[1]]
	else:
		patient_info["proband"] = {}
		patient_info["f1"] = {}
		patient_info["f2"] = {}

	### Check all required entries 
	if not options["accession"]:
		sys.exit("missing --accession <identifier>, must be provided either in the PHI info file or as command line option\n")
	if not options["sex"]:
		sys.exit("The sex must be provided either in the PHI info file or as command line option\n")

	if 'PANEL' in analysis_types:
		if len(analysis_types)>1:
			parser.error("--analysis PANEL can not be specified with other analyses")
		if not test_id:
			parser.error("missing --test_id")

	if 'WGS' not in analysis_types:
		if hpo_terms:
			parser.error("Only WGS analysis type accepts HPO terms")
		if (f1_relationship or options["f1_sex"] or options["f1_accession"] or options["f1_affected"] or f1_genome_name or f1_vcf or f1_checksum or
		    f2_relationship or options["f2_sex"] or options["f2_accession"] or options["f2_affected"] or f2_genome_name or f2_vcf or f2_checksum):
			parser.error("Only WGS analysis type accepts family members. Check patient_info_file if provided.")

	if 'WGS' in analysis_types:
		if not hpo_terms:
			parser.error("Missing --hpo_terms required for WGS analysis")

		if f1_relationship or options["f1_sex"] or options["f1_accession"] or options["f1_affected"]:
			if not (f1_relationship and options["f1_sex"] and options["f1_accession"]): 
				parser.error("--f1_relationship, --f1_sex and --f1_accession need to be specified for family member f1")

		if f2_relationship or options["f2_sex"] or options["f2_accession"] or options["f2_affected"]:
			if not (f2_relationship and options["f2_sex"] and options["f2_accession"]): 
				parser.error("--f2_relationship, --f2_sex and --f2_accession need to be specified for family member f2")

		if f1_checksum or f1_genome_name or f1_vcf:
			if not (f1_genome_name and f1_vcf):
				parser.error("--f1_genome and --f1_vcf are required")

		if f2_checksum or f2_genome_name or f2_vcf:
			if not (f2_genome_name and f2_vcf):
				parser.error("--f2_genome and --f2_vcf are required")


	### Format members data object
	members = []
	proband = format_member_object("PROBAND",
								   options["accession"],
								   options["sex"], 
								   True, 
								   patient_info["proband"])
	members.append(proband)

	if f1_relationship:
		f1 = format_member_object(f1_relationship, 
								  options["f1_accession"],
								  options["f1_sex"], 
								  options["f1_affected"], 
								  patient_info["f1"])
		members.append(f1)

	if f2_relationship:
		f2 = format_member_object(f2_relationship, 
								  options["f2_accession"],
								  options["f2_sex"], 
								  options["f2_affected"], 
								  patient_info["f2"])
		members.append(f2)

	#sys.stdout.write(f"Members: {members}\n")
	
	
	### Create case_container
	json_response = create_case_container(analysis_types,
										  test_id,
										  members,
										  hpo_terms,
										  platform,
										  assembly_version=assembly_version)
	if not json_response:
		sys.exit("ERROR: Could not create case container\n")

	case_id = json_response.get("case_container_id")
	sys.stdout.write(f"\nSUCCESS: created case container {case_id}\n")


	### Upload any genomes
	success = True
	member_ids = []

	if vcf:
		proband_url = json_response.get('urls')[0].get('url')
		member_ids.append(json_response.get('urls')[0].get('member_id'))
		genome = upload_genome_to_url(proband_url,
									  genome_name,
									  vcf,
									  assembly_version=assembly_version,
									  platform=platform,
									  checksum=checksum)
		if not genome:
			sys.stderr.write("ERROR: Failed to upload PROBAND vcf to case container\n")
			success = False
		
	if f1_vcf:
		f1_url = json_response.get('urls')[1].get('url')
		member_ids.append(json_response.get('urls')[1].get('member_id'))
		genome = upload_genome_to_url(f1_url,
									  f1_genome_name,
									  f1_vcf,
									  assembly_version=assembly_version,
									  platform=platform,
									  checksum=checksum)
		if not genome:
			sys.stderr.write(f"ERROR: Failed to upload {f1_relationship} vcf to case container\n")
			success = False

	if f2_vcf:
		f2_url = json_response.get('urls')[2].get('url')
		member_ids.append(json_response.get('urls')[2].get('member_id'))
		genome = upload_genome_to_url(f2_url,
									  f2_genome_name,
									  f2_vcf,
									  assembly_version=assembly_version,
									  platform=platform,
									  checksum=checksum)
		if not genome:
			sys.stderr.write(f"ERROR: Failed to upload {f2_relationship} vcf to case container\n")
			success = False

	if member_ids:
		if success:
			sys.stdout.write(f"SUCCESS: uploaded vcf files to members {member_ids}\n")
		else:
			sys.exit(f"ERROR: Failed to upload all genomes to case container {case_id}\n")

if __name__ == "__main__":
	main(sys.argv[1:])

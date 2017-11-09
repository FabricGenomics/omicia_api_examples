Omicia API
==========

Introduction
------------

October 25th, 2015

Omicia provides an API based on the HTTPS protocol, using HTTP requests (GET,
POST, PUT and DELETE) to securely transmit variation
data, launch analyses and retrieve finished report data.

With the exception of the online documentation, every request must authenticate
against our database of API Keys, providing the login and password according
to the HTTP basic access authentication method (see `Wikipedia - basic access`_).
Please contact support_ to have them generate an API Key for your application.

An API Key is tied to a specific Opal user, referred to as
the API User hereon. Any email messages generated when using the Opal API are sent
to the API User.

Omicia stores passwords in a one-way encrypted hash according to industry
standard security procedures.  Passwords cannot be recovered,
but we can issue a new API key upon request.

The API uses SSL-encrypted HTTP for its protocol, via the normal port for
secure HTTP, 443. Attempts to query the server with non-encrypted HTTP
request on port 80 (ie. http://api.fabricgenomics.com instead of
https://api.fabricgenomics.com) will return a 404 error response.

Most invalid requests (e.g. for invalid parameter values) return an HTTP status of
400, 404 or 422; authentication errors return an HTTP status of 401 or 403.

All dates and times are returned in PST.

Jump to:
`Uploading Genomes`_,
`Launching Clinical Reports`_,
`Uploading Quality Control Data`_,
`Extracting Report Variants`_


.. _vcf_upload:

|

Uploading Genomes
-----------------
Once you obtain an API Key you can start uploading your samples to Opal for
annotation, analysis and clinical report generation.  API Keys are associated with a single
Workspace (a group of Projects and Users), and genomes must be uploaded to specific projects
within that Workspace. You may either use an existing project, or leverage the API to
create a new project for this purpose.

To create a Project use a POST request against the :ref:`create_project` endpoint.
You will need to specify a Project name and optionally a description and a parameter to
indicate how the project should be shared with existing and future members of your workspace.
Projects are identified by a numeric ID. This ID is necessary when uploading,
listing and otherwise accessing genomes and reports.

To upload a VCF file use the :ref:`upload` endpoint. For example, to upload a
VCF file to project 10, one would create a PUT request against

   https://api.fabricgenomics.com/projects/10/genomes

specifying an external ID, genome label, sex, assembly version and format as query parameters
(as opposed to form parameters), and including the entirety of the file as the
body of the request.  The assembly version must be hg19 (internally we handle
GRCh37 and hg19 interchangeably).

The Omicia Api accepts VCF 4.0+ (see http://samtools.github.io/hts-specs/VCFv4.2.pdf)
preferably containing a single sample column.  Multi-sample VCF's can be uploaded, however
the ID returned by the upload call cannot be used to launch reports. The Opal VCF parser accepts
quality and read depth data in a variety of formats. Please refer to the Opal user guide for more
information, or contact support_ for specific questions.

Upon successful parsing, the uploaded genome is queued for annotation by the
Omicia Pipeline.  Panel and exome VCF's usually annotate within minutes, while
full genomes can take longer.

If any genome fails to annotate, the system will send an email notification to
the API User as well as the Omicia Support Team.

Opal assigns a unique ID to all uploaded genomes. These IDs are used to
identify the genome within Opal. External IDs are an alternate method
to identify and find genomes within Opal. Opal does not enforce uniqueness of
the external ID.

:ref:`Relevant example Python scripts:`

- `Create a project <https://github.com/Omicia/omicia_api_examples/blob/master/python/create_project.py>`_

- `Upload a genome <https://github.com/Omicia/omicia_api_examples/blob/master/python/upload_genome.py>`_

- `Upload a folder of genomes <https://github.com/Omicia/omicia_api_examples/blob/master/python/upload_genomes_folder.py>`_

- `Upload a folder of genomes, using a manifest <https://github.com/Omicia/omicia_api_examples/blob/master/python/upload_genomes_folder_with_manifest.py>`_

.. _workflow_submission:

|

Launching Clinical Reports
--------------------------
A clinical report combines genome variant data with other information relevant
to the sample being tested, such as patient information and quality control data.

Once all genomes are successfully uploaded, the API can be used to submit them
for clinical reporting. However, it is possible to create a clinical report
that does not yet reference any genomes, and then attach the genomes at a later
point in time. Any of the report types elaborated below can be created with genomes, or --
by specifying "null" in the JSON payload's genome_id attributes -- without genomes. Then
the :ref:`add_genomes_to_report` endpoint can be used to later attach an uploaded genome or
completed vaast report.

- To launch an exome report you will need to specify a genome ID (or null), assay type, and a filter ID.
  Use the :ref:`create_report` endpoint to create a report in the queue. This action
  can be performed as soon as a successful genome upload is complete, and need not wait for
  annotation.  The new report is queued in a "Waiting" state, and the Opal application
  will submit the report for processing as soon as the annotation finishes. For exomes
  this step will take several minutes.

- To launch a family report you will need to specify a proband genome ID, assay type, a mother genome
  ID, and a father genome ID (or null values for all 3). You can then use the :ref:`create_report`
  endpoint to create a report in the queue. In this case the system will first annotate the three
  genomes, then run a VAAST analysis and finally queue the Clinical Report for processing.
  This will take several hours.

  If any of the genomes fail to annotate, or if there are issues with the VAAST run,
  the system will send an email notification to the API User as well as the Omicia
  Support Team.

- To submit a panel report you must specify a genome ID (or null), assay type, panel ID and optionally a filter ID. Use the :ref:`create_report` endpoint to create a report
  in the queue.  This action can be performed as soon as a successful upload is complete,
  and need not wait for annotation.  The new report is queued in Waiting state, and the
  Opal application will submit the report for processing as soon as the annotation finishes.

Once a clinical report has been created, the :ref:`post_patient_fields` endpoint can be used to upload
custom Patient information.


:ref:`Relevant example Python scripts:`

- `Launch a panel report with a new genome <https://github.com/Omicia/omicia_api_examples/blob/master/python/launch_panel_report_new_genome.py>`_

- `Launch a panel report with an existing genome <https://github.com/Omicia/omicia_api_examples/blob/master/python/launch_panel_report_existing_genome.py>`_

- `Launch a panel report with no genome attached <https://github.com/Omicia/omicia_api_examples/blob/master/python/launch_panel_report_no_genome.py>`_

- `Launch a family report <https://github.com/Omicia/omicia_api_examples/blob/master/python/launch_family_report.py>`_

- `Launch a family report with no genomes attached <https://github.com/Omicia/omicia_api_examples/blob/master/python/launch_family_report_no_genome.py>`_

- `Add genome(s) to a clinical report <https://github.com/Omicia/omicia_api_examples/blob/master/python/add_genome_to_cr.py>`_

- `Add patient information to a clinical report <https://github.com/Omicia/omicia_api_examples/blob/master/python/post_patient_fields.py>`_

|

Uploading Quality Control Data
------------------------------
Quality control data, such as sequencing or alignment metrics, can be added to a clinical report.
Using the :ref:`post_qc_data` with a JSON payload consisting of, for example:

    {"Cluster density": 6, "Cluster PF": "3"}

will generate a Quality Control data entry for the clinical report, assuming that the assay type
associated with the clinical report contains those predefined quality control fields.

To check which quality control entries are associated with a clincal report, the following endpoint can be used (:ref:`get_qc_data`):

    https://api.fabricgenomics.com/reports/203/qc_data

:ref:`Relevant example Python scripts:`

- `View the assay types in a workspace <https://github.com/Omicia/omicia_api_examples/blob/master/python/get_assay_types.py>`_

- `Add a quality control data entry to a clinical report <https://github.com/Omicia/omicia_api_examples/blob/master/python/post_qc_data.py>`_

|

Extracting Report Variants
--------------------------
Once a clinical report has been completed and is ready to review,
its variants can be interpreted using the Opal webapp, but can also be exported at any time using
the API.

To check that a clinical report's status is indeed "Ready to Review", use the :ref:`get_one_report`
and supply the ID of the report in question. Alternately, query all clinical reports by
report status to check whether the report is ready to review (:ref:`get_reports`). In addition,
reports can be found by accession, by external ID or genome ID, also using the above endpoint.

In the case that the user wishes to export all variants, for example to interpret them outside
of the Opal system, the following endpoint can be used:

   https://api.fabricgenomics.com/reports/203/variants

A second use case comes up once a report's variants have been interpreted and prioritized, when a technique such as Sanger
Sequencing might be employed in order to validate them. To export the variants with a given status,
for example the variants waiting in a "Pending" state, as VCF or JSON the :ref:`get_variants`
endpoint can be used. For example:

   https://api.fabricgenomics.com/reports/203/variants?status=REVIEWED&format=VCF

After external validation has been performed, the confirmed variants' validation status can be set at
the :ref:`set_variant_status` endpoint. This way, a webapp user
will see which variants have been confirmed when they review the clinical report.

:ref:`Relevant example Python scripts:`

- `Get a clinical report's status <https://github.com/Omicia/omicia_api_examples/blob/master/python/get_report_status.py>`_
- `Get a clinical report's variants <https://github.com/Omicia/omicia_api_examples/blob/master/python/get_report_variants.py>`_
- `Set a clinical report's variants' statuses <https://github.com/Omicia/omicia_api_examples/blob/master/python/set_report_variants.py>`_

|

API Reference and Examples
--------------------------
Please refer to the following sections for specifics on API endpoints and
some end-to-end examples:

- :doc:`reference`

- `Python Examples <https://github.com/FabricGenomics/omicia_api_examples/tree/master/python>`_

- `Bash Examples <https://github.com/FabricGenomics/omicia_api_examples/tree/master/shell>`_

## License

Copyright 2017 Fabric Genomics, Inc. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0.

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

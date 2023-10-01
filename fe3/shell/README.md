# Fabric API v3
## Sample Shell Scripts

- `create_case.sh case.json` - add a new case to a workspace
- `get_cases.sh` - retrieve all cases in workspace
- `upload_genome.sh container_id member_id genome.vcf` - upload VCF for a sample in a container

## Sample Data File

- `new_case.json` - a sample JSON passed to `create_case.sh` containing minimal data to create a case

## Data Model
A *case container* is simply a grouping of 1, 2 or 3 samples (SOLO, DUO or TRIO), called *members*.  The PHI data and variant data (VCF) are stored for each *member* in a *case container*.  The *case container* also holds information describing the type of analysis and phenotype information.  Each *case container* has a unique `case_container_id`, which is displayed in the UI as simply a case `ID`.

## Tutorial

The provided shell scripts describe a workflow in which:
- a new case is created, which returns identifiers for the case and members
- a query returns all cases, which can be filtered for a case of interest
- a VCF file is uploaded, which triggers an analysis
- a report is retrieved describing the variants

### Authentication
Authentication uses HTTP Basic Authentication. The Fabric Enterprise server only accepts requests over SSL.  A FE user may be associated with multiple workspaces.  Username and password are both opaque identifiers (e.g. `BKFRASYXEUPENE1YMRLX` and `BWCFX0SU9Y7ENKNMNRVT4AOARP3GTKZPL9ROGWZA`).  

A separate API username and password are generated for each workspace.  Thus, a username uniquely maps to a workspace, so the API does not explicitly reference workspaces, but implicitly associates an authenticated session with a workspace.  All authenticated users have visibility of all cases in a workspace.
In this tutorial sample code, the username, password and server are stored as environment variables.  For example:

```
export FABRIC_API_LOGIN=BKFRASYXEUPENE1YMRLX
export FABRIC_API_PASSWORD=BWCFX0SU9Y7ENKNMNRVT4AOARP3GTKZPL9ROGWZA
export FABRIC_API_URL=https://api-test.omicia-remote.com
```

### Example

#### Case Creation
A case is created using `POST` on the `/case_containers` endpoint.  The API returns a payload that reports the new `case_container_id` and the URL to `POST` the VCF file.

```
% ./create_case.sh sample_data/new_case.json  
POST https://api-test.omicia-remote.com/case_containers -d @sample_data/new_case.json
{"urls": [{"url": "https://api-test.omicia-remote.com/case_containers/74472/members/1279/genome", "member_id": 1279}], "case_container_id": 74472}
```

#### Case Query
It is common that the case is created by a different system than the one that will upload a VCF.  For example, a LIMS may create the case and a secondary analysis pipeline may upload the VCF.  Typically a LIMS and secondary pipeline will share a sample accession number.  Thus, it is helpful to query the system for a case with a matching accession.

In this example, the `new_case.json` contains an accession of `uniq_sample_123`.  (Note: Fabric Enterprise does not enforce uniqueness.  It is the responsibility of the client to handle situations with duplicate accessions.)

Cases are queried using `GET` on the `/case_containers` endpoint.  An `objects` array contains an object per `case_container`. And each *case_container* includes a *members* array of objects for each sample in the case.  In our example, there is one sample (member).  By filtering on the JSON output below it should be straightforward to derive the `case_container_id` (e.g. 74472) and the `id` of the member with the matching `accession` (e.g. 1279).

```
% ./get_cases.sh
GET https://api-test.omicia-remote.com/case_containers
{
    "objects": [
        {
            "due_date": "2023-09-26T14:35:41+00:00",
            "id": 74472,
            "created_audit": {
                "date": "2023-09-30T20:05:23+00:00",
                "user": {
                    "firstname": "John",
                    "id": 175,
                    "lastname": "Doe"
                }
            },
            "analysis_summary": null,
            "analyses": [
                {
                    "hpo_terms": [
                        "HP:0001903"
                    ],
                    "analysis_type": "WGS",
                    "id": 1117,
                    "test_id": null
                }
            ],
            "members": [
                {
                    "phi": null,
                    "relationship": "PROBAND",
                    "accession": "uniq_sample_123",
                    "id": 1279,
                    "affected": true,
                    "sex": "MALE",
                    "genome": null
                }
            ],
            "modified_audit": null,
            "reports": []
        },
        ...truncated...
```

#### Genome Data Upload
The `case_container_id` and `member_id` are combined to form the upload URL on the `/genome` endpoint of the form `/case_containers/{case_container_id}/members/{member_id}/genome`.

A VCF or gzip'd VCF is uploaded by calling the `/genome` endpoint with FORM fields containing the VCF, the name of the VCF and the human genome assembly name, as follows:

```
% ./upload_genome.sh 74472 1279 path/to/uniq_sample_123.vcf.gz
POST https://api-test.omicia-remote.com/case_containers/74472/members/1279/genome -F genome_file=@/path/to/uniq_sample_123.vcf.gz -F genome_name=uniq_sample_123.vcf.gz -F assembly_version=b38
```

#### Retrieve Clinical Report
The clinical results can be retrieved using the `/report` endpoint.  Only *Approved* reports are accessible.  The `/report` endpoint returns a JSON object with all of the information that is used to create a PDF report.  Only the most current approved version is returned.
Historic and current PDFs for all approved reports for a case are also available.  Report IDs can be gleaned from the `/case_containers` endpoint.  The `pdf` endpoint returns a secure URL with a 10-minute expiration to retrieve the finalized report.  For example:

```
% ./get_report.sh 461369
{
    "text_fields": [
        {
            "label": "Recommendations",
            "body": "Free text entered by clinician."
        },
        {
            "label": "Lab Contact",
...truncated...
% ./get_report.sh 461369 580
GET https://api-test.omicia-remote.com/case_containers/461369/report/pdf/580
{"download_url": "https://fabric-test-fe3-phi.s3.amazonaws.com/clinical_reports/case_461369_580_report.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIAT4ARRE2JNOR6HV5N%2F20231001%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20231001T031747Z&X-Amz-Expires=600&X-Amz-SignedHeaders=host&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEOv%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJHMEUCIGmGiKKJVfgv39sbRd2E%2F2xibjbd5CbNkw2bw9yRoGKSAiEArGFyc1xkHBXEL6M9tJPgnTR%2BG84MY%2BauVA40IliThvkquAUI5P%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAEGgwyNjYzMjQ3NDc5MjIiDJq0BQZXUVTHBnBfmiqMBTvtkdvpVE78ro1%2B36wBM%2FQtnTsA7yDGC3dOK1sfHY124cOab6WhlurktVxq3ebYzISUFgpBmHDAp0S3Vxv%2BzBXLxEaKSCw8gRXricVw9bD0gRXSfhorVuBRRQCJD%2FNEvklpDFTWt9DrEI8HYLODZVvsw43CZp50tpvL2MIlc2C1wELAdmhYDjvPOWUMALgxUlIBayGjh8ZDaITxebEr7HrvkgCK0yDKLJwjIzwHsroBYcevZYyGbrqpy6sdtnQRyl1KBN9Xo6ewaKdGYaVBPHC5lKYqD%2BAq6vw%2FhgnHofG%2B9%2Bbld%2FSOGl866%2BPfg3FgUzeeD46%2FFglHnNYozvVMCr8bBOOpnmrvIK9k8kMpHvLu30A67leJKCW8B6plGmJYqZMt9dHpZD6mC%2BnSNl36320mqiRJWOn0jN%2FK0E2P2s8E7mJlmTub9iDBjcq%2BRzLP%2B9zX8Ch93EGQP3VSig8W8aMfM9hPf%2B5V3ypgNadd%2FATlXSDF6afNtmu%2Bkc%2BJkbbrxxGqDo6IeZ%2FpdTQztdglCtnS3ApnOMMG4IbA3tjdTD%2BsrTvDuk%2FfiSnYqb3CnpvfUZCEXti1UizRfFi75fAaJ8ksnNMqdQlqdOdhgsvcxal3irxBndK%2BAizw%2BspukSBgmvY3mhyVNieAwtjpWSziCUAbXp4tFMzzDrOnjAp2E7Wmw6lURG8BrkuX6KQ4%2BY0y9ahgHKXh3ziJrejUE95YbWifPJOWqJ8sqlv0gh2QvM82MMXtDgWJJj1kwEWVOVUmAQd6DsYHda%2FX2XEOt0GgeKBsC4%2FvAVWIEW5Pe%2FpIXiYwRJhVJKbfFgKAbP923iQeSpg2W4c02rCjP1898YAYaeQ%2BNZuSH2JkQ2yEGSMwy7TjqAY6sQFLSU5evgyhHFm6JCz3i%2BHQ7ilsQfe%2FAkPwluAfvKFE7SwtBCBT9ZvLG9NQ8W3Ek4ehPPGlKglpmF6Sew7r8VXMST9rvdNcxti2M4VPD%2FsyphCQHqdII8P7wO36MkY%2Bn1J0BVEfzC%2Fyr8L7Jl513ylIStrGzIudkAd6Q0B5Py11Gyz5ui%2B2re889wUejRyG0HcNe3eVsQC77aEHX6PNQWyKKKR7lhNjP4TbukyfckjlBbY%3D&X-Amz-Signature=c3934edd15305a621a49f13b3243bc6db9cd455805c899f6a217de4d9dbe8a18"}
```

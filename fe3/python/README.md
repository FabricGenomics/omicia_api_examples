# Fabric API v3
## Sample Python Script

`post_new_case.py` provides a script for creating URLs according to the v3 REST API to:

- create a case, specifying members, sex, relationships, affectedness and other workspace-specific metadata
- optionally upload VCFs

Patient information can be provided either on the command line or from a CSV file.

Set API key user and password in environment variables `FABRIC_API_LOGIN` and `FABRIC_API_PASSWORD`.

For command line usage data, run with `--help`.


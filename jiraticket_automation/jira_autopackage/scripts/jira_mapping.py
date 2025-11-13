# scripts/fetch_jira_mapping.py

from jira_autopackage.scripts.jira_fields import fetch_request_type_fields, parse_jira_fields, build_field_mapping, save_field_mapping_to_file
from jira_autopackage.utils import config
import os

# --- Load credentials from environment variables via config ---
JIRA_SERVICE_DESK_ID = os.getenv("JIRA_SERVICE_DESK_ID", config.JIRA_SERVICE_DESK_ID)
JIRA_REQUEST_TYPE_ID = os.getenv("JIRA_REQUEST_TYPE_ID", config.JIRA_REQUEST_TYPE_ID)

# Step 1 — Fetch raw fields from Jira
raw_fields = fetch_request_type_fields(JIRA_SERVICE_DESK_ID, JIRA_REQUEST_TYPE_ID)

# Step 2 — Parse into {name: fieldId}
jira_fields = parse_jira_fields(raw_fields)

# Step 3 — Map your DB columns
db_columns = [
    "newusername", "samplename", "phonenumber", "departmentname", 
    "job", "emailaddress", "costcenter", "telephonelinesandinstallations", 
    "handsetsandheadsets", "timeframe", "dateneededby", "approximateendingdate", 
    "Comments", "createdat"
]

field_mapping = build_field_mapping(db_columns, jira_fields)

# Step 4 — Save mapping for Module 4
save_field_mapping_to_file(field_mapping)


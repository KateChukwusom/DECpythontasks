import json
from jira_autopackage.utils import config
from jira_autopackage.scripts.jira_fields import (
    fetch_request_type_fields,
    parse_jira_fields,
    build_field_mapping,
    save_field_mapping_to_file
)

def main():
    print("Fetching Jira fields...")
    raw_fields = fetch_request_type_fields(config.JIRA_SERVICE_DESK_ID, config.JIRA_REQUEST_TYPE_ID)

    if not raw_fields:
        print("❌ Failed to fetch Jira fields. Check your Service Desk ID, Request Type ID, or API token.")
        return

    jira_fields = parse_jira_fields(raw_fields)
    print(f"✅ Retrieved {len(jira_fields)} Jira fields.")
    print(json.dumps(jira_fields, indent=2))  # optional: see what Jira returned

    db_columns = [
        "newusername", "samplename", "phonenumber", "departmentname",
        "job", "emailaddress", "costcenter", "telephonelinesandinstallations",
        "handsetsandheadsets", "timeframe", "dateneededby", "approximateendingdate",
        "Comments", "createdat"
    ]

    field_mapping = build_field_mapping(db_columns, jira_fields)
    save_field_mapping_to_file(field_mapping)

    print(f"\n✅ Mapping saved to field_mapping.json — contains {len(field_mapping)} fields.")
    print(json.dumps(field_mapping, indent=2))

if __name__ == "__main__":
    main()



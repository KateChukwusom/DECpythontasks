# test_create_two_tickets.py

from create_jira_tickets import map_submission_to_request_fields, create_request_on_jira
import json

# --- Example: Two test submissions from your DB ---
test_submissions = [
    {
        "newusername": "Alice Johnson",
        "phonenumber": "+1-555-111-2222",
        "departmentname": "IT",
        "job": "Network Engineer",
        "Comments": "Needs VPN access",
        "createdat": "2025-11-12",
        "emailaddress": "alice@example.com"
    },
    {
        "newusername": "Bob Smith",
        "phonenumber": "+1-555-333-4444",
        "departmentname": "Finance",
        "job": "Accountant",
        "Comments": "Requesting new phone",
        "createdat": "2025-11-13",
        "emailaddress": "bob@example.com"
    }
]

# --- Load your FIELD_MAPPING from create_jira_tickets.py or a JSON file ---
from create_jira_tickets import FIELD_MAPPING

# Loop through each test submission
for submission in test_submissions:
    request_fields = map_submission_to_request_fields(submission)
    
    print("Payload for Jira:")
    print(json.dumps(request_fields, indent=2))
    
    # Optionally create ticket in Jira
    create_ticket = input("Create ticket in Jira? (y/n): ").strip().lower()
    if create_ticket == "y":
        issue_key = create_request_on_jira(request_fields, raise_on_behalf_of=submission.get("emailaddress"))
        if issue_key:
            print(f"✅ Created ticket: {issue_key}")
        else:
            print(f"❌ Failed to create ticket for {submission.get('newusername')}")
    else:
        print("Skipped ticket creation.\n")


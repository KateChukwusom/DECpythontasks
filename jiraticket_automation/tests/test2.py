# test_module2.py

from jira_autopackage.scripts.fetch_records import fetch_records
from jira_autopackage.scripts.key_generator import generate_unique_key
from jira_autopackage.scripts.checktracker import unique_key_exists
from jira_autopackage.scripts.save_to_tracker import save_processed_record

# Step 1 — Fetch submissions
submissions = fetch_records()

if not submissions:
    print("No submissions found in database.")
else:
    print(f"Fetched {len(submissions)} submissions.")

# Step 2 — Test Module 2 on first 2 submissions
for submission in submissions[:2]:
    unique_key = generate_unique_key(submission)
    print("Generated unique key:", unique_key)

    exists_before = unique_key_exists(unique_key)
    print("Already in tracker?", exists_before)

    if not exists_before:
        save_processed_record(unique_key, submission.get("createdat"))
        print("Inserted into tracker.")
    else:
        print("Skipped, already processed.")


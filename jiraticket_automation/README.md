## Jira Ticket Automation Pipeline 

# Project Overview
This project automates the process of converting webform submissions into Jira Service Management tickets. It ensures:

Incremental processing: Only new submissions are handled.

Idempotency: No submission is processed twice.

Modularity: Each module handles a single responsibility.

Logging: All steps are logged for audit and debugging.

The pipeline fetches data from a webform database, generates unique keys, checks which submissions are already processed using a tracker database, maps fields to Jira ticket fields, creates Jira tickets, attaches submission data, and marks them as processed.

## Project Structure

jiraticket_automation/
├── jira_autopackage/
│   ├── __init__.py
│   ├── scripts/
│   │   ├── __init__.py
│   │   ├── fetch_submissions.py       # Module 1: Fetch submissions from DB
│   │   ├── generate_unique_key.py     # Module 2a: Generate unique keys
│   │   ├── check_tracker.py           # Module 2b: Check tracker for duplicates
│   │   ├── save_to_tracker.py         # Module 2c: Save processed submissions
│   │   ├── process_batch.py           # Module 3: Filter new submissions, batch processing
│   │   ├── jira_fields.py             # Module 4a: Fetch and map Jira fields
│   │   ├── create_jira_tickets.py    # Module 4b: Create tickets and attach forms
│   │   └── fetch_jira_mapping.py     # Helper: Initial Jira field mapping
├── setup/
│   ├── __init__.py
│   └── tracker_db.py                  # Tracker DB initialization
├── tracker/
│   └── tracker.db                     # SQLite tracker database
├── logs/                              # Module-specific log files
├── tests/                             # Optional test scripts
├── venv/
├── config.py                          # Reads .env for DB & Jira credentials
├── .env                               # Stores secrets
└── main.py                            # Orchestrator: runs full pipeline

##  Pipeline Modules - Conceptual Flow

# Module 1 – Fetch Submissions

- Check if webform Postgres database exists
-  Check if the table contains any data
- Batch processes 30 rows per run
- Continue batch processing after first run
- This uses the tracker’s last_processed_date:
- If last_processed_date exists, fetch only rows where submitted_date > last_processed_date
- If not, it's first run -- fetch first 30 rows
- Why batch size 30?- (Minimizes API load, Provides headroom for burst traffic, Performs incremental  updates efficiently, Prevents choking Jira API, Allows room for future growth)
- Tracker will update as we process each submission
- Next run, module fetches the next 30 rows
- This ensures incremental batch progression.

# Important Note

Creating a unique key: To ensure Idempotency. How do we ensure idempotency?
Idempotency here means that the automation script can run multiple times without creating the same jira ticket for the SAME submission, A unique key is created, a unique key is a string generated from fields that uniquely identify a submission, vecause idempotency says “ do not process the same unique key twice”.

-- Mechanism: 

Before processing a submission, check if the unique key exists in the tracker(sqlite database file)
If it exists, skip
If it does not exist, process the submission and insert in tracker when done. 

-- Goal: Already processed submission will not trigger duplicate jira    tickets when the script is run many times.

-- How do we ensure Incremental uniqueness(Loading)?

What does incremental means, - it means instead of processing all data in the database all at once everytime, process only the new submissions that haven’t been handled.

Using unique key, before  a submission is processed the scheduler checks if the unique key already exists in the database,
If yes, it is an old record – skip
If new, it is a new record- process and insert in the tracker.
So the automation incrementally processes new records and skips the previously processed records.


# Module Two - Unique Key Generation and Tracker
- Generates unique keys per submission (using fields + timestamp/hash).
- Checks the tracker DB for duplicates (idempotency).
- Inserts new unique keys into the tracker (incremental uniqueness).

# Module Three - Batch Processing
- Uses Module 2 to filter unprocessed submissions.
- Prepares a batch (configurable size, e.g., 30) for Jira ticket creation.
- Sorts submissions by creation date (oldest first).

# Module 4 – Jira Integration
- Field Mapping
- Fetches Jira request type fields via Jira API.
- Builds a mapping from DB columns → Jira fields.
- Saves mapping to field_mapping.json for repeated use.
- Ticket Creation
- Posts submissions to Jira using mapped fields.
- Attaches submissions as JSON or CSV files.
- Updates the tracker after successful ticket creation.

# Orchestrator – main.py
- Responsibilities:
- Loads field mapping or fetches it from Jira.
- Retrieves a batch of new submissions.
- Creates Jira tickets and attaches the submission data.
- Marks submissions as processed in the tracker.
- Logs all steps and warnings/errors.

# Logging
- Each module writes logs to logs/ folder.
- Examples: fetch_submissions.log, process_batch.log, create_jira_tickets.log.
- Logs include info, warnings, and errors for easy debugging.

# Best Practices Followed
- Modularity: Each module does one job.
- Idempotency: Tracker DB prevents duplicates.
- Incremental processing: Only new submissions processed.
- Error handling: Each module logs failures, skips problematic records.
- Config-driven: .env keeps credentials outside code.
- Batch processing: Prevents API rate limits.
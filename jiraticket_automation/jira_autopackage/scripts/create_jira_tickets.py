# scripts/create_jira_tickets.py

import requests
import json
from requests.auth import HTTPBasicAuth
from jira_autopackage.utils.log_setup import get_logger
from jira_autopackage.scripts.process_batch import get_new_batch, mark_batch_processed
from jira_autopackage.scripts.jira_fields import load_field_mapping_from_file
from jira_autopackage.utils import config
import os

logger = get_logger("create_jira_tickets")

# --- Load credentials from environment variables via config ---
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL", config.JIRA_BASE_URL)
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN", config.JIRA_API_TOKEN)
JIRA_USER_EMAIL = os.getenv("JIRA_USER_EMAIL", config.JIRA_USER_EMAIL)
JIRA_SERVICE_DESK_ID = os.getenv("JIRA_SERVICE_DESK_ID", config.JIRA_SERVICE_DESK_ID)
JIRA_REQUEST_TYPE_ID = os.getenv("JIRA_REQUEST_TYPE_ID", config.JIRA_REQUEST_TYPE_ID)


def create_ticket(submission, field_mapping):
    """Create a Jira ticket for one submission."""
    url = f"{JIRA_BASE_URL}/rest/servicedeskapi/request"
    headers = {"Content-Type": "application/json"}
    auth = HTTPBasicAuth(JIRA_USER_EMAIL, JIRA_API_TOKEN)

    # Build requestFieldValues dynamically
    request_fields = {}
    for db_col, jira_field in field_mapping.items():
        value = submission.get(db_col)
        if value:
            request_fields[jira_field] = value

    payload = {
        "serviceDeskId": JIRA_SERVICE_DESK_ID,
        "requestTypeId": JIRA_REQUEST_TYPE_ID,
        "requestFieldValues": request_fields
    }

    try:
        resp = requests.post(url, headers=headers, auth=auth, json=payload, timeout=30)
        if resp.status_code in [200, 201]:
            ticket = resp.json()
            logger.info(f"Ticket created for {submission.get('newusername')} → {ticket.get('issueKey')}")
            return ticket
        else:
            logger.error(f"Failed to create ticket for {submission.get('newusername')}: {resp.status_code} {resp.text}")
            return None
    except requests.RequestException as e:
        logger.error(f"HTTP error creating ticket for {submission.get('newusername')}: {e}")
        return None


def attach_submission(ticket_id, submission):
    """Attach submission JSON to Jira ticket."""
    url = f"{JIRA_BASE_URL}/rest/servicedeskapi/request/{ticket_id}/attachment"
    headers = {"X-Atlassian-Token": "no-check"}
    auth = HTTPBasicAuth(JIRA_USER_EMAIL, JIRA_API_TOKEN)

    # Convert submission dict to JSON bytes
    submission_json = json.dumps(submission, indent=2).encode("utf-8")
    files = {"file": ("submission.json", submission_json, "application/json")}

    try:
        resp = requests.post(url, headers=headers, auth=auth, files=files, timeout=30)
        if resp.status_code in [200, 201]:
            logger.info(f"Attached submission to ticket {ticket_id}")
            return True
        else:
            logger.error(f"Failed to attach submission: {resp.status_code} {resp.text}")
            return False
    except requests.RequestException as e:
        logger.error(f"HTTP error attaching submission to ticket {ticket_id}: {e}")
        return False


def process_batch_to_jira():
    """Main function: get batch, create tickets, attach forms, mark processed."""
    batch = get_new_batch()
    if not batch:
        logger.info("No new submissions to process.")
        return

    field_mapping = load_field_mapping_from_file()
    if not field_mapping:
        logger.error("No field mapping found. Aborting batch.")
        return

    successful_submissions = []

    for submission, unique_key in batch:
        ticket = create_ticket(submission, field_mapping)
        if ticket:
            ticket_id = ticket.get("issueKey")
            attached = attach_submission(ticket_id, submission)
            if attached:
                successful_submissions.append((submission, unique_key))

    # Mark only successfully processed submissions in tracker
    mark_batch_processed(successful_submissions)
    logger.info("Batch marked as processed in tracker.")

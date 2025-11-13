# tests/test_jira_integration.py

from jira_autopackage.scripts.process_batch import get_new_batch
from jira_autopackage.scripts.create_jira_tickets import create_ticket, attach_submission
from jira_autopackage.scripts.jira_fields import load_field_mapping_from_file
from jira_autopackage.utils.log_setup import get_logger

logger = get_logger("test_jira_integration")

# Load field mapping
field_mapping = load_field_mapping_from_file()
if not field_mapping:
    logger.error("No field mapping found. Fetch Jira fields first.")
    exit()

# Fetch batch (small batch for testing)
batch = get_new_batch()
if not batch:
    logger.info("No new submissions to process.")
    exit()

# Take first 2 submissions for safe testing
test_batch = batch[:2]

for submission, unique_key in test_batch:
    logger.info(f"Testing ticket creation for: {submission.get('newusername')} ({unique_key})")
    ticket = create_ticket(submission, field_mapping)
    if ticket:
        ticket_id = ticket.get("issueKey")
        logger.info(f"Ticket created: {ticket_id}")

        attached = attach_submission(ticket_id, submission)
        if attached:
            logger.info(f"Attachment successful for ticket {ticket_id}")
        else:
            logger.warning(f"Attachment failed for ticket {ticket_id}")
    else:
        logger.warning(f"Ticket creation failed for {submission.get('newusername')}")


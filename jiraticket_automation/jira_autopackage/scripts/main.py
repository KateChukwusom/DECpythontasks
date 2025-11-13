from jira_autopackage.scripts.process_batch import get_new_batch, mark_batch_processed
from jira_autopackage.scripts.create_jira_tickets import create_ticket, attach_submission
from jira_autopackage.scripts.jira_fields import load_field_mapping_from_file, fetch_request_type_fields, parse_jira_fields, build_field_mapping, save_field_mapping_to_file
from jira_autopackage.utils import config
from jira_autopackage.utils.log_setup import get_logger
import os

logger = get_logger("main_pipeline")

# --- Load Jira credentials from environment variables via config ---
JIRA_SERVICE_DESK_ID = os.getenv("JIRA_SERVICE_DESK_ID", config.JIRA_SERVICE_DESK_ID)
JIRA_REQUEST_TYPE_ID = os.getenv("JIRA_REQUEST_TYPE_ID", config.JIRA_REQUEST_TYPE_ID)

def main():
    try:
        # Step 1 — Ensure field mapping exists
        field_mapping = load_field_mapping_from_file()
        if not field_mapping:
            logger.info("Field mapping not found. Fetching Jira fields...")
            raw_fields = fetch_request_type_fields(JIRA_SERVICE_DESK_ID, JIRA_REQUEST_TYPE_ID)
            jira_fields = parse_jira_fields(raw_fields)
            db_columns = [
                "newusername", "samplename", "phonenumber", "departmentname",
                "job", "emailaddress", "costcenter", "telephonelinesandinstallations",
                "handsetsandheadsets", "timeframe", "dateneededby", "approximateendingdate",
                "Comments", "createdat"
            ]
            field_mapping = build_field_mapping(db_columns, jira_fields)
            save_field_mapping_to_file(field_mapping)

        # Step 2 — Get new batch
        logger.info("Fetching new submissions batch...")
        batch = get_new_batch()
        if not batch:
            logger.info("No new submissions to process. Exiting.")
            return

        # Step 3 — Create Jira tickets and attach submissions
        for submission, unique_key in batch:
            logger.info(f"Creating ticket for: {submission.get('newusername')} ({unique_key})")
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

        # Step 4 — Mark batch as processed
        mark_batch_processed(batch)
        logger.info("Batch marked as processed in tracker.")

    except Exception as e:
        logger.error(f"Pipeline failed: {e}")


if __name__ == "__main__":
    main()


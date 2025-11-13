# scripts/process_batch.py

from jira_autopackage.scripts.fetch_records import fetch_records
from jira_autopackage.scripts.key_generator import generate_unique_key
from jira_autopackage.scripts.checktracker import unique_key_exists
from jira_autopackage.scripts.save_to_tracker import save_processed_record
from jira_autopackage.utils.log_setup import get_logger

logger = get_logger("process_batch")

# Configurable batch size
BATCH_SIZE = 30


def get_new_batch():
    """
    Fetch submissions, generate unique keys, and return a batch of new submissions.
    Returns:

    """

    #Fetch all submissions
    submissions = fetch_records()
    if not submissions:
        logger.info("No submissions fetched from database.")
        return []

    #Sort submissions by createdat(date column) ascending (oldest first)
    submissions.sort(key=lambda x: x.get("createdat"))

    new_batch = []

    #Loop through submissions and select unprocessed ones
    for submission in submissions:
        unique_key = generate_unique_key(submission)

        if not unique_key:
            logger.warning("Skipping submission due to key generation failure.")
            continue

        if unique_key_exists(unique_key):
            logger.debug(f"Skipping already processed submission: {unique_key}")
            continue

        # Add to batch
        new_batch.append((submission, unique_key))

        # Stop once batch size is reached
        if len(new_batch) >= BATCH_SIZE:
            break

    logger.info(f"Prepared batch of {len(new_batch)} new submissions.")
    return new_batch


def mark_batch_processed(batch):
    """
    After Jira ticket creation, mark all submissions in batch as processed.
    """
    for submission, unique_key in batch:
        save_processed_record(unique_key, submission.get("createdat"))
        logger.debug(f"Marked submission {unique_key} as processed.")


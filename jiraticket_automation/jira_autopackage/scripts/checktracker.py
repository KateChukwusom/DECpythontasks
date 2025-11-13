"""This script checks if the unique key already exists in SQLite, so we do not return duplicates(idempotency detection"""

import sqlite3
from jira_autopackage.utils.log_setup import get_logger

logger = get_logger("check_tracker")


def unique_key_exists(unique_key):

    """If unqiue key exists, return True. If not, False"""

    try:
        conn = sqlite3.connect("tracker/tracker.db")
        cursor = conn.cursor()

        cursor.execute(
		"SELECT 1 FROM processed_records WHERE unique_key = ? LIMIT 1;",
		(unique_key,)
		)



        result = cursor.fetchone()
        conn.close()

        return result is not None

    except Exception as e:
        logger.error(f"Error checking unique key in tracker:{e}")
        return True 

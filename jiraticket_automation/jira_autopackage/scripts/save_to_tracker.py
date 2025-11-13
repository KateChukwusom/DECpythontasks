"""This module inserts the processed unique key into the tracker"""

import sqlite3
from jira_autopackage.utils.log_setup import get_logger

logger = get_logger("save_to_tracker")


def save_processed_record(unique_key, createdat):
    """save every processed unique key into the tracker db"""

    try:
        conn = sqlite3.connect("tracker/tracker.db")
        cursor = conn.cursor() 

        cursor.execute("""
		INSERT INTO processed_records(unique_key, createdat)
		VALUES(?,?);
		""", (unique_key, createdat))

        conn.commit()
        conn.close()

        logger.info(f"saved to tracker: {unique_key}")

    except Exception as e:
        logger.error(f"Error saving processed key:{e}")


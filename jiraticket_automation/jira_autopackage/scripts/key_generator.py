"""We import python built in cryptography hashing library to generate a 256-bit hash which is a combination
   of fields, hashing gives predictable fixed length keys"""

import hashlib
from jira_autopackage.utils.log_setup import get_logger
import sqlite3


logger = get_logger("key_generator")

def generate_unique_key(records):
    """We create this unique key so that two identical submissions never collide and to check if a given 
    unique key already exists in the SQLite tracker to avoid duplicates"""

    try:
        #Extract the fields, ensure value is a string, remove whitespace and normalize

        newusername = str(records.get("newusername", "")).strip()
        samplename = str(records.get("samplename", "")).strip().lower()
        emailaddress = str(records.get("emailaddress", "")).strip().lower()
        createdat = str(records.get("createdat", "")).strip()

        #We combine the fields and concatenate with a delimiter to prevent ambiguity
        combined = f"{newusername}|{samplename}|{emailaddress}|{createdat}"

        #Generate the hash
        unique_key = hashlib.sha256(combined.encode("utf-8")).hexdigest()

        logger.debug(f"Generated unique key for {emailaddress}:{unique_key}")

        return unique_key
    except Exception as e:
        logger.error(f"Error generating unique key: {e}")
        return None

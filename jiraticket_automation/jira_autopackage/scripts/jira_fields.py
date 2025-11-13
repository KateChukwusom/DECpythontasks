# scripts/jira_fields.py

import requests
import json
import time
from requests.auth import HTTPBasicAuth
from jira_autopackage.utils.log_setup import get_logger
from jira_autopackage.utils import config
import os

logger = get_logger("jira_fields")

# --- Load credentials from environment variables via config ---
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL", config.JIRA_BASE_URL)
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN", config.JIRA_API_TOKEN)
JIRA_USER_EMAIL = os.getenv("JIRA_USER_EMAIL", config.JIRA_USER_EMAIL)


def fetch_request_type_fields(service_desk_id, request_type_id, retries=3):
    """Fetch Jira fields for the given request type."""
    url = f"{JIRA_BASE_URL}/rest/servicedeskapi/requesttype/{request_type_id}/field"
    headers = {"Accept": "application/json"}
    auth = HTTPBasicAuth(JIRA_USER_EMAIL, JIRA_API_TOKEN)

    for attempt in range(1, retries + 1):
        try:
            resp = requests.get(url, headers=headers, auth=auth, timeout=30)
            if resp.status_code == 200:
                return resp.json()
            logger.warning(f"Attempt {attempt}: Got {resp.status_code} {resp.text}")
        except requests.RequestException as e:
            logger.error(f"HTTP error on attempt {attempt}: {e}")
        time.sleep(2 * attempt)

    logger.error("Failed to fetch Jira fields after retries.")
    return None


def parse_jira_fields(raw_fields):
    """Simplify Jira field JSON → dict of {name: id}."""
    if not raw_fields:
        return {}
    parsed = {f["name"]: f["fieldId"] for f in raw_fields if "name" in f and "fieldId" in f}
    logger.info(f"Parsed {len(parsed)} Jira fields.")
    return parsed


def build_field_mapping(db_columns, jira_fields):
    """Match DB columns to Jira field IDs or names."""
    mapping = {}
    for col in db_columns:
        # Try to match by clean name
        name_guess = col.replace("_", " ").title()
        jira_match = jira_fields.get(name_guess)
        if jira_match:
            mapping[col] = jira_match
        else:
            logger.warning(f"No match found for DB column '{col}'")
    return mapping


def save_field_mapping_to_file(mapping, filename="field_mapping.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(mapping, f, indent=2)
    logger.info(f"Mapping saved to {filename}")


def load_field_mapping_from_file(filename="field_mapping.json"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning("Mapping file not found, please fetch first.")
        return {}

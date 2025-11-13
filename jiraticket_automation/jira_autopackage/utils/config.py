import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", 6543))
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_USER_EMAIL= os.getenv("JIRA_USER_EMAIL")
JIRA_SERVICE_DESK_ID = os.getenv("JIRA_SERVICE_DESK_ID")
JIRA_REQUEST_TYPE_ID = os.getenv("JIRA_REQUEST_TYPE_ID")

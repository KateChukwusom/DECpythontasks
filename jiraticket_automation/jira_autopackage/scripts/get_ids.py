import requests
from requests.auth import HTTPBasicAuth
import os

url = f"{os.getenv('JIRA_BASE_URL')}/rest/servicedeskapi/servicedesk"
resp = requests.get(
    url,
    auth=HTTPBasicAuth(os.getenv("JIRA_USER_EMAIL"), os.getenv("JIRA_API_TOKEN")),
    headers={"Accept": "application/json"}
)
print(resp.status_code, resp.text)

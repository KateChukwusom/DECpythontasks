from jira_autopackage.scripts.fetch_records import fetch_records

records = fetch_records()

print ("Number of records fetched:", len(records))
print ("First submissions:", records[0] if records else "no records")

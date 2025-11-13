# tests/test_module3_refactored.py

from jira_autopackage.scripts.process_batch import get_new_batch, mark_batch_processed

def main():
    # Step 1 — Fetch a batch of unprocessed submissions
    batch = get_new_batch()

    if not batch:
        print("No new submissions to process.")
        return

    print(f"Batch size: {len(batch)}\nSubmissions in this batch:")

    # Step 2 — Display submission names and unique keys
    for submission, unique_key in batch:
        print(f"- {submission.get('samplename')} | {unique_key}")

    # Step 3 — Simulate Jira ticket creation
    print("\nSimulating Jira ticket creation...")
    for submission, unique_key in batch:
        # Mock success
        print(f"Ticket created for {submission.get('samplename')}")

    # Step 4 — Mark batch as processed in tracker
    mark_batch_processed(batch)
    print("\nBatch marked as processed in tracker.")

if __name__ == "__main__":
    main()


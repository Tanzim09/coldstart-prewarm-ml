import boto3
import json

# Set up CloudWatch Logs client
client = boto3.client('logs')

# Your Lambda log group
log_group = "/aws/lambda/lambda_cold_ai"

# Get log events (paginated)
paginator = client.get_paginator('filter_log_events')
pages = paginator.paginate(logGroupName=log_group)

all_events = []

for page in pages:
    events = page.get('events', [])
    all_events.extend(events)

# Save as clean JSON list
with open("lambda_logs.json", "w", encoding="utf-8") as f:
    json.dump(all_events, f, indent=2)

print(f" Downloaded {len(all_events)} log events to lambda_logs.json")

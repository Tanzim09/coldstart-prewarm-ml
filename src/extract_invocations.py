import json
import csv
from datetime import datetime

# Load logs
with open("lambda_logs.json", "r") as f:
    logs = json.load(f)

invocation_times = []

for log in logs:
    message = log["message"]
    timestamp = log["timestamp"]
    
    if "START RequestId" in message:
        # Convert timestamp to readable format
        readable_time = datetime.utcfromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
        invocation_times.append(readable_time)

# Sort timestamps
invocation_times.sort()

# Calculate delay between invocations
rows = []
previous_time = None

for ts in invocation_times:
    current_time = datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')
    if previous_time:
        delay = (current_time - previous_time).total_seconds()
    else:
        delay = 0
    rows.append([ts, int(delay)])
    previous_time = current_time

# Save to CSV
with open("invocation_log.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Timestamp (UTC)", "Delay (s)"])
    writer.writerows(rows)

print(f"✅ Extracted {len(rows)} total invocations to invocation_log.csv")

import json
import csv
from datetime import datetime
import re

# Load logs
with open("lambda_logs.json", "r") as file:
    logs = json.load(file)

cold_start_data = []

# Loop through logs to find INIT_START and matching REPORT
for i in range(len(logs)):
    log = logs[i]
    message = log["message"]

    if "INIT_START" in message:
        timestamp = log["timestamp"]
        readable_time = datetime.utcfromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')

        # Look ahead for the REPORT log
        for j in range(i, min(i + 10, len(logs))):
            report = logs[j]["message"]
            if "REPORT" in report and "Init Duration" in report:
                match = re.search(r"Init Duration: ([\d.]+) ms", report)
                if match:
                    duration = float(match.group(1))
                    cold_start_data.append([readable_time, duration])
                break

# Save to CSV
with open("cold_start_data.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp (UTC)", "Cold Start Duration (ms)"])
    writer.writerows(cold_start_data)

print(f"✅ Cold start data saved to cold_start_data.csv | Total rows: {len(cold_start_data)}")

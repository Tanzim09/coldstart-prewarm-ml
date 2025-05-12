import boto3
import time
import random
import csv
from datetime import datetime

# Lambda function name
FUNCTION_NAME = "lambda_cold_ai"


NUM_INVOCATIONS = 2000  


lambda_client = boto3.client("lambda")


with open("invocation_log.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Invocation #", "Timestamp (UTC)", "Delay (sec)", "Hour (UTC)"])

    def get_delay_based_on_time():
        
        current_hour = datetime.utcnow().hour

        # Peak traffic hours (9 AM to 6 PM UTC)
        if 9 <= current_hour < 18:
            return random.choice([1, 2, 3, 5, 10, 15, 20])
        # Off-peak hours (6 PM to 9 AM UTC
        else:
            return random.choice([30, 60, 120, 300, 420, 600, 900]) 

    def invoke_lambda():
        """Invoke the Lambda function once."""
        response = lambda_client.invoke(
            FunctionName=FUNCTION_NAME,
            InvocationType="RequestResponse"
        )
        status_code = response["ResponseMetadata"]["HTTPStatusCode"]
        return status_code

    for i in range(NUM_INVOCATIONS):
        timestamp = datetime.utcnow()
        hour = timestamp.hour
        readable_time = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        delay = get_delay_based_on_time()

        print(f" Invocation {i+1}/{NUM_INVOCATIONS}")
        print(f" {readable_time} UTC | Hour: {hour} | Next Delay: {delay} seconds")

        # Invoke the Lambda
        status = invoke_lambda()
        print(f" Lambda Invoked — Status Code: {status}\n")

        # Log the details to CSV
        writer.writerow([i+1, readable_time, delay, hour])

        # Wait for the next invocation
        time.sleep(delay)



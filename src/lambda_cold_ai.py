import time
from datetime import datetime

def lambda_handler(event, context):
    start_time = time.time()

    return {
        'statusCode': 200,
        'body': {
            'message': 'Hello from lambda_cold_ai!',
            'timestamp': str(datetime.utcnow()),
            'execution_time_ms': round((time.time() - start_time) * 1000, 3)
        }
    }

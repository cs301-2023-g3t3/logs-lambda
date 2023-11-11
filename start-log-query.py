import json
import boto3
from botocore.exceptions import NoCredentialsError
from datetime import datetime, timedelta

services = [
    "/aws/lambda/points-ledger-api",
    "/aws/lambda/makerchecker-api",
    "/aws/lambda/user-storage-api"
]

def lambda_handler(event, context):
    try:
        query_params = event.get('queryStringParameters', None)

        start = int(query_params.get('start', None))
        end = int(query_params.get('end', None))
        query = query_params.get('query', "")
        
        # Initialize the CloudWatch Logs client
        client = boto3.client('logs', region_name='ap-southeast-1')  # Change the region as needed

        query_string = f'fields @timestamp, @message | filter level = "info" | filter ACTION like /{query}/ or MESSAGE like /query/ | sort @timestamp desc | limit 100'
        response = client.start_query(
            logGroupNames=services,
            startTime=start,
            endTime=end,
            queryString=query_string
        )
        
        query_id = response['queryId']
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'queryId': query_id
            }),
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e)),
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
        }
import json
import boto3
from botocore.exceptions import NoCredentialsError
from datetime import datetime, timedelta

def lambda_handler(event, context):
    try:
        query_params = event.get('queryStringParameters', None)

        query_id = query_params.get('queryId', None)

        if not query_id:
            return {
                'statusCode': 400,
            }
        
        # Initialize the CloudWatch Logs client
        client = boto3.client('logs', region_name='ap-southeast-1')  # Change the region as needed

        response = client.get_query_results(queryId=query_id)
        
        return {
            'statusCode': 200,
            'body': json.dumps(response),
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
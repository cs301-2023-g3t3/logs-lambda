import json
import boto3

services = [
    "/aws/lambda/points-ledger-api",
    "/aws/lambda/makerchecker-api",
    "/aws/lambda/user-storage-api"
]

def lambda_handler(event, context):
    try:
        query_params = event.get('queryStringParameters', None)
        days = int(query_params.get('days', None))
        
        if (not days):
            return {
                statusCode: 400
            }
        
        client = boto3.client('logs')
        
        for service in services:
            client.put_retention_policy(
                logGroupName=service,
                retentionInDays=days
            )
        
        return {
            'statusCode': 200,
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
import json
import boto3

services = [
    "/aws/lambda/points-ledger-api",
    "/aws/lambda/makerchecker-api",
    "/aws/lambda/user-storage-api"
]

def lambda_handler(event, context):
    client = boto3.client('logs')
    
    # Get information about the log groups
    response = client.describe_log_groups(
        logGroupNamePrefix=services[0]
    )
    
    retention_days = response['logGroups'][0].get('retentionInDays', 'Not Set')

    return {
        'statusCode': 200,
        'body': json.dumps({
            'retentionInDays': retention_days
        }),
        'headers': {
            'Access-Control-Allow-Origin': '*',
        },
    }

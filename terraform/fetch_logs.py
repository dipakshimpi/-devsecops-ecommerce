import os
import boto3
import json

def lambda_handler(event, context):
    cw = boto3.client('logs')
    log_group = os.getenv('LOG_GROUP', '/aws/eks/ecommerce-cloud/logs')
    
    # Search for "ERROR" in the last 15 minutes
    try:
        response = cw.filter_log_events(
            logGroupName=log_group,
            filterPattern='ERROR',
            limit=10
        )
        
        messages = [event['message'] for event in response.get('events', [])]
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'error_logs': messages,
                'count': len(messages)
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

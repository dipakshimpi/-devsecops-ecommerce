import os
import json
import urllib.request

def lambda_handler(event, context):
    prom_url = os.getenv('PROM_URL')
    if not prom_url:
        return {'statusCode': 500, 'body': 'PROM_URL not set'}
        
    query = event.get('query', 'up')
    full_url = f"{prom_url}/api/v1/query?query={query}"
    
    try:
        with urllib.request.urlopen(full_url) as response:
            data = json.loads(response.read().decode())
            return {
                'statusCode': 200,
                'body': json.dumps(data)
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

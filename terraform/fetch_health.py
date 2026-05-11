import os
import boto3
import json

def lambda_handler(event, context):
    eks = boto3.client('eks')
    cluster_name = os.getenv('CLUSTER_NAME', 'ecommerce-cloud')
    
    try:
        # Get nodegroups
        nodegroups = eks.list_nodegroups(clusterName=cluster_name)['nodegroups']
        
        health_data = []
        for ng in nodegroups:
            details = eks.describe_nodegroup(clusterName=cluster_name, nodegroupName=ng)
            health_data.append({
                'nodegroup': ng,
                'status': details['nodegroup']['status'],
                'health': details['nodegroup'].get('health', 'Healthy')
            })
            
        return {
            'statusCode': 200,
            'body': json.dumps(health_data)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

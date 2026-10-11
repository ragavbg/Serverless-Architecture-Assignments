import boto3
from datetime import datetime

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    
    # Get the instance ID from the CloudWatch trigger event
    detail = event.get('detail', {})
    instance_id = detail.get('instance-id')
    
    if instance_id:
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        # Add tags to the newly launched instance
        ec2.create_tags(
            Resources=[instance_id],
            Tags=[
                {'Key': 'LaunchDate', 'Value': current_date},
                {'Key': 'Status', 'Value': 'AutoTagged'}
            ]
        )
        print(f"Successfully tagged Instance {instance_id} with date {current_date}")
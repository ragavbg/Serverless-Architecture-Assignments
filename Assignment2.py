import boto3
from datetime import datetime, timezone, timedelta

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket_name = 'YOUR_BUCKET_NAME_HERE' # <-- CHANGE THIS to your exact bucket name
    
    # Calculate the date 30 days ago
    thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
    
    # List all files in the bucket
    response = s3.list_objects_v2(Bucket=bucket_name)
    
    if 'Contents' in response:
        for obj in response['Contents']:
            last_modified = obj['LastModified']
            
            # If the file is older than 30 days, delete it
            if last_modified < thirty_days_ago:
                s3.delete_object(Bucket=bucket_name, Key=obj['Key'])
                print(f"Deleted old file: {obj['Key']}")
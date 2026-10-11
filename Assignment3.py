import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    response = s3.list_buckets()
    
    for bucket in response['Buckets']:
        bucket_name = bucket['Name']
        try:
            # Try to get encryption status
            s3.get_bucket_encryption(Bucket=bucket_name)
        except ClientError as e:
            # If it throws a "ConfigurationNotFound" error, it is unencrypted
            if e.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError':
                print(f"ALERT: Unencrypted bucket found -> {bucket_name}")
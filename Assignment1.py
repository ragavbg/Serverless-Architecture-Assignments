import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    
    # 1. Stop instances with tag 'Auto-Stop'
    stop_response = ec2.describe_instances(Filters=[{'Name': 'tag:Action', 'Values': ['Auto-Stop']}])
    stop_ids = [inst['InstanceId'] for res in stop_response['Reservations'] for inst in res['Instances'] if inst['State']['Name'] != 'stopped']
    
    if stop_ids:
        ec2.stop_instances(InstanceIds=stop_ids)
        print(f"Successfully stopped instances: {stop_ids}")
        
    # 2. Start instances with tag 'Auto-Start'
    start_response = ec2.describe_instances(Filters=[{'Name': 'tag:Action', 'Values': ['Auto-Start']}])
    start_ids = [inst['InstanceId'] for res in start_response['Reservations'] for inst in res['Instances'] if inst['State']['Name'] != 'running']
    
    if start_ids:
        ec2.start_instances(InstanceIds=start_ids)
        print(f"Successfully started instances: {start_ids}")
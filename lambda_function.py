import boto3
import datetime
import pytz
import os

def lambda_handler(event, context):
    timezone = 'America/New_York'
    
    ec2 = boto3.client('ec2')
    
    filters = [
        {'Name': 'tag:Schedule', 'Values': ['*']}
    ]
    
    instances = ec2.describe_instances(Filters=filters)
    
    tz = pytz.timezone(timezone)
    current_day = datetime.datetime.now(tz).strftime('%A').lower()
    current_time = datetime.datetime.now(tz).strftime('%H:%M')
    
    print(f"Current day: {current_day}, Current time: {current_time}")

    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            instance_state = instance['State']['Name']
            
            print(f"Processing instance: {instance_id}")
            print(f"Instance state: {instance_state}")

            schedule_tag = [tag['Value'] for tag in instance['Tags'] if tag['Key'] == 'Schedule'][0]
            print(f"Checking schedule for instance {instance_id}: {schedule_tag}")

            days, time_info = schedule_tag.split(' ')
            days = days.lower().split(',')

            if '-' in time_info:
                start_time, end_time = time_info.split('-')
            else:
                start_time = None
                end_time = time_info

            if current_day in days:
                if start_time and start_time <= current_time <= end_time:
                    if instance_state in ['stopped', 'stopping']:
                        print(f"Starting instance {instance_id}")
                        ec2.start_instances(InstanceIds=[instance_id])
                    else:
                        print(f"Instance {instance_id} is already running or starting. Skipping...")
                elif current_time >= end_time:
                    if instance_state in ['running', 'pending']:
                        print(f"Stopping instance {instance_id}")
                        ec2.stop_instances(InstanceIds=[instance_id])
                    else:
                        print(f"Instance {instance_id} is already stopped or stopping. Skipping...")
                else:
                    print(f"Instance {instance_id} is not scheduled for action. Skipping...")
            else:
                print(f"Instance {instance_id} is not scheduled for action today. Skipping...")

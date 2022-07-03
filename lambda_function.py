import os
import json
import boto3
import requests


def post_slack_h(data):
    post_url = os.environ.get("SLACK_WEBHOOK_URL")
    requests.post(post_url, data=json.dumps(data))


def lambda_handler(event, context):
    instance_id = event['detail']['instance-id']
    client = boto3.client('ec2')
    response = client.describe_instances(
        InstanceIds=[
            instance_id,
        ],
    )
    instance = response['Reservations'][0]['Instances'][0]
    fields = []

    try:
        for tag in instance['Tags']:
            if tag['Key'] != 'Name':
                continue
            instance_name = tag['Value']
            fields.append({
                'title': 'Name',
                'value': instance_name,
                'short': True,
            })
            break
    except:
        print('Tag does not exist.')

    fields.append({
        'title': 'Instance ID',
        'value': instance_id,
        'short': True,
    })
    fields.append({
        'title': 'Instance Type',
        'value': instance['InstanceType'],
        'short': True,
    })
    fields.append({
        'title': 'Availability Zone',
        'value': instance['Placement']['AvailabilityZone'],
        'short': True,
    })

    try:
        for interfaces in instance['NetworkInterfaces']:
            idx = interfaces['Attachment']['DeviceIndex']
            for ip_addresses in interfaces['PrivateIpAddresses']:
                fields.append({
                    'title': 'Private Ip Address (eth{})'.format(idx),
                    'value': ip_addresses.get('PrivateIpAddress'),
                    'short': True,
                })
                fields.append({
                    'title': 'Public Ip Address (eth{})'.format(idx),
                    'value': ip_addresses.get('Association', {}).get('PublicIp'),
                    'short': True,
                })
    except:
        print('NetworkInterfaces does not exist.')

    color = 'warning'
    if event['detail']['state'] == 'running':
        color = 'good'
    elif event['detail']['state'] == 'stopped':
        color = 'danger'

    instance_state = event['detail']['state']
    data = {
        'attachments': [{
            'pretext': 'Instance state is  *' + instance_state + '*.',
            'color': color,
            'fields': fields,
        }]
    }
    post_slack_h(data)

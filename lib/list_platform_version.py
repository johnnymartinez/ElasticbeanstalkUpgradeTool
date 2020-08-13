import boto3
import json


def list_platform_version():
    client = boto3.client('elasticbeanstalk')
    response = client.list_platform_versions()

    node_list = []

    pfl = response['PlatformSummaryList']
    for item in pfl:
        arn = item['PlatformArn']
        if 'Node.js' in arn:
            node_list.append(arn)

    node_list.sort()

    platform = ''.join(node_list[-1])

    latest_platform = platform.split('/')[2]
#     logging.INFO(latest_platform)
    print('\n\nThe latest node.js platform version is: ' + latest_platform)

    return latest_platform

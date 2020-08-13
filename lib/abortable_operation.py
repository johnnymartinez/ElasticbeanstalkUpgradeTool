import boto3
import time
import json


def abortable_operation_upgrade(envName):

    client = boto3.client('elasticbeanstalk')
    print('\n\nConnecting')

    print('\n\nChecking for ready status on environment -', envName)

    while True:

        abortable_response = client.describe_environments(
            EnvironmentNames=[envName],
            IncludeDeleted=False
        )

        status = abortable_response['Environments'][0]['Status']

        if status == 'Ready':
            print(envName, 'is now ready!')
            break
        else:
            print('''
            -----------------------------------------------------------------------------------------
                Sleeping for four minutes... waiting for immutable upgrade to finish.
            -----------------------------------------------------------------------------------------''')
            time.sleep(240)

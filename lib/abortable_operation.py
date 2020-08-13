import boto3
import time
import json


def abortable_operation(envName):

    client = boto3.client('elasticbeanstalk')
    print('\n\nConnecting')

    print('\n\nChecking to see if ', envName,
          ' is in a ready state.')

    while True:

        abortable_response = client.describe_environments(
            EnvironmentNames=[envName],
            IncludeDeleted=False
        )

        status = abortable_response['Environments'][0]['Status']

        if status == 'Ready':
            print("\n\n" + envName + ' is now ready!')
            break
        else:
            time.sleep(10)
            # print('''
            # -----------------------------------------------------------------------------------------
            #     Sleeping for another 10 seconds... waiting for configuration changes to finish up.
            # -----------------------------------------------------------------------------------------''')

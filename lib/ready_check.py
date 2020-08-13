import boto3

def ready_check(envName):

    try:
        client = boto3.client('elasticbeanstalk')
        response = client.describe_environments(EnvironmentNames=[envName],IncludeDeleted=False)

        status = response['Environments'][0]['Status']

        if status == 'Ready':
            print(f"{envName} ready")
            return False
        else:
            return True

    except Exception as e:
        print(e)

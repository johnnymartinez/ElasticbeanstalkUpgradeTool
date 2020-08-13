import boto3
from lib.list_platform_version import list_platform_version


def get_node_environments(list_platform_version):

    client = boto3.client('elasticbeanstalk')

    response_describe = client.describe_environments(IncludeDeleted=False)

    environment_names = []

    environments = response_describe['Environments']

    for env in environments:
        #print('\n\nChecking beanstalk instances for node platforms.')

        if 'Node.js' in env['SolutionStackName']:
            if list_platform_version not in env['PlatformArn']:
                environment_names.append(
                    (env['EnvironmentName'], env['ApplicationName']))


    return environment_names
 

import boto3
from commands.upgrade_environment import upgrade_environment


def get_node_env_var(env_list):

    client = boto3.client('elasticbeanstalk')

    prod_envs = []

    stage_envs = []

    for env, app in env_list:
        response = client.describe_configuration_settings(
            ApplicationName=app, EnvironmentName=env)
        print(
            f'\n\nRunning healthcheck on {env} and verifying environment variables to identify the lane for {env}.')

        option_settings = response['ConfigurationSettings'][0]['OptionSettings']

        for opts in option_settings:
            if opts['OptionName'] == 'HealthCheckSuccessThreshold':
                if opts['Value'] == 'Ok':
                    print('done with healthcheck')
            if opts['OptionName'] == 'NODE_ENV':
                if opts['Value'] == 'production':
                    prod_envs.append(env)
                    print(
                        f'\n\nHealth for {env} is "Ok", and NODE_ENV is set to production. {env} is ready for upgrade')
                else:
                    stage_envs.append(env)
                    print(
                        f'\n\nHealth for {env} is "Ok", and NODE_ENV is set to staging. {env} is ready for upgrade')

    return prod_envs, stage_envs

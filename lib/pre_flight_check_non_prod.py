import boto3
import time
from commands.set_deployment_immutable import set_deployment_immutable
from commands.set_update_type_immutable import set_update_type_immutable
from lib.abortable_operation import abortable_operation

global stage_environments


def pre_flight_check_non_prod(env_list):

    client = boto3.client('elasticbeanstalk')

    stage_envs = []

    for env, app in env_list:
        response = client.describe_configuration_settings(
            ApplicationName=app, EnvironmentName=env)
        print(
            f'\n\nRunning healthcheck, and checking environment variables to identify the lane for environment: {env}.')

        option_settings = response['ConfigurationSettings'][0]['OptionSettings']

        is_non_prod = True
        healthcheck_ok = False
        immutable = True
        rolling = False

        for opts in option_settings:
            if opts['OptionName'] == 'HealthCheckSuccessThreshold':
                if opts['Value'] == 'Ok':
                    healthcheck_ok = True

            if opts['OptionName'] == 'NODE_ENV':
                if opts['Value'] == 'production':
                    is_non_prod = False

            if opts['OptionName'] == 'DeploymentPolicy':
                if opts['Value'] != 'Immutable':
                    immutable = False

            if opts['OptionName'] == 'RollingUpdateType':
                if opts['Value'] != 'Immutable':
                    rolling = False

        if healthcheck_ok == True:
            print(
                f'\n\nHealth for {env} is "Ok", - {env} is ready for platform upgrade.')
            if is_non_prod == True:
                stage_envs.append(env)
                if immutable == False:
                    print(f'''\n\n
                    -----------------------------------------------------------------------------------------
                    {env} ''' + ''' is a non-prod environment and doesn't have its deployment 
                    policy set to immutable. Please wait while the deployment policy to be updated. Sleeping
                    in 10 second increments until instance is in a ready state.
                    -----------------------------------------------------------------------------------------''')
                    set_deployment_immutable(env)
                    abortable_operation(env)
                if rolling == False:
                    print(f'''\n\n
                    -----------------------------------------------------------------------------------------
                    {env} ''' + ''' is a non-prod environment and doesn't have its update type set 
                    to immutable. Please wait while the update type is set to immutable. Sleeping
                    in 10 second increments until instance is in a ready state.
                    -----------------------------------------------------------------------------------------''')
                    set_update_type_immutable(env)
                    abortable_operation(env)
        else:
            pass
    return stage_envs

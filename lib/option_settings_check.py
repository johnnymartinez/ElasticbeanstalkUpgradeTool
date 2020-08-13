import boto3
import time
from commands.set_deployment_immutable import set_deployment_immutable
from commands.set_update_type_immutable import set_update_type_immutable
from lib.abortable_operation import abortable_operation


def option_settings_check(env, app):

    client = boto3.client('elasticbeanstalk')

    response = client.describe_configuration_settings(
        ApplicationName=app,
        EnvironmentName=env,
    )

    option_settings = response['ConfigurationSettings'][0]['OptionSettings']

    is_prod = False
    healthcheck_ok = False
    immutable = True
    rolling = False

    for opts in option_settings:
        if opts['OptionName'] == 'HealthCheckSuccessThreshold':
            if opts['Value'] == 'Ok':
                healthcheck_ok = True

        if opts['OptionName'] == 'NODE_ENV':
            if opts['Value'] == 'production':
                is_prod = True

        if opts['OptionName'] == 'DeploymentPolicy':
            if opts['Value'] == 'Immutable':
                immutable = True

        if opts['OptionName'] == 'RollingUpdateType':
            if opts['Value'] == 'Immutable':
                rolling = True

    #settings:
    settings_info = {
        'is_prod'                           : is_prod,
        'is_healthy'                        : healthcheck_ok,
        'deployment_policy_immutable'       : immutable,
        'roling_update_type_immutable'      : rolling,
    }

    return settings_info


if __name__ == '__main__':
    option_settings_check()

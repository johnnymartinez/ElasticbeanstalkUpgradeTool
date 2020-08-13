'''Moved healthcheck to get_node_environments.py'''


# import boto3


# def health_check(env_list):

#     client = boto3.client('elasticbeanstalk')

#     result_list = []

#     for env, app in env_list:
#         response = client.describe_configuration_settings(
#             ApplicationName=app, EnvironmentName=env)
#         print(f"Checking health status for {env} | {app}")
#         option_settings = response['ConfigurationSettings'][0]['OptionSettings']
#         for opts in option_settings:
#             if opts['OptionName'] == 'HealthCheckSuccessThreshold':
#                 if opts['Value'] == 'Ok':
#                     result_list.append(env)

#     return result_list

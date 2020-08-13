import boto3
from subprocess import Popen, PIPE


def set_update_type_rolling(envName):
    print('\n\nChanging environment update type back to rolling.')

    command = ['aws', 'elasticbeanstalk', 'update-environment', '--environment-name', envName,
               '--option-settings', 'Namespace=aws:autoscaling:updatepolicy:rollingupdate,OptionName=RollingUpdateType,Value=Health']

    process = Popen(command, stdout=PIPE, stderr=PIPE)

    stdout, stderr = process.communicate()

    ls_list = stdout.decode('utf-8')

    print(f'''\n\n
            -----------------------------------------------------------------------------------------
                Upgrade is complete for ''' + envName + '''... Moving to next instance.
            -----------------------------------------------------------------------------------------''')

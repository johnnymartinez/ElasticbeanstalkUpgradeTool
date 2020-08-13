from subprocess import Popen, PIPE


def set_deployment_immutable(envName):

    print(
        f'\n\nChanging {envName} environments deployment policy to immutable.')

    command = ['aws', 'elasticbeanstalk', 'update-environment', '--environment-name', envName,
               '--option-settings', 'Namespace=aws:elasticbeanstalk:command,OptionName=DeploymentPolicy,Value=Immutable']

    process = Popen(command, stdout=PIPE, stderr=PIPE)

    stdout, stderr = process.communicate()

    ls_list = stdout.decode('utf-8')

    print('\n\nConfiguration for ' + envName +
          ' is being set to immutable deployment... Please wait.')

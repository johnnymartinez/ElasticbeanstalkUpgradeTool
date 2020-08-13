from subprocess import Popen, PIPE


def set_deployment_rolling(envName):

    print('\n\nChanging {envName} deployment policy to rolling.')

    command = ['aws', 'elasticbeanstalk', 'update-environment', '--environment-name', envName,
               '--option-settings', 'Namespace=aws:elasticbeanstalk:command,OptionName=DeploymentPolicy,Value=Rolling']

    process = Popen(command, stdout=PIPE, stderr=PIPE)

    stdout, stderr = process.communicate()

    ls_list = stdout.decode('utf-8')

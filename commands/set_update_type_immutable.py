from subprocess import Popen, PIPE


def set_update_type_immutable(envName):

    print('''\n\n
    -----------------------------------------------------------------------------------------
      Changing update type for ''' + envName + ''' to immutable deployment... Please wait.
    -----------------------------------------------------------------------------------------
        ''')

    command = ['aws', 'elasticbeanstalk', 'update-environment', '--environment-name', envName,
               '--option-settings', 'Namespace=aws:autoscaling:updatepolicy:rollingupdate,OptionName=RollingUpdateType,Value=Immutable']

    process = Popen(command, stdout=PIPE, stderr=PIPE)

    stdout, stderr = process.communicate()

    ls_list = stdout.decode('utf-8')

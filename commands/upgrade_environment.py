from subprocess import Popen, PIPE


def upgrade_environment(envName):
    print(f'''
            -----------------------------------------------------------------------------------------
                                Upgrading {envName}, please standby.
            -----------------------------------------------------------------------------------------''')

    command = ['beanstalk', 'upgrade', envName]

    process = Popen(command, stdout=PIPE, stderr=PIPE)

    stdout, stderr = process.communicate()

    ls_list = stdout.decode('utf-8')

    print(ls_list)

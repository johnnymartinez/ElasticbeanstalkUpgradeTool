from lib.abortable_operation import abortable_operation

from commands.upgrade_environment import upgrade_environment
from commands.set_deployment_immutable import set_deployment_immutable
from commands.set_deployment_rolling import set_deployment_rolling
from commands.set_update_type_immutable import set_update_type_immutable
from commands.set_update_type_rolling import set_update_type_rolling

from lib.ready_check import ready_check
from lib.option_settings_check import option_settings_check

import time
import json


def debug(message):
    if __name__ == "__main__":
        print(message)
    else:
        pass


def status_update(message, q):
    q.put(message)


# Get all from queue as a list
def queue_get_all(q):

    stuff = []

    while q.empty() == False:
        stuff.append(q.get())

    return stuff


# stage worker ListToProcess=my_list, s_timeout=600, m_processes=5
# def worker_process(beanstalk_env, shared_results, s_timeout=600, bool_prod=False):

def worker_process(q, beanstalk_env, shared_results, s_timeout, bool_prod):

    envName, appName = beanstalk_env

    print("envName: ", end='')
    print(envName)

    stage_bool = False

    status_update("getting option settings", q)
    options = option_settings_check(envName, appName)

    #print(json.dumps(options, indent=4, default=str))

    time.sleep(5)  # simulator
    while ready_check(envName):
        time.sleep(5)

    status_update("upgrading environment", q)
    # upgrade_environment(envName) # upgrade it

    time.sleep(5)  # simulator
    while ready_check(envName):
        status_update("waiting for ready environment", q)
        time.sleep(5)
        #status = waiting

    status_update("setting deployment rolling", q)
    # set_deployment_rolling(envName) # STAGE

    time.sleep(5)  # simulator
    while ready_check(envName):
        status_update("waiting for ready environment", q)
        time.sleep(5)
        #status = waiting

    status_update("set update type rolling", q)
    # set_update_type_rolling(envName) # STAGE

    time.sleep(5)  # simulator
    while ready_check(envName):
        status_update("waiting for ready environment", q)
        time.sleep(5)
        #status = waiting

    status_update("finished", q)


if __name__ == '__main__':
    worker_process()

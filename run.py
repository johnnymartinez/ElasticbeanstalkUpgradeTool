from lib.get_node_environments import get_node_environments
from lib.get_node_environments import get_node_environments
from lib.abortable_operation import abortable_operation
from lib.abortable_operation_upgrade import abortable_operation_upgrade
from lib.pre_flight_check_non_prod import pre_flight_check_non_prod

from lib.list_platform_version import list_platform_version
from commands.upgrade_environment import upgrade_environment
from commands.set_deployment_immutable import set_deployment_immutable
from commands.set_deployment_rolling import set_deployment_rolling
from commands.set_update_type_immutable import set_update_type_immutable
from commands.set_update_type_rolling import set_update_type_rolling

import time
import os
import sys
import json
import argparse
import datetime
import boto3


'''
    todo:
            1. READY FUNCTION -  DONE
            Need to sleep until environment is in a ready state... Otherwise, app throws error because the deployment
            Policy and ROLLING UPDATE TYPE functions need to finish running.

            2. Create a function to set Deployment policy to immutable. - DONE


            3. Create a function to set ROLLING UPDATE TYPE. - DONE

                                    Namespace:    aws:autoscaling:updatepolicy:rollingupdate
                                    OptionName:   RollingUpdateType
                                    Value:         Immutable

            4. Get beanstalk latest version from aws call and variablize it. - DONE

            5. Need to create a method for sleeping once the upgrade occurs... The current function is sleeping
            for five seconds... however, a complete upgrade - DONE

            6. Need to add in logic for changing STAGE ENV only to rolling dep policy. - DONE

            7. Need to skip the immutable config change for prod envs. - DONE

            8. Look for diffrent variations of NODE_ENV - DONE

            9. Need to throw in exception handling around try-catch. - DONE

        10. Logic to skip prod env on fridays. - Cron scheduling??? - Not Started

        11. Jenkins cron job - Not Started

        12. refactor for paralellel excution. - Not Started

        13. stub out how to notify specific developer with aws message. - Not Started

            14. Need to throw in logic to check if prod envs have immutable enabled. If not, enable for prod envs. - DONE
'''


from multiprocessor import main as multirun


def main():

    env_list = get_env_list()

    print("printing first list element for testing purposes: ", end='')
    print(env_list[0])

    # return

    multirun(ListToProcess=env_list, s_timeout=600, m_processes=5)


def get_env_list():
    """
        Worker function for the applicationself.
    """

    platform_version = list_platform_version()

    env_app_list = get_node_environments(platform_version)

    return env_app_list


# ---------------------------------------------------------------------------------------------------->
# ------------------------------------------ MAIN ------------------------------------------------->
# ---------------------------------------------------------------------------------------------------->

if __name__ == '__main__':
    main()

    # Python wrapper for beanstalker by Johnny Martinez

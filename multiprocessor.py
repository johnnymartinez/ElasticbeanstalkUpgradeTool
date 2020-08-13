from multiprocessing import Process, Manager, Value, Queue

import os, sys, time, json, datetime, random
#from get_bucket_directories import get_bucket_directories
#from workbook import create_workbook as workbook
from lib.display import display
from worker import worker_process

# args=(bucket_name, results, s_timeout, prefix)
def fake_worker(beanstalk_env, shared_results, s_timeout=600, bool_prod=False):
    print(beanstalk_env)
    time.sleep(10)


# get last status from queue
def get_status(q):

    last = None

    while q.empty() == False:
        last = q.get()

    return last



#========================================================================================================>
#========================================================================================================>
#================================== Multi processor right here ==========================================>
#========================================================================================================>
#========================================================================================================>




def main(ListToProcess=None, s_timeout=None, m_processes=None):

    #Stuff here
    p_list              = {}
    q_list              = {}
    latest_status       = {}
    more_data           = True
    status              = ''
    cont                = True
    manager             = Manager()
    shared_results      = manager.dict()
    list_size           = len(ListToProcess)
    exception_list      = []
    longest_env_name    = 0
    index_of_longest    = 0
    list_pointer        = 0
    bool_prod           = False


    # Manager loop
    while cont or more_data:


        # add more tasks to the list - max processes used here
        while len(p_list) < m_processes:
            #print("attempting to add another process")

            if list_pointer >= list_size:
                #print("no more processes in the list!")
                more_data = False
                break
            else:
                # Adding the process to the data structure here
                # More data to add? Time the process started?, items processed?


                beanstalk_env = ListToProcess[list_pointer]

                q_list[beanstalk_env] = Queue()
                p = Process(target=worker_process, args=(q_list[beanstalk_env], beanstalk_env, shared_results, s_timeout, bool_prod) )
                #p = Process(target=worker_process, args=(beanstalk_env, shared_results, s_timeout, bool_prod) )
                init_time = time.time()
                p.start()
                p_list[beanstalk_env] = (p , init_time)
                list_pointer = list_pointer + 1
                #dict should have a bigger size now

        cont = False

        time.sleep(.5)

        deletion_list = []

        # CHECK IF PROCESSES ARE FINISHED
        for proc in p_list:
            if p_list[proc][0].is_alive():
                cont = True #if any process is still alive set this flag to true
            else:
                try:
                    p_list[proc][0].join()
                    #print("PROC " + str(proc))
                    deletion_list.append(proc)
                    print(f"joined {proc}")
                except:
                    print("failed to join this thread. Didn't delete it either.")
                    #input("fuck")

        # remove processes that have been joined. I don't know what problems this could have if I delete my reference to a process that fails to join but isn't aliveself.
        # Problems could arise like having 5 blocked processes. No timeout mechanism either.
        # DELETING PROCESSES THAT HAVE FINISHED. You can't modify the data structure during iteration, at least you can't delete elements from it.
        for p in deletion_list:
            print(f"deletion {p}")
            del p_list[p]
            del q_list[p]

        # def get_status(q):
        for q_item in q_list:
            print(q_item)

            temp = get_status(q_list[q_item])

            if temp == None:
                pass
            else:
                latest_status[q_item] = temp

        try:
            pass
            display(p_list, latest_status, str(list_pointer) + "/" + str(list_size), m_processes, s_timeout, bucket=None)
        except Exception as e:
            print(e)
            pass
    #-----END WHILE-------------------------------------------------------->



if __name__ == '__main__':

    #Running tests here:
    my_list = [
        'tower',
        'bell',
        'clock',
        'watch',
        'signal',
        'word',
        'temp',
        'gas',
        'apple',
        'maps',
        'books',
        'things',
        'computer',
        'screen',
        'more',
        'random'
    ]
    #def main(ListToProcess=None, s_timeout=None, m_processes=None):
    main(ListToProcess=my_list, s_timeout=600, m_processes=5)

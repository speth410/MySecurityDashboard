import socket  # as we are opening sockets, need the module
 
import time # time our script
 
import threading # we want to multi thread this 
 
from queue import Queue # and have queue management


# create queue and threader      
q = Queue()
socket.setdefaulttimeout(0.55)
    
# lock thread during print so we get cleaner outputs
print_lock = threading.Lock()

cameras = []

# define our port scan process
def portscan(host):
 
   # create socket object
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   
   # try to connect
   try:
      # create/open connection
      conx = s.connect((host, 8554))
      
      # don't let thread contention screw up printing
      with print_lock:
         camera = host + ':8554'
         if camera not in cameras:
            cameras.append(camera)
        
      
      # close out that connection
      conx.close()
   except:
      pass
 
# threader thread pulls worker from queue and processes
def threader():
   while True:
      # gets worker from queue
      worker = q.get()
      # run job with savailable worker in queue (thread)
      portscan(worker)
 
      # complete with the job, shut down thread?
      q.task_done()


def scanNetwork():

    
    base_ip = "192.168.0."
    print ('Scanning Network for Open Ports: ', base_ip)
    

    
    # start time
    startTime = time.time()
    
    # 100 threads took 172 seconds
    # 200 threads took 87 seconds   
    for x in range(200):
        # thread id
        t = threading.Thread(target = threader)
        
        # classifying as a daemon, so they will die when the main dies
        t.daemon = True
        
        # begins, must come after daemon definition
        t.start()
        
    # this is the range or variable passed to the worker pool   
    for i in range(1, 255):
        q.put(base_ip + '{0}'.format(i))
    
    # wait until thrad terminates   
    q.join()
    
    
    # ok, give us a final time report
    runtime = float("%0.2f" % (time.time() - startTime))
    print("Run Time: ", runtime, "seconds")

    for i in range(len(cameras)):
        print('Camera(s) Found: ', cameras[i] + " ")

    return cameras

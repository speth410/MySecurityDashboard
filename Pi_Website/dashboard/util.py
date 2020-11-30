import socket  # as we are opening sockets, need the module
import time # time our script
import threading # we want to multi thread this 
from queue import Queue # and have queue management
import cv2


# create queue and threader      
q = Queue()
socket.setdefaulttimeout(0.55)
    
# lock thread during print so we get cleaner outputs
print_lock = threading.Lock()

cameras = []

port_num = 8554

class VideoCamera(object):
    stream_url = ""
    stream_name = ""
    stream = True

    def __init__(self, stream_url):
        self.stream_url = stream_url

    def getVideoCapture(self):
        return self.video

    def gen_frames(self):
        try:
            self.video = cv2.VideoCapture('rtsp://wowzaec2demo.streamlock.net/vod/mp4')

            while (True):
                # Capture frame-by-frame
                success, frame = self.video.read()  # read the camera frame
                if frame is None:
                    print("\nEmpty Frame!!!!!!!!!!\n")
                if not success:
                    print("ERROR STOPPING STREAM")
                    break
                else:
                    ret, buffer = cv2.imencode('.jpg', frame)
                    frame = buffer.tobytes()
                    yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

            self.video.release()
            cv2.destroyAllWindows()
        except socket.timeout as err:
            print(err)

    def stopStream(self):
        self.stream = False
    def startStream(self):
        self.stream = True
        self.video = cv2.VideoCapture(self.stream_url)

# define our port scan process
def portscan(host):
 
   # create socket object
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   
   # try to connect
   try:
      # create/open connection
      conx = s.connect((host, port_num))
      
      # don't let thread contention screw up printing
      with print_lock:
         camera = host + ':' + str(port_num)
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


def scanNetwork(ip=None, port=None):
   
   base_ip = ip

   print ('Scanning Network for Devices: ', base_ip, ":", port_num)
    
   startTime = time.time()
    
   # 200 = # of threads used
   for x in range(200):
      # thread id
      t = threading.Thread(target = threader)
        
      t.daemon = True
        
      t.start()
        
   # Test all ip addresses from 192.168.0.1 - 192.168.0.255
   for i in range(1, 255):
      q.put(base_ip + '{0}'.format(i))
    
   # wait until thrad terminates   
   q.join()
    
   runtime = float("%0.2f" % (time.time() - startTime))
   print("Run Time: ", runtime, "seconds")

   for i in range(len(cameras)):
      print('Camera(s) Found: ', cameras[i] + " ")

   return cameras

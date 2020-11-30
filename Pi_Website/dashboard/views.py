from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
from django.contrib.auth import authenticate, login
from . import util
import cv2
import time
import socket

streams = []



def addStream(stream_url):
    streams.append(util.VideoCamera(stream_url))

#addStream('rtsp://192.168.0.37:8554/mjpeg/1')
addStream('rtsp://wowzaec2demo.streamlock.net/vod/mp4')

def addCamera(request):

    if request.method == 'POST':
        new_stream = request.POST['stream_url']

        streams.append(util.VideoCamera(new_stream))

    for i in range(len(streams)):
           urls = [streams[i].getStreamURL()]
        
    connectedStreams = {'streams': urls}
    print (connectedStreams)

    return render(request, 'dashboard/dashboard.html', connectedStreams)



# Create your views here.

def video_feed(request):

    return StreamingHttpResponse(streams[0].gen_frames(), content_type='multipart/x-mixed-replace; boundary=frame')


@login_required(login_url='login/')
def dashboard(request):

    #cameras = {'cameras': util.scanNetwork()}
    return render(request, 'dashboard/dashboard.html')


def view_cameras(request):
    #camera = cv2.VideoCapture('rtsp://wowzaec2demo.streamlock.net/vod/mp4')
    return render(request, 'dashboard/view_cameras.html')

def user_login(request):

    if request.method == 'POST':
        # Process the request if posted data are available
        username = request.POST['username']
        password = request.POST['password']
        # Check username and password combination if correct
        user = authenticate(username=username, password=password)

        #user entered some data into fields
        if user is not None:
            # Save session as cookie to login the user
            login(request, user)
            # Success, now let's login the user.
            return render(request, 'dashboard/dashboard.html')
        else:
            # Incorrect credentials, let's throw an error to the screen.
            return render(request, 'dashboard/login.html', {'error_message': 'Incorrect username and / or password.'})
    else:
        # No post data availabe, let's just show the page to the user.
        return render(request, 'dashboard/login.html')

@login_required(login_url='login/')
def baseView(request):
    return render(request, 'dashboard/dashboard.html')

def registerView(request):

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard:user_login')
    else:
        form = UserCreationForm()

        return render(request, 'dashboard/register.html',{'form':form})

def scan(request):
    if request.method == 'POST':
        ip = request.POST['ip_addr']
        port = request.POST['port_num']

        cameras = {'cameras': util.scanNetwork(ip, port)}
        return render(request, 'dashboard/dashboard.html', cameras)
    
    else:
        cameras = {'cameras': util.scanNetwork()}
        return render(request, 'dashboard/dashboard.html', cameras)



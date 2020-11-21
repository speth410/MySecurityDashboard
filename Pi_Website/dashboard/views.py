from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

"""
userInfo = [
    {
        'username': 'Test User',
        'password': 'Test'
    }
]
"""

# Create your views here.

def baseView(request):
    return render(request, 'dashboard/base.html')

def registerView(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard:user_login')
    else:
        form = UserCreationForm()

        return render(request, 'dashboard/register.html',{'form':form})

#@login_required
def dashboard(request):
    #user = {
     #   'userInfo': userInfo
    #}
    return render(request, 'dashboard/dashboard.html')


def user_login(request):
        #return render(request, 'dashboard/login.html')
        #return redirect('dashboard:home')
        #test

        
        if request.method == 'POST':
            # Process the request if posted data are available
            username = request.POST['username']
            password = request.POST['password']
            # Check username and password combination if correct
            user = authenticate(username=username, password=password)
            return redirect('dashboard:home')
            

            #user entered some data into fields
            if user is not None:
                # Save session as cookie to login the user
                login(request, user)
                # Success, now let's login the user.
                return render(request, 'dashboard/dashboard.html')
            else:
                # Incorrect credentials, let's throw an error to the screen.
                return render(request, '', {'error_message': 'Incorrect username and / or password.'})
        else:
            # No post data availabe, let's just show the page to the user.
            return render(request, 'dashboard/login.html')



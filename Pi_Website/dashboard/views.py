from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

userInfo = [
    {
        'username': 'Test User',
        'password': 'Test'
    }
]
# Create your views here.

def login(request):
    return render(request, 'dashboard/login.html')

def dashboard(request):
    user = {
        'userInfo': userInfo
    }

    return render(request, 'dashboard/dashboard.html', user)


def user_login(request):
    return render(request, 'dashboard/login.html')
    '''
    if request.method == 'POST':
        # Process the request if posted data are available
        username = request.POST['username']
        password = request.POST['password']
        # Check username and password combination if correct
        user = authenticate(username=username, password=password)

        
        if user is not None:
            # Save session as cookie to login the user
            login(request, user)
            # Success, now let's login the user.
            return render(request, 'templates/dashboard/account.html')
        else:
            # Incorrect credentials, let's throw an error to the screen.
            return render(request, 'ecommerce/user/login.html', {'error_message': 'Incorrect username and / or password.'})
    else:
        # No post data availabe, let's just show the page to the user.
        return render(request, 'ecommerce/user/login.html')
        '''


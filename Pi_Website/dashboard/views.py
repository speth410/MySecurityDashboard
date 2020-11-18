from django.shortcuts import render
from django.http import HttpResponse

userInfo = [
    {
        'username': 'Test User',
        'password': 'Test'
    }
]
# Create your views here.

def login(request):
    return HttpResponse('<h1>Login</h1>')

def dashboard(request):
    user = {
        'userInfo': userInfo
    }
    return render(request, 'dashboard/dashboard.html', user)


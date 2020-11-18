from django.urls import path
from . import views

app_name = 'dashboard'
urlpatterns = [
    path('', views.dashboard, name='dashboard-home'),
    path('login/', views.user_login, name='user_login'),
    
]

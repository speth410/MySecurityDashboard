from django.urls import path
from . import views
#from . import util
from django.contrib.auth.views import LoginView,LogoutView





app_name = 'dashboard'
urlpatterns = [
    path('',views.baseView, name="home"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('login/', views.user_login, name="user_login"),
    path('register/', views.registerView,name="registerView"),
    path('logout/',LogoutView.as_view(),name="logout"),
    path('/video_feed', views.video_feed, name='video_feed'),
    path('view_cameras/', views.view_cameras, name='view_cameras'),
    #path('/scan_network', util.scanNetwork, name='scan_network')
    #path('', views.dashboard, name='dashboard-home'),
    #path('login/', views.user_login, name='user_login'),

    
]



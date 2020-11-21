from django.urls import path
from . import views
from django.contrib.auth.views import LoginView,LogoutView





app_name = 'dashboard'
urlpatterns = [
    path('',views.baseView, name="home"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('login/', views.user_login, name="user_login"),
    path('register/', views.registerView,name="registerView"),
    path('logout/',LogoutView.as_view(),name="logout"),
    
    
]



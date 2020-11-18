from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard-home'),
    path('login/', views.login, name='dashboard-login'),
]

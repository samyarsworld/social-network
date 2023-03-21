
from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect

from . import views

urlpatterns = [
    path("", views.dashboard, name='dashboard'),

    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    
]



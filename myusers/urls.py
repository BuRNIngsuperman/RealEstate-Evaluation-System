"""Defines url patterns for users."""

from django.urls import path
from django.contrib.auth.views import login

from . import views

app_name = 'myusers'
urlpatterns = [
    # Login page.
    path('login/', login, {'template_name': 'myusers/login.html'},
         name='login'),

    # Logout page.
    path('logout/', views.logout_view, name='logout'),

    # Registration page. 
    path('register/', views.register, name='register'),
]
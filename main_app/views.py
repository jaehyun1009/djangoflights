from django.shortcuts import render
from django.contrib.auth.views import LoginView

class Home(LoginView):
  template_name = 'home.html'
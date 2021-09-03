from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView
from .forms import SearchAirportForm
from .models import Airport, Profile, Ticket
import requests

class Home(LoginView):
  template_name = 'home.html'

class AirportCreate(LoginRequiredMixin, CreateView):
  model = Airport

def search(request):
  results = []
  if request.GET.get('code') or request.GET.get('name'):
    code = request.GET.get('code')
    name = request.GET.get('name')
    response = requests.get('https://raw.githubusercontent.com/jbrooksuk/JSON-Airports/master/airports.json')
    for obj in response.json():
      if code and name:
        if obj['name'] and name in obj['name'].lower() and obj['iata'] and code.upper() in obj['iata'] and len(results) < 50:
          results.append(obj)
      elif name and obj['name'] and name in obj['name'].lower() and len(results) < 50:
        results.append(obj)
      elif code and obj['iata'] and code.upper() in obj['iata'] and len(results) < 50:
        results.append(obj)
  return render(request, 'search.html', {
    'form': SearchAirportForm(),
    'results': results
  })

def get_airport(request):
  if request.method == 'POST':
    form = SearchAirportForm(request.POST)
    print(form)
    if form.is_valid():
      return render(request, 'search.html', {'form': form})
  else:
    form = SearchAirportForm()
  return render(request, 'search.html', {'form': form})

@login_required
def airports_index(request):
  return render(request, 'airports/index.html')

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in
      login(request, user)
      return redirect('airports_index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'signup.html', context)
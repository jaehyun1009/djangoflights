from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from .forms import SearchAirportForm
import requests

class Home(LoginView):
  template_name = 'home.html'

def search(request):
  code = None
  results = None
  if request.GET.get('code'):
    code = request.GET.get('code')
    response = requests.get('https://raw.githubusercontent.com/jbrooksuk/JSON-Airports/master/airports.json')
  return render(request, 'search.html', {
    'form': SearchAirportForm(),
    'code': code
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
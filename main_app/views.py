from django.contrib.auth import forms
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView
from .forms import SearchAirportForm
from .models import Airport, Profile, Ticket
import requests
from decimal import Decimal
from math import radians, cos, sin, asin, sqrt, log

class Home(LoginView):
  template_name = 'home.html'

class TicketList(LoginRequiredMixin, ListView):
  model = Ticket

def calculate_distance(origin_lat, origin_lon, dest_lat, dest_lon):
  radius = 3959.87433
  d_lat = radians(dest_lat - origin_lat)
  d_lon = radians(dest_lon - origin_lon)
  lat1 = radians(origin_lat)
  lat2 = radians(dest_lat)
  a = sin(d_lat/2)**2 + cos(lat1)*cos(lat2)*sin(d_lon/2)**2
  c = 2*asin(sqrt(a))
  return radius*c

def calculate_price(seat_class, origin_lat, origin_lon, dest_lat, dest_lon):
  base = 50
  modifier = 1
  if seat_class == 'B':
    modifier = 1.5
  if seat_class == 'F':
    modifier = 3
  distance = calculate_distance(origin_lat, origin_lon, dest_lat, dest_lon)
  return base + int(modifier * (distance/500)*log(distance, 1.1))

class TicketCreate(LoginRequiredMixin, CreateView):
  model = Ticket
  fields = ['seat_class', 'date', 'origin', 'destination']

  def form_valid(self, form):
    form.instance.price = calculate_price(form.instance.seat_class, 39, -70, 20, -42)
    form.instance.profile = Profile.objects.get(id=self.request.user.id)
    return super().form_valid(form)

def about(request):
  return render(request, 'about.html')

def search(request):
  results = []
  if request.GET.get('iata') or request.GET.get('name'):
    iata = request.GET.get('iata')
    name = request.GET.get('name')
    response = requests.get('https://raw.githubusercontent.com/jbrooksuk/JSON-Airports/master/airports.json')
    for obj in response.json():
      if 'name' in obj and 'iata' in obj and 'iso' in obj and 'lat' in obj and 'lon' in obj and obj['name'] != None and obj['iata'] != None and obj['iso'] != None and obj['lat'] != None and obj['lon'] != None:
        if iata and name:
          if name in obj['name'].lower() and iata.upper() in obj['iata'] and len(results) < 30:
            results.append(obj)
        elif name and name in obj['name'].lower() and len(results) < 30:
          results.append(obj)
        elif iata and iata.upper() in obj['iata'] and len(results) < 30:
          results.append(obj)
    for result in results:
      if (len(Airport.objects.filter(iata=result['iata'])) == 0) and result['name'] != None and result['iata'] != None and result['iso'] != None and result['lat'] != None and result['lon'] != None:
        result_data = Airport(
          name = result['name'],
          iata = result['iata'],
          iso = result['iso'],
          lat = Decimal(result['lat']),
          lon = Decimal(result['lon'])
        )
        result_data.save()
  send_results = Airport.objects.filter(iata__in=[result['iata'] for result in results])
  return render(request, 'search.html', {
    'form': SearchAirportForm(),
    'results': send_results
  })

def airports_index(request):
  user = Profile.objects.get(id=request.user.id)
  airports = user.airport.all()
  return render(request, 'main_app/airport_list.html', {
    'airports': airports
  })

def airports_detail(request, airport_id):
  if (request.user.id is not None):
    profile = Profile.objects.get(id=request.user.id)
    return render(request, 'main_app/airport_detail.html', {
      'airport': Airport.objects.get(id=airport_id),
      'profile': profile,
      'profile_airport': profile.airport.all()
    })
  else:
    return render(request, 'main_app/airport_detail.html', {
      'airport': Airport.objects.get(id=airport_id),
    })

@login_required
def assoc_airport(request, airport_id, profile_id):
  Profile.objects.get(id=profile_id).airport.add(airport_id)
  return redirect('airports_detail', airport_id=airport_id)

@login_required
def remove_assoc_airport(request, airport_id, profile_id):
  airport_to_be_removed = Airport.objects.get(id=airport_id)
  Profile.objects.get(id=profile_id).airport.remove(airport_to_be_removed)
  return redirect('airports_detail', airport_id=airport_id)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      profile = Profile(user=user)
      profile.save()
      # This is how we log a user in
      login(request, user)
      return redirect('airports_index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'signup.html', context)
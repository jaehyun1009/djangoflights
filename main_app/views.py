from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView
from django.conf import settings
from .forms import SearchAirportForm
from .models import Airport, Profile, Ticket
from decimal import Decimal
from math import radians, cos, sin, asin, sqrt
import re
import requests
from datetime import datetime, timedelta

# https://en.wikipedia.org/wiki/Haversine_formula
def calculate_distance(origin_lat, origin_lon, dest_lat, dest_lon):
  radius = 3959.87433
  lat1 = radians(origin_lat)
  lat2 = radians(dest_lat)
  d_lat = radians(dest_lat - origin_lat)
  d_lon = radians(dest_lon - origin_lon)
  angle = asin(sqrt(sin(d_lat/2)**2 + cos(lat1)*cos(lat2)*sin(d_lon/2)**2))
  return 2*radius*angle

def calculate_price(seat_class, origin_lat, origin_lon, dest_lat, dest_lon):
  base = 48
  modifier = 1
  if seat_class == 'B':
    modifier = 1.5
  if seat_class == 'F':
    modifier = 3
  distance = calculate_distance(origin_lat, origin_lon, dest_lat, dest_lon)
  return base + int(modifier * distance/12)

class Home(LoginView):
  template_name = 'home.html'

class TicketList(LoginRequiredMixin, ListView):
  model = Ticket

  def get_queryset(self):
    return Ticket.objects.filter(profile_id=self.request.user.id)

class TicketDetail(LoginRequiredMixin, DetailView):
  model = Ticket

  def get_context_data(self, **kwargs):
    context = super(TicketDetail, self).get_context_data(**kwargs)
    origin = context['object'].origin
    dest = context['object'].destination
    context['distance'] = round(calculate_distance(origin.lat, origin.lon, dest.lat, dest.lon),2)
    context['travel_time'] = context['object'].date + timedelta(minutes=round((context['distance']/475) * 60))
    return context

class TicketCreate(LoginRequiredMixin, CreateView):
  model = Ticket
  fields = ['seat', 'date', 'origin', 'destination']

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    airports = Profile.objects.get(id=self.request.user.id).airport.all()
    context['form'].fields['origin'].queryset = airports
    context['form'].fields['destination'].queryset = airports
    return context

  def form_valid(self, form):
    if form.instance.origin == form.instance.destination:
      return super().form_invalid(form)
    form.instance.seat_class = 'E'
    if re.search(r'0[1-4][A-D]', form.instance.seat):
      form.instance.seat_class = 'F'
    if re.search(r'0[5-9][A-G]|1[0-5][A-G]', form.instance.seat):
      form.instance.seat_class = 'B'
    form.instance.price = calculate_price(form.instance.seat_class, form.instance.origin.lat, form.instance.origin.lon, form.instance.destination.lat, form.instance.destination.lon)
    form.instance.profile = Profile.objects.get(id=self.request.user.id)
    return super().form_valid(form)

class TicketDelete(LoginRequiredMixin, DeleteView):
  model = Ticket
  success_url = '/tickets/'

class TicketUpdate(LoginRequiredMixin, UpdateView):
  model = Ticket
  fields = ['seat']

  def form_valid(self, form):
    form.instance.seat_class = 'E'
    if re.search(r'0[1-4][A-D]', form.instance.seat):
      form.instance.seat_class = 'F'
    if re.search(r'0[5-9][A-G]|1[0-5][A-G]', form.instance.seat):
      form.instance.seat_class = 'B'
    form.instance.price = calculate_price(form.instance.seat_class, form.instance.origin.lat, form.instance.origin.lon, form.instance.destination.lat, form.instance.destination.lon)
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

@login_required
def airports_index(request):
  airports = Profile.objects.get(id=request.user.id).airport.all()
  return render(request, 'main_app/airport_list.html', {
    'airports': airports
  })

def k_to_f(k):
  return int((k - 273.15)*(9/5)+32)

def get_index(idx):
  level = 'Good'
  if idx == 2:
    level = 'Moderate'
  elif idx == 3:
    level = 'Poor'
  elif idx == 4:
    level = 'Unhealthy'
  elif idx == 5:
    level = 'Very Unhealthy'
  return level

def airports_detail(request, airport_id):
  airport = Airport.objects.get(id=airport_id)
  airport_details = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={airport.lat}&lon={airport.lon}&appid={settings.WEATHER_API}').json()
  air_pollution = requests.get(f'http://api.openweathermap.org/data/2.5/air_pollution?lat={airport.lat}&lon={airport.lon}&appid={settings.WEATHER_API}').json()
  img_url = f"http://openweathermap.org/img/wn/{airport_details['weather'][0]['icon']}@2x.png"
  airport_details['visibility'] = round(airport_details['visibility']/1000, 3)
  temps = {
    'temp': k_to_f(airport_details['main']['temp']),
    'feels_like': k_to_f(airport_details['main']['feels_like']),
    'temp_min': k_to_f(airport_details['main']['temp_min']),
    'temp_max': k_to_f(airport_details['main']['temp_max'])
  }
  sunrise = datetime.fromtimestamp(airport_details['sys']['sunrise'] + airport_details['timezone']).strftime('%I:%M %p')
  sunset = datetime.fromtimestamp(airport_details['sys']['sunset'] + airport_details['timezone']).strftime('%I:%M %p')
  air_pollution_index = air_pollution['list'][0]['main']['aqi']
  air_pollution_level = get_index(air_pollution_index)
  if (request.user.id is not None):
    profile = Profile.objects.get(id=request.user.id)
    return render(request, 'main_app/airport_detail.html', {
      'profile': profile,
      'profile_airport': profile.airport.all(),
      'airport': airport,
      'airport_details': airport_details,
      'air_pollution': air_pollution,
      'img_url': img_url,
      'temps': temps,
      'sunrise': sunrise,
      'sunset': sunset,
      'air_pollution_index': air_pollution_index,
      'air_pollution_level': air_pollution_level
    })
  else:
    return render(request, 'main_app/airport_detail.html', {
      'airport': airport,
      'airport_details': airport_details,
      'air_pollution': air_pollution,
      'img_url': img_url,
      'temps': temps,
      'sunrise': sunrise,
      'sunset': sunset,
      'air_pollution_index': air_pollution_index,
      'air_pollution_level': air_pollution_level
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
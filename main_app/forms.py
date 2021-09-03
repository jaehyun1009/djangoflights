from django.forms import ModelForm
from .models import Airport

class SearchAirportForm(ModelForm):
  class Meta:
    model = Airport
    fields = ['name', 'code']
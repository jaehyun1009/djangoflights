from django.forms import ModelForm
from .models import Airport

class AirportForm(ModelForm):
  class Meta:
    model = Airport
    fields = ['code']
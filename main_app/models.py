from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

CLASSES = (
  ('E', 'Economy'),
  ('B', 'Business'),
  ('F', 'First Class')
)

class Airport(models.Model):
  name = models.CharField(max_length=100)
  code = models.CharField(max_length=3)
  iso = models.CharField(max_length=2)
  lat = models.DecimalField(decimal_places=6, max_digits=10)
  lon = models.DecimalField(decimal_places=6, max_digits=10)

  def __str__(self):
    return self.code

  def get_absolute_url(self):
    return reverse('airports_detail', kwargs={'airport_id': self.id})

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  airport = models.ManyToManyField(Airport)

class Ticket(models.Model):
  price = models.IntegerField()
  seat_class = models.CharField(
    max_length=1,
    choices=CLASSES,
    default=CLASSES[0][0]
  )
  origin = models.ManyToManyField(Airport, related_name='origin_airport')
  destination = models.ManyToManyField(Airport, related_name='destination_airport')
  profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

  def __str__(self):
    return f'Ticket from {self.origin.code} to {self.destination.code}'

  def get_absolute_url(self):
    return reverse('tickets_detail', kwargs={'ticket_id': self.id})
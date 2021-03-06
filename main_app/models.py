from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

CLASSES = (
  ('E', 'Economy'),
  ('B', 'Business'),
  ('F', 'First Class')
)

class Airport(models.Model):
  name = models.CharField('Airport Name', max_length=100, blank=True)
  iata = models.CharField('3-digit Airport Code', max_length=3, blank=True, unique=True)
  iso = models.CharField('Country Code', max_length=2)
  lat = models.DecimalField(decimal_places=6, max_digits=12)
  lon = models.DecimalField(decimal_places=6, max_digits=12)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse("airports_detail", kwargs={"airport_id": self.id})

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  airport = models.ManyToManyField(Airport, blank=True)

class Ticket(models.Model):
  price = models.IntegerField()
  seat = models.CharField(
    max_length=3,
    validators=[
      RegexValidator('^0[1-4][A-D]|0[5-9][A-G]|1[0-5][A-G]|1[6-9][A-J]|2[0-9][A-J]|3[0-4][A-J]$',
        message='Please follow instructions on picking a seat number.',
        code='invalid_seat'
      )
    ]
  )
  seat_class = models.CharField(
    max_length=1,
    choices=CLASSES,
    default=CLASSES[0][0],
  )
  date = models.DateTimeField()
  origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='origin_airport')
  destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='destination_airport')
  profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

  def __str__(self):
    return f'Ticket #{self.id}'

  def get_absolute_url(self):
    return reverse("tickets_detail", kwargs={"pk": self.id})
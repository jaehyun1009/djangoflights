from django.contrib import admin
from .models import Airport, Ticket, Profile

# Register your models here.
admin.site.register(Airport)
admin.site.register(Ticket)
admin.site.register(Profile)
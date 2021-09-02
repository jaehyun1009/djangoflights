from django.urls import path
from . import views

urlpatterns = [
  path('', views.Home.as_view(), name='home'),
  path('search/', views.search, name='search'),
  path('airports/', views.airports_index, name='airports_index'),
  path('accounts/signup/', views.signup, name='signup')
]
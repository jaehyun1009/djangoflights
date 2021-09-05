from django.urls import path
from . import views

urlpatterns = [
  path('', views.Home.as_view(), name='home'),
  path('about/', views.about, name='about'),
  path('search/', views.search, name='search'),
  path('airports/', views.airports_index, name='airports_index'),
  path('airports/<int:airport_id>/', views.airports_detail, name='airports_detail'),
  path('airports/<int:airport_id>/assoc_airport/<int:profile_id>/', views.assoc_airport, name='assoc_airport'),
  path('airports/<int:airport_id>/remove_assoc/<int:profile_id>/', views.remove_assoc_airport, name='remove_assoc_airport'),
  path('tickets/', views.TicketList.as_view(), name='tickets_index'),
  path('tickets/create/', views.TicketCreate.as_view(), name='tickets_create'),
  path('tickets/<int:pk>', views.TicketDetail.as_view(), name='tickets_detail'),
  path('accounts/signup/', views.signup, name='signup')
]
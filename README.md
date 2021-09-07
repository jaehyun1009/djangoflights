<p align="center">
  <img src='./main_app/static/images/logo-dark.svg' width='500'>
</p>

## Introduction
Django Flights is a full-stack web application built primarily using Python and Django where the user can add airports to their list and purchase (imaginary) tickets between two airports, automatically calculating ticket price based on how far the destination is from the origin.

## How to Use this Application
Press Search on the navbar to search for an airport by its name or 3-digit IATA code. In order to access the app's full functionality, user has to signup and login. Once a user is logged in, they can add an airport to their list. Afterwards, the user can then purchase airplane tickets provided they have at least 2 different airports added to their list as origin and destination.

## Deployment Link
https://djangoflights.herokuapp.com/

## Planning Materials
### Trello Board
https://trello.com/b/yds2NpEE/django-flights
### Wireframe
![Wireframe](https://trello.com/1/cards/6130211d87e66f57c1514029/attachments/6130214d0b2aa71bf0ca0a14/previews/6130214d0b2aa71bf0ca0a48/download/Untitled.png)
### Entity-Relationship Diagram
![ERD](https://trello.com/1/cards/61304e1f786931069897fae1/attachments/6137a1154e09b665e6975932/previews/6137a1164e09b665e6975941/download/Screen_Shot_2021-09-07_at_10.27.27_AM.png)

## Screenshots
### Login Page
This is the page that will show if you go to this website for the first time.  
![Login](https://i.imgur.com/KPIA3Gv.png)
### Signup Page
![Signup](https://i.imgur.com/taWzTvj.png)
### Info Page
Also shows up in home page url if you are logged in.  
![Info](https://i.imgur.com/RO6dXU9.png)
### Search Airport Page
Search by airport name (In this case, I typed in Texas in the 'Airport Name' field.)  
![PageName](https://i.imgur.com/VfNvqe0.png)
Search by airport IATA code (In this case, I typed in ICN in the '3-digit airport code' field.)  
![PageIata](https://i.imgur.com/n6b2FAd.png)
### Airport Detail Page
![AirportDetail](https://i.imgur.com/JEtjfzl.png)
### Airport List Page
![AirportList](https://i.imgur.com/PNRZszj.png)
### Ticket List Page
![TicketList](https://i.imgur.com/zwjwj5e.png)
### New Ticket Page
![NewTicket](https://i.imgur.com/voah6Nm.png)
Showcasing Flatpickr  
![Flatpickr](https://i.imgur.com/a2U7ZiY.png)
### Ticket Detail Page
![TicketDetail](https://i.imgur.com/UllPW1q.png)
## Technologies Used
- Python
- Django
- HTML5
- CSS
- Javascript
- PostgreSQL

## Disclaimer
This project is not officially endorsed by Django Software Foundation and/or by the Django Core team. See the <a href='https://www.djangoproject.com/trademarks/'>Django Trademark License Agreement</a> for usage of Django name on this project.

## Additional Resources
- [Flatpickr](https://flatpickr.js.org/)
- [OpenWeatherAPI](https://openweathermap.org/)
- [Custom Airport JSON API](https://github.com/jbrooksuk/JSON-Airports)
- Air pollution icons from https://www.wunderground.com
- Plane image from https://www.vectorstock.com/royalty-free-vector/plane-top-view-vector-10020407
- Ticket Checkout image from https://geoparkinillustration.files.wordpress.com/2020/05/airportcheck-inqueue.jpg
- Airport Lounge Background from https://www.vecteezy.com/vector-art/1637736-airport-lounge-background

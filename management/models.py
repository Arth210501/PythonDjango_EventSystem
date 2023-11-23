from django.db import models
import datetime
# Create your models here.


class Login(models.Model):
    FIRSTNAME = models.CharField(max_length=50)
    LASTNAME = models.CharField(max_length=50)
    USERNAME = models.CharField(max_length=64, unique=True)
    PASSWORD = models.CharField(max_length=50)
    EMAIL = models.EmailField(max_length=64)
    ROLE = models.CharField(max_length=10)


class Events(models.Model):
    Name = models.CharField(max_length=100)
    Place = models.CharField(max_length=100)
    Description = models.CharField(max_length=500)
    Tickets_Price = models.BigIntegerField()
    Total_Ticket = models.BigIntegerField()
    Event_Date = models.DateTimeField(default=datetime.datetime.today)
    Event_Image = models.ImageField(upload_to='Event_Images/', null=True)
    Event_Poster = models.ImageField(upload_to='Event_Posters', null=True)


class Booking(models.Model):
    Username = models.CharField(max_length=64)
    BookingCode = models.CharField(max_length=10)
    First_name = models.CharField(max_length=50)
    Last_name = models.CharField(max_length=50)
    Email = models.CharField(max_length=64)
    Phone = models.CharField(max_length=13)
    Address = models.CharField(max_length=100)
    City = models.CharField(max_length=20)
    Postal_code = models.CharField(max_length=8)
    State = models.CharField(max_length=20)
    Country = models.CharField(max_length=10)
    NameOnCard = models.CharField(max_length=50)
    CreditCardType = models.CharField(max_length=20)
    CreditCardNumber = models.CharField(max_length=20)
    CvvCode = models.CharField(max_length=3)
    CardExpirationDate = models.CharField(max_length=10)
    EventName = models.CharField(max_length=100)
    TicketPrice = models.BigIntegerField()
    NumberOfTickets = models.BigIntegerField()





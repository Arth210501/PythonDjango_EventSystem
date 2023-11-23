import requests
from django.shortcuts import render, redirect
from .models import *
import hashlib
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
import math
import random


# Create your views here.


def index(request):
    title = 'Home'
    event = Events.objects.all()
    if request.session.has_key('username'):
        user = request.session['username']
        fname = Login.objects.get(USERNAME=user)
        fname = fname.FIRSTNAME
        request.session['fname'] = fname
        role = request.session['role']
        if role == 'Admin':
            return render(request, 'adminhome.html', {'user': fname, 'events': event})
        else:
            return render(request, 'index.html', {'title': title, 'user': fname, 'events': event})
    else:
        return render(request, 'index.html', {'title': title, 'events': event})


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        password = hashlib.md5(str.encode(password)).hexdigest()

        if Login.objects.filter(USERNAME=email, PASSWORD=password).exists():
            login = Login.objects.get(USERNAME=email)
            role = login.ROLE
            request.session['username'] = email
            request.session['role'] = role
            return redirect('Home')
        else:
            messages.error(request, 'Invalid Credentials!!')
            return redirect('Login')
    else:
        return render(request, 'login.html', {'title': 'Login'})


def register(request):
    if request.method == 'POST':
        role = 'user'
        fname = request.POST['first_name']
        lname = request.POST['last_name']
        password = request.POST['password']
        email = request.POST['email']

        User_Validation = Login.objects.filter(USERNAME=email)
        if User_Validation.count() > 0:
            messages.error(request, 'Email already used!!!')
            return redirect('Register')
        else:
            password = hashlib.md5(str.encode(password)).hexdigest()
            User_Registration = Login(ROLE=role, USERNAME=email, FIRSTNAME=fname, LASTNAME=lname, EMAIL=email,
                                      PASSWORD=password)
            User_Registration.save()
            messages.success(request, 'You are fully registration successful!!!!')
            return redirect('Login')
    else:
        return render(request, 'register.html', {'title': 'Register'})


def logout(request):
    del request.session['role']
    del request.session['username']
    del request.session['fname']
    return redirect('Home')


def create_event(request):
    fname = request.session['fname']
    if request.session.has_key('username'):
        if request.method == 'POST':
            ename = request.POST['event_name']
            eplace = request.POST['event_place']
            edate = request.POST['date']
            etprice = request.POST['price']
            ettotle = request.POST['total_tickets']
            edescription = request.POST['description']
            eimage = request.FILES['image']
            eposter = request.FILES['poster']
            event = Events(Name=ename, Place=eplace, Event_Date=edate, Tickets_Price=etprice, Total_Ticket=ettotle,
                           Description=edescription, Event_Image=eimage, Event_Poster=eposter)
            event.save()
            messages.success(request, 'Event Created Successfully!!!!')
            return redirect('CreateEvent')
        else:
            return render(request, 'create_event.html', {'title': 'Create Event' ,'user': fname})
    else:
        return redirect('Login')


def add_to_cart(request):
    if request.session.has_key('username'):
        pro = request.POST.get('id')
        cart = request.session.get('cart')
        if cart:
            quen = cart.get(pro)
            if quen:
                cart[pro] = quen + 1
            else:
                cart[pro] = 1
        else:
            cart = {}
            cart[pro] = 1

        request.session['cart'] = cart
        return redirect('Home')
    else:
        return redirect('Login')


def cart(request):
    if request.session.has_key('username'):
        user = request.session['fname']
        role = request.session['role']
        if request.session.has_key('cart'):
            ids = list(request.session.get('cart').keys())
            event = Events.objects.filter(id__in=ids)
            return render(request, 'cart.html', {'title': 'cart', 'events': event, 'user': user, 'role': role})
        else:
            return render(request, 'cart.html', {'title': 'cart', 'user': user, 'role': role})
    else:
        return redirect('Login')


def quantity_update(request):
    pro = request.POST.get('product')
    remove = request.POST.get('remove')
    cart = request.session.get('cart')
    quen = cart.get(pro)
    if remove:
        if quen <= 1:
            cart.pop(pro)
        else:
            cart[pro] = quen - 1
    else:
        cart[pro] = quen + 1

    request.session['cart'] = cart
    return redirect('Cart')


def checkout(request):
    if request.session.has_key('username'):
        user = request.session['fname']
        role = request.session['role']
        if request.session.has_key('cart'):
            ids = list(request.session.get('cart').keys())
            event = Events.objects.filter(id__in=ids)
            return render(request, 'checkout.html', {'title': 'checkout', 'events': event, 'user': user, 'role': role})
        else:
            return render(request, 'checkout.html', {'title': 'checkout', 'user': user, 'role': role})
    return redirect('Login')


def place_order(request):
    if request.session.has_key('username'):
        user = request.session['fname']
        string = '1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcefghijklmnopqrstuvwxyz'
        lent = len(string)
        otp = ""
        for i in range(6):
            otp += string[math.floor(random.random() * lent)]

        bookingcode = otp
        username = request.session['username']
        f_name = request.POST.get('firstname')
        l_name = request.POST.get('lastname')
        email = request.POST.get('email')
        phone = request.POST.get('telephone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        pcode = request.POST.get('postcode')
        state = request.POST.get('zone')
        country = request.POST.get('country')
        nameoncard = request.POST.get('cardname')
        cctype = request.POST.get('cardtype')
        cnumber = request.POST.get('cardno')
        cvv = request.POST.get('cvv')
        expiration = request.POST.get('exdate')
        cart = request.session.get('cart')
        event = Events.objects.filter(id__in=list(cart.keys()))
        for e in event:
            order = Booking(Username=username, BookingCode=bookingcode, First_name=f_name, Last_name=l_name,
                            Email=email,
                            EventName=e.Name, Phone=phone, Address=address, City=city, Postal_code=pcode, State=state,
                            Country=country, NameOnCard=nameoncard, CreditCardType=cctype, CreditCardNumber=cnumber,
                            CvvCode=cvv, CardExpirationDate=expiration, TicketPrice=e.Tickets_Price,
                            NumberOfTickets=cart.get(str(e.id)))

            order.save()

        request.session['cart'] = {}
        booking = Booking.objects.get(BookingCode=bookingcode)
        vent = Events.objects.get(Name=booking.EventName)
        vent.Total_Ticket = vent.Total_Ticket - booking.NumberOfTickets
        vent.save()
        message = 'Dear ' + booking.First_name + ',\n\t Your ' + str(booking.NumberOfTickets) + ' Tickets are booked for ' + booking.EventName + \
                  '\nNote:- Can not replay on this mail.'
        send_mail('Booking conformation', message, settings.EMAIL_HOST_USER, [booking.Email], fail_silently=False)
        return render(request, 'orderplaced.html', {'title': 'orderplaced', 'user': user})

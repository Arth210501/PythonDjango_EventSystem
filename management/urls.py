from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='Home'),
    path('login', views.login, name='Login'),
    path('register', views.register, name='Register'),
    path('logout', views.logout, name='Logout'),
    path('createevent', views.create_event, name='CreateEvent'),
    path('addtocart', views.add_to_cart, name='Add_to_Cart'),
    path('cart', views.cart, name='Cart'),
    path('quantity_update', views.quantity_update, name='Quantity_Update'),
    path('checkout', views.checkout, name='Checkout'),
    path('placeorder', views.place_order, name='Place_order')
]

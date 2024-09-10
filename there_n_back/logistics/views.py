from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import HttpResponse
from django.views.generic import CreateView
from math import acos, sin, cos, radians
from datetime import timedelta
import decimal


# Custom User Resigtration

# def register(request):
#     return render(request, 'register.html')

class client_register(CreateView):
    model = User
    form_class = ClientSignUpForm
    template_name = 'register_client.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('client_dashboard')

class dispatcher_register(CreateView):
    model = User
    form_class = DispatcherSignUpForm
    template_name = 'register_dispatcher.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('dispatcher_dashboard')


def login_request(request):
    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None :
                login(request,user)
                if user.is_dispatcher:
                    return redirect('dispatcher_dashboard')
                else:
                    return redirect('client_dashboard')
            else:
                messages.error(request,"Invalid username or password")
        else:
                messages.error(request,"Invalid username or password")
    return render(request, 'login.html',
    context={'form':AuthenticationForm()})

def logout_view(request):
    logout(request)
    return redirect('/')


##### MAIN

def client_check(user):
    return user.is_client

def dispatcher_check(user):
    return user.is_dispatcher

def home(request):
    return render(request, 'home.html')

def no_access(request):
    return render(request, 'no_access.html')

@login_required
@user_passes_test(client_check, login_url='no_access')
def client_dashboard(request):
    return render(request, 'client_dashboard.html')


@login_required
@user_passes_test(dispatcher_check, login_url='no_access')
def dispatcher_dashboard(request):
    return render(request, 'dispatcher_dashboard.html')


# VEHICLES MANAGEMENT
@login_required
@user_passes_test(dispatcher_check, login_url='no_access')
def crud_vehicles(request):
    return render(request, 'vehicles.html', {'data': Vehicle.objects.all()})

@login_required
@user_passes_test(dispatcher_check, login_url='no_access')
def add_vehicle(request):
    if request.method == 'POST':
        form = AddVehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save()
            return redirect('vehicles')
    else:
        form = AddVehicleForm()
    return render(request, 'add_vehicle.html', {'form': form})


@login_required
@user_passes_test(dispatcher_check, login_url='no_access')
def delete_vehicle(request, pk):
    obj = get_object_or_404(Vehicle, id=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('vehicles')
    return render(request, 'delete_item.html', {'object': obj})


# DRIVERS MANAGEMENT
@login_required
@user_passes_test(dispatcher_check, login_url='no_access')
def crud_drivers(request):
    return render(request, 'drivers.html', {'data': Driver.objects.all()})

@login_required
@user_passes_test(dispatcher_check, login_url='no_access')
def add_driver(request):
    if request.method == 'POST':
        form = AddDriverForm(request.POST)
        if form.is_valid():
            driver = form.save()
            return redirect('drivers')
    else:
        form = AddDriverForm()
    return render(request, 'add_driver.html', {'form': form})


@login_required
@user_passes_test(dispatcher_check, login_url='no_access')
def delete_driver(request, pk):
    obj = get_object_or_404(Driver, id=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('drivers')
    return render(request, 'delete_item.html', {'object': obj})


# CITIES MANAGEMENT
@login_required
@user_passes_test(dispatcher_check, login_url='no_access')
def crud_cities(request):
    return render(request, 'cities.html', {'data': City.objects.all()})


@login_required
@user_passes_test(dispatcher_check, login_url='no_access')
def add_city(request):
    if request.method == 'POST':
        form = AddCityForm(request.POST)
        if form.is_valid():
            city = form.save()
            return redirect('cities')
    else:
        form = AddCityForm()
    return render(request, 'add_city.html', {'form': form})


@login_required
@user_passes_test(dispatcher_check, login_url='no_access')
def delete_city(request, pk):
    obj = get_object_or_404(City, id=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('cities')
    return render(request, 'delete_item.html', {'object': obj})


# ROUTES MANAGEMENT
@login_required
@user_passes_test(dispatcher_check, login_url='no_access')
def crud_routes(request):
    return render(request, 'routes.html', {'data': CityConnection.objects.all()})


def calculate_distance(city1, city2):
    # https://www.geeksforgeeks.org/great-circle-distance-formula/

    lat1, lon1 = radians(city1.latitude), radians(city1.longitude)
    lat2, lon2 = radians(city2.latitude), radians(city2.longitude)
    r = 6371  # Earth's radius in kilometers

    d = r * acos(cos(lat1)*cos(lat2)*cos(lon1-lon2) + sin(lat1)*sin(lat2))
    return d

@login_required
@user_passes_test(dispatcher_check, login_url='no_access')
def add_route(request):
    if request.method == 'POST':
        form = AddRouteForm(request.POST)
        if form.is_valid():
            
            route = form.save(commit=False)
            route.distance = calculate_distance(route.city1, route.city2)
            route.save()
            return redirect('routes')
    else:
        form = AddRouteForm()
    return render(request, 'add_route.html', {'form': form})

@login_required
@user_passes_test(dispatcher_check, login_url='no_access')
def delete_route(request, pk):
    obj = get_object_or_404(CityConnection, id=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('routes')
    return render(request, 'delete_item.html', {'object': obj})


# CLIENT SHIPMENTS AND ORDERS MANAGEMENT
@login_required
@user_passes_test(client_check, login_url='no_access')
def client_shipments(request):
    # Select shipments related to that user's orders
    orders = Order.objects.filter(client=request.user.client)
    data = Shipment.objects.filter(order__in = orders, status='in_transit')
    return render(request, 'client_shipments.html', {'data': data})

@login_required
@user_passes_test(client_check, login_url='no_access')
def client_delivered(request):
    # Select delivered shipments related to that user's orders
    orders = Order.objects.filter(client=request.user.client)
    data = Shipment.objects.filter(order__in = orders, status='delivered')
    return render(request, 'client_delivered.html', {'data': data})

@login_required
@user_passes_test(client_check, login_url='no_access')
def client_orders(request):
    # Select only pending orders by that user
    orders = Order.objects.filter(client = request.user.client).exclude(status='accepted')
    return render(request, 'client_orders.html', {'data': orders})

@login_required
@user_passes_test(client_check, login_url='no_access')
def add_order(request):
    if request.method == 'POST':
        form = AddOrderForm(request.POST)
        if form.is_valid():            
            order = form.save(commit=False)
            order.client = request.user.client
            order.is_pending = True
            order.save()
            return redirect('client_orders')
    else:
        form = AddOrderForm()
    return render(request, 'add_order.html', {'form': form})

@login_required
@user_passes_test(client_check, login_url='no_access')
def leave_review(request, pk):
    if request.method == 'POST':
        form = AddReviewForm(request.POST)
        if form.is_valid():
            shipment = get_object_or_404(Shipment, pk=pk)            
            review = form.save(commit=False)
            review.shipment = shipment
            review.save()
            return redirect('client_delivered')
    else:
        form = AddReviewForm()
    return render(request, 'leave_review.html', {'form': form})




# DISPATCHER SHIPMENTS AND ORDERS MANAGEMENT
@login_required
@user_passes_test(dispatcher_check, login_url='no_access')
def dispatcher_orders(request):
    orders = Order.objects.filter(status='pending')
    return render(request, 'dispatcher_orders.html', {'data': orders})

@login_required
@user_passes_test(dispatcher_check, login_url='no_access')
def dispatcher_shipments(request):
    # Add shipments related to that dispatcher
    return render(request, 'dispatcher_shipments.html', {'data': Shipment.objects.filter(status='in_transit')})

@login_required
@user_passes_test(dispatcher_check, login_url='no_access')
def mark_shipment(request, pk):
    obj = get_object_or_404(Shipment, id = pk)
    if request.method == 'POST':
        obj.status = 'delivered'
        obj.save()
        return redirect('dispatcher_shipments')
    return render(request,'mark_shipment.html')

def calculate_price(order):
    return order.weight * order.volume * order.city_connection.distance * decimal.Decimal(0.5)

@login_required
@user_passes_test(dispatcher_check, login_url='no_access')
def view_order(request, pk):
    order = get_object_or_404(Order, id=pk)
    if Driver.objects.filter(is_available=True).exists():
        form = AddShipmentForm(request.POST)
        if request.method == 'POST':
            if form.is_valid():
                shipment = form.save(commit=False)
                shipment.order = order
                shipment.status = 'in_transit'
                shipment.price = calculate_price(order)
                order.status = 'accepted'
                order.save()
                driver = shipment.driver
                driver.is_available = False
                driver.save()
                shipment.save()            
                return redirect('dispatcher_orders')
        return render(request, 'view_order.html', {'item': order, 'form': form})
    else:
        return render(request, 'view_order_no_driver.html', {'item': order})
        

    


@login_required
@user_passes_test(dispatcher_check, login_url='no_access')
def reject_order(request, pk):
    order = get_object_or_404(Order, id=pk)
    if request.method == 'POST':
        order.status = 'rejected'
        order.save()
        return redirect('dispatcher_orders')
    return render(request, 'reject_order.html', {'object': order})


@login_required
@user_passes_test(dispatcher_check, login_url='no_access')
def dispatcher_delivered(request):
    return render(request, 'dispatcher_delivered.html', {'data': Shipment.objects.filter(status='delivered')})


# # REGISTRATION
# def register_client(request):
#     if request.method == 'POST':
#         form = ClientRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('client_dashboard')
#     else:
#         form = ClientRegistrationForm()
    
#     return render(request, 'register_client.html', {'form': form})


# def register_dispatcher(request):
#     if request.method == 'POST':
#         form = DispatcherRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('dispatcher_dashboard')
#     else:
#         form = DispatcherRegistrationForm()
    
#     return render(request, 'register_dispatcher.html', {'form': form})
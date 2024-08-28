from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.http import HttpResponse
from django.views.generic import CreateView
from math import acos, sin, cos, radians
from datetime import timedelta
import decimal

def home(request):
    return render(request, 'home.html')

@login_required
def client_dashboard(request):
    return render(request, 'client_dashboard.html')


@login_required
def dispatcher_dashboard(request):
    return render(request, 'dispatcher_dashboard.html')


# VEHICLES MANAGEMENT
@login_required
def crud_vehicles(request):
    return render(request, 'vehicles.html', {'data': Vehicle.objects.all()})

@login_required
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
def delete_vehicle(request, pk):
    obj = get_object_or_404(Vehicle, id=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('vehicles')
    return render(request, 'delete_item.html', {'object': obj})


# DRIVERS MANAGEMENT
@login_required
def crud_drivers(request):
    return render(request, 'drivers.html', {'data': Driver.objects.all()})

@login_required
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
def delete_driver(request, pk):
    obj = get_object_or_404(Driver, id=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('drivers')
    return render(request, 'delete_item.html', {'object': obj})


# CITIES MANAGEMENT
@login_required
def crud_cities(request):
    return render(request, 'cities.html', {'data': City.objects.all()})


@login_required
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
def delete_city(request, pk):
    obj = get_object_or_404(City, id=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('cities')
    return render(request, 'delete_item.html', {'object': obj})


# ROUTES MANAGEMENT
@login_required
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
def delete_route(request, pk):
    obj = get_object_or_404(CityConnection, id=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('routes')
    return render(request, 'delete_item.html', {'object': obj})


# CLIENT SHIPMENTS AND ORDERS MANAGEMENT
@login_required
def client_shipments(request):
    return render(request, 'client_shipments.html', {'data': Shipment.objects.all()})

@login_required
def client_orders(request):
    return render(request, 'client_orders.html', {'data': Order.objects.all()})

@login_required
def add_order(request):
    if request.method == 'POST':
        form = AddOrderForm(request.POST)
        if form.is_valid():            
            order = form.save(commit=False)
            order.client = request.user
            order.save()
            return redirect('client_orders')
    else:
        form = AddOrderForm()
    return render(request, 'add_order.html', {'form': form})


# REGISTRATION
def register_client(request):
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('client_dashboard')
    else:
        form = ClientRegistrationForm()
    
    return render(request, 'register_client.html', {'form': form})


def register_dispatcher(request):
    if request.method == 'POST':
        form = DispatcherRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dispatcher_dashboard')
    else:
        form = DispatcherRegistrationForm()
    
    return render(request, 'register_dispatcher.html', {'form': form})



def calculate_price(shipment):
    return shipment.weight * shipment.volume * decimal.Decimal(1.25)
    


# class ClientSignUpView(CreateView):
#     model = CustomUser
#     form_class = ClientSignUpForm
#     template_name = 'register_client.html'

#     def get_context_data(self, **kwargs):
#         kwargs['user_type'] = 'client'
#         return super().get_context_data(**kwargs)

#     def form_valid(self, form):
#         user = form.save()
#         login(self.request, user)
#         return redirect('client_dashboard')
    

# class DispatcherSignUpView(CreateView):
#     model = CustomUser
#     form_class = DispatcherSignUpForm
#     template_name = 'register_dispatcher.html'

#     def get_context_data(self, **kwargs):
#         kwargs['user_type'] = 'dispatcher'
#         return super().get_context_data(**kwargs)

#     def form_valid(self, form):
#         user = form.save()
#         login(self.request, user)
#         return redirect('dispatcher_dashboard')
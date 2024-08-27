"""
URL configuration for there_n_back project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from logistics import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
    
    path('vehicles/', views.crud_vehicles, name='vehicles'),
    path('vehicles/add/', views.add_vehicle, name='add_vehicle'),
    path('vehicles/<int:pk>/delete/', views.delete_vehicle, name='delete_vehicle'),

    path('drivers/', views.crud_drivers, name='drivers'),
    path('driver/add/', views.add_driver, name='add_driver'),
    path('drivers/<int:pk>/delete/', views.delete_driver, name='delete_driver'),

    path('cities/', views.crud_cities, name='cities'),
    path('cities/add/', views.add_city, name='add_city'),
    path('cities/<int:pk>/delete/', views.delete_city, name='delete_city'),

    path('routes/', views.crud_routes, name='routes'),
    path('routes/add/', views.add_route, name='add_route'),
    path('routes/<int:pk>/delete/', views.delete_route, name='delete_route'),
    
    path('client_shipments/', views.client_shipments, name='client_shipments'),
    path('client_shipments/add/', views.add_shipment, name='add_shipment'),

    path('client_dashboard/', views.client_dashboard, name='client_dashboard'),
    path('dispatcher_dashboard/', views.dispatcher_dashboard, name='dispatcher_dashboard'),
    path('register/client/', views.register_client, name='register_client'),
    path('register/dispatcher/', views.register_dispatcher, name='register_dispatcher'),
    # path('register/client/', views.ClientSignUpView.as_view(), name='register_client'),
    # path('register/dispatcher/', views.DispatcherSignUpView.as_view(), name='register_dispatcher'),
]


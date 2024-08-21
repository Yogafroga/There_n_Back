from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Client, Dispatcher

class ClientRegistrationForm(UserCreationForm):
    class Meta:
        model = Client
        fields = ['email', 'name', 'phone', 'type', 'password1', 'password2']


class DispatcherRegistrationForm(UserCreationForm):
    class Meta:
        model = Dispatcher
        fields = ['email', 'name', 'password1', 'password2']


        
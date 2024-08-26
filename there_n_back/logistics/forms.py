from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.db import transaction

class ClientRegistrationForm(UserCreationForm):
    class Meta:
        model = Client
        fields = ['email', 'name', 'phone', 'type', 'password1', 'password2']


class DispatcherRegistrationForm(UserCreationForm):
    class Meta:
        model = Dispatcher
        fields = ['email', 'name', 'password1', 'password2']

class AddVehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['load_capacity', 'vehicle_type']

class AddDriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['name', 'license_category', 'vehicle']

class AddCityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['city_name', 'latitude', 'longitude']


# class ClientSignUpForm(UserCreationForm):

#     phone = forms.CharField(max_length=20)
#     type = forms.ChoiceField(choices=Client.CLIENT_TYPE_CHOICES)

#     class Meta(UserCreationForm.Meta):
#         model = CustomUser

#     @transaction.atomic
#     def save(self):
#         user = super().save(commit=False)
#         user.is_student = True
#         user.save()
#         client = Client.objects.create(user=user)
#         client.phone = self.cleaned_data.get('phone')
#         client.type = self.cleaned_data.get('type')
#         return user

    
# class DispatcherSignUpForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = CustomUser

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.is_dispatcher = True
#         if commit:
#             user.save()
#         return user
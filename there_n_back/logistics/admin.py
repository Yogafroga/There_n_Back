from django.contrib import admin
from .models import Client, Dispatcher

class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'phone', 'type', 'is_active', 'date_joined')
    ordering = ('email',)  # Измените на существующее поле, например, 'email'

class DispatcherAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'is_active', 'date_joined')
    ordering = ('email',)  # Измените на существующее поле, например, 'email'

admin.site.register(Client, ClientAdmin)
admin.site.register(Dispatcher, DispatcherAdmin)
from django.shortcuts import render, redirect
from .forms import ClientRegistrationForm, DispatcherRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.http import HttpResponse

def home(request):
    return render(request, 'home.html')

@login_required
def client_dashboard(request):
    return render(request, 'client_dashboard.html')


@login_required
def dispatcher_dashboard(request):
    return render(request, 'dispatcher_dashboard.html')

def register_client(request):
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Авторизуем пользователя сразу после регистрации
            return redirect('client_dashboard')  # Перенаправляем на главную страницу или другую страницу по вашему выбору
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
